import pandas as pd
import geopandas as gpd
import contextily as cx
from setup_file_data import setup_data

pd.set_option('display.max_rows', 700)
pd.set_option('display.max_columns', 100)

# visualize all plants that are operational in east germany
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

opdf

grouped = opdf.groupby(["federal_state"], as_index=False)
fed_state = grouped["number_of_solar_modules"].sum()

fed_state.plot(kind='bar', title='Total number of PV units by state', ylabel='Total number of PV units(log scale)',
               xlabel='State', figsize=(10, 10), logy=True, color='darkorange')
