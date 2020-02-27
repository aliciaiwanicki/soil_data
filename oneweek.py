import pandas as pd
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
import glob
import matplotlib.dates as mdates
import matplotlib.ticker as plticker



#----------------------------------------------- FLUXES ---------------------------------------------
a = pd.read_csv('/Volumes/WSU/2. ALL DATA FILES/(5) Combined SFP Files/SFP output files in STD (wheat)/noniso_20191016_20191021.txt', engine='python', delimiter='\t', header = 0)
b = pd.read_csv('/Volumes/WSU/2. ALL DATA FILES/(5) Combined SFP Files/SFP output files in STD (wheat)/noniso_20191021_20191023.txt', engine='python', delimiter='\t', header = 0)
c = pd.read_csv('/Volumes/WSU/2. ALL DATA FILES/(5) Combined SFP Files/SFP output files in STD (wheat)/noniso_20191023_20191028.txt', engine='python', delimiter='\t', header = 0)

noniso = pd.concat([a,b,c], sort = False)
noniso.index = pd.to_datetime(noniso.Date_IV)
noniso = noniso.sort_index()

noniso.loc[~(noniso['Lin_Flux[2]'] > 0), 'Lin_Flux[2]'] = np.nan            # Clip negative FLUX values to NaN
noniso.loc[~(noniso['Exp_Flux[2]'] > 0), 'Exp_Flux[2]'] = np.nan
#noniso.loc[~(noniso['Lin_Flux[2]'] = 1), 'Lin_Flux[2]'] = np.nan
noniso.loc[~(noniso['Lin_R2[2]'] > 0.70), 'Lin_Flux[2]'] = 0                # Change N2O fluxes with R2 values < 0.7 to 0
noniso.loc[~(noniso['Exp_R2[2]'] > 0.70), 'Exp_Flux[2]'] = 0 

LinExp = noniso['Lin_R2[2]'] >= noniso['Exp_R2[2]']
ten = (noniso['Exp_R2[2]']-noniso['Lin_R2[2]'])/noniso['Lin_R2[2]'] <= .1
LinExp = LinExp | ten
#N2O_Flux = []; N2O_Flux = pd.DataFrame(N2O_Flux)
# Creates a column called 'Flux' as part of this.
noniso['N2O_Flux'] = noniso['Exp_Flux[2]']              # Sets the entire column equal to Exp_Flux[2] data
noniso['N2O_Flux'][LinExp] = noniso['Lin_Flux[2]']     
noniso['LinExp'] = LinExp                               # Sets just the times when LinExp == True to the Lin_Flux[2] data; should just replace those few columns
noniso['N2O_N_Flux'] = noniso['N2O_Flux']*(28/44)
noniso['N2O_N_Flux_nmol/m2/s'] = noniso['N2O_N_Flux']*22.72

print(sum(LinExp))

gr_chambers = noniso.groupby('Port#')
for k in gr_chambers.groups.keys():
    gr = gr_chambers.get_group(k)

daily_noniso = pd.DataFrame()
daily_noniso['N2O_N_Flux_daily_mean'] = noniso['N2O_N_Flux_nmol/m2/s'].resample('D').mean()
daily_noniso['N2O_N_Flux_daily_max'] = noniso['N2O_N_Flux_nmol/m2/s'].resample('D').max()
daily_noniso['N2O_N_Flux_daily_min'] = noniso['N2O_N_Flux_nmol/m2/s'].resample('D').min()
daily_noniso['Datetime'] = daily_noniso.index
            
chamber_means = noniso.groupby('Port#').resample('B').mean()
# each indiv port number??

gr = noniso.groupby('Port#')          
a = gr.get_group(1) #WP
b = gr.get_group(2) #WPWP
c = gr.get_group(3) #WPWB
d = gr.get_group(4) #WP
e = gr.get_group(5) #WPWB
f = gr.get_group(6) #WP
g = gr.get_group(7) #WP
h = gr.get_group(8) #WPBP

daily_noniso['Tcham_mean'] = noniso['Tcham_IV'].resample('D').mean()
daily_noniso['Tcham_max'] = noniso['Tcham_IV'].resample('D').max()
daily_noniso['Tcham_min'] = noniso['Tcham_IV'].resample('D').min()

#-----------------------------------------------  SOIL DATA   -----------------------------------------------
df_soil = pd.read_csv('/Volumes/WSU/1. PYTHON Code/One Week/df_soil_STD.csv',index_col=None, header = 0)
df_soil.index = pd.to_datetime(df_soil.Datetime)
df_soil = df_soil.sort_index()

df_soil_daily = pd.read_csv('/Volumes/WSU/1. PYTHON Code/One Week/df_soil_daily.csv',index_col=None, header = 0)
df_soil_daily.index = pd.to_datetime(df_soil_daily.Datetime)
df_soil_daily = df_soil_daily.sort_index()


