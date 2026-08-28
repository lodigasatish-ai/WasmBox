from ..intrinsics import _clamp, _decode_utf8, _encode_utf8, _load, _store
from ..types import Err, Ok, Result
import ctypes
from dataclasses import dataclass
from enum import Enum
from typing import List, Union
import wasmtime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from .. import Root

@dataclass
class Function:
    protocol: str
    name: str

@dataclass
class Constructor:
    module: str
    protocol: str

@dataclass
class Static:
    module: str
    protocol: str
    name: str

@dataclass
class FunctionExportKindFreestanding:
    value: Function

@dataclass
class FunctionExportKindConstructor:
    value: Constructor

@dataclass
class FunctionExportKindMethod:
    value: str

@dataclass
class FunctionExportKindStatic:
    value: Static

FunctionExportKind = Union[FunctionExportKindFreestanding, FunctionExportKindConstructor, FunctionExportKindMethod, FunctionExportKindStatic]

@dataclass
class ReturnStyleNone_:
    pass

@dataclass
class ReturnStyleNormal:
    pass

@dataclass
class ReturnStyleResult:
    pass

ReturnStyle = Union[ReturnStyleNone_, ReturnStyleNormal, ReturnStyleResult]

@dataclass
class FunctionExport:
    kind: FunctionExportKind
    return_style: ReturnStyle

@dataclass
class Resource:
    package: str
    name: str

@dataclass
class Record:
    package: str
    name: str
    fields: List[str]

@dataclass
class Flags:
    package: str
    name: str
    u32_count: int

@dataclass
class Tuple:
    count: int

@dataclass
class Case:
    name: str
    has_payload: bool

@dataclass
class Variant:
    package: str
    name: str
    cases: List[Case]

@dataclass
class Enum:
    package: str
    name: str
    count: int

class OptionKind(Enum):
    NON_NESTING = 0
    NESTING = 1

@dataclass
class ResultRecord:
    has_ok: bool
    has_err: bool

@dataclass
class Symbols:
    exports: List[FunctionExport]
    resources: List[Resource]
    records: List[Record]
    flags: List[Flags]
    tuples: List[Tuple]
    variants: List[Variant]
    enums: List[Enum]
    options: List[OptionKind]
    results: List[ResultRecord]

