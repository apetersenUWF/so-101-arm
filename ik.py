import sympy as sp
import numpy as np
sp.init_printing(use_unicode=True)
o1, o2, o3, o4, o5 = sp.symbols('o1, o2, o3, o4, o5')
# dh = sp.Matrix([[o1 + sp.pi/2, 0.0542, 0.0304, sp.rad(-90)], 
#                 [o2, 0, 0.028, 0],
#                 [o3, 0, 0.1349, 0],
#                 [o4 + sp.pi/2, 0, 0, sp.rad(90)],
#                 [o5, 0.1592, -0.0197, 0]])
dh = sp.Matrix([[o1, 0.0542, 0.0304, sp.rad(-90)], 
                [o2, 0, 0.028, 0],
                [o3, 0, 0.1349, 0],
                [o4, 0, 0, sp.rad(-90)],
                [o5, 0.1592, 0, 0]])
base_to_joint1 = sp.Matrix([[1, 0, 0, 0.0388],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0.0624],
                            [0, 0, 0, 1]])
def fk(dh, base_to_joint1):
    rows, cols = sp.shape(dh)
    transforms = []
    for i in range(rows):
        row = dh.row(i)
        theta = row[0]
        d = row[1]
        a = row[2]
        alpha = row[3]
        h = sp.zeros(4, 4)
        h[0, 0] = sp.cos(theta)
        h[0, 1] = sp.sin(theta) * sp.cos(alpha) * -1
        h[0, 2] = sp.sin(theta) * sp.sin(alpha)
        h[0, 3] = a * sp.cos(theta)
        h[1, 0] = sp.sin(theta)
        h[1, 1] = sp.cos(theta) * sp.cos(alpha)
        h[1, 2] = sp.cos(theta) * sp.sin(alpha) * -1
        h[1, 3] = a * sp.sin(theta)
        h[2, 1] = sp.sin(alpha)
        h[2, 2] = sp.cos(alpha)
        h[2, 3] = d
        h[3, 3] = 1
        transforms.append(h)
    h_0_to_n = base_to_joint1
    for i in range(len(transforms)):
        h_0_to_n = h_0_to_n * transforms[i]
    return h_0_to_n
transform = sp.trigsimp(fk(dh, base_to_joint1))
calc_fk = sp.lambdify((o1, o2, o3, o4, o5), transform, "numpy")
theta1, theta2, theta3, theta4, theta5 = 0, 0, 0, 0, 0
result_matrix = calc_fk(theta1, theta2, theta3, theta4, theta5)
print("***FK Result***")
print(np.round(result_matrix, 4))
sp.pprint(transform)
