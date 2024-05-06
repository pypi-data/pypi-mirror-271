from __future__ import annotations
from typing import Any
import numpy as np
from .e import eread, ewrite,einput
import classutilities

_MEMMAP = None
_ADDRMAP = {}

class bitfield(object):
    r"""
    base class for bitfield, all bitfield should inherit from this class
    subclass should explicitly define `_fields_` and `_addr_` to specify the bitfield layout and address, for example:

    Examples
    --------
    >>> class BF(bitfield):
    ...     _addr_ = 0x4ff0
    ...     _fields_ = [
    ...         ("A", 8),
    ...         ("B", 12),
    ...         ("", 2),
    ...         ("C", 2),
    ...     ]
    >>> bf = BF(0x123456)
    >>> bf.A == (0x123456 >> 0) & ((1<<8)-1)
    True
    >>> bf.B == (0x123456 >> 8) & ((1<<12)-1)
    True
    >>> bf.C == (0x123456 >> 22) & ((1<<2)-1)
    True
    >>> hex(bf.data)
    '0x123456'
    >>> np.binary_repr(bf.data,24) # doctest: +NORMALIZE_WHITESPACE
        '000100100011010001010110'
    >>> #CC__BBBBBBBBBBBBAAAAAAAA
    >>> bf.A = 0
    >>> bf.C = 2
    >>> hex(bf.data)
    '0x923400'
    >>> np.binary_repr(bf.data,24) # doctest: +NORMALIZE_WHITESPACE
        '100100100011010000000000'
    >>> #CC__BBBBBBBBBBBBAAAAAAAA
    >>> bf.addr
    '4ff0'
    >>> bf.addr_
    20464
    >>> bf.size
    3
    >>> bf.bin
    '100100100011010000000000'
    >>> bf.name
    'BF'
    >>> bf.bytes
    b'\x004\x92'
    >>> print(bf)
    BF @ 4ff0 = 0x923400
      A[7:0] = 0x0
      B[19:8] = 0x234
      C[23:22] = 0x2
    <BLANKLINE>
    >>> mem_map = {}
    >>> load_memmap(mem_map)
    >>> bf.write()
    >>> mem_map
    {20464: 0, 20465: 52, 20466: 146}
    >>> bf2 = BF().load()
    >>> bf2.data == bf.data
    True
    >>> BF.get("A")
    0
    >>> BF.set("B",0)
    >>> mem_map
    {20464: 0, 20465: 0, 20466: 144}
    >>> BF.set(value=0x123456) # 0x12==18, 0x34==52, 0x56==86 
    >>> mem_map
    {20464: 86, 20465: 52, 20466: 18}
    >>> BF.get() # 0x123456 == 1193046
    1193046
    >>> bf.diff(bf2) # return None if two bitfields are the same
    >>> bf2.B = 0
    >>> print(bf.diff(bf2))
    BF @ 4ff0 = 0x923400 => 0x900000
      B[19:8] = 0x234 => 0x0
    <BLANKLINE>
    >>> bf.jam()
    jam 0x00,0x4ff0
    jam 0x34,0x4ff1
    jam 0x92,0x4ff2
    >>> _ADDRMAP
    {20464: <class 'libzac.bitfield.BF'>, 20465: <class 'libzac.bitfield.BF'>, 20466: <class 'libzac.bitfield.BF'>}
    """
    _fields_ = []
    _addr_ = 0
    __ENDIANESS = 'little'
    def __init__(self, data:int=0):
        """initialize bitfield with data, data will be masked by the size of bitfield"""
        self._data = data & ((1<<(self.size*8))-1)
        shift = 0
        for field,bit in self._fields_:
            mask = ((1<<bit)-1) << shift
            def getter(self, mask=mask, shift=shift): # `mask=mask` will remember current value of mask
                return (self.data & mask) >> shift
            def setter(self, value, mask=mask, shift=shift):
                self._data = ((value << shift) & mask) | (self.data & ~mask)
            if field:
                setattr(type(self),field,property(getter, setter)) # dynamically add property to class
            shift += bit
    
    def __init_subclass__(cls):
        for byte in range(cls.size):
            _ADDRMAP[cls.addr_+byte] = cls

    def __str__(self):
        """print all info about the bitfield"""
        s = f"{self.__class__.__name__} @ {self.addr} = {self.hex}\n"
        start = 0
        for field,bit in self._fields_:
            if field:
                width = f"[{start+bit-1:d}:{start:d}]" if bit > 1 else f"[{start}]"
                s += f"  {field}{width} = {hex(getattr(self,field))}\n"
            start += bit
        return s
    
    def __repr__(self):
        return self.__str__()
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        """prevent add new attribute other than _fields_ and _data"""
        if __name in [field for field,bit in self._fields_]+["_data"]:
            super().__setattr__(__name, __value)
        else:
            raise AttributeError(f"Bitfield '{self.name}' has no field '{__name}'")
        
    @classutilities.classproperty
    def addr(cls):
        """return the address(string, '8b1c') of the bitfield"""
        return einput(cls._addr_, output_int=False)
    @classutilities.classproperty
    def addr_(cls):
        """return the address(int, 0x8b1c/35612) of the bitfield"""
        return einput(cls._addr_, output_int=True)
    @classutilities.classproperty
    def size(cls):
        """return the number of bytes of the bitfield"""
        return (sum([bit for field,bit in cls._fields_])-1)//8 + 1
    @classutilities.classproperty
    def name(cls):
        return cls.__name__
    
    @classmethod
    def load(cls):
        """read a bitfield from memory and return an instance of it"""
        return cls().read()
    @classmethod
    def get(cls, field=None): 
        """get a signle bit field, if field is None, get all data"""
        bf = cls.load()
        if field:
            return getattr(bf, field)
        else:
            return bf.data
    @classmethod
    def set(cls, field=None, value=0):
        """set a single bit field while keep others untouched, if field is None, set value as binary"""
        if field:
            bf = cls.load()
            setattr(bf, field, value)
        else:
            bf = cls(value)
        bf.write()
    @classmethod
    def show(cls):
        """show current info of the bitfield in memory"""
        print(cls.load())

    @property
    def data(self):
        return self._data
    @property
    def bin(self):
        return np.binary_repr(self.data,self.size*8)
    @property
    def hex(self):
        return f"0x{self.data:0{self.size*2}x}"
    @property
    def bytes(self):
        """convert self.data to bytes"""
        return self.data.to_bytes(self.size, self.__ENDIANESS) 

    def read(self, verbose=False):
        """read `self.size` bytes from memory to self.data at address `self.addr`"""
        if _MEMMAP is not None:
            r = np.zeros(self.size,dtype="u1")
            for i in range(self.size):
                r[i] = _MEMMAP.get(self.addr_+i,0)
        else:
            r = eread(self.addr, self.size) # read `self.size` bytes from memory at address `self.addr`
        if verbose:
            print(f"read {r} @ {self.addr}")
        self._data = int.from_bytes(r.tobytes(), self.__ENDIANESS)
        return self

    def write(self, verbose=False):
        """write `self.size` bytes of self.data to memory at address `self.addr`"""
        if verbose:
            print(f"write {self.hex} @ {self.addr}")
        if _MEMMAP is not None:
            byte = np.frombuffer(self.data.to_bytes(self.size, self.__ENDIANESS),"u1")
            for i in range(self.size):
                _MEMMAP[self.addr_+i] = byte[i]
        else:
            ewrite(self.addr, self.hex, length=self.size) # write `self.size` bytes to memory at address `self.addr`

    def diff(self, another:bitfield, verbose=False):
        """diff two bitfields, return None if they are the same, otherwise return the diff string"""
        if isinstance(another, type(self)):
            if self.data == another.data:
                return None
            s = ""
            for this,that in zip(str(self).splitlines(), str(another).splitlines()):
                this_value = this.split("=")[1]
                that_value = that.split("=")[1]
                if this_value == that_value:
                    if verbose:
                        s += this+"\n"
                else:
                    s += this + " =>" + that_value + "\n"
            return s
        else:
            raise TypeError(f'Try to diff "{another.name}" to "{self.name}"')
        
    def jam(self):
        """print 'jam val,addr' for each byte"""
        data = np.frombuffer(self.bytes,"u1")
        for i in range(self.size):
            print(f"jam 0x{data[i]:02x},0x{self.addr_+i:x}")


def load_memmap(mem_map:dict={}):
    global _MEMMAP
    _MEMMAP = mem_map