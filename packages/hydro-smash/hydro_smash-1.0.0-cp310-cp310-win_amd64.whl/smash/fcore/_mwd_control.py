"""
Module mwd_control


Defined at ../smash/fcore/derived_type/mwd_control.f90 lines 25-91

(MWD) Module Wrapped and Differentiated.

Type
----

- ControlDT
Control vector used in optimize and quantities required by the optimizer

========================== =====================================
`Variables`                Description
========================== =====================================
``x``                      Control vector
``l``                      Control vector lower bound
``u``                      Control vector upper bound
``x_bkg``                  Control vector background
``l_bkg``                  Control vector lower bound background
``u_bkg``                  Control vector upper bound background
``nbd``                    Control vector kind of bound

----------

- ControlDT_initialise
- ControlDT_copy
"""
from __future__ import print_function, absolute_import, division
from smash.fcore._f90wrap_decorator import f90wrap_getter_char_array, f90wrap_setter_char_array
from smash.fcore import _libfcore
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("libfcore.ControlDT")
class ControlDT(f90wrap.runtime.FortranDerivedType):
    def dealloc(self):
        return controldt_dealloc(self)
    def copy(self):
        return controldt_copy(self)
    """
    Type(name=controldt)
    
    
    Defined at ../smash/fcore/derived_type/mwd_control.f90 lines 28-39
    
    """
    def __init__(self, nbk, handle=None):
        """
        self = Controldt(nbk)
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 lines 42-64
        
        Parameters
        ----------
        nbk : int array
        
        Returns
        -------
        this : Controldt
        
        only: sp
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _libfcore.f90wrap_controldt_initialise(nbk=nbk)
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Controldt
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 lines 66-78
        
        Parameters
        ----------
        this : Controldt
        
        """
        try:
            if self._alloc:
                _libfcore.f90wrap_controldt_finalise(this=self._handle)
        except:
            pass
    
    @property
    def n(self):
        """
        Element n ftype=integer  pytype=int
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 29
        
        """
        return _libfcore.f90wrap_controldt__get__n(self._handle)
    
    @n.setter
    def n(self, n):
        _libfcore.f90wrap_controldt__set__n(self._handle, n)
    
    @property
    def nbk(self):
        """
        Element nbk ftype=integer pytype=int
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 31
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_controldt__array__nbk(self._handle)
        if array_handle in self._arrays:
            nbk = self._arrays[array_handle]
        else:
            nbk = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_controldt__array__nbk)
            self._arrays[array_handle] = nbk
        return nbk
    
    @nbk.setter
    def nbk(self, nbk):
        self.nbk[...] = nbk
    
    @property
    def x(self):
        """
        Element x ftype=real(sp) pytype=float
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 32
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_controldt__array__x(self._handle)
        if array_handle in self._arrays:
            x = self._arrays[array_handle]
        else:
            x = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_controldt__array__x)
            self._arrays[array_handle] = x
        return x
    
    @x.setter
    def x(self, x):
        self.x[...] = x
    
    @property
    def l(self):
        """
        Element l ftype=real(sp) pytype=float
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 33
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_controldt__array__l(self._handle)
        if array_handle in self._arrays:
            l = self._arrays[array_handle]
        else:
            l = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_controldt__array__l)
            self._arrays[array_handle] = l
        return l
    
    @l.setter
    def l(self, l):
        self.l[...] = l
    
    @property
    def u(self):
        """
        Element u ftype=real(sp) pytype=float
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 34
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_controldt__array__u(self._handle)
        if array_handle in self._arrays:
            u = self._arrays[array_handle]
        else:
            u = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_controldt__array__u)
            self._arrays[array_handle] = u
        return u
    
    @u.setter
    def u(self, u):
        self.u[...] = u
    
    @property
    def x_bkg(self):
        """
        Element x_bkg ftype=real(sp) pytype=float
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 35
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_controldt__array__x_bkg(self._handle)
        if array_handle in self._arrays:
            x_bkg = self._arrays[array_handle]
        else:
            x_bkg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_controldt__array__x_bkg)
            self._arrays[array_handle] = x_bkg
        return x_bkg
    
    @x_bkg.setter
    def x_bkg(self, x_bkg):
        self.x_bkg[...] = x_bkg
    
    @property
    def l_bkg(self):
        """
        Element l_bkg ftype=real(sp) pytype=float
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 36
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_controldt__array__l_bkg(self._handle)
        if array_handle in self._arrays:
            l_bkg = self._arrays[array_handle]
        else:
            l_bkg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_controldt__array__l_bkg)
            self._arrays[array_handle] = l_bkg
        return l_bkg
    
    @l_bkg.setter
    def l_bkg(self, l_bkg):
        self.l_bkg[...] = l_bkg
    
    @property
    def u_bkg(self):
        """
        Element u_bkg ftype=real(sp) pytype=float
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 37
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_controldt__array__u_bkg(self._handle)
        if array_handle in self._arrays:
            u_bkg = self._arrays[array_handle]
        else:
            u_bkg = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_controldt__array__u_bkg)
            self._arrays[array_handle] = u_bkg
        return u_bkg
    
    @u_bkg.setter
    def u_bkg(self, u_bkg):
        self.u_bkg[...] = u_bkg
    
    @property
    def nbd(self):
        """
        Element nbd ftype=integer pytype=int
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 38
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_controldt__array__nbd(self._handle)
        if array_handle in self._arrays:
            nbd = self._arrays[array_handle]
        else:
            nbd = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_controldt__array__nbd)
            self._arrays[array_handle] = nbd
        return nbd
    
    @nbd.setter
    def nbd(self, nbd):
        self.nbd[...] = nbd
    
    @property
    @f90wrap_getter_char_array
    def name(self):
        """
        Element name ftype=character(lchar) pytype=str
        
        
        Defined at ../smash/fcore/derived_type/mwd_control.f90 line 39
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_controldt__array__name(self._handle)
        if array_handle in self._arrays:
            name = self._arrays[array_handle]
        else:
            name = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_controldt__array__name)
            self._arrays[array_handle] = name
        return name
    
    @name.setter
    @f90wrap_setter_char_array
    def name(self, name):
        self.name[...] = name
    
    
    def __repr__(self):
        ret = [self.__class__.__name__]
        for attr in dir(self):
            if attr.startswith("_"):
                continue
            try:
                value = getattr(self, attr)
            except Exception:
                continue
            if callable(value):
                continue
            elif isinstance(value, f90wrap.runtime.FortranDerivedTypeArray):
                n = len(value)
                nrepr = 4
                if n == 0:
                    continue
                else:
                    repr_value = [value[0].__class__.__name__] * min(n, nrepr)
                if n > nrepr:
                    repr_value.insert(2, "...")
                repr_value = repr(repr_value)
            else:
                repr_value = repr(value)
            ret.append(f"    {attr}: {repr_value}")
        return "\n".join(ret)
    
    
    _dt_array_initialisers = []
    

def controldt_copy(self):
    """
    this_copy = controldt_copy(self)
    
    
    Defined at ../smash/fcore/derived_type/mwd_control.f90 lines 80-84
    
    Parameters
    ----------
    this : Controldt
    
    Returns
    -------
    this_copy : Controldt
    
    """
    this_copy = _libfcore.f90wrap_controldt_copy(this=self._handle)
    this_copy = \
        f90wrap.runtime.lookup_class("libfcore.ControlDT").from_handle(this_copy, \
        alloc=True)
    return this_copy

def controldt_dealloc(self):
    """
    controldt_dealloc(self)
    
    
    Defined at ../smash/fcore/derived_type/mwd_control.f90 lines 88-91
    
    Parameters
    ----------
    this : Controldt
    
    """
    _libfcore.f90wrap_controldt_dealloc(this=self._handle)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "mwd_control".')

for func in _dt_array_initialisers:
    func()
