"""
Module mwd_parameters_manipulation


Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 60-1058

(MWD) Module Wrapped and Differentiated

Subroutine
----------

- get_serr_mu
- get_serr_sigma
- get_rr_parameters
- get_rr_states
- get_serr_mu_parameters
- get_serr_sigma_parameters
- set_rr_parameters
- set_rr_states
- set_serr_mu_parameters
- set_serr_sigma_parameters
- sigmoide
- inv_sigmoide
- scaled_sigmoide
- inv_scaled_sigmoid
- sigmoide2d
- scaled_sigmoide2d
- sbs_control_tfm
- sbs_inv_control_tfm
- normalize_control_tfm
- normalize_inv_control_tfm
- control_tfm
- inv_control_tfm
- uniform_rr_parameters_get_control_size
- uniform_rr_initial_states_get_control_size
- distributed_rr_parameters_get_control_size
- distributed_rr_initial_states_get_control_size
- multi_linear_rr_parameters_get_control_size
- multi_linear_rr_initial_states_get_control_size
- multi_polynomial_rr_parameters_get_control_size
- multi_polynomial_rr_initial_states_get_control_size
- serr_mu_parameters_get_control_size
- get_control_sizes
- uniform_rr_parameters_fill_control
- uniform_rr_initial_states_fill_control
- distributed_rr_parameters_fill_control
- distributed_rr_initial_states_fill_control
- multi_linear_rr_parameters_fill_control
- multi_linear_rr_initial_states_fill_control
- multi_polynomial_rr_parameters_fill_control
- multi_polynomial_rr_initial_states_fill_control
- serr_mu_parameters_fill_control
- serr_sigma_parameters_fill_control
- fill_control
- uniform_rr_parameters_fill_parameters
- uniform_rr_initial_states_fill_parameters
- distributed_rr_parameters_fill_parameters
- distributed_rr_initial_states_fill_parameters
- multi_linear_rr_parameters_fill_parameters
- multi_linear_rr_initial_states_fill_parameters
- multi_polynomial_rr_parameters_fill_parameters
- multi_polynomial_rr_initial_states_fill_parameters
- serr_mu_parameters_fill_parameters
- serr_sigma_parameters_fill_parameters
- fill_parameters
"""
from __future__ import print_function, absolute_import, division
from smash.fcore import _libfcore
import f90wrap.runtime
import logging
import numpy

_arrays = {}
_objs = {}

def get_serr_mu(self, mesh, parameters, output, serr_mu):
    """
    get_serr_mu(self, mesh, parameters, output, serr_mu)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 78-92
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    output : Outputdt
    serr_mu : float array
    
    only: MuFunk_vect, SigmaFunk_vect
    only: sp, dp
    only: SetupDT
    only: MeshDT
    only: Input_DataDT
    only: ParametersDT
    only: RR_ParametersDT
    only: RR_StatesDT
    only: SErr_Mu_ParametersDT
    only: SErr_Sigma_ParametersDT
    only: OutputDT
    only: OptionsDT
    only: ReturnsDT
    only: ControlDT_initialise, ControlDT_finalise
    """
    _libfcore.f90wrap_get_serr_mu(setup=self._handle, mesh=mesh._handle, \
        parameters=parameters._handle, output=output._handle, serr_mu=serr_mu)

def get_serr_sigma(self, mesh, parameters, output, serr_sigma):
    """
    get_serr_sigma(self, mesh, parameters, output, serr_sigma)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 96-110
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    output : Outputdt
    serr_sigma : float array
    
    """
    _libfcore.f90wrap_get_serr_sigma(setup=self._handle, mesh=mesh._handle, \
        parameters=parameters._handle, output=output._handle, serr_sigma=serr_sigma)

def get_rr_parameters(self, key, vle):
    """
    get_rr_parameters(self, key, vle)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 113-126
    
    Parameters
    ----------
    rr_parameters : Rr_Parametersdt
    key : str
    vle : float array
    
    """
    _libfcore.f90wrap_get_rr_parameters(rr_parameters=self._handle, key=key, \
        vle=vle)

