import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import glob
import matplotlib.dates as mdates
import matplotlib.ticker as plticker

## Port 1-4: Moisture (m3/m3 VWC)     Port 1.1-4.1: Soil Temp (C)
# 4P Port 4 broken
# 1P Port 2 broken

#-------------------------------  1P   -------------------------------
path = '/Volumes/TOSHIBA EXT/Backups/WSU(jan15)/ALL DATA FILES/(3) Soil Data/1Pcsv'
all_files = glob.glob(path + "/*.csv")                                              
li = []

for filename in all_files:
    df = pd.read_csv(filename, header = 0, index_col='1P10', skiprows=(1,2))
    li.append(df)
    
soil1P = pd.concat(li, axis=0)                  
#soil1P.rename(columns={'1P10':'DateTime'}, inplace=True)
soil1P.index = pd.to_datetime(soil1P.index)
soil1P = soil1P.sort_index()
soil1P = soil1P[soil1P.index > '2019-05-15']

soil1P['soil1P_mean_moisture'] = soil1P[['Port 1', 'Port 3', 'Port 4']].mean(axis=1)
soil1P['soil1P_mean_temp'] = soil1P[['Port 1.1', 'Port 2.1', 'Port 3.1', 'Port 4.1']].mean(axis=1)


#-------------------------------  2P   -------------------------------
path2 = '/Volumes/TOSHIBA EXT/Backups/WSU(jan15)/ALL DATA FILES/(3) Soil Data/2Pcsv'
all_files2 = glob.glob(path2 + "/*.csv")                                              
li2 = []

for filename2 in all_files2:
    df2 = pd.read_csv(filename2, header = 0, index_col='2P10', skiprows=(1,2))        
    li2.append(df2)
    
soil2P = pd.concat(li2, axis=0)                  
#soil1P.rename(columns={'1P10':'DateTime'}, inplace=True)
soil2P.index = pd.to_datetime(soil2P.index)
soil2P = soil2P.sort_index()
soil2P = soil2P[soil2P.index > '2019-05-15']

soil2P['soil2P_mean_moisture'] = soil2P[['Port 1', 'Port 2', 'Port 3', 'Port 4']].mean(axis=1)
soil2P['soil2P_mean_temp'] = soil2P[['Port 1.1', 'Port 2.1', 'Port 3.1', 'Port 4.1']].mean(axis=1)


#-------------------------------  3P   -------------------------------
path3 = '/Volumes/TOSHIBA EXT/Backups/WSU(jan15)/ALL DATA FILES/(3) Soil Data/3Pcsv'
all_files3 = glob.glob(path3 + "/*.csv")                                              
li3 = []

for filename3 in all_files3:
    df3 = pd.read_csv(filename3, header = 0, index_col='3P10', skiprows=(1,2))        
    li3.append(df3)
    
soil3P = pd.concat(li3, axis=0)                  
#soil1P.rename(columns={'1P10':'DateTime'}, inplace=True)
soil3P.index = pd.to_datetime(soil3P.index)
soil3P = soil3P.sort_index()
soil3P = soil3P[soil3P.index > '2019-05-15']
soil3P['soil3P_mean_moisture'] = soil3P[['Port 1', 'Port 2', 'Port 3', 'Port 4']].mean(axis=1)
soil3P['soil3P_mean_temp'] = soil3P[['Port 1.1', 'Port 2.1', 'Port 3.1', 'Port 4.1']].mean(axis=1)


#-------------------------------  4P   -------------------------------
path4 = '/Volumes/TOSHIBA EXT/Backups/WSU(jan15)/ALL DATA FILES/(3) Soil Data/4Pcsv'
all_files4 = glob.glob(path4 + "/*.csv")                                              
li4 = []

for filename4 in all_files4:
    df4 = pd.read_csv(filename4, header = 0, index_col='4P10', skiprows=(1,2))        
    li4.append(df4)
    
soil4P = pd.concat(li4, axis=0)                  
#soil1P.rename(columns={'1P10':'DateTime'}, inplace=True)
soil4P.index = pd.to_datetime(soil4P.index)
soil4P = soil4P.sort_index()
soil4P = soil4P[soil4P.index > '2019-05-15']

