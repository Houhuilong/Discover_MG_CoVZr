# -*- coding: utf-8 -*-
"""
Created on Wed July 13 2016

@author: fangren, T Williams
"""


import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from os.path import basename
import imp
import scipy
from scipy import interpolate


from plotTernary import plt_ternary_save


path = '..//..//data//CoFeZr//master_data//'
save_path =  '..//..//figures//'


basename1 = 'CLEANED_Sample4_master_metadata.csv'
basename2 = 'CLEANED_Sample5_master_metadata.csv'
basename3 = 'CLEANED_Sample6_master_metadata.csv'

filename1 = path + basename1
filename2 = path + basename2
filename3 = path + basename3

data1 = np.genfromtxt(filename1, delimiter=',', skip_header = 1)
data2 = np.genfromtxt(filename2, delimiter=',', skip_header = 1)
data3 = np.genfromtxt(filename3, delimiter=',', skip_header = 1)

data = np.concatenate((data1, data2, data3))

plate_x = data[:, 1]
plate_y = data[:, 2]
Fe_alpha = data[:, 60]
Co_alpha = data[:, 62]
Co = data[:,54]
Fe = data[:,55]
Zr = data[:,56]
peak_position = data[:,64]
peak_width = data[:,65]
peak_intensity = data[:,66]


peak_width_neighborhood = np.copy(peak_width)

#
# ternary_data = np.concatenate(([Co],[Fe],[Zr],[peak_width]), axis = 0)
# ternary_data = np.transpose(ternary_data)
#
# plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','Fe','Zr'), scale=100,
#                        sv=True, svpth=save_path, svflnm='FWHM_CoFeZr',
#                        cbl='FWHM', vmin = 0.05, vmax = 0.57, cmap='viridis_r', cb=True, style='h')
# # plt.close('all')
# # plt.figure(1)
# # plt.scatter(plate_y, plate_x, c = peak_width, s = 100, cmap = 'viridis_r')
# # plt.clim(0.314, 0.964)
# # plt.savefig(save_path + 'wafer')
#
#
#
# ternary_data = np.concatenate(([Co],[Fe],[Zr],[peak_position]), axis = 0)
# ternary_data = np.transpose(ternary_data)
#
# plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','Fe','Zr'), scale=100,
#                        sv=True, svpth=save_path, svflnm='peak_position_CoFeZr',
#                        cbl='Peak position', vmin = 2.68, vmax = 3.05, cmap='viridis', cb=True, style='h')


# ternary_data = np.concatenate(([Co],[Fe],[Zr],[[1]*len(Co)]), axis = 0)
# ternary_data = np.transpose(ternary_data)
#
# plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','Fe','Zr'), scale=100,
#                        sv=True, svpth=save_path, svflnm='black_low',
#                        cbl='Scale', cmap='gray', cb=True, style='h')
#


#
# ternary_data = np.concatenate(([Co],[Fe],[Zr],[Fe_alpha]), axis = 0)
# ternary_data = np.transpose(ternary_data)
#
# plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','Fe','Zr'), scale=100,
#                        sv=True, svpth=save_path, svflnm='Fe_alpha',
#                        cbl='Scale', cmap='viridis', cb=True, style='h')
#
#
# ternary_data = np.concatenate(([Co],[Fe],[Zr],[Co_alpha]), axis = 0)
# ternary_data = np.transpose(ternary_data)
#
# plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','Fe','Zr'), scale=100,
#                        sv=True, svpth=save_path, svflnm='Co_alpha',
#                        cbl='Scale', cmap='viridis', cb=True, style='h')


# neighborhood voting
neighborhood_window = 1


for i in range(len(Co)):
    for j in range(len(Co)):
        if abs(Co[i]-Co[j]) < neighborhood_window\
        and abs(Zr[i]-Zr[j]) < neighborhood_window\
        and abs(Fe[i]-Fe[j]) < neighborhood_window:
            peak_width_ave = np.average([peak_width[i], peak_width[j]])
            peak_width_min = np.min([peak_width[i], peak_width[j]])
            peak_width_max = np.max([peak_width[i], peak_width[j]])
            peak_width_neighborhood[i] = peak_width_max
            peak_width_neighborhood[j] = peak_width_max
        else:
            continue


# ternary_data = np.concatenate(([Co],[Fe],[Zr],[peak_width_neighborhood]), axis = 0)
# ternary_data = np.transpose(ternary_data)
#
# plotTernary.plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','Fe','Zr'), scale=100,
#                        sv=True, svpth=save_path, svflnm='peak_width_neighborhood_low',
#                        cbl='FWHM', vmin = 0.341, vmax = 0.5, cmap='viridis_r', cb=True, style='h')
#

# interpolation
peak_width_func = interpolate.Rbf(Co, Zr, Fe, peak_width_neighborhood, function='multiquadric', smooth=0.3)


Co_range = np.arange(min(Co), max(Co), 1)
Zr_range = np.arange(min(Zr), max(Zr), 1)


Co_new = []
Zr_new = []
Fe_new = []

peak_width_new = []

for i in Co_range:
    for j in Zr_range:
        if i + j <= 93.5 and i+j >= 23.7:
            try:
                Co_new.append(i)
                Zr_new.append(j)
                Fe_new.append(100-i-j)
                peak_width_new.append(float(peak_width_func(i, j, (100-i-j))))
            except(ValueError):
                continue


Co_new = np.array(Co_new)
Zr_new = np.array(Zr_new)
Fe_new = np.array(Fe_new)
peak_width_new = np.array(peak_width_new)

print peak_width.max(), peak_width.min()
print peak_width_new.max(), peak_width_new.min()


ternary_data = np.concatenate(([Co_new],[Fe_new],[Zr_new],[peak_width_new]), axis = 0)
ternary_data = np.transpose(ternary_data)

plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','Fe','Zr'), scale=100,
                       sv=True, svpth=save_path, svflnm='FWHM_interpolated_CoFeZr',
                       cbl='FWHM', vmin = 0.2, vmax = 0.57, cmap='viridis_r', cb=True, style='h')



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


ternary_data = np.concatenate(([Co_new],[Fe_new],[Zr_new],[labels]), axis = 0)
ternary_data = np.transpose(ternary_data)

plt_ternary_save(ternary_data, tertitle='',  labelNames=('Co','Fe','Zr'), scale=100,
                       sv=True, svpth=save_path, svflnm='GFA_CoFeZr',
                       cbl='Scale', vmax = 1, vmin = 0.1, cmap='viridis_r', cb=True, style='h')



labels_measured = []
for pw in peak_width:
    if pw < 0.16:
        label = 0
    elif pw > 0.57:
        label = 1
    else:
        label = 0.5
    labels_measured.append(label)

labels_measured = np.array(labels_measured)

save_path2 = '..//..//machine-learning//datasets//new-data//'


data = np.concatenate(([Co], [Fe], [Zr],  [labels_measured]))
np.savetxt(save_path2+'GFA_CoFeZr.csv', data.T, header = 'Co, Fe, Zr, is_glass', delimiter=',', fmt='%1.3f', comments='')

