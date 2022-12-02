import pandas as pd
import geopandas as gpd
import contextily as cx
from setup_file_data import setup_data

pd.set_option('display.max_rows', 700)
pd.set_option('display.max_columns', 100)

#visualize all plants that are operational in east germany
# set file path as relative path(if doesn't work then use raw string)
path = "./data/Stromerzeuger_east_data.csv"
path = r'D:\Main\RWTH Study\Data Analytics and Visualization Lab\pycharm_projects\DVA-LAB\Agro_PV_Data\data\Stromerzeuger_east_data.csv'
delimiter = ";"
df = setup_data(path, delimiter)
df
# find out all categories of operational status
df['operational_status'].unique()
# reults translation:
# 'In operation', 'In planning', 'Finally decommissioned','Temporarily suspended'

# selecting only operational PV
opdf = df[df['operational_status'] == 'In Betrieb']
# filter out latitudes and longitudes which are not NaN
latdf = opdf[opdf['latitude'].notnull()]
latdf = opdf[opdf['longitude'].notnull()]
#check once
latdf.isnull().sum()

# make your own custom geopandas data frame using these GPS coordinates
visdf = gpd.GeoDataFrame(latdf, geometry=gpd.points_from_xy(latdf.longitude, latdf.latitude, crs="epsg:4326"))
# check the crs which is now GPS based
visdf.crs
# if you want to overlay these points onto the actual map of Germany
# then first convert the coordinate reference system(crs) from GPS to epsg=3857
gdf = visdf.to_crs(epsg=3857)
# plot only the points first
ax = gdf.plot()
# then overlay the map using the epsg=3857 crs
cx.add_basemap(ax)
