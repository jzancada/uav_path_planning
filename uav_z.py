# uav
import numpy as np
import matplotlib.pyplot as plt

Ts = 0.2

class uav_class:
    # define class
    def __init__(self, x0 = 0, x0_dot = 0):
        self.x = x0
        self.x_dot = x0_dot
        self.u_lim = 1

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
        return u

    def disp(self):
        print 'x=%.02f' % self.x, ', x_dot=%.02f' % self.x_dot



uav = uav_class(1.0, 0)

list_x=[]
list_x_dot=[]
list_u=[]
# Cte de control
K = 4
# posicion requerida
x_req = 0 
for k in range(40):
    uav.disp()
    u = uav.control_x(x_req, K, Ts)
    uav.next(u, Ts)
    list_x.append(uav.x)
    list_x_dot.append(uav.x_dot)
    list_u.append(u)

print list_u

# posicion    
plt.figure()
plt.plot(list_x)
plt.xlabel('sample')
plt.ylabel('x [m]')
plt.grid()
# plt.xlim([0, 1])
plt.draw()
plt.savefig('test_1.png')


# velocidad    
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

plt.show()


print list_u