import xarray as xr
import matplotlib.pyplot as plt
import sys
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

fname = "data/LAI_mean_monthly_1981-2015.nc4"
ds = xr.open_dataset(fname)

# Subset by SE Aus
ds = ds.where((ds.lon >= 140) & (ds.lon <= 154) & \
              (ds.lat >= -40) & (ds.lat <= -28), drop=True)

lat = ds.lat.values
lon = ds.lon.values
bottom, top = lat[0], lat[-1] # Need to reverse these as the image is flipped
left, right = lon[0], lon[-1]

fig = plt.figure(figsize=(9,6))
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.sans-serif'] = "Helvetica"

ax = plt.axes(projection=ccrs.PlateCarree())

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.5,
                  color='black', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False
gl.xlines = False
gl.ylines = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
ax.coastlines(resolution='10m', linewidth=1.0, color='black')
ax.add_feature(cartopy.feature.OCEAN)
cmap = plt.cm.viridis
img = ax.imshow(ds.LAI[5,:,:], origin='lower', transform=ccrs.PlateCarree(),
                interpolation='nearest', cmap=cmap,
                extent=(left, right, bottom, top))
cbar = plt.colorbar(img, cmap=cmap,
                    orientation='vertical', shrink=0.9, pad=0.07)
cbar.ax.set_title("LAI (m$^{2}$ m$^{-2}$)", fontsize=12)

#ax.set_ylabel("Latitude")
#ax.set_xlabel("Longtiude")
ax.text(-0.10, 0.55, 'Latitude', va='bottom', ha='center',
        rotation='vertical', rotation_mode='anchor',
        transform=ax.transAxes, fontsize=14)
ax.text(0.5, -0.1, 'Longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes, fontsize=14)

fig.savefig("SE_AUS_GIMMS_LAI3g_ver2.png", dpi=150, bbox_inches='tight',
            pad_inches=0.1)
plt.show()
