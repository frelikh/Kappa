import numpy as n
from matplotlib import pyplot as plt

lower_bound_u = 0.99793
upper_bound_u = 1.01808

upper_bound_w = 1.2674
lower_bound_w = 1.1467

u_kappa = []
w_kappa = []

total = []

for i in range(4):
    for j in range(8):
        for k in range(4):
            for l in range(4):
		print i,j,k,l
                infile = n.loadtxt('/mnt/data2/renata/Simulations/Tables/table%d%d_%d%d.txt' %(i,j,k,l))
                kappa_dir = '/mnt/data2/renata/Simulations/Kappa_maps/Plane35/KappasByCenter/'
                kappa_infile = kappa_dir+'kappas%d%d_%d%d.txt' %(k,l,i,j)

                n_u = infile[:,3]
                n_w = infile[:,4]

                mask_u = (n_u < upper_bound_u) & (n_u > lower_bound_u)
                mask_w = (n_w < upper_bound_w) & (n_w > lower_bound_w)

		data1 = n.loadtxt(kappa_infile)
		kappa = data1[:,4]
		chosen_kappa_u = kappa[mask_u]
                chosen_kappa_w = kappa[mask_w]

		u_kappa = n.append(u_kappa,chosen_kappa_u)
                w_kappa = n.append(w_kappa,chosen_kappa_w)
                total = n.append(total,kappa)

