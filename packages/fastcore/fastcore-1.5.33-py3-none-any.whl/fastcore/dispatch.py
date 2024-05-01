# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/04_dispatch.ipynb.

# %% ../nbs/04_dispatch.ipynb 1
from __future__ import annotations
from .imports import *
from .foundation import *
from .utils import *

from collections import defaultdict

# %% auto 0
__all__ = ['typedispatch', 'lenient_issubclass', 'sorted_topologically', 'TypeDispatch', 'DispatchReg', 'retain_meta',
           'default_set_meta', 'cast', 'retain_type', 'retain_types', 'explode_types']

# %% ../nbs/04_dispatch.ipynb 5
def lenient_issubclass(cls, types):
    "If possible return whether `cls` is a subclass of `types`, otherwise return False."
    if cls is object and types is not object: return False # treat `object` as highest level
    try: return isinstance(cls, types) or issubclass(cls, types)
    except: return False

# %% ../nbs/04_dispatch.ipynb 7
def sorted_topologically(iterable, *, cmp=operator.lt, reverse=False):
    "Return a new list containing all items from the iterable sorted topologically"
    l,res = L(list(iterable)),[]
    for _ in range(len(l)):
        t = l.reduce(lambda x,y: y if cmp(y,x) else x)
        res.append(t), l.remove(t)
    return res[::-1] if reverse else res

# %% ../nbs/04_dispatch.ipynb 11
def _chk_defaults(f, ann):
    pass
# Implementation removed until we can figure out how to do this without `inspect` module
#     try: # Some callables don't have signatures, so ignore those errors
#         params = list(inspect.signature(f).parameters.values())[:min(len(ann),2)]
#         if any(p.default!=inspect.Parameter.empty for p in params):
#             warn(f"{f.__name__} has default params. These will be ignored.")
#     except ValueError: pass

# %% ../nbs/04_dispatch.ipynb 12
def _p2_anno(f):
    "Get the 1st 2 annotations of `f`, defaulting to `object`"
    hints = type_hints(f)
    ann = [o for n,o in hints.items() if n!='return']
    if callable(f): _chk_defaults(f, ann)
    while len(ann)<2: ann.append(object)
    return ann[:2]

# %% ../nbs/04_dispatch.ipynb 17
class _TypeDict:
    def __init__(self): self.d,self.cache = {},{}

    def _reset(self):
        self.d = {k:self.d[k] for k in sorted_topologically(self.d, cmp=lenient_issubclass)}
        self.cache = {}

    def add(self, t, f):
        "Add type `t` and function `f`"
        if not isinstance(t, tuple): t = tuple(L(union2tuple(t)))
        for t_ in t: self.d[t_] = f
        self._reset()

    def all_matches(self, k):
        "Find first matching type that is a super-class of `k`"
        if k not in self.cache:
            types = [f for f in self.d if lenient_issubclass(k,f)]
            self.cache[k] = [self.d[o] for o in types]
        return self.cache[k]

    def __getitem__(self, k):
        "Find first matching type that is a super-class of `k`"
        res = self.all_matches(k)
        return res[0] if len(res) else None

    def __repr__(self): return self.d.__repr__()
    def first(self): return first(self.d.values())

