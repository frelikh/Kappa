import numpy as n
from matplotlib import pyplot as plt

"""
1. Reads in a list of names of the Yan fields
2. Outputs a file with the number counts for each of the 4
   circles on each of the Yan fields - there will be
   4*n.size(roots) number counts
3. After running this, we can take the mean of the number
   counts to get N_pp
"""
roots = n.loadtxt('/mnt/data1/renata/ACS/yan_good_nonhaggles.list',dtype='S17')

x_yan = [1694,1774,3164,3243]
y_yan = [1542,3075,1627,3160]


printthis = []

for i in range(n.size(roots)):
    infile = '%s_f814w.cat' %roots[i]
    x,y,sgc,fwhm,mag,a,b = n.loadtxt(infile,unpack=True,usecols=(1,2,4,21,9,18,19))
  
    for j in range(4):

        radius = n.sqrt(n.power((x_yan[j]-x),2)+n.power((y_yan[j]-y),2))
        mask_radius = (radius < 900) & (radius > 50)
        mask_mag = (mag < 24.5) & (mag > 18.5)
        mask_e = (b/a) > 0.12
        mask_fwhm = (fwhm > 2.5)
        mask_sgc = sgc < 1.1

        mask = mask_radius & mask_e &  mask_mag & mask_fwhm & mask_sgc
        distance = radius[mask]
        
        ngal_tot = distance.size
        
        printthis = n.append(printthis,ngal_tot)

f = open('dist.txt','w')
for s in range(n.size(printthis)):
    f.write('%f\n' %printthis[s])
f.close()

m = n.mean(printthis)
print m
