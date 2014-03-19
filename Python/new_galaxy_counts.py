import sys
import numpy as n
import numbercts as num

yans = []
yans_weighted = []

# since there are four Yan files for each of the four coordinates,
# first put all of them in one list for the sums, and one list
# for the weighted sums

for i in range(4):
    name = 'Yan Counts/yan%s.txt' % i

    # gets the data for a give yan list
    count,count_w = n.loadtxt(name,unpack=True,usecols=(1,2))


    # now, add to the list of all sums and weighted sums
    yans = n.append(yans,count)
    yans_weighted = n.append(yans_weighted,count_w)

# means and medians of the entire Yan lists

yans_median = n.median(yans)
yans_mean = n.mean(yans)

yans_weighted_median = n.median(yans_weighted)
yans_weighted_mean = n.mean(yans_weighted)

infile = 'Lens Counts/lens.txt'
data,data_w = n.loadtxt(infile,unpack=True,usecols=(1,2),dtype=float)

new_lens_mean = data/yans_mean
new_lens_median = data/yans_median

new_lens_mean_w = data_w/yans_weighted_mean
new_lens_median_w = data_w/yans_weighted_median

lensroot = n.loadtxt('lenses_root.list',dtype='S11')
nlens = lensroot.size

puppy = input("What is the maximum magnitude?") * 10

f = open('new_table%d.txt' %puppy,'w')

cosmosfile = n.loadtxt('cosmostable.txt',dtype=float)

one = 'COSMOS'
two = 'Yan'
cosmos_unw = 64.175
cosmos_w = 2.526

f.write('# Number Counts\n')
f.write('\n')
f.write('# Field            N_gal(unweighted)  ratio_to_Yan_mean   N_gal(weighted) ratio_to_Yan_mean(weighted)\n')
f.write('# -----------      -----------------  ------------------  --------------  -------------------------- \n')
f.write('%-11s %14.3f %17.3f %17.3f %17.3f\n' %(one,cosmos_unw,(64.175/yans_mean),cosmos_w,(2.526/yans_weighted_mean)))
           
for i in range(nlens):
    f.write('%-11s %14.3f %17.3f %17.3f %17.3f\n' % (lensroot[i], data[i], new_lens_mean[i], data_w[i], new_lens_mean_w[i]))

f.write('%-11s %14.3f %17.3f %17.3f %17.3f' %(two,yans_mean,(yans_mean/yans_mean),yans_weighted_mean,yans_weighted_mean/yans_weighted_mean))
f.close()