def get_rr_states(self, key, vle):
    """
    get_rr_states(self, key, vle)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 128-141
    
    Parameters
    ----------
    rr_states : Rr_Statesdt
    key : str
    vle : float array
    
    """
    _libfcore.f90wrap_get_rr_states(rr_states=self._handle, key=key, vle=vle)

def get_serr_mu_parameters(self, key, vle):
    """
    get_serr_mu_parameters(self, key, vle)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 143-156
    
    Parameters
    ----------
    serr_mu_parameters : Serr_Mu_Parametersdt
    key : str
    vle : float array
    
    """
    _libfcore.f90wrap_get_serr_mu_parameters(serr_mu_parameters=self._handle, \
        key=key, vle=vle)

def get_serr_sigma_parameters(self, key, vle):
    """
    get_serr_sigma_parameters(self, key, vle)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 158-171
    
    Parameters
    ----------
    serr_sigma_parameters : Serr_Sigma_Parametersdt
    key : str
    vle : float array
    
    """
    _libfcore.f90wrap_get_serr_sigma_parameters(serr_sigma_parameters=self._handle, \
        key=key, vle=vle)

def set_rr_parameters(self, key, vle):
    """
    set_rr_parameters(self, key, vle)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 173-186
    
    Parameters
    ----------
    rr_parameters : Rr_Parametersdt
    key : str
    vle : float array
    
    """
    _libfcore.f90wrap_set_rr_parameters(rr_parameters=self._handle, key=key, \
        vle=vle)

def set_rr_states(self, key, vle):
    """
    set_rr_states(self, key, vle)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 188-201
    
    Parameters
    ----------
    rr_states : Rr_Statesdt
    key : str
    vle : float array
    
    """
    _libfcore.f90wrap_set_rr_states(rr_states=self._handle, key=key, vle=vle)

def set_serr_mu_parameters(self, key, vle):
    """
    set_serr_mu_parameters(self, key, vle)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 203-216
    
    Parameters
    ----------
    serr_mu_parameters : Serr_Mu_Parametersdt
    key : str
    vle : float array
    
    """
    _libfcore.f90wrap_set_serr_mu_parameters(serr_mu_parameters=self._handle, \
        key=key, vle=vle)

def set_serr_sigma_parameters(self, key, vle):
    """
    set_serr_sigma_parameters(self, key, vle)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 218-231
    
    Parameters
    ----------
    serr_sigma_parameters : Serr_Sigma_Parametersdt
    key : str
    vle : float array
    
    """
    _libfcore.f90wrap_set_serr_sigma_parameters(serr_sigma_parameters=self._handle, \
        key=key, vle=vle)

def sigmoide(x, res):
    """
    sigmoide(x, res)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 233-237
    
    Parameters
    ----------
    x : float
    res : float
    
    """
    _libfcore.f90wrap_sigmoide(x=x, res=res)

def inv_sigmoide(x, res):
    """
    inv_sigmoide(x, res)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 239-243
    
    Parameters
    ----------
    x : float
    res : float
    
    """
    _libfcore.f90wrap_inv_sigmoide(x=x, res=res)

def scaled_sigmoide(x, l, u, res):
    """
    scaled_sigmoide(x, l, u, res)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 245-250
    
    Parameters
    ----------
    x : float
    l : float
    u : float
    res : float
    
    """
    _libfcore.f90wrap_scaled_sigmoide(x=x, l=l, u=u, res=res)

def inv_scaled_sigmoid(x, l, u, res):
    """
    inv_scaled_sigmoid(x, l, u, res)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 252-260
    
    Parameters
    ----------
    x : float
    l : float
    u : float
    res : float
    
    """
    _libfcore.f90wrap_inv_scaled_sigmoid(x=x, l=l, u=u, res=res)

