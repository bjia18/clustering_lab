import clusters as clus
func=clus.pearson
best_k=7

import matplotlib.pyplot as plt
import numpy as np
import bisect_k
import hierarchical
import word_cloud
from sse_and_centroid import*

def read_file():
    d_range=range(2,8)
    data=[]
    countries=[]
    file=open('processed_data.csv')
    for i in file:
        j=i.strip('\n').split(',')
        countries.append([j[0], j[1]])
        data.append([int(j[m]) for m in d_range])

    file.close()
    return data, countries

def elbow_method(data):
    # Data for plotting
    max_range=range(1,25)
    x_k=[]
    y_sse=[]
    for i in max_range:
        raw_clusters = clus.kcluster(data, distance=func, k=i)
        clusters=eliminate(raw_clusters)
        x_k.append(i)
        y_sse.append(sse(clusters, data))

    fig, ax = plt.subplots()
    ax.plot(x_k, y_sse)

    ax.set(xlabel='k', ylabel='sse',title='elbow chart')
    fig.savefig("test.png")
    plt.show()

def test_metrics(data):
    sse_metrics=[]
    metrics=['manhattan','euclidean','cosine','pearson','tanimoto']
    clusters=eliminate(clus.kcluster(data, distance=clus.manhattan, k=best_k))
    sse_metrics.append(sse(clusters, data))
    clusters=eliminate(clus.kcluster(data, distance=clus.euclidean, k=best_k))
    sse_metrics.append(sse(clusters, data))
    clusters=eliminate(clus.kcluster(data, distance=clus.cosine, k=best_k))
    sse_metrics.append(sse(clusters, data))
    clusters=eliminate(clus.kcluster(data, distance=clus.pearson, k=best_k))
    sse_metrics.append(sse(clusters, data))
    clusters=eliminate(clus.kcluster(data, distance=clus.tanimoto, k=best_k))
    sse_metrics.append(sse(clusters, data))
    
    fig, ax = plt.subplots()
    ax.plot(metrics, sse_metrics)

    ax.set(xlabel='metrics', ylabel='sse',title='measure distance metrics')
    fig.savefig("metrics.png")
    plt.show()

def eliminate(raw_clusters):
    clusters=[]
    for i in range(len(raw_clusters)):
        if len(raw_clusters[i]) != 0:
            clusters.append(raw_clusters[i])
    return clusters

def b_k(data, countries):
    raw_clusters = bisect_k.bisect([list(range(len(data)))], data, distance=clus.pearson, k=7)
    clusters = []
    for i in range(best_k):
        if len(raw_clusters[i]) == 0:
            continue
        clusters.append(raw_clusters[i])
        print('cluster {}:'.format(i + 1))
        print([countries[r] for r in clusters[i]])

    print("sse: " + str(sse(clusters, data)))

def main():
    data, countries=read_file()
    #elbow_method(data)
    #test_metrics(data)
    #b_k(data, countries)
    #hierarchical.hier(data,countries)
    final_clusters = []
    final_country_clusters = []
    best_sse=5
    for j in range(1001):
        raw_clusters = clus.kcluster(data, distance=func, k=best_k)
        clusters=[]
        country_clusters=[]
        for i in range(best_k):
            if len(raw_clusters[i]) == 0:
                continue
            clusters.append(raw_clusters[i])
            #print('cluster {}:'.format(i + 1))
            #print([countries[j] for j in raw_clusters[i]])
            country_clusters.append([countries[j][1] for j in raw_clusters[i]])
        temp_sse=sse(clusters, data)
        print('process: '+str(j))
        if temp_sse<best_sse:
            best_sse=temp_sse
            final_clusters=clusters
            final_country_clusters=country_clusters
    print('best sse: '+str(best_sse)) 
    file = open('cluster_results.json', "w")
    for i in range(len(final_country_clusters)):
        c = final_country_clusters[i]
        for country in c:
            file.write("['" + country + "', " + str(i) + "],\n")
    file.close()
    word_cloud.cloud(final_clusters, data)

if __name__ == "__main__":
    main()
