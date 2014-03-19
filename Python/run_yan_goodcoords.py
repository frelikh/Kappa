import numpy as n
import numbercts as num

#this is the directory with the Yan files
indir = '/mnt/data1/renata/ACS/Cat_yan/'

#read in the file with the yan catalog names                                                                                                               
yanroots = n.loadtxt(indir+'Yan_fits/Yan_circles/yan_numbering.txt',dtype = 'S33')

#number of yan fields
nlens = yanroots.size

count_tot = 0

g = open(indir+'Yan_fits/Yan_counts/yancount_all.txt','w')
g.write('#Circle Index  N_total      N_wt_r\n')
g.write('#---------------------------------\n')

for i in range(nlens):
    coordfile = indir+'Yan_fits/Yan_circles/reg%d.txt' %i

    data = n.loadtxt(coordfile,dtype='S33')

    f = open(indir+'Yan_fits/Yan_counts/yancount%d.txt' %i,'w')
    f.write('#Circle Index  N_total      N_wt_r\n')
    f.write('#---------------------------------\n')

    #this is the number of circles (usually either 3 or 4)
    ncircles = data.size

    #empty arrays for weighted and unweighted galaxy number counts                                                                                             #each row in an array corresponds to a 45 arcsecond radius circle                                                                                   
    #on a given yan field

    ngal_tot = n.zeros(ncircles)
    ngal_wt_r = n.zeros(ncircles)

    count = 0
    #loop over the 3 or 4 circles on the Yan field to get the number counts for each circle
    for item in data:
        
        #these are the coordinates for the centers
        x_center = float(item[7:15])
        y_center = float(item[17:25])

        catname = indir+'%s' %yanroots[i]
        
        #runs choose_radius on the Yan field for a given circle
        x,y,dist,mag,x1,y1 = num.choose_radius(catname,x_obj=x_center,y_obj=y_center,rad_max=45,rad_min=10,magnitude=24.5)

        
        ngal_tot[count] = x.size + x1.size
        ngal_wt_r[count] = n.sum(1./dist) + 0.1*x1.size

        f.write('%8d %12.3f %12.3f\n' %(count, ngal_tot[count], ngal_wt_r[count]))
        g.write('%8d %12.3f %12.3f\n' %(count_tot, ngal_tot[count], ngal_wt_r[count]))
        #increments the loop counter
        count = count + 1
        count_tot = count_tot + 1
    f.close()
g.close()
