#%%
# uav
import numpy as np
import matplotlib.pyplot as plt

# tiempo de muestreo [segundos]
Ts = 0.2

class uav_class:
    # define class
    def __init__(self, x_ini = 0, x_dot_ini = 0):
        self.x = x_ini
        self.x_dot = x_dot_ini
        self.u_lim = .4
        self.v_lim = 2.
        self.x0 = 1.
        self.N = 2 # divide u (retrasa control aceleracion)
        self.K = np.sqrt(self.u_lim / (2.0*self.x0))
        self.x0_dot_lim = np.sqrt(2.0*self.x0*self.u_lim)

    # siguiente muestra
    def next(self, u, Ts):
        self.x = self.x + self.x_dot*Ts
        self.x_dot = self.x_dot + u*Ts; 

    # limita la aceleracion (entada)
    def limita_u(self, u):
        uOut = u
        if abs(uOut)>self.u_lim:
            uOut = np.sign(uOut)*self.u_lim            
        return uOut

    # limita la velocidad 
    def limita_v(self, v):
        vOut = v
        if abs(vOut)>self.v_lim:
            vOut = np.sign(vOut)*self.v_lim            
        return vOut

    # control de posicion
    def control_x_0(self, x_req, K, Ts):
        u = 0.0
        e_x = self.x - x_req
        uTs = -self.x_dot -K*(e_x + self.x_dot*Ts) 
        u = uTs/Ts
        u = self.limita_u(u)
        return u

    def control_x_1(self, x_req, Ts):
        e_x = self.x - x_req

        if self.x > 2*self.x0:
            v_next = -np.sqrt( (self.x - self.x0)*2*self.u_lim)
        elif self.x < -2*self.x0:
            v_next =  np.sqrt(-(self.x + self.x0)*2*self.u_lim)
        else:
            v_next = -self.K*e_x

        v_next = self.limita_v(v_next)
        # v_next = v + u*Ts

        u = (v_next - self.x_dot)/Ts
        ## retrasa u
        u = u / self.N
        u = self.limita_u(u)
        return u

    def disp(self):
        print 'x=%.02f' % self.x, ', x_dot=%.02f' % self.x_dot


# se crea uav (de)
# posicion inicial
x_ini = 20
# posicion inicial
x_dot_ini = 0
uav = uav_class(x_ini, x_dot_ini)

list_x=[]
list_x_dot=[]
list_u=[]
# Cte de control
print ("==================")
print ("K          = %.3f" % uav.K)
print ("x0_dot_lim = %.3f" % uav.x0_dot_lim)
print ("==================")

# posicion requerida
x_req = 0 
for k in range(100):
#    uav.disp()
    u = uav.control_x_1(x_req, Ts)
    uav.next(u, Ts)
    list_x.append(uav.x)
    list_x_dot.append(uav.x_dot)
    list_u.append(u)


# posicion    
plt.plot(list_x)
plt.xlabel('sample')
plt.ylabel('x [m]')
plt.grid()
# plt.xlim([0, 1])
plt.draw()
plt.savefig('test_1.png')


# posicion    
plt.figure()
plt.plot(list_x_dot)
plt.xlabel('sample')
plt.ylabel('x_dot [m/s]')
plt.grid()
# plt.xlim([0, 1])
plt.draw()
plt.savefig('test_2.png')


# control    
plt.figure()
plt.plot(list_u)
plt.xlabel('sample')
plt.ylabel('u [m/s/s]')
plt.grid()
# plt.xlim([0, 1])
plt.draw()
plt.savefig('test_3.png')

# plano x -x_dot
plt.figure()
plt.plot(list_x, list_x_dot)
plt.draw()
plt.xlabel('x')
plt.ylabel('x_dot')
plt.savefig('test_4.png')

plt.show()


print "%.1f" % list_u