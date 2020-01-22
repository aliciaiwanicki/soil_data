import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt

# Columns soil2P_mean_moisture & soil2P_mean_temp no up to year 2056
# After pulling out the averaged columns from the orig df's (1P thru 4P), the new df (soil_mean) adds several sig figs to some of the values. Not sure if significant.
# The orig df's for 1P thru 4P have between 68160 and 68163 rows, but the soil_mean df has 66528 rows, even after I choose the date range i want
# Can't get empty cells to fill with NaN

soil_mean = pd.read_csv('soildata_means.csv',index_col = None, header = 0)
soil_mean.index = pd.to_datetime(soil_mean.DateTime)
soil_mean = soil_mean[(soil_mean.index > '2019-05-15') & (soil_mean.index <= '2020-1-1')]
soil_mean.replace(r'\s+',np.nan,regex=True)

soil_mean.to_csv('soil_mean_test.csv', index=True)

##soildata_means = soildata_means[['soil1P_mean_moisture', 'soil2P_mean_moisture', 'soil3P_mean_moisture', 'soil4P_mean_moisture']].astype(np.float64)
##soildata_means = soildata_means.astype(np.float64)
##soildata_means = soildata_means['soil1P_mean_moisture'].astype(float)

soil_mean['soil_moisture_mean'] = soil_mean[['soil1P_mean_moisture', 'soil2P_mean_moisture', 'soil3P_mean_moisture', 'soil4P_mean_moisture']].mean(axis=1)
soil_mean['soil_temp_mean'] = soil_mean['soil1P_mean_temp', 'soil2P_mean_temp', 'soil3P_mean_temp', 'soil4P_mean_temp'].mean(axis=1)

fig, ax = plt.subplots()
soil_mean['soil_temp_mean'].plot(color = 'blue')
plt.show()