# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 16:13:55 2019

@author: jzancada
"""

import numpy as np
import matplotlib.pyplot as plt

#%%
# Tiempo muestreo
Ts = 0.2

#clase
class uav_class:
    # define class
    def __init__(self, x0 = 0, x0_dot = 0, u_lim = 0.2):
        self.x = x0
        self.x_dot = x0_dot
        self.u_lim = u_lim

    def next(self, u, Ts):
        self.x = self.x + self.x_dot*Ts
        self.x_dot = self.x_dot + u*Ts; 

    def limita_u(self, u):
        uOut = u
        if abs(uOut)>self.u_lim:
            uOut = np.sign(uOut)*self.u_lim
            
        return uOut

    def control_x(self, x_req, K, Ts):
        u = 0.0
        e_x = self.x - x_req
        uTs = -self.x_dot -K*(e_x + self.x_dot*Ts) 
        u = uTs/Ts
        u = self.limita_u(u)
        sigma = K*self.x + self.x_dot 
        return u, sigma

    def disp(self):
        print ('x=%.02f' % self.x, ', x_dot=%.02f' % self.x_dot)

#%% 
# crea arrays
N = 1000
x     = np.zeros((N,1),dtype=float)        
x_dot = np.zeros((N,1),dtype=float)        
u     = np.zeros((N,1),dtype=float)        
sigma = np.zeros((N,1),dtype=float)        

#limite U
U = 0.2
K = 0.316
# creo un uav
x0 = -200
uav   = uav_class(x0,0, U)
buque = uav_class(0,)

#%% simulacion
# inicializa x0, x_dot0
x    [0] = uav.x
x_dot[0] = uav.x_dot

for k in range(0,x.size-1):
    # control
    u[k], sigma[k] = uav.control_x(0,K,Ts);
    # next
    uav.next(u[k],Ts)
    # se guarada informacion
    x    [k+1] = uav.x
    x_dot[k+1] = uav.x_dot

#%% resultados
# posicion    
plt.figure()
plt.plot(x)
plt.xlabel('sample')
plt.ylabel('x [m]')
plt.grid()
# plt.xlim([0, 1])
plt.draw()
plt.savefig('test_1.png')

# velocidad    
plt.figure()
plt.plot(x_dot)
plt.xlabel('sample')
plt.ylabel('x_dot [m/s]')
plt.grid()
# plt.xlim([0, 1])
plt.draw()
plt.savefig('test_2.png')

# pos-vel    
plt.figure()
plt.plot(x,x_dot)
plt.xlabel('x ')
plt.ylabel('x_dot')
plt.grid()
# plt.xlim([0, 1])
plt.draw()
plt.savefig('test_2.png')

# sigma
plt.figure()
plt.plot(sigma)
plt.xlabel('sample')
plt.ylabel('sigma')
plt.grid()
# plt.xlim([0, 1])
plt.draw()
plt.savefig('test_2.png')


# u    
plt.figure()
plt.plot(u)
plt.xlabel('sample')
plt.ylabel('u [m/s/s]')
plt.grid()
# plt.xlim([0, 1])
plt.draw()
plt.savefig('test_2.png')


