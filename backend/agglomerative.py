# import base64
# import io
# import sys
# import json
# import os
# import warnings
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from sklearn.cluster import AgglomerativeClustering
# from sklearn.metrics import silhouette_score
# from scipy.cluster.hierarchy import linkage, dendrogram

# warnings.filterwarnings('ignore')

# try:
#     # -----------------------------
#     # 1. Λήψη παραμέτρων
#     # -----------------------------
#     dataset_id = sys.argv[1]
#     k_input = int(sys.argv[2])

#     file_mapping = {
#         '1': 'dataset1.from2013.csv',
#         '2': 'dataset2.from2019.csv',
#         '3': 'dataset3.difsfrom2013.csv',
#         '4': 'dataset4.difsfrom2019.csv'
#     }

#     if dataset_id not in file_mapping:
#         raise ValueError("Μη έγκυρο Dataset ID")

#     # -----------------------------
#     # 2. Φόρτωση dataset
#     # -----------------------------
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(base_dir, 'datasets', file_mapping[dataset_id])

#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Το αρχείο {file_mapping[dataset_id]} δεν βρέθηκε!")

#     df = pd.read_csv(file_path)

#     # -----------------------------
#     # 3. Επιλογή features
#     # -----------------------------
#     if dataset_id in ['1', '2']:
#         feature_cols = [c for c in df.columns if c.startswith('base_')]
#     else:
#         feature_cols = [c for c in df.columns if c.startswith('diff_')]

#     df = df.dropna(subset=feature_cols).fillna(0)
#     data_for_clustering = df[feature_cols].copy()

#     # -----------------------------
#     # 4. Αυτόματος υπολογισμός k
#     # -----------------------------
#     if k_input == 0:
#         best_k = 3
#         best_score = -1
#         for i in range(2, 9):
#             test_model = AgglomerativeClustering(n_clusters=i)
#             labels = test_model.fit_predict(data_for_clustering)
#             score = silhouette_score(data_for_clustering, labels)
#             if score > best_score:
#                 best_score = score
#                 best_k = i
#         final_k = best_k
#     else:
#         final_k = k_input

#     # -----------------------------
#     # 5. Τελικό Agglomerative
#     # -----------------------------
#     model = AgglomerativeClustering(n_clusters=final_k, linkage='ward')
#     df['Cluster'] = model.fit_predict(data_for_clustering).astype(str)

#     # -----------------------------
#     # 6. Στατιστικά για JS
#     # -----------------------------
#     field_analysis = pd.crosstab(df['Cluster'], df['field']).fillna(0).to_dict(orient='index')
#     pref_analysis = pd.crosstab(df['Cluster'], df['avg_pref_success']).fillna(0).to_dict(orient='index')

#     # -----------------------------
#     # 7. Dendrogram (base64)
#     # -----------------------------
#     plt.figure(figsize=(10, 5))
#     Z = linkage(data_for_clustering, method='ward')
#     dendrogram(Z, link_color_func=lambda k: 'lightblue')
#     plt.title("Dendrogram – Agglomerative Clustering")
#     plt.tight_layout()

#     buf1 = io.BytesIO()
#     plt.savefig(buf1, format='png')
#     plt.close()
#     dendrogram_b64 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    


#     # -----------------------------
#     # 8. Heatmap (base64)
#     # -----------------------------
#     plt.figure(figsize=(8, 6))
#     sns.heatmap(data_for_clustering, cmap='viridis')
#     plt.tight_layout()

#     buf2 = io.BytesIO()
#     plt.savefig(buf2, format='png')
#     plt.close()
#     heatmap_b64 = base64.b64encode(buf2.getvalue()).decode('utf-8')

#     # -----------------------------
#     # 9. ΤΕΛΙΚΟ JSON (ΜΟΝΟ ΕΝΑ!)
#     # -----------------------------
#     response = {
#         "status": "success",
#         "k": final_k,
#         "dataset": dataset_id,
#         "algorithm": "agglomerative",
#         "field_distribution": field_analysis,
#         "preference_distribution": pref_analysis,
#         "dendrogram": "data:image/png;base64," + dendrogram_b64,
#         "heatmap": "data:image/png;base64," + heatmap_b64
#     }

#     print(json.dumps(response))

# except Exception as e:
#     print(json.dumps({"status": "error", "message": str(e)}))








import sys
import json
import os
import warnings
import pandas as pd
import io
import base64


import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.decomposition import PCA 

warnings.filterwarnings('ignore')


def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')

