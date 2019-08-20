# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 17:17:20 2019

@author: Ge
"""
import os
import csv
import math
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import squareform, pdist
from math import sin, cos, asin, sqrt, radians

#calculate spherical distance
def haversine(lonlat1, lonlat2):
    lat1, lon1 = lonlat1
    lat2, lon2 = lonlat2
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def clustering_by_dbscan(X, eps, minpts):
    distance_matrix = squareform(pdist(X, (lambda u, v: haversine(u, v))))

    db = DBSCAN(eps=eps, min_samples=minpts, metric='precomputed')
    y_db = db.fit_predict(distance_matrix)
    X['cluster'] = y_db
    labels = db.labels_
    raito = len(labels[labels[:] == -1]) / len(labels)
    print('eps  ' + str(eps) + '  minpts  ' + str(minpts) +
          "   噪声比为" + str(raito))
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    respath = '//Users/qpple/Desktop/Dissertation/flickrSpider/cluster/parameter/eps'\
              + str(eps) + 'minpts' + str(minpts)
    if not os.path.exists(respath):
        os.mkdir(respath)
    for i in range(n_clusters_):
        one_cluster = X[labels == i]
        one_cluster.to_csv(respath + '/class' + str(i) + '.csv',
                           encoding='utf-8')
    plt.scatter(X['lat'], X['lng'], c=X['cluster'])
    plt.savefig(respath + '/ result.png')
    plt.show()

csv_path = "//Users/qpple/Desktop/Dissertation/flickrSpider/cluster/del_newpicinfo_filter.csv"
reader = csv.reader(open(csv_path, 'r', encoding='utf-8'))
location = {}
lat = []
lng = []
for i, row in enumerate(reader):
    if i == 0:
        continue
    lat.append(float(row[5]))
    lng.append(float(row[6]))
location['lat'] = lat
location['lng'] = lng
eps = 0.2
minpts = 5
while not math.isclose(eps, 3.0):
    while minpts <= 30:
        clustering_by_dbscan(pd.DataFrame(location), round(eps, 1), minpts)
        minpts += 5
    minpts = 5
    eps += 0.2



