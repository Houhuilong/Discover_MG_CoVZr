# -*- coding: utf-8 -*-
"""
Created on Wed July 13 2016

@author: fangren
contributed by T Williams
"""


import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from os.path import basename
import imp
import scipy
from scipy import interpolate


plotTernary = imp.load_source("plt_ternary_save", "plotTernary.py")


path = '..//..//data//CoVZr//master_data//'
save_path = '..//..//figures//'

basename1 = 'CLEANED_Sample9_master_metadata_low.csv'
basename2 = 'CLEANED_Sample10_master_metadata_low.csv'
basename3 = 'CLEANED_Sample18_master_metadata_low.csv'

filename1 = path + basename1
filename2 = path + basename2
filename3 = path + basename3

data1 = np.genfromtxt(filename1, delimiter=',', skip_header = 1)
data2 = np.genfromtxt(filename2, delimiter=',', skip_header = 1)
data3 = np.genfromtxt(filename3, delimiter=',', skip_header = 1)

data = np.concatenate((data1[:, :69], data2[:, :69], data3[:, :69]))

Co = data[:,57]*100
V = data[:,58]*100
Zr = data[:,59]*100
peak_position = data[:,60]
peak_width = data[:,61]
peak_intensity = data[:,62]
peak_width_neighborhood = np.copy(peak_width)



# neighborhood voting
neighborhood_window = 1


for i in range(len(Co)):
    for j in range(len(Co)):
        if abs(Co[i]-Co[j]) < neighborhood_window\
        and abs(V[i]-V[j]) < neighborhood_window\
        and abs(Zr[i]-Zr[j]) < neighborhood_window:
            peak_width_ave = np.average([peak_width[i], peak_width[j]])
            peak_width_min = np.min([peak_width[i], peak_width[j]])
            peak_width_max = np.max([peak_width[i], peak_width[j]])
            peak_width_neighborhood[i] = peak_width_max
            peak_width_neighborhood[j] = peak_width_max
        else:
            continue




# interpolation
peak_width_func = interpolate.Rbf(Co, V, Zr, peak_width_neighborhood, function='multiquadric', smooth=0.3)

Co_range = np.arange(7.5, 81.7, 1)
V_range = np.arange(8.7, 76.5, 1)


Co_new = []
V_new = []
Zr_new = []

peak_width_new = []

for i in Co_range:
    for j in V_range:
        if i + j <= 91.5 and i+j >= 29.5:
            try:
                Co_new.append(i)
                V_new.append(j)
                Zr_new.append(100-i-j)
                peak_width_new.append(float(peak_width_func(i, j, (100-i-j))))
            except(ValueError):
                continue


Co_new = np.array(Co_new)
V_new = np.array(V_new)
Zr_new = np.array(Zr_new)
peak_width_new = np.array(peak_width_new)

print peak_width.max(), peak_width.min()
print peak_width_new.max(), peak_width_new.min()


# ternary_data = np.concatenate(([Co_new],[V_new],[Zr_new],[peak_width_new]), axis = 0)
# ternary_data = np.transpose(ternary_data)
#
# plotTernary.plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','V','Zr'), scale=100,
#                        sv=True, svpth=save_path, svflnm='Figure3b_FWHM_interpolated_CoVZr',
#                        cbl='FWHM', vmin = 0.341, vmax = 0.964, cmap='viridis_r', cb=True, style='h')
#

labels = []
for pw in peak_width_new:
    # if pw < 0.16:
    #     label = 0
    if pw < 0.57:
         label = 0
    elif pw >= 0.57:
        label = 1
    # else:
    #     label = 0.5
    labels.append(label)


ternary_data = np.concatenate(([Co_new],[V_new],[Zr_new],[labels]), axis = 0)
ternary_data = np.transpose(ternary_data)

plotTernary.plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','V','Zr'), scale=100,
                       sv=True, svpth=save_path, svflnm='Figure3b_GFA_CoVZr',
                       cbl='Glass forming', vmax = 1, vmin = 0.1, cmap='viridis_r', cb=True, style='h')


plt.close('all')


# labels = []
# for pw in peak_width:
#     if pw < 0.16:
#         label = 0
#     elif pw > 0.57:
#         label = 1
#     else:
#         label = 0.5
#     labels.append(label)
#
#
# save_path_2 = 'C:\\Research_FangRen\\Data\\July2016\\CoVZr_ternary\\Theory\\'
# data = np.concatenate(([Co], [V], [Zr], [peak_width], [labels]))
# np.savetxt(save_path_2+'peak_width_low.csv', data.T, delimiter=',')


print peak_position.max(), peak_position.min()
print peak_width.max(), peak_width.min()