soil4P['soil4P_mean_moisture'] = soil4P[['Port 1', 'Port 2', 'Port 3']].mean(axis=1)
soil4P['soil4P_mean_temp'] = soil4P[['Port 1.1', 'Port 2.1', 'Port 3.1', 'Port 4.1']].mean(axis=1)


#---------------------  NEW DF OF COMBINED MOISTURE & TEMP MEANS   -----------------------
Index2 = list(set(list(soil1P.index) + list(soil2P.index) + list(soil3P.index) + list(soil4P.index)))
Index2.sort()
soildata_means = pd.DataFrame({'soil1P_mean_moisture': [soil1P.loc[Date, 'soil1P_mean_moisture'] if Date in soil1P.index else np.nan for Date in Index2],\
                'soil2P_mean_moisture': [soil2P.loc[Date, 'soil2P_mean_moisture'] if Date in soil2P.index else np.nan for Date in Index2],\
                'soil3P_mean_moisture': [soil3P.loc[Date, 'soil3P_mean_moisture'] if Date in soil3P.index else np.nan for Date in Index2],\
                'soil4P_mean_moisture': [soil4P.loc[Date, 'soil4P_mean_moisture'] if Date in soil4P.index else np.nan for Date in Index2],\
                'soil1P_mean_temp': [soil1P.loc[Date, 'soil1P_mean_temp'] if Date in soil1P.index else np.nan for Date in Index2],\
                'soil2P_mean_temp': [soil2P.loc[Date, 'soil2P_mean_temp'] if Date in soil2P.index else np.nan for Date in Index2],\
                'soil3P_mean_temp': [soil3P.loc[Date, 'soil3P_mean_temp'] if Date in soil3P.index else np.nan for Date in Index2],\
                'soil4P_mean_temp': [soil4P.loc[Date, 'soil4P_mean_temp'] if Date in soil4P.index else np.nan for Date in Index2]},\
                index = Index2)
soildata_means.index.name = 'DateTime'
##soildata_means = soildata_means[np.isfinite(soildata_means['soil1P_mean_moisture'])]
##soildata_means = soildata_means.astype(np.float64)
##soildata_means = soildata_means['soil1P_mean_moisture'].astype(float)

# Mean of all moisture and temp columns
##soildata_means['soil_moisture_mean'] = soildata_means[['soil1P_mean_moisture', 'soil2P_mean_moisture', 'soil3P_mean_moisture', 'soil4P_mean_moisture']].mean(axis=1)
##soildata_means['soil_temp_mean'] = soildata_means['soil1P_mean_temp', 'soil2P_mean_temp', 'soil3P_mean_temp', 'soil4P_mean_temp'].mean(axis=1)

#soildata_means.to_csv('soildata_means.csv', index=True)

#-------------------------------  FIGURE 1   -------------------------------
fig, axes = plt.subplots(nrows=4,ncols=1,figsize=(12,6))
soil1P['Port 1'].plot(ax = axes[0], subplots=True, color = 'blue')
soil1P['Port 2'].plot(ax = axes[0], subplots=True, color = 'red')
soil1P['Port 3'].plot(ax = axes[0], subplots=True, color = 'green')
soil1P['Port 4'].plot(ax = axes[0], subplots=True, color = 'orange')
soil2P['Port 1'].plot(ax = axes[1], subplots=True, color = 'blue')
soil2P['Port 2'].plot(ax = axes[1], subplots=True, color = 'red')
soil2P['Port 3'].plot(ax = axes[1], subplots=True, color = 'green')
soil2P['Port 4'].plot(ax = axes[1], subplots=True, color = 'orange')
soil3P['Port 1'].plot(ax = axes[2], subplots=True, color = 'blue')
soil3P['Port 2'].plot(ax = axes[2], subplots=True, color = 'red')
soil3P['Port 3'].plot(ax = axes[2], subplots=True, color = 'green')
soil3P['Port 4'].plot(ax = axes[2], subplots=True, color = 'orange')
soil4P['Port 1'].plot(ax = axes[3], subplots=True, color = 'blue')
soil4P['Port 2'].plot(ax = axes[3], subplots=True, color = 'red')
soil4P['Port 3'].plot(ax = axes[3], subplots=True, color = 'green')