def sigmoide2d(x, res):
    """
    sigmoide2d(x, res)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 262-266
    
    Parameters
    ----------
    x : float array
    res : float array
    
    """
    _libfcore.f90wrap_sigmoide2d(x=x, res=res)

def scaled_sigmoide2d(x, l, u, res):
    """
    scaled_sigmoide2d(x, l, u, res)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 268-274
    
    Parameters
    ----------
    x : float array
    l : float
    u : float
    res : float array
    
    """
    _libfcore.f90wrap_scaled_sigmoide2d(x=x, l=l, u=u, res=res)

def sbs_control_tfm(self):
    """
    sbs_control_tfm(self)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 276-299
    
    Parameters
    ----------
    parameters : Parametersdt
    
    """
    _libfcore.f90wrap_sbs_control_tfm(parameters=self._handle)

def sbs_inv_control_tfm(self):
    """
    sbs_inv_control_tfm(self)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 301-320
    
    Parameters
    ----------
    parameters : Parametersdt
    
    """
    _libfcore.f90wrap_sbs_inv_control_tfm(parameters=self._handle)

def normalize_control_tfm(self):
    """
    normalize_control_tfm(self)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 322-333
    
    Parameters
    ----------
    parameters : Parametersdt
    
    """
    _libfcore.f90wrap_normalize_control_tfm(parameters=self._handle)

def normalize_inv_control_tfm(self):
    """
    normalize_inv_control_tfm(self)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 335-346
    
    Parameters
    ----------
    parameters : Parametersdt
    
    """
    _libfcore.f90wrap_normalize_inv_control_tfm(parameters=self._handle)

