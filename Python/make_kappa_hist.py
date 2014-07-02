import numpy as n
from matplotlib import pyplot as plt

un_c = 0.867
lower_bound_u = un_c*0.98
upper_bound_u = un_c*1.02

w_c = 0.985
upper_bound_w = w_c*1.02
lower_bound_w = w_c*0.98

u_kappa = []
w_kappa = []

total = []

for i in range(4):
    for j in range(8):
        for k in range(4):
            for l in range(4):
		#print i,j,k,l
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
                
                print '%d %d' %(chosen_kappa_u.size, len(u_kappa))

mean_u = n.mean(u_kappa)
mean_w = n.mean(w_kappa)
mean_total = n.mean(total)


plt.figure(1)
plt.subplot(3,1,1)

n1,bins1,patches1 = plt.hist(u_kappa,50,histtype='step',color='b',range=[-0.2,0.3])
#n1,bins1,patches1 = plt.hist(u_kappa,50,histtype='step',color='b',normed=1,range=[-0.2,0.3])
print n1
plt.xlabel('Kappa')
plt.ylabel('Probability')
plt.axvline(x=mean_u,color='b')
plt.title('Unweighted Number Counts')

sigma = u_kappa.std()
textstr = '$\mu=%.4f$\n$\sigma=%.4f$'%(mean_u, sigma)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords
plt.text(0.20, 15, textstr, fontsize=14,
        verticalalignment='top', bbox=props)


plt.subplot(3,1,2)
n2,bins2,patches2 = plt.hist(w_kappa,50,histtype='step',color='g',normed=1,range=[-0.2,0.3])

plt.xlabel('Kappa')
plt.ylabel('Probability')
plt.axvline(x=mean_w,color='g')
plt.title('Weighted Number Counts')
sigma = w_kappa.std()
textstr = '$\mu=%.4f$\n$\sigma=%.4f$'%(mean_w, sigma)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords
plt.text(0.2, 15, textstr, fontsize=14,
        verticalalignment='top', bbox=props)


plt.subplot(3,1,3)
n3,bins3,patches3 = plt.hist(total,50,histtype='step',color='r',normed=1,range=[-0.2,0.3])
plt.xlabel('Kappa')
plt.ylabel('Probability')
plt.axvline(x=mean_total,color='r')
plt.title('Total Kappa Distribution for Random Lines of Sight')

sigma = total.std()
textstr = '$\mu=%.4f$\n$\sigma=%.4f$'%(mean_total, sigma)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords
plt.text(0.2, 15, textstr, fontsize=14,
        verticalalignment='top', bbox=props)

plt.show()
