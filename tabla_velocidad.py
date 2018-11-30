#%%
import numpy as np

# Tabla de velocidades en funcion de la distancia
# conocida la aceleracion maxima 
u_max = 0.4 # [m/s/s]
list_x = [ 1,  2, 5, 10, 20]
# numero elementos en la lista
N = len(list_x)
#inicializa la lista x_dot
list_x_dot = []

#calculo de x_dot en funcion de la distancia
for k in range(N):
    x = list_x[k]
    v_lim = np.sqrt(2*u_max*x)
    list_x_dot.append(v_lim)

# print resultados
print '-------- --------'
print '- x ---- - x_dot-'
print '-------- --------'
for k in range(N):
    print '%8.2f' % list_x[k],'%8.2f' % list_x_dot[k]
print '-------- --------'
