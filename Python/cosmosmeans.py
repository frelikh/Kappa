import sys
import numpy as n
import numbercts as num

yans = []
yans_weighted = []

'''
OK here replace Yan with COSMOS for everything
'''

# since there are four Yan files for each of the four coordinates,
# first put all of them in one list for the sums, and one list
# for the weighted sums

indir = '/mnt/data1/renata/ACS/'
for i in range(4):
    name = indir+'Cosmos_counts/cosmos%s.txt' % i

    # gets the data for a given COSMOS list
    count,count_w = n.loadtxt(name,unpack=True,usecols=(1,2))


    # now, add to the list of all sums and weighted sums
    yans.append(count)
    yans_weighted.append(count_w)

# means and medians of the entire COSMOS lists

#yans_median = n.median(yans)
yans_mean = n.mean(yans)
yans_median = n.median(yans)

yans_weighted_median = n.median(yans_weighted)
yans_weighted_mean = n.mean(yans_weighted)



f = open(indir+'Cosmos_counts/cosmostable.txt','w')
f.write('%10.3f %10.3f %10.3f %10.3f' %(yans_mean,yans_mean/yans_mean,yans_weighted_mean,yans_weighted_mean/yans_weighted_mean))
f.close()


'''
print yans_median
print yans_mean

print yans_weighted_median
print yans_weighted_mean
'''

infile = indir+'Lens Counts/lens.txt'
data,data_w = n.loadtxt(infile,unpack=True,usecols=(1,2))

new_lens_mean = data/yans_mean
new_lens_median = data/yans_median

new_lens_mean_w = data_w/yans_weighted_mean
new_lens_median_w = data_w/yans_weighted_median

lensroot = n.loadtxt(indir+'lenses_root.list',dtype='S11')
nlens = lensroot.size

puppy = input("What is the maximum magnitude?")

f = open('cosmos_unw_sums%d.txt' %puppy,'w')
f.write('# Unweighted Sums\n')
f.write('\n')
f.write('# Lens_name        ratio_to_Cosmos_mean  ratio_to_Cosmos_median\n')
f.write('# -----------      -----------------  ------------------\n')
for i in range(nlens):
    f.write('%-11s    %10.3f      %10.3f\n' % (lensroot[i],new_lens_mean[i],new_lens_median[i]))
f.close()

f = open('cosmos_w_sums%d.txt' %puppy,'w')
f.write('# Weighted Sums\n')
f.write('\n')
f.write('# Lens_name        ratio_to_Cosmos_mean  ratio_to_Cosmos_median\n')
f.write('# -----------      -----------------  ------------------\n')
for i in range(nlens):
    f.write('%-11s    %10.3f      %10.3f\n' % (lensroot[i],new_lens_mean_w[i],new_lens_median_w[i]))
f.close()
