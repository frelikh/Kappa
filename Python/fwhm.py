import numpy as n
from matplotlib import pyplot as plt

roots = n.loadtxt('/mnt/data1/renata/ACS/yan_good_nonhaggles.list',dtype='S17')

#x_yan = [1694,1774,3164,3243]
#y_yan = [1542,3075,1627,3160]


printthis = []

for i in range(n.size(roots)):
    infile = '%s_f814w.cat' %roots[i]
    x,y,sgc,fwhm,mag,a,b = n.loadtxt(infile,unpack=True,usecols=(1,2,4,21,9,18,19))

    mask_mag = (mag < 24.5) & (mag > 18.5)
    mask_e = (b/a) > 0.12
    mask_fwhm = (fwhm > 2.6) & (fwhm < 3.5)
#    mask_sgc = sgc < 0.8

    mask = mask_e &  mask_mag & mask_fwhm

    new = sgc[mask]
    printthis = n.append(printthis,new)

print printthis
