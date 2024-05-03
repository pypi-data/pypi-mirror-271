"""
Module mw_optimize


Defined at ../smash/fcore/optimize/mw_optimize.f90 lines 12-352

(MW) Module Wrapped.

Subroutine
----------

- sbs_optimize
- lbfgsb_optimize
- optimize
- multiple_optimize_sample_to_parameters
- multiple_optimize_save_parameters
- multiple_optimize
"""
from __future__ import print_function, absolute_import, division
from smash.fcore import _libfcore
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def sbs_optimize(self, mesh, input_data, parameters, output, options, returns):
    """
    sbs_optimize(self, mesh, input_data, parameters, output, options, returns)
    
    
    Defined at ../smash/fcore/optimize/mw_optimize.f90 lines 29-161
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    output : Outputdt
    options : Optionsdt
    returns : Returnsdt
    
    """
    _libfcore.f90wrap_sbs_optimize(setup=self._handle, mesh=mesh._handle, \
        input_data=input_data._handle, parameters=parameters._handle, \
        output=output._handle, options=options._handle, returns=returns._handle)

def lbfgsb_optimize(self, mesh, input_data, parameters, output, options, \
    returns):
    """
    lbfgsb_optimize(self, mesh, input_data, parameters, output, options, returns)
    
    
    Defined at ../smash/fcore/optimize/mw_optimize.f90 lines 163-241
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    output : Outputdt
    options : Optionsdt
    returns : Returnsdt
    
    """
    _libfcore.f90wrap_lbfgsb_optimize(setup=self._handle, mesh=mesh._handle, \
        input_data=input_data._handle, parameters=parameters._handle, \
        output=output._handle, options=options._handle, returns=returns._handle)

def optimize(self, mesh, input_data, parameters, output, options, returns):
    """
    optimize(self, mesh, input_data, parameters, output, options, returns)
    
    
    Defined at ../smash/fcore/optimize/mw_optimize.f90 lines 243-257
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    output : Outputdt
    options : Optionsdt
    returns : Returnsdt
    
    """
    _libfcore.f90wrap_optimize(setup=self._handle, mesh=mesh._handle, \
        input_data=input_data._handle, parameters=parameters._handle, \
        output=output._handle, options=options._handle, returns=returns._handle)

def multiple_optimize_sample_to_parameters(sample, samples_kind, samples_ind, \
    parameters):
    """
    multiple_optimize_sample_to_parameters(sample, samples_kind, samples_ind, \
        parameters)
    
    
    Defined at ../smash/fcore/optimize/mw_optimize.f90 lines 259-274
    
    Parameters
    ----------
    sample : float array
    samples_kind : int array
    samples_ind : int array
    parameters : Parametersdt
    
    """
    _libfcore.f90wrap_multiple_optimize_sample_to_parameters(sample=sample, \
        samples_kind=samples_kind, samples_ind=samples_ind, \
        parameters=parameters._handle)

def multiple_optimize_save_parameters(self, parameters, options, \
    optimized_parameters):
    """
    multiple_optimize_save_parameters(self, parameters, options, \
        optimized_parameters)
    
    
    Defined at ../smash/fcore/optimize/mw_optimize.f90 lines 276-294
    
    Parameters
    ----------
    setup : Setupdt
    parameters : Parametersdt
    options : Optionsdt
    optimized_parameters : float array
    
    """
    _libfcore.f90wrap_multiple_optimize_save_parameters(setup=self._handle, \
        parameters=parameters._handle, options=options._handle, \
        optimized_parameters=optimized_parameters)

def multiple_optimize(self, mesh, input_data, parameters, output, options, \
    samples, samples_kind, samples_ind, cost, q, optimized_parameters):
    """
    multiple_optimize(self, mesh, input_data, parameters, output, options, samples, \
        samples_kind, samples_ind, cost, q, optimized_parameters)
    
    
    Defined at ../smash/fcore/optimize/mw_optimize.f90 lines 296-352
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    output : Outputdt
    options : Optionsdt
    samples : float array
    samples_kind : int array
    samples_ind : int array
    cost : float array
    q : float array
    optimized_parameters : float array
    
    """
    _libfcore.f90wrap_multiple_optimize(setup=self._handle, mesh=mesh._handle, \
        input_data=input_data._handle, parameters=parameters._handle, \
        output=output._handle, options=options._handle, samples=samples, \
        samples_kind=samples_kind, samples_ind=samples_ind, cost=cost, q=q, \
        optimized_parameters=optimized_parameters)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "mw_optimize".')

for func in _dt_array_initialisers:
    func()
