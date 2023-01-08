import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Shapefile path according to data level...only change if you want to add a shapefile
shape_files = {
    'assembly' : './shapefiles/TELANGANA_ASSEMBLY/TELANGANA_ASSEMBLY.shp',
    'sub_district_hq' : './shapefiles/TELANGANA_Sub_District_Hq/TELANGANA_Sub_District_Hq.shp',
    'sub_district' : './shapefiles/TELANGANA_SUBDISTRICTS/TELANGANA_SUBDISTRICTS.shp',
    'district_hq' : './shapefiles/TELANGANA_District_Hq/TELANGANA_District_Hq.shp',
    'district' : './shapefiles/TELANGANA_DISTRICTS/TELANGANA_DISTRICTS.shp',
    'parliament' : './shapefiles/TELANGANA_parliament/TELANGANA_parliament.shp',
    'state' : './shapefiles/TELANGANA_STATE/TELANGANA_STATE.shp'
}

shape_file_index_name = {
    'assembly' : 'AC_NAME',
    'sub_district_hq' : 'dtname',
    'sub_district' : 'sdtname',
    'district_hq' : 'DIST_HQ',
    'district' : 'dtname',
    'parliament' : 'PC_NAME',
    'state' : 'STNAME'
}

# Data file path
data_file = "./data/Industries_telangana_2015_2016.xlsx"

# Level of your data (assembly, sub_district_hq, sub_district, district_hq, district, parliament, state)
data_level = "district"

# Make sure your data file consists of a index column with name "place" and values according to the names given in shapefile for that level of data
# Put your data value column name here in this variable
data_value_column = "Employees"
data_index_column = "Districts"

# Title for the graph
graph_title = 'Overview of Industries and Investment for districtwise from Telangana open data portal'

if __name__=="__main__":
    df = pd.read_excel(data_file)
    shp_gdf = gpd.read_file(shape_files[data_level])
    merged = shp_gdf.set_index(shape_file_index_name[data_level]).join(df.set_index(data_index_column))

    # Adding label annotation
    merged['coords'] = merged['geometry'].apply(lambda x: x.representative_point().coords[:])
    merged['coords'] = [coords[0] for coords in merged['coords']]

    fig, ax = plt.subplots(1, figsize=(12, 12))
    ax.axis('off')
    ax.set_title(graph_title, fontdict={'fontsize': '15', 'fontweight' : '3'})
    fig = merged.plot(column=data_value_column, cmap='RdYlGn', linewidth=0.5, ax=ax, edgecolor='0.2',legend=True)

    for idx, row in merged.iterrows():
        plt.annotate(text=str(idx) + " \n " + str(row[data_value_column]), xy=row['coords'],
                 horizontalalignment='center')
    plt.show()