#-----------------------------------------------  WEATHER DATA   -----------------------------------------------
## PCFS Weather files reformatted and QA/QC'd by A.Iwanicki. See "ReadMe" in Data folder for details. All PST timestamps converted to STD.

weather = pd.read_csv('/Volumes/WSU/2. ALL DATA FILES/(4) PCFS Weather Data/PCFS MET STN PRECIP/Monthly PCFS weather (combined)/PCFS_weather_jan2019_feb2020_STD.csv',index_col=None, header = 0)
weather.index = pd.to_datetime(weather.Datetime_STD)
weather = weather.sort_index()


#-----------------------------------------------  FIGURES   -----------------------------------------------
fig, axes = plt.subplots(nrows=4,ncols=1,figsize=(12,8))
a['N2O_N_Flux_nmol/m2/s'].plot(ax = axes[0], marker='o', ms = 2, lw=0.8, color = '#FF33FF')
b['N2O_N_Flux_nmol/m2/s'].plot(ax = axes[0], marker='o', ms = 2, lw=0.8, color = '#CC0000')
c['N2O_N_Flux_nmol/m2/s'].plot(ax = axes[0], marker='o', ms = 2, lw=0.8, color = '#8408B9')
d['N2O_N_Flux_nmol/m2/s'].plot(ax = axes[0], marker='o', ms = 2, lw=0.8, color = '#48C9B0')
e['N2O_N_Flux_nmol/m2/s'].plot(ax = axes[0], marker='o', ms = 2, lw=0.8, color = '#1976D2')
f['N2O_N_Flux_nmol/m2/s'].plot(ax = axes[0], marker='o', ms = 2, lw=0.8, color = '#66FF33')
g['N2O_N_Flux_nmol/m2/s'].plot(ax = axes[0], marker='o', ms = 2, lw=0.8, color = '#F4D03F')
h['N2O_N_Flux_nmol/m2/s'].plot(ax = axes[0], marker='o', ms = 2, lw=0.8, color = '#FF8F00')                            
                                
lgnd1 = axes[0].legend(loc="top left", ncol=4, fontsize = 6)
lgnd1.get_texts()[0].set_text('1')
lgnd1.get_texts()[1].set_text('2')
lgnd1.get_texts()[2].set_text('3')
lgnd1.get_texts()[3].set_text('4')
lgnd1.get_texts()[4].set_text('5')
lgnd1.get_texts()[5].set_text('6')
lgnd1.get_texts()[6].set_text('7')
lgnd1.get_texts()[7].set_text('8') 
                                 
axes[0].set_ylabel(r'$\frac{nmol-N_{2}O-N}{m^{2}-s}$', size=12) 
axes[1].set_ylabel(r'$\frac{nmol-N_{2}O-N}{m^{2}-s}$', size=12)
axes[2].set_ylabel('mm', size=10)
axes[3].set_ylabel('$^\circ$C', size=10)
axes[2].get_yaxis().set_label_coords(-0.04,0.5)
axes[3].get_yaxis().set_label_coords(-0.04,0.5)
                              
daily_noniso['N2O_N_Flux_daily_max'].plot(ax = axes[1], c='grey', ms=1, alpha=0.5, lw=1.5, label='Max Flux')
daily_noniso['N2O_N_Flux_daily_min'].plot(ax = axes[1], c='darkgrey', alpha=0.5, lw=1.5, label='Min Flux')
daily_noniso['N2O_N_Flux_daily_mean'].plot(ax = axes[1], marker='o', ms = 2, linestyle=':', color = 'red', lw=0.5, label='Mean Flux')
axes[1].fill_between(daily_noniso.index, daily_noniso['N2O_N_Flux_daily_min'], daily_noniso['N2O_N_Flux_daily_max'], alpha=0.1)
fig.subplots_adjust(left=0.09,bottom=0.16, right=0.94,top=0.90, wspace=0.2, hspace=0)                         

#plot other variables
weather['Precip_Avg_mm'].plot(ax = axes[2], color = 'blue')
df_soil['soil_avg_%_VWC'].plot(ax = axes[2], secondary_y=True, color='blue', alpha=0.5, linewidth=2)
daily_noniso['Tcham_mean'].plot(ax = axes[3], color='red', linewidth=2, label='Ambient Air')
df_soil_daily['soil_temp_mean'].plot(ax=axes[3], color='black', linewidth=2, label='Surface Soil')

# Date limit
axes[0].set_xlim(['2019-10-16', '2019-10-28'])
axes[1].set_xlim(['2019-10-16', '2019-10-28'])
axes[2].set_xlim(['2019-10-16', '2019-10-28'])
axes[3].set_xlim(['2019-10-16', '2019-10-28'])
# X -Axis Titles
axes[0].set_xlabel('', size=1)
axes[1].set_xlabel('', size=1)
axes[2].set_xlabel('', size=1)
axes[3].set_xlabel('Date/Time (STD)', size=13)

axes[0].set_xticklabels([])
axes[1].set_xticklabels([])
axes[2].set_xticklabels([])
