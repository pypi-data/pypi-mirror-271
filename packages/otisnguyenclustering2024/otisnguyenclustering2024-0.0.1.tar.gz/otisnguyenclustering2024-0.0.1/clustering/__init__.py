from sklearn.cluster import KMeans, DBSCAN, MeanShift, AgglomerativeClustering, SpectralClustering, Birch, OPTICS
from yellowbrick.cluster import KElbowVisualizer #calculate n_clusters
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.decomposition import PCA

def find_max_min_with_key(d, max_or_min):
    max_key = None
    max_value = max_or_min(d.values())
    for key, value in d.items():
        if value == max_value:  # Only check for equality with max_value
            max_key = key
    return max_key, max_value    

def all_cluster_labels(clean_csv,k_number):
    clustering_algorithms = {
        'KMeans': KMeans(n_clusters= k_number, random_state=42),  # Adjust n_clusters as needed
        'MeanShift': MeanShift(bandwidth=0.5),  # Adjust bandwidth as needed
        'Spectral Clustering': SpectralClustering(n_clusters= k_number, random_state=42),  # Adjust n_clusters as needed
        'Hierarchical Clustering (Ward)': AgglomerativeClustering(n_clusters= k_number, linkage='ward'),  # Adjust n_clusters as needed
        'OPTICS': OPTICS(min_samples=10),  # Adjust min_samples as needed
        'BIRCH': Birch(n_clusters = k_number),  # Adjust n_clusters as needed
    }
    cluster_labels = {}
    # # Perform clustering and store labels
    for model_name, model in clustering_algorithms.items():
        model.fit(clean_csv)
        labels = model.labels_
        # Ensure there are more than one label and less than the number of samples
        if 1 < len(set(labels)) < len(clean_csv):
            cluster_labels[model_name] = labels
    return cluster_labels

def find_most_frequent_string(data):
  # Tạo từ điển để lưu trữ số lần xuất hiện
  counts = Counter(data)
  most_frequent_string = counts.most_common(1)[0][0]
  return most_frequent_string

# def best_algorithms(clean_csv,k_number):
#     result =[]
#     cluster_labels = all_cluster_labels(clean_csv,k_number)
#     print("===========================")
#     #SILHOUETTE 
#     silhouette_scores = {}
#     for model_name, labels in cluster_labels.items():
#         # Calculate silhouette scores only if there are valid labels
#         if labels is not None and len(set(labels)) > 1:
#             silhouette_scores[model_name] = silhouette_score(clean_csv, labels)
        
#     # Print silhouette scores
#     max_silhouette, max_value = find_max_min_with_key(silhouette_scores, max)
#     print(f"The best algorithms with silhouette is : {max_silhouette} ({max_value})")
#     result.append(max_silhouette)

#     #CALINSHI HARABASZ
#     calinski_harabasz_scores = {}
#     for model_name, labels in cluster_labels.items():
#         # Calculate silhouette scores only if there are valid labels
#         if labels is not None and len(set(labels)) > 1:
#             calinski_harabasz_scores[model_name] = calinski_harabasz_score(clean_csv, labels)

#     # Print calinski_harabasz_score
#     max_calinski_harabasz, max_value = find_max_min_with_key(calinski_harabasz_scores, max)
#     print(f"The best algorithms with Calinski Harabasz is : {max_calinski_harabasz} ({max_value})")
#     result.append(max_calinski_harabasz)
#     #DAVIES BOULDIN 
#     davies_bouldin_scores = {}
#     for model_name, labels in cluster_labels.items():
#         # Calculate silhouette scores only if there are valid labels
#         if labels is not None and len(set(labels)) > 1:
#             davies_bouldin_scores[model_name] = davies_bouldin_score(clean_csv, labels)

#     # Print davies_bouldin_scores
#     min_calinski_harabasz, min_value =  find_max_min_with_key(davies_bouldin_scores, min)
#     print(f"The best algorithms with Davies Bouldin is: {min_calinski_harabasz} ({min_value})")
#     print("===========================")
#     result.append(min_calinski_harabasz)

#     best = find_most_frequent_string(result)
#     print("We highly recommend the best algorithms is:", best )
#     return best

