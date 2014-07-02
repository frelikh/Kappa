import pangloss as pg
import sys
import numpy as n
import numbercts as num

""" Get inputs """
if len(sys.argv)>1:
   listfile = sys.argv[1]
   print ""
   print "Reading binary kappa list from %s" % listfile
   print ""
   print sys.argv
   print ""
else:
   print ""
   print "ERROR: Expected an input filename but there was none."
   print ""
   sys.exit(1)

""" Read in the binary kappa names (which are strings of maximum length 11) """

indir = '/mnt/data2/renata/Simulations/Kappa_maps/Plane37/'
lensroot = n.loadtxt(indir+'list_of_maps.txt',dtype='S60')
nlens = lensroot.size

for z in range(nlens):
   infile = indir+'%s' % lensroot[z]
   test = pg.Kappamap(infile,False)