# %% ../nbs/04_dispatch.ipynb 18
class TypeDispatch:
    "Dictionary-like object; `__getitem__` matches keys of types using `issubclass`"
    def __init__(self, funcs=(), bases=()):
        self.funcs,self.bases = _TypeDict(),L(bases).filter(is_not(None))
        for o in L(funcs): self.add(o)
        self.inst = None
        self.owner = None

    def add(self, f):
        "Add type `t` and function `f`"
        if isinstance(f, staticmethod): a0,a1 = _p2_anno(f.__func__)
        else: a0,a1 = _p2_anno(f)
        t = self.funcs.d.get(a0)
        if t is None:
            t = _TypeDict()
            self.funcs.add(a0, t)
        t.add(a1, f)

    def first(self):
        "Get first function in ordered dict of type:func."
        return self.funcs.first().first()

    def returns(self, x):
        "Get the return type of annotation of `x`."
        return anno_ret(self[type(x)])

    def _attname(self,k): return getattr(k,'__name__',str(k))
    def __repr__(self):
        r = [f'({self._attname(k)},{self._attname(l)}) -> {getattr(v, "__name__", type(v).__name__)}'
             for k in self.funcs.d for l,v in self.funcs[k].d.items()]
        r = r + [o.__repr__() for o in self.bases]
        return '\n'.join(r)

    def __call__(self, *args, **kwargs):
        ts = L(args).map(type)[:2]
        f = self[tuple(ts)]
        if not f: return args[0]
        if isinstance(f, staticmethod): f = f.__func__
        elif self.inst is not None: f = MethodType(f, self.inst)
        elif self.owner is not None: f = MethodType(f, self.owner)
        return f(*args, **kwargs)

    def __get__(self, inst, owner):
        self.inst = inst
        self.owner = owner
        return self

    def __getitem__(self, k):
        "Find first matching type that is a super-class of `k`"
        k = L(k)
        while len(k)<2: k.append(object)
        r = self.funcs.all_matches(k[0])
        for t in r:
            o = t[k[1]]
            if o is not None: return o
        for base in self.bases:
            res = base[k]
            if res is not None: return res
        return None

# %% ../nbs/04_dispatch.ipynb 77
class DispatchReg:
    "A global registry for `TypeDispatch` objects keyed by function name"
    def __init__(self): self.d = defaultdict(TypeDispatch)
    def __call__(self, f):
        if isinstance(f, (classmethod, staticmethod)): nm = f'{f.__func__.__qualname__}'
        else: nm = f'{f.__qualname__}'
        if isinstance(f, classmethod): f=f.__func__
        self.d[nm].add(f)
        return self.d[nm]

typedispatch = DispatchReg()

# %% ../nbs/04_dispatch.ipynb 84
_all_=['cast']

# %% ../nbs/04_dispatch.ipynb 85
def retain_meta(x, res, as_copy=False):
    "Call `res.set_meta(x)`, if it exists"
    if hasattr(res,'set_meta'): res.set_meta(x, as_copy=as_copy)
    return res

# %% ../nbs/04_dispatch.ipynb 86
def default_set_meta(self, x, as_copy=False):
    "Copy over `_meta` from `x` to `res`, if it's missing"
    if hasattr(x, '_meta') and not hasattr(self, '_meta'):
        meta = x._meta
        if as_copy: meta = copy(meta)
        self._meta = meta
    return self

# %% ../nbs/04_dispatch.ipynb 87
@typedispatch
def cast(x, typ):
    "cast `x` to type `typ` (may also change `x` inplace)"
    res = typ._before_cast(x) if hasattr(typ, '_before_cast') else x
    if risinstance('ndarray', res): res = res.view(typ)
    elif hasattr(res, 'as_subclass'): res = res.as_subclass(typ)
    else:
        try: res.__class__ = typ
        except: res = typ(res)
    return retain_meta(x, res)

# %% ../nbs/04_dispatch.ipynb 93
def retain_type(new, old=None, typ=None, as_copy=False):
    "Cast `new` to type of `old` or `typ` if it's a superclass"
    # e.g. old is TensorImage, new is Tensor - if not subclass then do nothing
    if new is None: return
    assert old is not None or typ is not None
    if typ is None:
        if not isinstance(old, type(new)): return new
        typ = old if isinstance(old,type) else type(old)
    # Do nothing the new type is already an instance of requested type (i.e. same type)
    if typ==NoneType or isinstance(new, typ): return new
    return retain_meta(old, cast(new, typ), as_copy=as_copy)

# %% ../nbs/04_dispatch.ipynb 97
def retain_types(new, old=None, typs=None):
    "Cast each item of `new` to type of matching item in `old` if it's a superclass"
    if not is_listy(new): return retain_type(new, old, typs)
    if typs is not None:
        if isinstance(typs, dict):
            t = first(typs.keys())
            typs = typs[t]
        else: t,typs = typs,None
    else: t = type(old) if old is not None and isinstance(old,type(new)) else type(new)
    return t(L(new, old, typs).map_zip(retain_types, cycled=True))

# %% ../nbs/04_dispatch.ipynb 99
def explode_types(o):
    "Return the type of `o`, potentially in nested dictionaries for thing that are listy"
    if not is_listy(o): return type(o)
    return {type(o): [explode_types(o_) for o_ in o]}
