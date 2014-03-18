""" 
This code is just an example of how to read in columns from a textfile.
 This can be useful in reading in a SExtractor catalog.  It also involves
 selecting a subset of the rows that satisfy some condition(s).

To execute this program, just type "python example_renata.py [filename]"
where [filename] is the file that you want to read in.

Note that triple quotes denote a comment block.
You can also comment out a line by starting it with the hash sign (#).

Python is a bit odd in that if-then statements, etc., don't have "endif"
 statements or don't define the executable block with {}.  Instead,
 python defines these blocks by the indentation.  

Version history:
 2013_11_18: CDF, Initial version
 2013_11_27: added b/a selection to mask function, changed fwhm selection from pixels to
             arcseconds, and from 2.5 pixels to 0.13 arcseconds(as described in paper...it shouldn't
             make too much difference which one to use but the paper one gives 2.6 pixels)
 2013_11_28: added selection by radius
 2014_01_20: changed the input of the choose_radius function to include a maximum magnitude, with a default of 24.5
"""

# At the beginning load the python libraries that you are going to use.
# This program may not use the math library, but it is included to give
#  an example of the "from [library] import [function(s)]" syntax.
# If you don't use a line like this, then you would have to call, for example,
#  sqrt as math.sqrt

import math
from math import fabs,sqrt
import numpy as n  # Use this syntax to create a short-cut name to a library
import sys,os

"""
Here we can define functions.
"""

def read_catalog(infile,verbose=True):
   """
   This function reads in the columns that are needed from one of the
   catalog files.  For now, these columns are:
    x, y, sgclass, fwhm, mag, a_image, b_image
   Therefore, this function should be called in the following way:

     x,y,sgclass,fwhm,mag,a_image,b_image = read_catalog(infile)

   Inputs:
    Required:
     infile  - input file name
    Optional
     verbose - set this variable to True if you want to print out
               diagnostic information.  Default = True

   """
   if verbose:
      print ""
      print "Reading in %s" % infile
   """ 
   You could just read in the full catalog and then define each variable
   as a column in the file (see the next few lines, which are commented
   out because there is a shorter way to do this)
   """
   #data = n.loadtxt(infile)
   #x = data[:,1]
   #y = data[:,2]
   """ ... or, you could do things this way """
   x,y,sgclass,fwhm,mag,a_image,b_image = n.loadtxt(infile,unpack=True,usecols=(1,2,4,21,9,18,19))
   
   if verbose:
      print "Read in %d objects from %s." % (x.size,infile)

   return x,y,sgclass,fwhm,mag,a_image,b_image

def write_regfile(x,y,outfile,radius=25,color='red',shape='circle'):
   """
   This function will create a ds9 region file given the input x and y
   coordinates.

   Inputs:
    Required:
     x       - array containing the x coordinates
     y       - array containing the y coordinates
     outfile - file name for output region file
    Optional:
     radius  - radius of circles in region file, default=10
     color   - color of regions, default='green'
     shape   - shapes of regions, default='circle'

   """

   """ Open the output file for writing """
   f = open(outfile,'w')

   """ Print header information """
   f.write('global color=%s\n' % color)
   """ Loop over the coordinates """
   for i in range(x.size):
      f.write('image;%s(%d,%d,%d)\n' % (shape,x[i],y[i],radius))

   """ Close the output file """
   f.close()
   print ''
   print 'Wrote coordinate to regions file: %s' % outfile
   print ''

def choose_gals(infile,sgclass_max=1.1,fwhm_min=0.13,mag_min=19,ellip_min=0.12,arcsec_per_px=0.05,mag_max=24.5):

   """
   This function calls the read_catalog function, chooses the galaxies
   using the mask, and returns the x,y coordinates and the magnitudes
   of the galaxies.

   Can return either xgal,ygal,mgal or the mask itself...which one should I use?
   """

   x,y,sgclass,fwhm,mag,a_image,b_image = read_catalog(infile)
   
   #the next line converts pixels to arcseconds

   fwhm_arcsec=fwhm*arcsec_per_px
   ellip = b_image/a_image

   mask = (sgclass<sgclass_max) & (fwhm_arcsec>fwhm_min) & (mag>=mag_min) & (ellip>ellip_min) & (mag <= mag_max)

   xgal = x[mask]
   ygal = y[mask]
   mgal = mag[mask]

   return xgal,ygal,mgal

def choose_radius(infile,x_obj=2900,y_obj=2400,rad_max=45, rad_min=10,arcsec_per_px=0.05,magnitude=24.5):

   """
   This function chooses the galaxies that are within a specified radius
   of an object with coordinates (x_obj,y_obj).

   Are we working in arcseconds or pixels? It's probably better to use arcseconds
   because pixels aren't always the same and everything is in
   arcseconds in the paper. So rad_max is in arcseconds.
   """

   #first, choose which ones are galaxies
   xgal,ygal,mgal = choose_gals(infile,mag_max=magnitude)

   #choose the ones within a certain radius
   a = (n.square(xgal-x_obj)+n.square(ygal-y_obj))
   b = n.sqrt(a)*arcsec_per_px

   # Make masks
   #
   # *** Add magnitude limits to mask ***
   #
   mask = (b<rad_max) & (b>rad_min)
   mask2 = (b<rad_min)

   x1 = xgal[mask]
   y1 = ygal[mask]
   mgal1 = mgal[mask]
   dist = b[mask]

   x2 = xgal[mask2]
   y2 = ygal[mask2]

   return x1,y1,dist,mgal1,x2,y2
