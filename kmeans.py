import numpy as np
import pandas as pd
import random
class kmeans:
    
    def haversine_dist(p1 = None, p2 = None):
        lon1 = p1[0]
        lon2 = p2[0]
        lat1 = p1[1]
        lat2 = p2[1]
        pi = np.pi
        R = 6371000 #earth radius in meters
        phi1 = lat1 * pi / 180 #convert to radian
        phi2 = lat2 * pi / 180 #convert to radian
        delta_phi = (lat2 - lat1) * pi / 180
        delta_lambda = (lon2 - lon1) * pi / 180

        a = (np.sin(delta_phi/2))**2 + np.cos(phi1) * np.cos(phi2) * ((np.sin(delta_lambda/2))**2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

        distance = R * c #haversine distance between point1 and point 2 in meters
        return(round(distance, 2))
    
    def sample(ar, n):
        #np.random.seed(1)
        random_sample = np.random.choice(ar,replace = False, size = n)
        return(random_sample)

    def centroids(coords, weights, cluster, K):
        ret = []
        for k in range(K):
            indexes= np.where(cluster == k)
            ret.append(np.average(coords[indexes], weights = weights[indexes], axis = 0))
        return ret


    def k_means(K, df_city):
        counter = 0
        num_cities = len(df_city)
        np_coord = np.array([df_city['longitude'], df_city['latitude']]).transpose()
        np_weights = np.array(df_city['population'])
        init_centroids_index =  random.sample(range(len(np_coord)), K) #kmeans.sample(np_coord,K)
        distance_matrix = np.array([[np.nan]*K]*num_cities)
        cluster = np.array([np.nan]*num_cities)
        centroid_long = np.array([np.nan]*K)
        centroid_lat = np.array([np.nan]*K)
        for k in range(0, K):
            for i in range(0, num_cities):
                city_i = np_coord[i].astype(int)
                centroid_k = np_coord[init_centroids_index[k]]
                distance_matrix[i][k] = kmeans.haversine_dist(city_i,centroid_k)
        for i in range(0, num_cities):
            cluster[i] = np.argmin(distance_matrix[i])
        

        #iter
        old_cluster = np.array([np.nan]*len(cluster))
        new_cluster = np.copy(cluster)
        max = 100
        while not np.array_equal(old_cluster, new_cluster, equal_nan = False) and max > 0:
            old_cluster = np.copy(new_cluster)
            for k in range(0, K):
   
                cluster_k = np.where(old_cluster == k) #city index of cluster k
                centroid_long[k], centroid_lat[k] = np.average(np_coord[cluster_k], weights = np_weights[cluster_k], axis = 0)
              
            
            for k in range(0, K):
                for i in range(0, num_cities):
                    city_i = np_coord[i]
                    centroid_k = np.array([centroid_long[k], centroid_lat[k]])
                    distance_matrix[i][k] = kmeans.haversine_dist(city_i,centroid_k)
            
            for i in range(0, num_cities):
                cluster[i] = np.argmin(distance_matrix[i])
            new_cluster = np.copy(cluster)
            max-=1
        return kmeans.centroids(np_coord, np_weights, cluster, K), np_coord


    def run_kmeans(K, df):
        while True:
            try:
                data = kmeans.k_means(K, df)
                return data
            except Exception as e:
                pass
