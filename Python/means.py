import numpy as n

indir = '/nfs/virgo-home/renata/Data1/ACS/'
yan_file = indir+'Cat_yan/Yan_fits/Yan_counts/yancount_all.txt'
lens_file = indir+'Lens Counts/lens.txt'
lensroots = indir+'lenses_root.list'

yan_unw,yan_w = n.loadtxt(yan_file,unpack=True,usecols=(1,2))
lens_unw,lens_w = n.loadtxt(lens_file,unpack=True,usecols=(1,2))
lens_roots = n.loadtxt(lensroots,dtype='S22')

yan_mean_unw = n.mean(yan_unw)
yan_mean_w = n.mean(yan_w)

f = open('finalcounts.txt','w')
f.write('#Lens       Unweighted Count  Weighted Count\n')
f.write('#-------------------------------------------\n')

nlens = lens_roots.size

for i in range(nlens):
    f.write('%12s %15.3f %15.3f\n' %(lens_roots[i],(lens_unw[i]/yan_mean_unw),(lens_w[i]/yan_mean_w)))

f.close()