def control_tfm(self, options):
    """
    control_tfm(self, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 348-357
    
    Parameters
    ----------
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_control_tfm(parameters=self._handle, options=options._handle)

def inv_control_tfm(self, options):
    """
    inv_control_tfm(self, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 359-368
    
    Parameters
    ----------
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_inv_control_tfm(parameters=self._handle, \
        options=options._handle)

def uniform_rr_parameters_get_control_size(self, n):
    """
    uniform_rr_parameters_get_control_size(self, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 370-374
    
    Parameters
    ----------
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_uniform_rr_parameters_get_control_size(options=self._handle, \
        n=n)

def uniform_rr_initial_states_get_control_size(self, n):
    """
    uniform_rr_initial_states_get_control_size(self, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 376-380
    
    Parameters
    ----------
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_uniform_rr_initial_states_get_control_size(options=self._handle, \
        n=n)

def distributed_rr_parameters_get_control_size(self, options, n):
    """
    distributed_rr_parameters_get_control_size(self, options, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 382-387
    
    Parameters
    ----------
    mesh : Meshdt
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_distributed_rr_parameters_get_control_size(mesh=self._handle, \
        options=options._handle, n=n)

def distributed_rr_initial_states_get_control_size(self, options, n):
    """
    distributed_rr_initial_states_get_control_size(self, options, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 389-394
    
    Parameters
    ----------
    mesh : Meshdt
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_distributed_rr_initial_states_get_control_size(mesh=self._handle, \
        options=options._handle, n=n)

def multi_linear_rr_parameters_get_control_size(self, options, n):
    """
    multi_linear_rr_parameters_get_control_size(self, options, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 396-406
    
    Parameters
    ----------
    setup : Setupdt
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_multi_linear_rr_parameters_get_control_size(setup=self._handle, \
        options=options._handle, n=n)

def multi_linear_rr_initial_states_get_control_size(self, options, n):
    """
    multi_linear_rr_initial_states_get_control_size(self, options, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 408-418
    
    Parameters
    ----------
    setup : Setupdt
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_multi_linear_rr_initial_states_get_control_size(setup=self._handle, \
        options=options._handle, n=n)

def multi_polynomial_rr_parameters_get_control_size(self, options, n):
    """
    multi_polynomial_rr_parameters_get_control_size(self, options, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 420-430
    
    Parameters
    ----------
    setup : Setupdt
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_multi_polynomial_rr_parameters_get_control_size(setup=self._handle, \
        options=options._handle, n=n)

def multi_polynomial_rr_initial_states_get_control_size(self, options, n):
    """
    multi_polynomial_rr_initial_states_get_control_size(self, options, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 432-442
    
    Parameters
    ----------
    setup : Setupdt
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_multi_polynomial_rr_initial_states_get_control_size(setup=self._handle, \
        options=options._handle, n=n)

def serr_mu_parameters_get_control_size(self, n):
    """
    serr_mu_parameters_get_control_size(self, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 444-448
    
    Parameters
    ----------
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_serr_mu_parameters_get_control_size(options=self._handle, n=n)

def serr_sigma_parameters_get_control_size(self, n):
    """
    serr_sigma_parameters_get_control_size(self, n)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 450-454
    
    Parameters
    ----------
    options : Optionsdt
    n : int
    
    """
    _libfcore.f90wrap_serr_sigma_parameters_get_control_size(options=self._handle, \
        n=n)

def get_control_sizes(self, mesh, options, nbk):
    """
    get_control_sizes(self, mesh, options, nbk)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 456-478
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    options : Optionsdt
    nbk : int array
    
    """
    _libfcore.f90wrap_get_control_sizes(setup=self._handle, mesh=mesh._handle, \
        options=options._handle, nbk=nbk)

def uniform_rr_parameters_fill_control(self, mesh, parameters, options):
    """
    uniform_rr_parameters_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 480-499
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_uniform_rr_parameters_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def uniform_rr_initial_states_fill_control(self, mesh, parameters, options):
    """
    uniform_rr_initial_states_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 501-520
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_uniform_rr_initial_states_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def distributed_rr_parameters_fill_control(self, mesh, parameters, options):
    """
    distributed_rr_parameters_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 522-546
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_distributed_rr_parameters_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def distributed_rr_initial_states_fill_control(self, mesh, parameters, options):
    """
    distributed_rr_initial_states_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 548-572
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_distributed_rr_initial_states_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def multi_linear_rr_parameters_fill_control(self, mesh, parameters, options):
    """
    multi_linear_rr_parameters_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 574-603
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_multi_linear_rr_parameters_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def multi_linear_rr_initial_states_fill_control(self, mesh, parameters, \
    options):
    """
    multi_linear_rr_initial_states_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 605-634
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_multi_linear_rr_initial_states_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def multi_polynomial_rr_parameters_fill_control(self, mesh, parameters, \
    options):
    """
    multi_polynomial_rr_parameters_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 636-671
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_multi_polynomial_rr_parameters_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def multi_polynomial_rr_initial_states_fill_control(self, mesh, parameters, \
    options):
    """
    multi_polynomial_rr_initial_states_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 673-708
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_multi_polynomial_rr_initial_states_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def serr_mu_parameters_fill_control(self, mesh, parameters, options):
    """
    serr_mu_parameters_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 710-730
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_serr_mu_parameters_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def serr_sigma_parameters_fill_control(self, mesh, parameters, options):
    """
    serr_sigma_parameters_fill_control(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 732-752
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_serr_sigma_parameters_fill_control(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def fill_control(self, mesh, input_data, parameters, options):
    """
    fill_control(self, mesh, input_data, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 754-781
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_fill_control(setup=self._handle, mesh=mesh._handle, \
        input_data=input_data._handle, parameters=parameters._handle, \
        options=options._handle)

def uniform_rr_parameters_fill_parameters(self, mesh, parameters, options):
    """
    uniform_rr_parameters_fill_parameters(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 783-800
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_uniform_rr_parameters_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def uniform_rr_initial_states_fill_parameters(self, mesh, parameters, options):
    """
    uniform_rr_initial_states_fill_parameters(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 802-819
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_uniform_rr_initial_states_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def distributed_rr_parameters_fill_parameters(self, mesh, parameters, options):
    """
    distributed_rr_parameters_fill_parameters(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 821-839
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_distributed_rr_parameters_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def distributed_rr_initial_states_fill_parameters(self, mesh, parameters, \
    options):
    """
    distributed_rr_initial_states_fill_parameters(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 841-859
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_distributed_rr_initial_states_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def multi_linear_rr_parameters_fill_parameters(self, mesh, input_data, \
    parameters, options):
    """
    multi_linear_rr_parameters_fill_parameters(self, mesh, input_data, parameters, \
        options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 861-887
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_multi_linear_rr_parameters_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, input_data=input_data._handle, \
        parameters=parameters._handle, options=options._handle)

def multi_linear_rr_initial_states_fill_parameters(self, mesh, input_data, \
    parameters, options):
    """
    multi_linear_rr_initial_states_fill_parameters(self, mesh, input_data, \
        parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 889-915
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_multi_linear_rr_initial_states_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, input_data=input_data._handle, \
        parameters=parameters._handle, options=options._handle)

def multi_polynomial_rr_parameters_fill_parameters(self, mesh, input_data, \
    parameters, options):
    """
    multi_polynomial_rr_parameters_fill_parameters(self, mesh, input_data, \
        parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 917-944
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_multi_polynomial_rr_parameters_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, input_data=input_data._handle, \
        parameters=parameters._handle, options=options._handle)

def multi_polynomial_rr_initial_states_fill_parameters(self, mesh, input_data, \
    parameters, options):
    """
    multi_polynomial_rr_initial_states_fill_parameters(self, mesh, input_data, \
        parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 946-973
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_multi_polynomial_rr_initial_states_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, input_data=input_data._handle, \
        parameters=parameters._handle, options=options._handle)

def serr_mu_parameters_fill_parameters(self, mesh, parameters, options):
    """
    serr_mu_parameters_fill_parameters(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 975-991
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_serr_mu_parameters_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def serr_sigma_parameters_fill_parameters(self, mesh, parameters, options):
    """
    serr_sigma_parameters_fill_parameters(self, mesh, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines 993-1009
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_serr_sigma_parameters_fill_parameters(setup=self._handle, \
        mesh=mesh._handle, parameters=parameters._handle, options=options._handle)

def fill_parameters(self, mesh, input_data, parameters, options):
    """
    fill_parameters(self, mesh, input_data, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines \
        1011-1034
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_fill_parameters(setup=self._handle, mesh=mesh._handle, \
        input_data=input_data._handle, parameters=parameters._handle, \
        options=options._handle)

def parameters_to_control(self, mesh, input_data, parameters, options):
    """
    parameters_to_control(self, mesh, input_data, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines \
        1036-1047
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_parameters_to_control(setup=self._handle, mesh=mesh._handle, \
        input_data=input_data._handle, parameters=parameters._handle, \
        options=options._handle)

def control_to_parameters(self, mesh, input_data, parameters, options):
    """
    control_to_parameters(self, mesh, input_data, parameters, options)
    
    
    Defined at ../smash/fcore/routine/mwd_parameters_manipulation.f90 lines \
        1049-1058
    
    Parameters
    ----------
    setup : Setupdt
    mesh : Meshdt
    input_data : Input_Datadt
    parameters : Parametersdt
    options : Optionsdt
    
    """
    _libfcore.f90wrap_control_to_parameters(setup=self._handle, mesh=mesh._handle, \
        input_data=input_data._handle, parameters=parameters._handle, \
        options=options._handle)


_array_initialisers = []
_dt_array_initialisers = []

try:
    for func in _array_initialisers:
        func()
except ValueError:
    logging.debug('unallocated array(s) detected on import of module \
        "mwd_parameters_manipulation".')

for func in _dt_array_initialisers:
    func()
