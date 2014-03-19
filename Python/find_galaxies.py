import numpy as n
import numbercts as num

'''
1. Read in the Yan catalog, with id#, x-coordinate,y-coordinate,star/galaxy,
fwhm,magnitude,a, and b-length
2. Set the coordinates for the center of the four circles on the field
3. Loop over the 4 circles, computing an unweighted number count for each:
    - choosing only the objects we want: magnitude, eccentricity, fwhm, star/galaxy
    - 18.5 < Mag < 24.5
    - (b/a) > 0.12
    - fwhm > 2.6 arcseconds
    - sgc < 0.7
4. Writes 4 reg files for ds9, corresponding to each of the circles
5. Lists all the (flagged) galaxies in yan_gal.txt
'''

infile = 'ACSJ022717-405550_f814w.cat'
idnum,x,y,sgc,fwhm,mag,a,b = n.loadtxt(infile,unpack=True,usecols=(0,1,2,4,21,9,18,19))

ids = []
x_vals = []
y_vals = []
mag_vals = []

x_yan = [1694,1774,3164,3243]
y_yan = [1542,3075,1627,3160]

for j in range(4):
    radius = n.sqrt(n.power((x_yan[j]-x),2)+n.power((y_yan[j]-y),2))
    mask_radius = (radius < 900) & (radius > 50)
    mask_mag = (mag < 24.5) & (mag > 18.5)
    mask_e = (b/a) > 0.12
    mask_fwhm = (fwhm > 2.6) & (fwhm < 3.5)
    mask_sgc = sgc < 0.8

    mask = mask_sgc & mask_radius & mask_e &  mask_mag & mask_fwhm
    
    ids1 = idnum[mask]
    x_vals1 = x[mask]
    y_vals1 = y[mask]
    mag_vals1 = mag[mask]

    ids = n.append(ids,ids1)
    x_vals = n.append(x_vals,x_vals1)
    y_vals = n.append(y_vals,y_vals1)
    mag_vals = n.append(mag_vals,mag_vals1)

    outfile = 'find_galaxies1%d.reg' %j
    num.write_regfile(x_vals1,y_vals1,outfile,radius=30,color='blue')

f = open('yan_gal.txt','w')
f.write('#Galaxy ID  X-coord   Y-coord   Magnitude\n')
f.write('#----------------------------------------\n')
for s in range(n.size(ids)):
    f.write('%8.2f %8.2f %8.2f %8.2f\n' %(ids[s],x_vals[s],y_vals[s],mag_vals[s]))
f.close()

#outfile = 'find_galaxies.reg'
#num.write_regfile(x_vals,y_vals,outfile)
