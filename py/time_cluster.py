import numpy as np
import pandas as pd
import geopandas as gp
from sklearn.cluster import KMeans
import shapely
from descartes import PolygonPatch


# -- load the data
data = pd.read_csv('/scratch/share/gdobler/parqa/output/Tables/'
                   'ParkQualityScores/QualityArea_ZipCode_FiscalYears.csv')

zips = gp.GeoDataFrame.from_file('/scratch/share/gdobler/parqa/output/'
                                 'ShapeData/ZIPCODE_Modified_Final.shp')

# -- prepare the data
cols  = ['F2{0:03}'.format(i) for i in range(4,16)]
vals  = data[cols].values
vals -=vals[:,np.newaxis].mean(-1)
vals /=vals[:,np.newaxis].std(-1)

# -- cluster
km = KMeans(n_clusters=5)
km.fit(vals)

# -- assign clusters to zips
zips['cluster'] = np.zeros(len(zips),dtype=int)-1
dzips = [i for i in data.ZIPCODE]

for ii in range(len(zips)):
    tzip = int(zips.ZIPCODE[ii])
    if tzip in dzips:
        zips['cluster'][ii] = km.labels_[dzips.index(tzip)]


# -- assign color
zips['color'] = np.zeros(len(zips),dtype=str)
for tcluster in range(km.n_clusters):
    print("tcluster = " + str(tcluster))
    zips['color'][zips['cluster']==tcluster] = 'red'
    zips['color'][zips['cluster']!=tcluster] = 'none'

    # -- plot
    close('all')
    yrs = range(2004,2016)
    fig, ax = plt.subplots(1,2,figsize=[10,5])
    fig.set_facecolor('white')
    ax[1].set_xlim([-74.26,-74.26+0.6])
    ax[1].set_ylim([40.4,40.4+0.6])
    ax[1].axis('off')
    for ii in range(len(zips)):
        geo = zips['geometry'][ii]
        tzip = zips.ZIPCODE[ii]
        if type(geo)==shapely.geometry.polygon.Polygon:
            ax[1].add_patch(PolygonPatch(geo,fc=zips['color'][ii],
                                         linewidth=0.2))

    ax[0].plot(yrs,vals[km.labels_==tcluster].T,color='k',lw=0.1)
    ax[0].plot(yrs,km.cluster_centers_[tcluster],color='indianred')
    ax[0].set_title('Cluster {0}'.format(tcluster))
    fig.canvas.draw()
    fig.savefig('../Outputs/cluster_{0}_{1}.png'.format(tcluster,
                                                        km.n_clusters),
                clobber=True)
