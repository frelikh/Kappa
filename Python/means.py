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
data,data_w = n.loadtxt(infile,unpack=True,usecols=(1,2))

new_lens_mean = data/yans_mean
new_lens_median = data/yans_median

new_lens_mean_w = data_w/yans_weighted_mean
new_lens_median_w = data_w/yans_weighted_median

lensroot = n.loadtxt('lenses_root.list',dtype='S11')
nlens = lensroot.size

puppy = input("What is the maximum magnitude?") * 10

f = open('new_unw_sums%d.txt' %puppy,'w')

f.write('# Unweighted Sums\n')
f.write('\n')
f.write('# Lens_name        ratio_to_Yan_mean  ratio_to_Yan_median\n')
f.write('# -----------      -----------------  ------------------\n')
for i in range(nlens):
    f.write('%-11s    %10.3f      %10.3f\n' % (lensroot[i],new_lens_mean[i],new_lens_median[i]))
f.close()

f = open('new_w_sums%d.txt' %puppy,'w')
f.write('# Weighted Sums\n')
f.write('\n')
f.write('# Lens_name        ratio_to_Yan_mean  ratio_to_Yan_median\n')
f.write('# -----------      -----------------  ------------------\n')
for i in range(nlens):
    f.write('%-11s    %10.3f      %10.3f\n' % (lensroot[i],new_lens_mean_w[i],new_lens_median_w[i]))
f.close()