plt.tight_layout()
#axes[0].set_xlim(['2019-05-15', '2020-01-01'])
axes[1].set_xlim(['2019-05-15', '2020-01-01'])
#axes[2].set_xlim(['2019-05-15', '2020-01-01'])
#axes[3].set_xlim(['2019-05-15', '2020-01-01'])

# Tick Font Size (x,y)
axes[0].tick_params(axis='x', labelsize=7)  #rotation=60
axes[1].tick_params(axis='x', labelsize=7)
axes[2].tick_params(axis='x', labelsize=7)
axes[3].tick_params(axis='x', labelsize=7)
axes[0].tick_params(axis='y', labelsize=7)
axes[1].tick_params(axis='y', labelsize=7)
axes[2].tick_params(axis='y', labelsize=7)
axes[3].tick_params(axis='y', labelsize=7)

# X-Axis Titles
axes[0].set_xlabel('', size=1)
axes[1].set_xlabel('', size=1)
axes[2].set_xlabel('', size=1)
axes[3].set_xlabel('Date/Time', size=8)

# Y-Axis Titles
axes[0].set_title('Soil Moisture ($m^{3}$/$m^{3}$ VWC)', size=10)
axes[0].set_ylabel('1P', size=8)
axes[1].set_ylabel('2P', size=8)
axes[2].set_ylabel('3P', size=8)
axes[3].set_ylabel('4P', size=8)

axes[0].legend(loc="lower right",ncol=4, fontsize = 'x-small')

#-------------------------------  FIGURE 2   -------------------------------
fig2, axes = plt.subplots(nrows=4,ncols=1,figsize=(12,6))
soil1P['Port 1.1'].plot(ax = axes[0], subplots=True, color = 'blue', linewidth=0.5)
soil1P['Port 2.1'].plot(ax = axes[0], subplots=True, color = 'red', linewidth=0.5)
soil1P['Port 3.1'].plot(ax = axes[0], subplots=True, color = 'green', linewidth=0.5)
soil1P['Port 4.1'].plot(ax = axes[0], subplots=True, color = 'orange', linewidth=0.5)
soil2P['Port 1.1'].plot(ax = axes[1], subplots=True, color = 'blue', linewidth=0.5)
soil2P['Port 2.1'].plot(ax = axes[1], subplots=True, color = 'red', linewidth=0.5)
soil2P['Port 3.1'].plot(ax = axes[1], subplots=True, color = 'green', linewidth=0.5)
soil2P['Port 4.1'].plot(ax = axes[1], subplots=True, color = 'orange', linewidth=0.5)
soil3P['Port 1.1'].plot(ax = axes[2], subplots=True, color = 'blue', linewidth=0.5)
soil3P['Port 2.1'].plot(ax = axes[2], subplots=True, color = 'red', linewidth=0.5)
soil3P['Port 3.1'].plot(ax = axes[2], subplots=True, color = 'green', linewidth=0.5)
soil3P['Port 4.1'].plot(ax = axes[2], subplots=True, color = 'orange', linewidth=0.5)
soil4P['Port 1.1'].plot(ax = axes[3], subplots=True, color = 'blue', linewidth=0.5)
soil4P['Port 2.1'].plot(ax = axes[3], subplots=True, color = 'red', linewidth=0.5)
soil4P['Port 3.1'].plot(ax = axes[3], subplots=True, color = 'green', linewidth=0.5)

plt.tight_layout()
#axes[0].set_xlim(['2019-05-15', '2020-01-01'])
axes[1].set_xlim(['2019-05-15', '2020-01-01'])
#axes[2].set_xlim(['2019-05-15', '2020-01-01'])
#axes[3].set_xlim(['2019-05-15', '2020-01-01'])

# Tick Font Size (x,y)
axes[0].tick_params(axis='x', labelsize=7)  #rotation=60
axes[1].tick_params(axis='x', labelsize=7)
axes[2].tick_params(axis='x', labelsize=7)
axes[3].tick_params(axis='x', labelsize=7)
axes[0].tick_params(axis='y', labelsize=7)
axes[1].tick_params(axis='y', labelsize=7)
axes[2].tick_params(axis='y', labelsize=7)
axes[3].tick_params(axis='y', labelsize=7)

