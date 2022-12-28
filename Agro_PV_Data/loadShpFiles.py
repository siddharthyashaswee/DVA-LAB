import pandas as pd
import numpy as np
import geopandas as gpd
import contextily as cx
import matplotlib as plt
from setup_file_data import setup_data
from setup_file_data import select_operational_units

pd.set_option('display.max_rows', 700)
pd.set_option('display.max_columns', 100)

# visualize all plants that are operational in east germany
# set file path as relative path(if doesn't work then use raw string)
path = "./data/Stromerzeuger_east_data.csv"
path = r'D:\Main\RWTH Study\Data Analytics and Visualization Lab\pycharm_projects\DVA-LAB\Agro_PV_Data\data\Stromerzeuger_east_data.csv'
delimiter = ";"
df = setup_data(path, delimiter)
df.dtypes
# find out all categories of operational status
df['operational_status'].unique()
# reults translation:
# 'In operation', 'In planning', 'Finally decommissioned','Temporarily suspended'

# selecting only operational PV
opdf = df[df['operational_status'] == 'In Betrieb']
opdf.isnull().sum()
# filter out latitudes and longitudes which are not NaN
latdf = opdf[opdf['latitude'].notnull()]
latdf = opdf[opdf['longitude'].notnull()]
# check once
latdf.isnull().sum()
# make your own custom geopandas data frame using these GPS coordinates
visdf = gpd.GeoDataFrame(latdf, geometry=gpd.points_from_xy(latdf.longitude, latdf.latitude, crs="epsg:4326"))

# load the shape file
path = r'D:\Main\RWTH Study\Data Analytics and Visualization Lab\pycharm_projects\DVA-LAB\Agro_PV_Data\data\DEU_adm\DEU_adm1.shp'
germany = gpd.read_file(path)
germany.crs
germany.plot(figsize=(20, 20))

# filter out your states
east_germany_state_names = ['Berlin', 'Brandenburg', 'Sachsen', 'Sachsen-Anhalt']
east_germany = germany.loc[germany['NAME_1'].isin(east_germany_state_names)]
east_germany.plot(figsize=(20, 20))

# colors for individual states
state_colors = {'Berlin': 'lightcoral', 'Brandenburg': 'lightblue', 'Sachsen-Anhalt': 'khaki', 'Sachsen': 'plum'}
colormap = plt.colors.ListedColormap([state_colors[b] for b in east_germany.NAME_1.unique()])

# base map
ax = east_germany.plot(cmap=colormap, figsize=(20, 20))

# all pv units
visdf.plot(ax=ax, marker='d', color='black', markersize=6)

###############################################################################
# comparison where the gross power of the unit is less than installed capacity
###############################################################################
icvGp = setup_data()
# how many null values
icvGp.isnull().sum()  # installed_capacity 54
icvGp = select_operational_units(icvGp)
icvGp.isnull().sum()  # installed_capacity 0
#no null values for installed_capacity where the units are operational
icvGp.dtypes
icvGp.shape[0]


# filter out NaN installation capacity - no need
#icvGp.dropna(subset=['installed_capacity'])

#how many units work on less than installation capacity?
icvGp[icvGp['gross_power_of_the_unit'] < icvGp['installed_capacity']].shape[0]
icvGp[icvGp['gross_power_of_the_unit'] == icvGp['installed_capacity']].shape[0]
icvGp[icvGp['gross_power_of_the_unit'] > icvGp['installed_capacity']].shape[0]

icvGp['absolute'] = (icvGp['installed_capacity'] - icvGp['gross_power_of_the_unit'])
icvGpBehind=icvGp[icvGp['gross_power_of_the_unit'] < icvGp['installed_capacity']]
icvGpBehind
icvGpBehind['percentage_behind_target'] = (icvGpBehind['installed_capacity'] - icvGpBehind['gross_power_of_the_unit']) / icvGpBehind['installed_capacity']

plt.pyplot.hist(icvGpBehind[['percentage_behind_target']])

icvGpBehind[icvGpBehind['percentage_behind_target'] > 0.85].shape[0]
icvGpBehind.sort_values('percentage_behind_target', ascending=False)

###############################################################################
# comparison where the net power of the unit is less than gross power
###############################################################################
diffIcvGp = pd.DataFrame()
diffIcvGp['absolute'] = (icvGp['installed_capacity'] - icvGp['gross_power_of_the_unit'])
diffIcvGp['per_unit'] = (icvGp['installed_capacity'] - icvGp['gross_power_of_the_unit']) / icvGp['number_of_solar_modules']
diffIcvGp['no_of_modules'] = icvGp['number_of_solar_modules']
diffIcvGp.sort_values('absolute', ascending=False)
diffIcvGp.sort_values('per_unit')

icvGp['percentage_behind_target'] = (icvGp['installed_capacity'] - icvGp['gross_power_of_the_unit']) / icvGp['installed_capacity']
icvGp[['percentage_behind_target']]
icvGp.sort_values('percentage_behind_target', ascending=False)

# filter out 0% lackings first
icvGp[icvGp['percentage_behind_target'] != 0.0]
icvGp = icvGp[icvGp['percentage_behind_target'] != 0]

plt.pyplot.hist(icvGp[['percentage_behind_target']])

diffIcvGp.shape[0]

gpltnpdf = gpd.GeoDataFrame(icvGp, geometry=gpd.points_from_xy(icvGp.longitude, icvGp.latitude, crs="epsg:4326"))

# base map
ax = east_germany.plot(cmap=colormap, figsize=(20, 20))
gpltnpdf.plot(ax=ax, marker='d', color='teal', markersize=6)

# most percentage of lost power
gpminusnp = setup_data(path, delimiter)
gpminusnp.isnull().sum()

gpminusnp['percentage_lost'] = (gpminusnp['gross_power_of_the_unit'] - gpminusnp['net_power_rating_of_the_unit']) / \
                               gpminusnp['gross_power_of_the_unit']
gpminusnp[['percentage_lost']]
plt.pyplot.hist(gpminusnp[['percentage_lost']])
gpminusnp[gpminusnp['percentage_lost'] > 0.3].shape[0]

# base map
ax = east_germany.plot(cmap=colormap, figsize=(20, 20))
highest_loss = gpminusnp[gpminusnp['percentage_lost'] > 0.3]
lossdf = gpd.GeoDataFrame(highest_loss,
                          geometry=gpd.points_from_xy(highest_loss.longitude, highest_loss.latitude, crs="epsg:4326"))
lossdf.shape[0]
lossdf.plot(ax=ax, marker='d', color='black', markersize=6)

# does one state have all these high losses?
total_high_loss_by_state = lossdf.groupby(['federal_state'])
total_high_loss_by_state.sort_values(ascending=False)

total_high_loss_by_state.plot(kind='bar', title='Total number of PV units by state',
                              ylabel='Total number of PV units(log scale)', xlabel='State', figsize=(10, 10), logy=True,
                              color='darkorange')
