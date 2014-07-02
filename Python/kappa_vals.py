import pangloss as pg
import sys
import numpy as n
import numbercts as num

degree = (n.pi / 180.0)
L_field = 4.0 * degree
N_pix_per_dim = 4096
L_pix         = L_field / N_pix_per_dim

indir = '/nfs/virgo-home/renata/gallifrey_2/Simulations/Kappa_maps/Plane35'


# loading list of files to be read in
lensroot = n.loadtxt(indir+'/list_of_fits.txt',dtype='S65')
nlens = lensroot.size

for z in range(nlens):
   print z

   infile = indir+'/%s' % lensroot[z]

   # creates object of class Kappamap, infile is the kappa map in FITS format
   test = pg.Kappamap(infile)
   test.read_in_fits_data()
   
   first = lensroot[z][10]
   second = lensroot[z][12]

   n1 = int(float(first))
   n2 = int(float(second))

   for j in range(4):
      for i in range(4):

		 # coordinates of the centers of the circles - 90 arcseconds apart, radius 45 arcseconds
         centers = '/nfs/virgo-home/renata/Kappa_fits/Centers/center_px_vals%d%d.txt' %(i,j)
         a,b,c,d = n.loadtxt(centers,unpack=True,usecols=(0,1,2,3),skiprows=2,dtype=float)
		 
	     # a and b are in arcseconds, c and d are in pixels         

         kappas = open(indir+'/KappasByCenter/kappas%d%d_%d%d.txt' %(i,j,n1,n2),'w')
         kappas.write('#xvalue      yvalue     x-pixel    y-pixel    kappa\n')
         kappas.write('#--------------------------------------------------\n')

		 # there's 40*40=1600 circles
         for q in range(1600):
            xvalue = a[q]
            yvalue = b[q]
            ix = c[q]
            iy = d[q]

            kappa_val = test.at(xvalue,yvalue)
            kappas.write('%8.8f %8.8f %8.2f %8.2f %8.4f \n' % (xvalue, yvalue, ix, iy, kappa_val))

         kappas.close()
