import numpy as n
from matplotlib import pyplot as plt


# Plug in Yan Counts here
un_c = 1.23
lower_bound_u = 0.95*un_c
upper_bound_u = 1.05*un_c

# Plug in COSMOS Counts here
w_c = 1.057
upper_bound_w = 1.02*w_c
lower_bound_w = 0.98*w_c

u_kappa = []
w_kappa = []

total = []

for i in range(4):
    for j in range(8):
        for k in range(4):
            for l in range(4):
		print i,j,k,l
                infile = n.loadtxt('/mnt/data2/renata/Simulations/Tables/table%d%d_%d%d.txt' %(i,j,k,l))
                kappa_dir = '/mnt/data2/renata/Simulations/Kappa_maps/Plane30/KappasByCenter/'
                kappa_infile = kappa_dir+'kappas%d%d_%d%d.txt' %(k,l,i,j)

                n_u = infile[:,3]
                n_w = infile[:,4]

                mask_u = (n_u < upper_bound_u) & (n_u > lower_bound_u)
                mask_w = (n_w < upper_bound_w) & (n_w > lower_bound_w)

                # again, choose the kappas with the number counts in the correct range

		data1 = n.loadtxt(kappa_infile)
		kappa = data1[:,4]
		chosen_kappa_u = kappa[mask_u]
                chosen_kappa_w = kappa[mask_w]

		u_kappa = n.append(u_kappa,chosen_kappa_u)
                w_kappa = n.append(w_kappa,chosen_kappa_w)
                total = n.append(total,kappa)

mean_u = n.mean(u_kappa)
mean_w = n.mean(w_kappa)
mean_total = n.mean(total)


plt.clf()
n1,bins1,patches1 = plt.hist(u_kappa,50,histtype='step',color='b',normed=1,range=[-0.1,0.4])
plt.xlabel('Kappa')
plt.ylabel('Count')
plt.axvline(x=mean_u,color='b')

sigma1 = u_kappa.std()
#textstr = '$\mu=%.4f$\n$\sigma=%.4f$'%(mean_u, sigma)
#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords
#plt.text(0.20, 15, textstr, fontsize=14,
#verticalalignment='top', bbox=props)


n2,bins2,patches2 = plt.hist(w_kappa,50,histtype='step',color='g',normed=1,range=[-0.1,0.4])

plt.axvline(x=mean_w,color='g')
sigma2 = w_kappa.std()
#textstr = '$\mu=%.4f$\n$\sigma=%.4f$'%(mean_w, sigma)
#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords
#plt.text(0.2, 15, textstr, fontsize=14,
#verticalalignment='top', bbox=props)


n3,bins3,patches3 = plt.hist(total,50,histtype='step',color='r',normed=1,range=[-0.1,0.4],label='Total')
plt.axvline(x=mean_total,color='r')

sigma3 = total.std()
textstr = ' Blue: $\mu_{Yan} =%.4f$\n Green: $\mu_{COSMOS} =%.4f$\n Red: $\mu_{total}=%.4f$'%(mean_u,mean_w,mean_total)
#textstr = 'Blue: $\mu=%.4f$\nRed: $\mu_{total}=%.4f$'%(mean_u,mean_total)    
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
#place a text box in upper left in axes coords
plt.text(0.2, 5, textstr, fontsize=14,
        verticalalignment='top', bbox=props)

plt.title('Kappa Distribution for SDSS1138')
plt.show()
