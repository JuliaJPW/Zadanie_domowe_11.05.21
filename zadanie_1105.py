import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
gdf = gpd.read_file('PD_STAT_GRID_CELL_2011.shp')
gdf.plot("TOT", legend=True)

#podpunkt 2: układ
gdf.to_crs("EPSG:4326")

#podpunkt 3: wyznaczenie cendroid dla poligonów
gdf['centroid']=gdf.centroid

#podpunkt 4: wyznaczenie regularnej siatki fishnet
import shapely
xmin, ymin, xmax, ymax = [13, 48, 25, 56]

n_cells = 30
cell_size = (xmax-xmin)/n_cells

grid_cells = []
for x0 in np.arange(xmin, xmax+cell_size, cell_size):
    for y0 in np.arange(ymin, ymax+cell_size, cell_size):
        #bounds
        x1 = x0-cell_size
        y1 = y0+cell_size
        grid_cells.append(shapely.geometry.box(x0, y0, x1, y1))
cell = gpd.GeoDataFrame(grid_cells, columns=['geometry'])
ax = gdf.plot(markersize = 0.1, figsize=(12,8), column = "TOT", cmap="jet")

plt.autoscale(False)
cell.plot(ax=ax, facecolor = "none", edgecolor = 'grey')
ax.axis("off")
        
#podpunkt 6: spatial join     
merged = geopandas.sjoin(gdf, cell, how='left', op = 'within')

#podpunkt 7: agregacja
dissolve = merged.dissolve(by="index_right", aggfunc = "sum")

#podpunkt 8: przypisanie wartoci do oczek siatki
cell.loc[dissolve.index, 'TOT']=dissolve.TOT.values

#podpunkt 9: wizualizacja
ax = cell.plot(column='TOT', figsize=(12,8), cmap='viridis', vmax=700000, edgecolor="grey", legend=True)
plt.autoscale(False)
ax.set_axis_off()
plt.axis('equal');
plt.title('Liczba ludnosci na siatce')

#praca domowa
#Wyznacz liczbę ludności w siatce dla:
#a) Przedziału wiekowego 0-14
#b) Przedziału wiekowego 15-64
#c) Przedziału wiekowego >65
#d) Ludności męskiej w przedziałach wiekowych z podpunktów a-c
#e) Ludności żeńskiej w przedziałach wiekowych z podpunktów a-c
#f) Ratio liczby ludności do powierzchni dla danego województwa