class Exports:
    component: 'Root'
    
    def __init__(self, component: 'Root') -> None:
        self.component = component
    def init(self, caller: wasmtime.Store, app_name: str, symbols: Symbols, stub_wasi: bool) -> Result[None, str]:
        ptr = self.component._realloc0(caller, 0, 0, 4, 84)
        assert(isinstance(ptr, int))
        ptr0, len1 = _encode_utf8(app_name, self.component._realloc0, self.component._core_memory0, caller)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 4, len1)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 0, ptr0)
        record = symbols
        field = record.exports
        field2 = record.resources
        field3 = record.records
        field4 = record.flags
        field5 = record.tuples
        field6 = record.variants
        field7 = record.enums
        field8 = record.options
        field9 = record.results
        vec = field
        len46 = len(vec)
        result = self.component._realloc0(caller, 0, 0, 4, len46 * 32)
        assert(isinstance(result, int))
        for i47 in range(0, len46):
            e = vec[i47]
            base10 = result + i47 * 32
            record11 = e
            field12 = record11.kind
            field13 = record11.return_style
            if isinstance(field12, FunctionExportKindFreestanding):
                payload = field12.value
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base10, 0, 0)
                record14 = payload
                field15 = record14.protocol
                field16 = record14.name
                ptr17, len18 = _encode_utf8(field15, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 8, len18)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 4, ptr17)
                ptr19, len20 = _encode_utf8(field16, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 16, len20)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 12, ptr19)
            elif isinstance(field12, FunctionExportKindConstructor):
                payload21 = field12.value
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base10, 0, 1)
                record22 = payload21
                field23 = record22.module
                field24 = record22.protocol
                ptr25, len26 = _encode_utf8(field23, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 8, len26)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 4, ptr25)
                ptr27, len28 = _encode_utf8(field24, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 16, len28)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 12, ptr27)
            elif isinstance(field12, FunctionExportKindMethod):
                payload29 = field12.value
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base10, 0, 2)
                ptr30, len31 = _encode_utf8(payload29, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 8, len31)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 4, ptr30)
            elif isinstance(field12, FunctionExportKindStatic):
                payload32 = field12.value
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base10, 0, 3)
                record33 = payload32
                field34 = record33.module
                field35 = record33.protocol
                field36 = record33.name
                ptr37, len38 = _encode_utf8(field34, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 8, len38)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 4, ptr37)
                ptr39, len40 = _encode_utf8(field35, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 16, len40)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 12, ptr39)
                ptr41, len42 = _encode_utf8(field36, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 24, len42)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base10, 20, ptr41)
            else:
                raise TypeError("invalid variant specified for FunctionExportKind")
            if isinstance(field13, ReturnStyleNone_):
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base10, 28, 0)
            elif isinstance(field13, ReturnStyleNormal):
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base10, 28, 1)
            elif isinstance(field13, ReturnStyleResult):
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base10, 28, 2)
            else:
                raise TypeError("invalid variant specified for ReturnStyle")
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 12, len46)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 8, result)
        vec57 = field2
        len59 = len(vec57)
        result58 = self.component._realloc0(caller, 0, 0, 4, len59 * 16)
        assert(isinstance(result58, int))
        for i60 in range(0, len59):
            e48 = vec57[i60]
            base49 = result58 + i60 * 16
            record50 = e48
            field51 = record50.package
            field52 = record50.name
            ptr53, len54 = _encode_utf8(field51, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base49, 4, len54)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base49, 0, ptr53)
            ptr55, len56 = _encode_utf8(field52, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base49, 12, len56)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base49, 8, ptr55)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 20, len59)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 16, result58)
        vec79 = field3
        len81 = len(vec79)
        result80 = self.component._realloc0(caller, 0, 0, 4, len81 * 24)
        assert(isinstance(result80, int))
        for i82 in range(0, len81):
            e61 = vec79[i82]
            base62 = result80 + i82 * 24
            record63 = e61
            field64 = record63.package
            field65 = record63.name
            field66 = record63.fields
            ptr67, len68 = _encode_utf8(field64, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base62, 4, len68)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base62, 0, ptr67)
            ptr69, len70 = _encode_utf8(field65, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base62, 12, len70)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base62, 8, ptr69)
            vec75 = field66
            len77 = len(vec75)
            result76 = self.component._realloc0(caller, 0, 0, 4, len77 * 8)
            assert(isinstance(result76, int))
            for i78 in range(0, len77):
                e71 = vec75[i78]
                base72 = result76 + i78 * 8
                ptr73, len74 = _encode_utf8(e71, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base72, 4, len74)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base72, 0, ptr73)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base62, 20, len77)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base62, 16, result76)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 28, len81)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 24, result80)
        vec93 = field4
        len95 = len(vec93)
        result94 = self.component._realloc0(caller, 0, 0, 4, len95 * 20)
        assert(isinstance(result94, int))
        for i96 in range(0, len95):
            e83 = vec93[i96]
            base84 = result94 + i96 * 20
            record85 = e83
            field86 = record85.package
            field87 = record85.name
            field88 = record85.u32_count
            ptr89, len90 = _encode_utf8(field86, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base84, 4, len90)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base84, 0, ptr89)
            ptr91, len92 = _encode_utf8(field87, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base84, 12, len92)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base84, 8, ptr91)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base84, 16, _clamp(field88, 0, 4294967295))
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 36, len95)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 32, result94)
        vec101 = field5
        len103 = len(vec101)
        result102 = self.component._realloc0(caller, 0, 0, 4, len103 * 4)
        assert(isinstance(result102, int))
        for i104 in range(0, len103):
            e97 = vec101[i104]
            base98 = result102 + i104 * 4
            record99 = e97
            field100 = record99.count
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base98, 0, _clamp(field100, 0, 4294967295))
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 44, len103)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 40, result102)
        vec126 = field6
        len128 = len(vec126)
        result127 = self.component._realloc0(caller, 0, 0, 4, len128 * 24)
        assert(isinstance(result127, int))
        for i129 in range(0, len128):
            e105 = vec126[i129]
            base106 = result127 + i129 * 24
            record107 = e105
            field108 = record107.package
            field109 = record107.name
            field110 = record107.cases
            ptr111, len112 = _encode_utf8(field108, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base106, 4, len112)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base106, 0, ptr111)
            ptr113, len114 = _encode_utf8(field109, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base106, 12, len114)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base106, 8, ptr113)
            vec122 = field110
            len124 = len(vec122)
            result123 = self.component._realloc0(caller, 0, 0, 4, len124 * 12)
            assert(isinstance(result123, int))
            for i125 in range(0, len124):
                e115 = vec122[i125]
                base116 = result123 + i125 * 12
                record117 = e115
                field118 = record117.name
                field119 = record117.has_payload
                ptr120, len121 = _encode_utf8(field118, self.component._realloc0, self.component._core_memory0, caller)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base116, 4, len121)
                _store(ctypes.c_uint32, self.component._core_memory0, caller, base116, 0, ptr120)
                _store(ctypes.c_uint8, self.component._core_memory0, caller, base116, 8, int(field119))
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base106, 20, len124)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base106, 16, result123)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 52, len128)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 48, result127)
        vec140 = field7
        len142 = len(vec140)
        result141 = self.component._realloc0(caller, 0, 0, 4, len142 * 20)
        assert(isinstance(result141, int))
        for i143 in range(0, len142):
            e130 = vec140[i143]
            base131 = result141 + i143 * 20
            record132 = e130
            field133 = record132.package
            field134 = record132.name
            field135 = record132.count
            ptr136, len137 = _encode_utf8(field133, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base131, 4, len137)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base131, 0, ptr136)
            ptr138, len139 = _encode_utf8(field134, self.component._realloc0, self.component._core_memory0, caller)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base131, 12, len139)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base131, 8, ptr138)
            _store(ctypes.c_uint32, self.component._core_memory0, caller, base131, 16, _clamp(field135, 0, 4294967295))
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 60, len142)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 56, result141)
        vec146 = field8
        len148 = len(vec146)
        result147 = self.component._realloc0(caller, 0, 0, 1, len148 * 1)
        assert(isinstance(result147, int))
        for i149 in range(0, len148):
            e144 = vec146[i149]
            base145 = result147 + i149 * 1
            _store(ctypes.c_uint8, self.component._core_memory0, caller, base145, 0, (e144).value)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 68, len148)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 64, result147)
        vec155 = field9
        len157 = len(vec155)
        result156 = self.component._realloc0(caller, 0, 0, 1, len157 * 2)
        assert(isinstance(result156, int))
        for i158 in range(0, len157):
            e150 = vec155[i158]
            base151 = result156 + i158 * 2
            record152 = e150
            field153 = record152.has_ok
            field154 = record152.has_err
            _store(ctypes.c_uint8, self.component._core_memory0, caller, base151, 0, int(field153))
            _store(ctypes.c_uint8, self.component._core_memory0, caller, base151, 1, int(field154))
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 76, len157)
        _store(ctypes.c_uint32, self.component._core_memory0, caller, ptr, 72, result156)
        _store(ctypes.c_uint8, self.component._core_memory0, caller, ptr, 80, int(stub_wasi))
        ret = self.component.lift_callee0(caller, ptr)
        assert(isinstance(ret, int))
        load = _load(ctypes.c_uint8, self.component._core_memory0, caller, ret, 0)
        expected: Result[None, str]
        if load == 0:
            expected = Ok(None)
        elif load == 1:
            load159 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 4)
            load160 = _load(ctypes.c_int32, self.component._core_memory0, caller, ret, 8)
            ptr161 = load159
            len162 = load160
            list = _decode_utf8(self.component._core_memory0, caller, ptr161, len162)
            expected = Err(list)
        else:
            raise TypeError("invalid variant discriminant for expected")
        tmp = expected
        self.component._post_return0(caller, ret)
        return tmp
    