def get_cluster_labels(model_name, data, k_number):
    clustering_algorithms = {
            'KMeans': KMeans(n_clusters= k_number, random_state=42),  # Adjust n_clusters as needed
            'MeanShift': MeanShift(bandwidth=0.5),  # Adjust bandwidth as needed
            'Spectral Clustering': SpectralClustering(n_clusters= k_number, random_state=42),  # Adjust n_clusters as needed
            'Hierarchical Clustering (Ward)': AgglomerativeClustering(n_clusters= k_number, linkage='ward'),  # Adjust n_clusters as needed
            'OPTICS': OPTICS(min_samples=10),  # Adjust min_samples as needed
            'BIRCH': Birch(n_clusters = k_number),  # Adjust n_clusters as needed
        }
    if model_name not in clustering_algorithms:
        raise ValueError(f"Unsupported model name: {model_name}")

    model = clustering_algorithms[model_name]
    model.fit(data)
    labels = model.labels_
    return labels

def cal_parameters_n_clusters(data):
      # Khởi tạo KMeans và KElbowVisualizer
    kmeans = KMeans(random_state=0)
    visualizer = KElbowVisualizer(kmeans, k=(2, 10))  # Chỉ số k từ 2 đến 10
    visualizer.fit(data)
    # visualizer.show()
    
    # Lấy giá trị k tối ưu từ elbow_value_
    optimal_k = visualizer.elbow_value_
    return optimal_k



def evaluate_clustering_algorithms(data):
    optimal_n_clusters = cal_parameters_n_clusters(data)
 
    algorithms = {
        "KMeans": KMeans(n_clusters=optimal_n_clusters),
        "AgglomerativeClustering": AgglomerativeClustering(n_clusters=optimal_n_clusters, linkage='ward'),
        "SpectralClustering": SpectralClustering(n_clusters=optimal_n_clusters),
        # "BIRCH": Birch(n_clusters=optimal_n_clusters),
        "OPTICS": OPTICS(min_samples=10)
    }

    scores = {}
    for alg_name, algorithm in algorithms.items():
        algorithm.fit(data)
        labels = algorithm.labels_

        # Kiểm tra số nhãn trước khi tính toán
        unique_labels = np.unique(labels)
        if len(unique_labels) < 2:
            print(f"Ignoring algorithm {alg_name} due to insufficient clusters.")
            continue

        silhouette = silhouette_score(data, labels)
        calinski_harabasz = calinski_harabasz_score(data, labels)
        davies_bouldin = davies_bouldin_score(data, labels)

        scores[alg_name] = {
            "silhouette": silhouette,
            "calinski_harabasz": calinski_harabasz,
            "davies_bouldin": davies_bouldin
        }
    
    # In ra các chỉ số đánh giá
    for alg_name, scores_dict in scores.items():
        print(f"Thuật toán: {alg_name}")
        print(f"Silhouette Score: {scores_dict['silhouette']}")
        print(f"Calinski Harabasz Score: {scores_dict['calinski_harabasz']}")
        print(f"Davies Bouldin Score: {scores_dict['davies_bouldin']}")
        print("--------------------------")

    if not scores:
        print("Không có thuật toán nào phù hợp.")
        return None

    # Chọn thuật toán dựa trên các tiêu chí
    best_algorithm = max(scores, key=lambda k: (
        scores[k]["silhouette"],
        scores[k]["calinski_harabasz"],
        -scores[k]["davies_bouldin"]
    ))
    
    return best_algorithm

def clustering(RFM):
    optimal_n_clusters = cal_parameters_n_clusters(RFM)
    # Evaluate clustering algorithms to get the best algorithm
    best_algorithm = evaluate_clustering_algorithms(RFM)

    if best_algorithm == "KMeans":
        print("using kmeans")
        clustering_algorithm = KMeans(n_clusters=optimal_n_clusters)
    elif best_algorithm == "AgglomerativeClustering":
        print("using AgglomerativeClustering")
        clustering_algorithm = AgglomerativeClustering(n_clusters=optimal_n_clusters, linkage='ward')
    elif best_algorithm == "SpectralClustering":
        print("using SpectralClustering")
        clustering_algorithm = SpectralClustering(n_clusters=optimal_n_clusters)
    elif best_algorithm == "OPTICS":
        print("using OPTICS")
        clustering_algorithm = OPTICS(min_samples=50)
    else:
        print("using kmeans as default")
        clustering_algorithm = KMeans(n_clusters=optimal_n_clusters)

    clustering_algorithm.fit(RFM)
    RFM['Clusters'] = clustering_algorithm.labels_

    return RFM