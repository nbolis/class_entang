
# coding: utf-8

# In[ ]:

# import necessary modules
# uncomment to get plots displayed in notebook
#%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from classy import Class
from scipy.optimize import fsolve
from scipy.interpolate import interp1d
import math


# In[ ]:

# esthetic definitions for the plots
font = {'size'   : 16, 'family':'STIXGeneral'}
axislabelfontsize='large'
matplotlib.rc('font', **font)
matplotlib.mathtext.rcParams['legend.fontsize']='medium'
plt.rcParams["figure.figsize"] = [8.0,6.0]


# In[ ]:

#############################################
#
# Cosmological parameters and other CLASS parameters
#   custom1 = pivot scale k_0, 
#   custom2= amplitude A_s, 
#   custom3 = spectral index n_s,
#   custom4= mu, specator field hankel funciton order,
#   custom5 = alpha magnitude for SEn, 
#   custom6. must be <1 =  theta, bogolioubov phase, 
#   custom7 =  delta, bogoloiubov magnitude for MEn,
#   custom2= amplitude A_t, 
#   custom3 = tensor spectral index n_t

common_settings_entang = {
    'command' : '../external_Pk/generate_Pk_entang_w_tensors.py',
    'custom1' : 0.05,    
    'custom2' : 2.215e-9,
    'custom3' : 0.9624,
    'custom4' : 1.5,
    'custom5' : 1.0,
    'custom6' : 0.001, #1.5708,
    'custom7' : 0.01,
    'custom8' : 2.215e-9,
    'custom9' : 9.624,
    'h' : 0.67556,
    'T_cmb' : 2.7255,
    'omega_b' : 0.022032,
    'N_ur' : 3.046,
    'omega_cdm' : 0.12038,
    'Omega_dcdmdr' : 0.0,
    'N_ncdm' : 0,
    'Omega_k' : 0.,
    'Omega_fld' : 0,
    'Omega_scf' : 0,
    'YHe' : 'BBN',
    'recombination' : 'RECFAST',
    'reio_parametrization' : 'reio_camb',
    'z_reio' : 11.357,
    'reionization_exponent' : 1.5,
    'reionization_width' : 0.5,
    'helium_fullreio_redshift' : 3.5,
    'helium_fullreio_width' : 0.5,
    'annihilation' : 0.,
    'decay' : 0.,
    'output' : 'tCl,pCl,lCl',
    'modes' : 's',
    'lensing' : 'yes',
    'ic' : 'ad',
    'gauge' : 'synchronous',
    'P_k_ini type' : 'external_Pk',
    'k_pivot' : 0.05,
    'l_max_scalars' : 3000,
}


 

common_settings = {# wich output? ClTT, transfer functions delta_i and theta_i
                   'output':'tCl,pCl,lCl',
                   'lensing':'yes',
                   # LambdaCDM parameters
                   'h':0.67556,
                   'omega_b':0.022032,
                   'omega_cdm':0.12038,
                   'A_s':2.215e-9,
                   'n_s':0.9619,
                   'tau_reio':0.0925,
                   'r' : 0.1,
                   'n_t' : 'scc',        
                   'alpha_t' : 'scc',
                   'modes' : 's,t',
                   # Take fixed value for primordial Helium (instead of automatic BBN adjustment)
                   'YHe':0.246,
                   # other output and precision parameters
                   'l_max_scalars':5000}
###############
#
# call CLASS
#

### normal one #####
M = Class()
M.set(common_settings)
M.compute()
cl_tot_normal = M.raw_cl(3000)
cl_lensed_normal = M.lensed_cl(3000)
M.struct_cleanup()  # clean output
M.empty()      


M = Class()
M.set(common_settings_entang)
M.compute()
cl_tot = M.raw_cl(3000)
cl_lensed = M.lensed_cl(3000)
M.struct_cleanup()  # clean output
M.empty()           # clean input
#
M.set(common_settings_entang) # new input
M.set({'temperature contributions':'tsw'})
M.compute()
cl_tsw = M.raw_cl(3000)
M.struct_cleanup()
M.empty()
#
M.set(common_settings_entang)
M.set({'temperature contributions':'eisw'})
M.compute()
cl_eisw = M.raw_cl(3000)
M.struct_cleanup()
M.empty()
#
M.set(common_settings_entang)
M.set({'temperature contributions':'lisw'})
M.compute()
cl_lisw = M.raw_cl(3000)
M.struct_cleanup()
M.empty()
#
M.set(common_settings_entang)
M.set({'temperature contributions':'dop'})
M.compute()
cl_dop = M.raw_cl(3000)
#
#################
#
# start plotting
#
#################
#

## comparing regular and entangled


plt.xlim([2,3000])
plt.xlabel(r"$\ell$")
plt.ylabel(r"$\ell (\ell+1) C_l^{TT} / 2 \pi \,\,\, [\times 10^{10}]$")
plt.grid()
#
ell = cl_tot['ell']
factor = 1.e10*ell*(ell+1.)/2./math.pi

plt.semilogx(ell,factor*cl_tot['tt'],'r-',label=r'$\mathrm{total}$')
plt.semilogx(ell,factor*cl_tot_normal['tt'],'k-',label=r'$\mathrm{tot norm}$')



#plt.xlim([2,3000])

#plt.xlabel(r"$\ell$")
#plt.ylabel(r"$\ell (\ell+1) C_l^{TT} / 2 \pi \,\,\, [\times 10^{10}]$")
#plt.grid()
#
#ell = cl_tot['ell']
#factor = 1.e10*ell*(ell+1.)/2./math.pi
#plt.semilogx(ell,factor*cl_tsw['tt'],'c-',label=r'$\mathrm{T+SW}$')
#plt.semilogx(ell,factor*cl_eisw['tt'],'r-',label=r'$\mathrm{early-ISW}$')
#plt.semilogx(ell,factor*cl_lisw['tt'],'y-',label=r'$\mathrm{late-ISW}$')
#plt.semilogx(ell,factor*cl_dop['tt'],'g-',label=r'$\mathrm{Doppler}$')
#plt.semilogx(ell,factor*cl_tot['tt'],'r-',label=r'$\mathrm{total}$')
#plt.semilogx(ell,factor*cl_lensed['tt'],'k-',label=r'$\mathrm{lensed}$')
#
plt.legend(loc='right',bbox_to_anchor=(1.4, 0.5))


# In[ ]:

plt.savefig('cltt_terms.pdf',bbox_inches='tight')
