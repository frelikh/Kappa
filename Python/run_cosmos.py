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

""" Read in the lens root names  """
indir = '/mnt/data1/renata/ACS/'
root1,root2 = n.loadtxt(indir+'COSMOS_all.list',dtype=int,unpack=True,usecols=(0,1))
nlens = root1.size

""" 
Set up containers to hold the total and distance-weighted numbers of galaxies
"""
ngal_tot  = n.zeros(nlens)
ngal_wt_r = n.zeros(nlens) 

#Since each of the 19 lenses will have its own x and y-coordinate, I have
#to set up lists with x and y values

#loop over the files containing the coordinates of the lenses

x_yan = [1545,1961,3649,4025]
y_yan = [3728,1824,3880,2000]

#prompt for the maximum magnitude

maximum_mag = input("What is the maximum magnitude?")

""" Loop over the files in the input list """
for j in range(4):
   f = open(indir+'Cosmos_counts/cosmos%d.txt' % j,'w')

   for i in range(nlens):
      catname = indir+'Cat_cosmos/%s'%str(root1[i]).zfill(6)+'+'+'%s'%str(root2[i]).zfill(4)+'_I.cat'
      x,y,dist,mag,x1,y1 = num.choose_radius(catname,x_obj=x_yan[j],y_obj=y_yan[j],rad_max=45,rad_min=10,magnitude=maximum_mag)

# catname corresponds to: one of the lenses
# choose_radius selects all the galaxies close to the specific lens -> array of
# a bunch of things: x,y coordinates of the galaxies
# inside the 2 circlular regions around the lens, dist from lens, and
# x1,y1 coordinates of the galaxies inside the inner circle of the lens
# then, the number of galaxies in the donut is computes, as well
# as the weighted sum by distance (for the galaxies in the donuts)...

# 1/10 for each in inner circle
      ngal_tot[i] = x.size + x1.size
      ngal_wt_r[i] = n.sum(1./dist) + 0.1*x1.size

   f.write('#Lens        N_total  N_wt_r\n')
   f.write('#----------- -------  ------\n')
   for i in range(nlens):
      f.write( '%-11s    %3d      %.3f\n' % (str(root1[i]).zfill(6),ngal_tot[i],ngal_wt_r[i]))
   f.write('\n')
   f.close()
   
""" Here calculate the weighted number of galaxies, too """


""" 
Print out the output 

This might also be a good place to save the output and make a regions file
"""
"""
print ''
print 'Lens        N_total  N_wt_r'
print '----------- -------  ------'
for i in range(nlens):
   print '%-11s    %3d' % (lensroot[i],ngal_tot[i])
print ''
"""
