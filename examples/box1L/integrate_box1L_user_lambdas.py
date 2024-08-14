#!/usr/bin/env python3
from pySecDec.integral_interface import DistevalLibrary
import json

# load the library
name = 'box1L'
box1L = DistevalLibrary(f'{name}/disteval/{name}.json', verbose=True)

#Print the names of each kernel (sectors at each expansion order)
with open(f'{name}/disteval/{name}_integral.json') as f:
    integral_information = json.load(f)
kernels = integral_information['kernels']
print(f'Order of the {len(kernels)} kernels are')
for i, k in enumerate(kernels):
    print(f'k{i}: {k}')

integral_name = 'box1L_integral'

#Set the starting values for the deformation parameters in each kernel to be [0.1,0.2,0.3] (lambda1, lambda2, lambda3)
initial_deformation_parameters = {(integral_name,k) : [0.1, 0.2, 0.3] for k in kernels}

#integrate  
result = box1L(parameters={"s": 4.0, "t": -0.75, "s1": 1.25, "msq": 1.0},
               epsrel=1e-3, epsabs=1e-10, format="json", initial_deformation_parameters=initial_deformation_parameters)
values = result["sums"]["box1L"]

# examples how to access individual orders
print('Numerical Result')
print('eps^-2:', values[(-2,)][0], '+/- (', values[(-2,)][1], ')')
print('eps^-1:', values[(-1,)][0], '+/- (', values[(-1,)][1], ')')
print('eps^0 :', values[( 0,)][0], '+/- (', values[( 0,)][1], ')')

print('Analytic Result')
print('eps^-2: -0.1428571429')
print('eps^-1: 0.6384337090')
print('eps^0 : -0.426354612+I*1.866502363')

input('Continue.. (press Enter)')

#### We can choose to specify deformation parameters for only some of the sectors.. (remove some at random)
initial_deformation_parameters.pop((integral_name,kernels[0]))
initial_deformation_parameters.pop((integral_name,kernels[5]))
initial_deformation_parameters.pop((integral_name,kernels[6]))
initial_deformation_parameters.pop((integral_name,kernels[7]))
initial_deformation_parameters.pop((integral_name,kernels[-1]))

#integrate  
result = box1L(parameters={"s": 4.0, "t": -0.75, "s1": 1.25, "msq": 1.0},
               epsrel=1e-3, epsabs=1e-10, format="json", initial_deformation_parameters=initial_deformation_parameters)
values = result["sums"]["box1L"]

print('Numerical Result')
print('eps^-2:', values[(-2,)][0], '+/- (', values[(-2,)][1], ')')
print('eps^-1:', values[(-1,)][0], '+/- (', values[(-1,)][1], ')')
print('eps^0 :', values[( 0,)][0], '+/- (', values[( 0,)][1], ')')

print('Analytic Result')
print('eps^-2: -0.1428571429')
print('eps^-1: 0.6384337090')
print('eps^0 : -0.426354612+I*1.866502363')

input('Continue.. (press any key)')

#### In a Euclidean region we do not need any deformation to get correct results.
initial_deformation_parameters = {(integral_name,k) : [0, 0, 0] for k in kernels} #set all parameters to 0
result = box1L(parameters={"s": -4.0, "t": -0.75, "s1": -1.25, "msq": 1.0}, 
               epsrel=1e-3, epsabs=1e-10, format="json", initial_deformation_parameters=initial_deformation_parameters) # (notice the phase-space point is different to above)
values = result["sums"]["box1L"]

print('eps^-2:', values[(-2,)][0], '+/- (', values[(-2,)][1], ')')
print('eps^-1:', values[(-1,)][0], '+/- (', values[(-1,)][1], ')')
print('eps^0 :', values[( 0,)][0], '+/- (', values[( 0,)][1], ')')