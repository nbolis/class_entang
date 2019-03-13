#!/usr/bin/python
from __future__ import print_function
import sys
from math import exp
import numpy as np

# README:
#
# This is an example python script for the external_Pk mode of Class.
# It generates the primordial spectrum of LambdaCDM.
# It can be edited and used directly, though keeping a copy of it is recommended.
#
# Two (maybe three) things need to be edited:
#
# 1. The name of the parameters needed for the calculation of Pk.
#    "sys.argv[1]" corresponds to "custom1" in Class, an so on

try :
    k_0           = float(sys.argv[1])
    A             = float(sys.argv[2])
    n_s           = float(sys.argv[3])
    mu            = float(sys.argv[4])                 # spectator field hankel function order (controlls mass)
    alpha         = float(sys.argv[5])                 # bogoloubov parameter magnitude
    theta         = float(sys.argv[6])                 # theta_alpha + theta_gamma   phases of bogolioubov 
    delta         = float(sys.argv[7])                 # delta bogolioubov parameter amplitude              
   # gamma          = float(sys.argv[6])

# Error control, no need to touch
except IndexError :
    raise IndexError("It seems you are calling this script with too few arguments.")
except ValueError :
    raise ValueError("It seems some of the arguments are not correctly formatted. "+
                     "Remember that they must be floating point numbers.")

# 2. The function giving P(k), including the necessary import statements.
#    Inside this function, you can use the parameters named in the previous step.

#### Pk for simple entangled case SEn, only anihilation operators from the two fields mixing, and massless spectator. Here |gamma|^2 = 1-|alpha|^2

def P(k) :
    return A * ((alpha**2) *  (k/k_0)**(n_s-1.) + (1.-alpha**2) *  (k/k_0)**(3.- 2.* mu)+ 2.0* alpha * np.sqrt(1.-alpha**2) * np.cos(theta)* (k/k_0)**(0.5 * n_s +1. - mu ))

#### Pk for mixed entangled case MEn, creation and anihilation operators from the two fields mixing, and massless spectator. Here |delta|^2 = -1+|alpha|^2

#def P(k) :
 #   return A * (np.sqrt(1. + delta**2) *  (k/k_0)**(n_s-1.) + (delta**2) *  (k/k_0)**(3.- 2.* mu) - 2.0* delta * np.sqrt(delta**2 + 1.) * np.cos(theta)* (k/k_0)**(0.5 * n_s +1. - mu ))


# 3. Limits for k and precision:
#    Check that the boundaries are correct for your case.
#    It is safer to set k_per_decade primordial slightly bigger than that of Class.

k_min = 1.e-6
k_max  = 10.
k_per_decade_primordial = 200.

#
# And nothing should need to be edited from here on.
#

# Filling the array of k's
ks = [float(k_min)]
while ks[-1] <= float(k_max) :
    ks.append(ks[-1]*10.**(1./float(k_per_decade_primordial)))

# Filling the array of Pk's
for k in ks :
    P_k = P(k)
    print("%.18g %.18g" % (k, P_k))

