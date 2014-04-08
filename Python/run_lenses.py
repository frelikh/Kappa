"""
For now this program just runs choose_radius for each one of the lenses
"""

import sys
import numpy as n
import numbercts as num

""" Get inputs """
if len(sys.argv)>1:
   listfile = sys.argv[1]
   print ""
   print "Reading lens list from %s" % listfile
   print ""
   print sys.argv
   print ""
else:
   print ""
   print "ERROR: Expected an input filename but there was none."
   print ""
   sys.exit(1)

""" Read in the lens root names (which are strings of maximum length 11) """
indir = '/nfs/virgo-home/renata/Data1/ACS/'
lensroot = n.loadtxt(indir+'lenses_root.list',dtype='S11')
nlens = lensroot.size

""" 
Set up containers to hold the total and distance-weighted numbers of galaxies
"""
ngal_tot  = n.zeros(nlens)
ngal_wt_r = n.zeros(nlens) 

maximum_mag = input('What is the maximum magnitude?')

""" Loop over the files in the input list """
for i in range(nlens):
   catname = '/nfs/virgo-home/renata/Data1/ACS/Cat_lenses/%s_F814W.cat' % lensroot[i]

   data = n.loadtxt(catname)
   dist = data[:,41]

   x,y,sgclass,fwhm,mag,a_image,b_image = n.loadtxt(catname,unpack=True,usecols=(1,2,4,21,9,18,19))
   
   fwhm_arcsec=fwhm*0.05
   ellip = b_image/a_image

   # mask = (sgclass<0.5) & (fwhm_arcsec>0.13) & (mag>19) & (ellip>0.12)

   mask1 = (dist<45) & (dist>10) & (sgclass<1.1) & (fwhm_arcsec>0.175) & (mag>=18.5) & (mag <= maximum_mag) & (ellip>0.12)
   mask2 = (dist<10) & (dist>2.5) & (sgclass<1.1) & (fwhm_arcsec>0.175) & (mag>18.5) & (mag <= maximum_mag) & (ellip>0.12)
   mask_all = (mask1) | (mask2)

   s1 = dist[mask1]
   s2 = dist[mask2]
   x45 = x[mask_all]
   y45 = y[mask_all]


   ngal_tot[i] = s1.size + s2.size
   ngal_wt_r[i] = n.sum(1./s1) + 0.1*s2.size

   """ Here calculate the weighted number of galaxies, too """
   ''' Here, make a regions file'''

   outfile = indir+'Cat_lenses/%s_F814W_gals_45.reg' % lensroot[i]
   num.write_regfile(x45,y45,outfile)
""" 
Print out the output 

This might also be a good place to save the output and make a regions file
"""
f = open(indir+'Lens Counts/lens.txt','w')
f.write('#Lens        N_total  N_wt_r\n')
f.write('#----------- -------  ------\n')
for i in range(nlens):
   f.write('%-11s    %3d    %8.3f\n' % (lensroot[i],ngal_tot[i],ngal_wt_r[i]))
f.write('\n')
f.close()