try:
    # 1. Λήψη παραμέτρων 
    dataset_id = sys.argv[1]
    k_input = int(sys.argv[2])
    linkage_method = sys.argv[3] if len(sys.argv) > 3 else 'ward' 
    file_mapping = {
        '1': 'dataset1.from2013.csv',
        '2': 'dataset2.from2019.csv',
        '3': 'dataset3.difsfrom2013.csv',
        '4': 'dataset4.difsfrom2019.csv'
    }

    if dataset_id not in file_mapping:
        raise ValueError("Μη έγκυρο Dataset ID")

  
    # 2. Φόρτωση dataset
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '../datasets', file_mapping[dataset_id])

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Το αρχείο {file_mapping[dataset_id]} δεν βρέθηκε!")

    df = pd.read_csv(file_path)

    # 3. Επιλογή features

    if dataset_id in ['1', '2']:
        feature_cols = [c for c in df.columns if c.startswith('base_')]
    else:
        feature_cols = [c for c in df.columns if c.startswith('diff_')]

    df = df.dropna(subset=feature_cols).fillna(0)
    data_for_clustering = df[feature_cols].copy()

    # 4. Αυτόματος υπολογισμός k

    if k_input == 0:
        best_k = 3
        best_score = -1
        for i in range(2, 9):
            test_model = AgglomerativeClustering(n_clusters=i)
            labels = test_model.fit_predict(data_for_clustering)
            score = silhouette_score(data_for_clustering, labels)
            if score > best_score:
                best_score = score
                best_k = i
        final_k = best_k
    else:
        final_k = k_input

    # 5. Τελικό Agglomerative

    model = AgglomerativeClustering(n_clusters=final_k, linkage=linkage_method)
    df['Cluster'] = model.fit_predict(data_for_clustering).astype(str)

    labels = model.fit_predict(data_for_clustering)
    sil_score = float(silhouette_score(data_for_clustering, labels)) 
   
    sse_value = 0.0
    for i in range(final_k):
        cluster_data = data_for_clustering[labels == i]
        if len(cluster_data) > 0:
            centroid = cluster_data.mean(axis=0) 
            sse_value += ((cluster_data - centroid) ** 2).sum().sum() 
    sse_value = float(sse_value)

    # 6. Στατιστικά για JS
  
  
    field_analysis = pd.crosstab(df['Cluster'], df['field']).fillna(0).to_dict(orient='index') if 'field' in df.columns else {}
    pref_analysis = pd.crosstab(df['Cluster'], df['avg_pref_success']).fillna(0).to_dict(orient='index') if 'avg_pref_success' in df.columns else {}


    # ΠΑΡΑΓΩΓΗ ΓΡΑΦΗΜΑΤΩΝ 

    
  
    sample_size = min(1000, len(df))
    df_sample = df.sample(n=sample_size, random_state=42) if len(df) > 1000 else df

    # Α) PARALLEL COORDINATES
    fig_parallel = plt.figure(figsize=(12, 6))
    cols_to_plot = feature_cols + ['Cluster']
    pd.plotting.parallel_coordinates(df_sample[cols_to_plot], 'Cluster', colormap='Set1', alpha=0.5)
    plt.xticks(rotation=45)
    parallel_b64 = fig_to_base64(fig_parallel)

    # Β) PCA (2D)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data_for_clustering)
    
    fig_pca = plt.figure(figsize=(8, 6))
    plt.scatter(pca_result[:, 0], pca_result[:, 1], c=model.labels_, cmap='Set1', s=30, alpha=0.7, edgecolor='k')

    plt.xlabel(f"Συνιστώσα 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    plt.ylabel(f"Συνιστώσα 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    pca_b64 = fig_to_base64(fig_pca)

    # Γ) DENDROGRAM
    fig_dendro = plt.figure(figsize=(10, 5))
    Z = linkage(data_for_clustering, method=linkage_method)
    dendrogram(Z, link_color_func=lambda k: 'lightblue')
    plt.title("Dendrogram – Agglomerative Clustering")
    dendrogram_b64 = fig_to_base64(fig_dendro)

    # Δ) HEATMAP Συσχετίσεων
    fig_heatmap = plt.figure(figsize=(10, 8))
    corr_matrix = data_for_clustering.corr()
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0)
    heatmap_b64 = fig_to_base64(fig_heatmap)



    # 9. ΤΕΛΙΚΟ JSON 

    response = {
        "status": "success",
        "k": final_k,
        "dataset": dataset_id,
        "algorithm": "agglomerative",
        "field_distribution": field_analysis,
        "preference_distribution": pref_analysis,
        "parallel_coords": parallel_b64, 
        "pca": pca_b64,                  
        "dendrogram": dendrogram_b64,
        "heatmap": heatmap_b64,
        "sse": sse_value,
        "silhouette": sil_score
    }

    print(json.dumps(response))

except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}))