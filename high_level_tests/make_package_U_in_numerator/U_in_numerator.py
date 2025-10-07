#!/usr/bin/env python3
from pySecDec.loop_integral import loop_package
import pySecDec as psd

# Bug reported by Chia-Wei in Aug. 2025, fixed Oct. 2025.
# The integral contains U in the numerator, which was identified as a constant in make_package. Contour deformation was then not applied to this factor.

if __name__ == "__main__":
    
    li = psd.LoopIntegralFromPropagators(
    loop_momenta = ['q'],
    external_momenta = ['p1','p2'],
    Lorentz_indices = ['mu' ], #,'nu'],
    propagators = [
        '(q+p1+p2)**2-mc**2',
        '(q)**2-mpi**2',
        'q**2-mpole**2'],
    powerlist = [1, 1, 1],
    regulators=["eps"],
    numerator = 'mb * mb + q(mu)*p1(mu)',
    replacement_rules = [
                            ('p1*p1', 'mD**2'),
                            ('p2*p2', 'mcc**2'),
                            ('p1*p2', 'mb**2/2-mcc**2/2 - mD**2/2')
                        ]
    )

    psd.loop_package(
    name = 'U_in_numerator',
    loop_integral = li,
    real_parameters = ['mcc','mD','mb','mc','mpi','mpole'],
    requested_orders = [0],
    form_optimization_level = 3,
    decomposition_method = 'geometric',
    contour_deformation = True,
    )
