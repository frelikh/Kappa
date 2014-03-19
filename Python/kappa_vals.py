import pangloss as pg
import sys
import numpy as n
import numbercts as num

degree = (n.pi / 180.0)
L_field = 4.0 * degree
N_pix_per_dim = 4096
L_pix         = L_field / N_pix_per_dim

""" Get inputs """
if len(sys.argv)>1:
   listfile = sys.argv[1]
   print ""
   print "Reading fits kappa list from %s" % listfile
   print ""
   print sys.argv
   print ""
else:
   print ""
   print "ERROR: Expected an input filename but there was none."
   print ""
   sys.exit(1)

""" Read in the binary kappa names (which are strings of maximum length 11) """

indir = '/nfs/virgo-home/renata/gallifrey_2/Simulations/Kappa_maps/Plane25'

lensroot = n.loadtxt(indir+'/list_of_fits.txt',dtype='S65')
nlens = lensroot.size

for z in range(nlens):
   print z

   infile = indir+'/%s' % lensroot[z]
   test = pg.Kappamap(infile)
   test.read_in_fits_data()
   
   first = lensroot[z][10]
   second = lensroot[z][12]
   
   #print first
   #print second

   n1 = int(float(first))
   n2 = int(float(second))

   for j in range(4):
      for i in range(4):
         centers = '/nfs/virgo-home/renata/Kappa_fits/Centers/center_px_vals%d%d.txt' %(i,j)
         a,b,c,d = n.loadtxt(centers,unpack=True,usecols=(0,1,2,3),skiprows=2,dtype=float)
         
         kappas = open(indir+'/KappasByCenter/kappas%d%d_%d%d.txt' %(i,j,n1,n2),'w')
         kappas.write('#xvalue      yvalue     x-pixel    y-pixel    kappa\n')
         kappas.write('#--------------------------------------------------\n')

         for q in range(1600):
            xvalue = a[q]
            yvalue = b[q]
            ix = c[q]
            iy = d[q]

            kappa_val = test.at(xvalue,yvalue)
            kappas.write('%8.8f %8.8f %8.2f %8.2f %8.4f \n' % (xvalue, yvalue, ix, iy, kappa_val))

         kappas.close()
