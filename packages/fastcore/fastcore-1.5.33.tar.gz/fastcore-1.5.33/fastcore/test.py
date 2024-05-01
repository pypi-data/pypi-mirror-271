# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_test.ipynb.

# %% auto 0
__all__ = ['TEST_IMAGE', 'TEST_IMAGE_BW', 'exception', 'test_fail', 'test', 'nequals', 'test_eq', 'test_eq_type', 'test_ne',
           'is_close', 'test_close', 'test_is', 'test_shuffled', 'test_stdout', 'test_warns', 'test_fig_exists',
           'ExceptionExpected']

# %% ../nbs/00_test.ipynb 1
from .imports import *
from collections import Counter
from contextlib import redirect_stdout

# %% ../nbs/00_test.ipynb 6
def test_fail(f, msg='', contains='', args=None, kwargs=None):
    "Fails with `msg` unless `f()` raises an exception and (optionally) has `contains` in `e.args`"
    args, kwargs = args or [], kwargs or {}
    try: f(*args, **kwargs)
    except Exception as e:
        assert not contains or contains in str(e)
        return
    assert False,f"Expected exception but none raised. {msg}"

# %% ../nbs/00_test.ipynb 10
def test(a, b, cmp, cname=None):
    "`assert` that `cmp(a,b)`; display inputs and `cname or cmp.__name__` if it fails"
    if cname is None: cname=cmp.__name__
    assert cmp(a,b),f"{cname}:\n{a}\n{b}"

# %% ../nbs/00_test.ipynb 16
def nequals(a,b):
    "Compares `a` and `b` for `not equals`"
    return not equals(a,b)

# %% ../nbs/00_test.ipynb 20
def test_eq(a,b):
    "`test` that `a==b`"
    test(a,b,equals, cname='==')

# %% ../nbs/00_test.ipynb 25
def test_eq_type(a,b):
    "`test` that `a==b` and are same type"
    test_eq(a,b)
    test_eq(type(a),type(b))
    if isinstance(a,(list,tuple)): test_eq(map(type,a),map(type,b))

# %% ../nbs/00_test.ipynb 27
def test_ne(a,b):
    "`test` that `a!=b`"
    test(a,b,nequals,'!=')

# %% ../nbs/00_test.ipynb 29
def is_close(a,b,eps=1e-5):
    "Is `a` within `eps` of `b`"
    if hasattr(a, '__array__') or hasattr(b,'__array__'):
        return (abs(a-b)<eps).all()
    if isinstance(a, (Iterable,Generator)) or isinstance(b, (Iterable,Generator)):
        return all(abs(a_-b_)<eps for a_,b_ in zip(a,b))
    return abs(a-b)<eps

# %% ../nbs/00_test.ipynb 30
def test_close(a,b,eps=1e-5):
    "`test` that `a` is within `eps` of `b`"
    test(a,b,partial(is_close,eps=eps),'close')

# %% ../nbs/00_test.ipynb 32
def test_is(a,b):
    "`test` that `a is b`"
    test(a,b,operator.is_, 'is')

# %% ../nbs/00_test.ipynb 34
def test_shuffled(a,b):
    "`test` that `a` and `b` are shuffled versions of the same sequence of items"
    test_ne(a, b)
    test_eq(Counter(a), Counter(b))

# %% ../nbs/00_test.ipynb 38
def test_stdout(f, exp, regex=False):
    "Test that `f` prints `exp` to stdout, optionally checking as `regex`"
    s = io.StringIO()
    with redirect_stdout(s): f()
    if regex: assert re.search(exp, s.getvalue()) is not None, f"regex '{exp}' did not not match stdout '{s.getvalue()}'"
    else: test_eq(s.getvalue(), f'{exp}\n' if len(exp) > 0 else '')

# %% ../nbs/00_test.ipynb 40
def test_warns(f, show=False):
    with warnings.catch_warnings(record=True) as w:
        f()
        assert w, "No warnings raised"
        if show:
            for e in w: print(f"{e.category}: {e.message}")

# %% ../nbs/00_test.ipynb 43
TEST_IMAGE = 'images/puppy.jpg'

# %% ../nbs/00_test.ipynb 45
TEST_IMAGE_BW = 'images/mnist3.png'

# %% ../nbs/00_test.ipynb 47
def test_fig_exists(ax):
    "Test there is a figure displayed in `ax`"
    assert ax and len(ax.figure.canvas.tostring_argb())

# %% ../nbs/00_test.ipynb 50
class ExceptionExpected:
    "Context manager that tests if an exception is raised"
    def __init__(self, ex=Exception, regex=''): self.ex,self.regex = ex,regex
    def __enter__(self): pass
    def __exit__(self, type, value, traceback):
        if not isinstance(value, self.ex) or (self.regex and not re.search(self.regex, f'{value.args}')):
            raise TypeError(f"Expected {self.ex.__name__}({self.regex}) not raised.")
        return True

# %% ../nbs/00_test.ipynb 53
exception = ExceptionExpected()
