import sys
import numpy as n
import numbercts as num

""" Read in the lens root names (which are strings of maximum length 11) """

lensroot = n.loadtxt('listofSA.txt',dtype='S72')
nlens = lensroot.size

# there's gonna be 64 * 16 nlens

for z in range(1024):

    print z

    inputfile = './Sim_data/SA_galaxies/%s' % lensroot[z]

    # first and second just specify which of the 64 fields we're looking at
    # third is the x-coordinate on the 4X4 grid
    # fourth is the y-coordinate on the 4x4 grid

    first = lensroot[z][10]
    second = lensroot[z][12]
    third = lensroot[z][14]
    fourth = lensroot[z][16]

    # need to convert all of them from string to float

    n1 = (float(first))
    n2 = (float(second))
    n3 = (float(third))
    n4 = (float(fourth))

    # reads in x,y, and magnitude of galaxies in each of the simulated fields

    x,y,mag = n.loadtxt(inputfile,unpack=True,usecols=(6,7,15),skiprows=1)

    degree = (n.pi / 180.0)
    L_field = 4.0 * degree
    N_pix_per_dim = 4096
    L_pix         = L_field / N_pix_per_dim
    step = 45.0 * 1024.0 / 3600.0
    # this converts x and y radian coordinates into pixels

    ix = (x + 0.5 * L_field) / L_pix - 0.5
    iy = (y + 0.5 * L_field) / L_pix - 0.5

    # this maps the pixels from their position on the 4096 by 4096 grid into a 1024 by 1024 grid

    new_x = ix % 1024
    new_y = iy % 1024

    center_x = n.zeros(40)
    center_y = n.zeros(40)

    arcsec_per_px = 3600.0/1024.0

    # this creates an array with x-values of centers of circles in pixels
    # on this fake 1024 by 1024 grid, 90 arcseconds apart

    for i in range(40):
        center_x[i] = (45 / arcsec_per_px) + i * (90 / arcsec_per_px)

    # same as above, but with y

    for i in range(40):
       center_y[i] = (45 / arcsec_per_px) + i * (90 / arcsec_per_px)

       count = 0

       # for each circle, choose galaxies by radius and sum
       # b is a list of distances of each galaxy, in pixels, from a given circle radius

       # I need a table with 1600 circles and their corresponding sums
       # count keeps track of the index of each circle
       # start with zero

       ngal_tot = n.zeros(1600)
       ngal_wt_r = n.zeros(1600)
       x_biggrid = n.zeros(1600)
       y_biggrid = n.zeros(1600)

    f = open('./SATables/table%d%d_%d%d.txt' %(n1,n2,n3,n4),'w')
    f.write('#Circle     x_coord  y_coord    N_total    N_wt_r\n')
    f.write('#------     -------  -------    -------    -------\n')

    for i in range(40):
       for j in range(40):
          #print '%d , %d' % (j,i)
          a = (n.square(new_x - center_x[j]) + n.square(new_y - center_y[i]))
          b = n.sqrt(a)

          mask1 = (b < (45 / arcsec_per_px)) & (b > (10 / arcsec_per_px)) & (mag < 25.3)
          mask2 = (b < (10 / arcsec_per_px)) & (b > (2.5 / arcsec_per_px)) & (mag < 25.3)

          s1 = b[mask1] * arcsec_per_px
          s2 = b[mask2] * arcsec_per_px

          ngal_tot[count] = s1.size + s2.size
          
          ngal_wt_r[count] = n.sum(1./s1) + 0.1*s2.size


          # this takes the 45 arcsecond radius (i.e. step) and increments x (or y) on the
          # big grid, starting from the leftmost bottom corner of each 1 X 1 tile

          x_biggrid[count] = step + 2 * step * j + n3 * 1024
          y_biggrid[count] = step + 2 * step * i + n4 * 1024
          
          count += 1
          # keeping track of: 
          # 1. number in list of 1600
          # 2. x and y on kappa map
          # 3. unweighted number count divided by mean
          # 4. weighted number count divided by mean

    for rat in range(1600):
       f.write('%8d %8.2f %8.2f %12.4f %12.4f\n' %(rat, x_biggrid[rat], y_biggrid[rat], (ngal_tot[rat] / n.mean(ngal_tot)), (ngal_wt_r[rat] / n.mean(ngal_wt_r))))
    f.close()
