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
        self.v_lim = 20.
        self.x0 = 1.
        self.N = 2 # divide u (retrasa control aceleracion)
        self.K = np.sqrt(self.u_lim / (2.0*self.x0))
        self.x0_dot_lim = np.sqrt(2.0*self.x0*self.u_lim)
        self.tabla_velocidad_x     = [ 1,  5, 10, 20]
        self.tabla_velocidad_x_dot = [.1, .2, .3, 4]

    # siguiente muestra
    def next(self, u, Ts):
        self.x = self.x + self.x_dot*Ts
        self.x_dot = self.x_dot + u*Ts; 

    # limita la aceleracion (entada)
    def limita_u(self, u):
        uOut = u
        factor = 1.1 # magen del 10%
        u_lim_factor = self.u_lim * factor
        if abs(uOut)>u_lim_factor:
            uOut = np.sign(uOut)*u_lim_factor       
        return uOut

    # velocidad maxima en funcion de la distancia
    def get_v_lim_table(self, x):
        N = len(self.tabla_velocidad_x)
        #inicializa al primer elemento de la tabla (el mas cercano a 0.0)
        v_max = self.tabla_velocidad_x_dot[0]
        for k in range(N):
            if x > self.tabla_velocidad_x[k]:
                # actualiza v_max
                v_max = self.tabla_velocidad_x_dot[k]
                continue
            else:
                break
        return v_max

    # limita la velocidad 
    def limita_v(self, v):
        vOut = v
        # velocidad maxima por table en funcion de la distancia
        v_lim_tabla = self.get_v_lim_table(self.x)
        # velocidad maxima por control
        v_lim = min(self.v_lim,v_lim_tabla)
        if abs(vOut)>v_lim:
            vOut = np.sign(vOut)*v_lim            
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
x_ini = 60
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
for k in range(150):
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