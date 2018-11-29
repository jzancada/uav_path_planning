# uav
Ts = 0.2

class uav_class:
    # define class
    def __init__(self):
        self.x = 0
        self.x_dot = 0

    def next(self, u, Ts):
        self.x = self.x + self.x_dot*Ts
        self.x_dot = self.x_dot + u*Ts; 

    def control_x(self, x_req, Ts):
        u = 0.0
        e_x = self.x - x_req
        # e_x[0] = x[0] - x_req
        # e_x[1] = x[1] - x_req =
        #        = x[0] + x_dot[0]*Ts - x_req
        # e_x[2] = x[1] + x_dot[1]*Ts - x_req
        #        = x[0] + x_dot[0]*Ts +(x_dot[0]*Ts+u[0])*Ts - x_req
        # e_x[2] = 0
        u = x_req - self.x - self.x_dot*Ts
        u = u/Ts
        u = u - self.x_dot*Ts
        return u

    def disp(self):
        print 'x=%.02f' % self.x, ', x_dot=%.02f' % self.x_dot


import matplotlib.pyplot as plt

uav = uav_class()
list_x=[]
list_u=[]
for k in range(20):
    list_x.append(1)
    uav.disp()
    u = uav.control_x(1, Ts)
    list_u.append(u)
    uav.next(u, Ts)
plt.plot([1,2,3,4])
plt.ylabel('some numbers')
plt.grid()
plt.xlim([0, 1])
plt.show()

print list_u