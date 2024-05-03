"""
Module mwd_physio_data


Defined at ../smash/fcore/derived_type/mwd_physio_data.f90 lines 22-49

(MWD) Module Wrapped and Differentiated.

Type
----

- Physio_DataDT
Physiographic data used to force the regionalization, among other things.

======================== =======================================
`Variables`              Description
======================== =======================================
``descriptor`` Descriptor maps field [(descriptor dependent)]
``l_descriptor`` Descriptor maps field min value [(descriptor dependent)]
``u_descriptor`` Descriptor maps field max value [(descriptor dependent)]
======================== =======================================

Subroutine
----------

- Physio_DataDT_initialise
- Physio_DataDT_copy
"""
from __future__ import print_function, absolute_import, division
from smash.fcore import _libfcore
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

@f90wrap.runtime.register_class("libfcore.Physio_DataDT")
class Physio_DataDT(f90wrap.runtime.FortranDerivedType):
    def copy(self):
        return physio_datadt_copy(self)
    """
    Type(name=physio_datadt)
    
    
    Defined at ../smash/fcore/derived_type/mwd_physio_data.f90 lines 27-30
    
    """
    def __init__(self, setup, mesh, handle=None):
        """
        self = Physio_Datadt(setup, mesh)
        
        
        Defined at ../smash/fcore/derived_type/mwd_physio_data.f90 lines 33-43
        
        Parameters
        ----------
        setup : Setupdt
        mesh : Meshdt
        
        Returns
        -------
        this : Physio_Datadt
        
        only: sp
        only: SetupDT
        only: MeshDT
        """
        f90wrap.runtime.FortranDerivedType.__init__(self)
        result = _libfcore.f90wrap_physio_datadt_initialise(setup=setup._handle, \
            mesh=mesh._handle)
        self._handle = result[0] if isinstance(result, tuple) else result
    
    def __del__(self):
        """
        Destructor for class Physio_Datadt
        
        
        Defined at ../smash/fcore/derived_type/mwd_physio_data.f90 lines 27-30
        
        Parameters
        ----------
        this : Physio_Datadt
            Object to be destructed
        
        
        Automatically generated destructor for physio_datadt
        """
        try:
            if self._alloc:
                _libfcore.f90wrap_physio_datadt_finalise(this=self._handle)
        except:
            pass
    
    @property
    def descriptor(self):
        """
        Element descriptor ftype=real(sp) pytype=float
        
        
        Defined at ../smash/fcore/derived_type/mwd_physio_data.f90 line 28
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_physio_datadt__array__descriptor(self._handle)
        if array_handle in self._arrays:
            descriptor = self._arrays[array_handle]
        else:
            descriptor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_physio_datadt__array__descriptor)
            self._arrays[array_handle] = descriptor
        return descriptor
    
    @descriptor.setter
    def descriptor(self, descriptor):
        self.descriptor[...] = descriptor
    
    @property
    def l_descriptor(self):
        """
        Element l_descriptor ftype=real(sp) pytype=float
        
        
        Defined at ../smash/fcore/derived_type/mwd_physio_data.f90 line 29
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_physio_datadt__array__l_descriptor(self._handle)
        if array_handle in self._arrays:
            l_descriptor = self._arrays[array_handle]
        else:
            l_descriptor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_physio_datadt__array__l_descriptor)
            self._arrays[array_handle] = l_descriptor
        return l_descriptor
    
    @l_descriptor.setter
    def l_descriptor(self, l_descriptor):
        self.l_descriptor[...] = l_descriptor
    
    @property
    def u_descriptor(self):
        """
        Element u_descriptor ftype=real(sp) pytype=float
        
        
        Defined at ../smash/fcore/derived_type/mwd_physio_data.f90 line 30
        
        """
        array_ndim, array_type, array_shape, array_handle = \
            _libfcore.f90wrap_physio_datadt__array__u_descriptor(self._handle)
        if array_handle in self._arrays:
            u_descriptor = self._arrays[array_handle]
        else:
            u_descriptor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                    self._handle,
                                    _libfcore.f90wrap_physio_datadt__array__u_descriptor)
            self._arrays[array_handle] = u_descriptor
        return u_descriptor
    
    @u_descriptor.setter
    def u_descriptor(self, u_descriptor):
        self.u_descriptor[...] = u_descriptor
    
    
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
    

def physio_datadt_copy(self):
    """
    this_copy = physio_datadt_copy(self)
    
    
    Defined at ../smash/fcore/derived_type/mwd_physio_data.f90 lines 45-49
    
    Parameters
    ----------
    this : Physio_Datadt
    
    Returns
    -------
    this_copy : Physio_Datadt
    
    """
    this_copy = _libfcore.f90wrap_physio_datadt_copy(this=self._handle)
    this_copy = \
        f90wrap.runtime.lookup_class("libfcore.Physio_DataDT").from_handle(this_copy, \
        alloc=True)
    return this_copy


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "mwd_physio_data".')

for func in _dt_array_initialisers:
    func()
