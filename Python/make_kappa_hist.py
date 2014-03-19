import numpy as n
from matplotlib import pyplot as plt

lower_bound_u = 1.198
upper_bound_u = 1.324

lower_bound_w = 2.25
upper_bound_w = 2.35

u_kappa = []
w_kappa = []

for i in range(4):
    for j in range(8):
        for k in range(4):
            for l in range(4):
		print i,j,k,l
                infile = n.loadtxt('/mnt/data2/renata/Simulations/Tables/table%d%d_%d%d.txt' %(i,j,k,l))
                kappa_dir = '/mnt/data2/renata/Simulations/Kappa_maps/Plane28/KappasByCenter/'
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