# X-Axis Titles
axes[0].set_xlabel('', size=1)
axes[1].set_xlabel('', size=1)
axes[2].set_xlabel('', size=1)
axes[3].set_xlabel('Date/Time', size=8)

# Y-Axis Titles
axes[0].set_title('Soil Temperature (deg C)', size=10)
axes[0].set_ylabel('1P', size=8)
axes[1].set_ylabel('2P', size=8)
axes[2].set_ylabel('3P', size=8)
axes[3].set_ylabel('4P', size=8)

axes[1].legend(loc="upper right",ncol=4, fontsize = 'x-small')

#-------------------------------  FIGURE 3   -------------------------------
fig3, ax = plt.subplots(figsize=(16,4))
soil1P['soil1P_mean_moisture'].plot(color = 'orange', linewidth=0.5)
soil2P['soil2P_mean_moisture'].plot(color = 'r', linewidth=0.5)
soil3P['soil3P_mean_moisture'].plot(color = 'purple', linewidth=0.5)
soil4P['soil4P_mean_moisture'].plot(color = 'blue', linewidth=0.5)
ax.set_xlim(['2019-05-15', '2020-01-01'])
ax.set_xlabel('Date/Time', size=8)
ax.set_ylabel('Mean Soil Moisture ($m^{3}$/$m^{3}$ VWC)', size=8)
ax.tick_params(axis='x', labelsize=7) 
ax.tick_params(axis='y', labelsize=7)
ax.set_title('Mean VWC (m3/m3)', size=10)
ax.legend()
plt.show()

#-------------------------------  FIGURE 4   -------------------------------
fig4, ax = plt.subplots(figsize=(16,4))
soil1P['soil1P_mean_temp'].plot(color = 'orange', linewidth=0.5)
soil2P['soil2P_mean_temp'].plot(color = 'r', linewidth=0.5)
soil3P['soil3P_mean_temp'].plot(color = 'purple', linewidth=0.5)
soil4P['soil4P_mean_temp'].plot(color = 'blue', linewidth=0.5)
ax.set_xlim(['2019-05-15', '2020-01-01'])
ax.set_xlabel('Date/Time', size=8)
ax.set_ylabel('Mean Soil Temperature (deg C)', size=8)
ax.tick_params(axis='x', labelsize=7)
ax.tick_params(axis='x', labelsize=7) 
ax.tick_params(axis='y', labelsize=7)
ax.set_title('Mean Temperature (deg C)', size=10)
ax.legend()
plt.show()

#-------------------------------  FIGURE 5   -------------------------------
fig5, ax = plt.subplots()
soildata_means['soil1P_mean_moisture'].plot(color = 'orange', linewidth=0.5)
soildata_means['soil2P_mean_moisture'].plot(color = 'r', linewidth=0.5)
soildata_means['soil3P_mean_moisture'].plot(color = 'purple', linewidth=0.5)
soildata_means['soil4P_mean_moisture'].plot(color = 'blue', linewidth=0.5)
ax.set_xlim(['2019-05-15', '2020-01-01'])
ax.set_xlabel('Date/Time', size=8)
ax.set_ylabel('Mean Soil Temperature (deg C)', size=8)
ax.tick_params(axis='x', labelsize=7)
ax.tick_params(axis='x', labelsize=7) 
ax.tick_params(axis='y', labelsize=7)
plt.show()



#-------------------------------  UNUSED FIGURE   -------------------------------
#fig2, axes = plt.subplots(nrows=4,ncols=1,figsize=(12,6))
#soil1P['soil1P_mean_moisture'].plot(ax = axes[0], subplots=True, color = 'orange')
#soil2P['soil2P_mean_moisture'].plot(ax = axes[1], subplots=True, color = 'r')
#soil3P['soil3P_mean_moisture'].plot(ax = axes[2], subplots=True, color = 'purple')
#soil4P['soil4P_mean_moisture'].plot(ax = axes[3], subplots=True, color = 'blue')
#axes[1].set_xlim(['2019-05-15', '2020-01-01'])




