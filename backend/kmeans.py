# import sys
# import json
# import pandas as pd
# from sklearn.cluster import KMeans
# from sqlalchemy import create_engine
# import warnings

# # Αγνοούμε τα warnings για να έχουμε καθαρό JSON output
# warnings.filterwarnings('ignore') 

# try:
#     # 1. Παράμετροι από την PHP
#     dataset_id = sys.argv[1]
#     k_clusters = int(sys.argv[2])

#     # 2. Σύνδεση με τη Βάση (Βάλε τον κωδικό σου αν υπάρχει, π.χ. root:password)
#     engine = create_engine("mysql+pymysql://root:Mysqlgiannis7@localhost/schema")

#     # 3. Επιλογή Query ανάλογα με το Dataset
#     if dataset_id == '1':
#         feature_cols = ['base_2013', 'base_2014', 'base_2015', 'base_2016', 'base_2017', 'base_2018', 'base_2019', 'base_2020', 'base_2021', 'base_2022', 'base_2023', 'base_2024', 'base_2025']
#         query = """
#         SELECT b.code, MAX(b.field) AS field, u.title AS university,
#         (SELECT ROUND(SUM(s.protimisi * s.plithos) / NULLIF(SUM(s.plithos), 0)) FROM statistics s WHERE s.code = b.code AND s.category = 1) AS avg_pref_success,
#         MAX(CASE WHEN b.year = 2013 AND b.cat_title LIKE '90%% ΓΕΝΙΚΗ%%ΣΕΙΡΑ%%' THEN b.vasitel END) AS base_2013, MAX(CASE WHEN b.year = 2014 AND b.cat_title = '90%% ΓΕΛ/ΕΠΑΛΒ ΓΕΝ.ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2014, MAX(CASE WHEN b.year = 2015 AND b.cat_title = '90%% ΓΕΛ/ΕΠΑΛΒ ΓΕΝ.ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2015, MAX(CASE WHEN b.year = 2016 AND b.cat_title = 'ΓΕΛ ΓΕΝ.ΣΕΙΡΑ ΗΜ. (ΝΕΟ)' THEN b.vasitel END) AS base_2016, MAX(CASE WHEN b.year = 2017 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2017, MAX(CASE WHEN b.year = 2018 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2018, MAX(CASE WHEN b.year = 2019 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2019, MAX(CASE WHEN b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)' THEN b.vasitel END) AS base_2020, MAX(CASE WHEN b.year = 2021 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2021, MAX(CASE WHEN b.year = 2022 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2022, MAX(CASE WHEN b.year = 2023 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2023, MAX(CASE WHEN b.year = 2024 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2024, MAX(CASE WHEN b.year = 2025 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2025
#         FROM base b JOIN dept d ON b.code = d.code JOIN university u ON d.uni_id = u.id
#         WHERE (b.year = 2013 AND b.cat_title LIKE '90%% ΓΕΝΙΚΗ%%ΣΕΙΡΑ%%') OR (b.year IN (2014, 2015) AND b.cat_title = '90%% ΓΕΛ/ΕΠΑΛΒ ΓΕΝ.ΣΕΙΡΑ ΗΜ.') OR (b.year = 2016 AND b.cat_title = 'ΓΕΛ ΓΕΝ.ΣΕΙΡΑ ΗΜ. (ΝΕΟ)') OR (b.year IN (2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025) AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.') OR (b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)')
#         GROUP BY b.code, u.title HAVING COUNT(DISTINCT b.year) = 13;
#         """

#     elif dataset_id == '2':
#         feature_cols = ['base_2019', 'base_2020', 'base_2021', 'base_2022', 'base_2023', 'base_2024', 'base_2025']
#         query = """
#         SELECT b.code, MAX(b.field) AS field, u.title AS university, (SELECT ROUND(SUM(s.protimisi * s.plithos) / NULLIF(SUM(s.plithos), 0)) FROM statistics s WHERE s.code = b.code AND s.category = 1) AS avg_pref_success,
#         MAX(CASE WHEN b.year = 2019 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2019, MAX(CASE WHEN b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)' THEN b.vasitel END) AS base_2020, MAX(CASE WHEN b.year = 2021 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2021, MAX(CASE WHEN b.year = 2022 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2022, MAX(CASE WHEN b.year = 2023 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2023, MAX(CASE WHEN b.year = 2024 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2024, MAX(CASE WHEN b.year = 2025 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS base_2025
#         FROM base b JOIN dept d ON b.code = d.code JOIN university u ON d.uni_id = u.id
#         WHERE (b.year = 2019 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.') OR (b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)') OR (b.year IN (2021, 2022, 2023, 2024, 2025) AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.')
#         GROUP BY b.code, u.title HAVING COUNT(DISTINCT b.year) = 7;
#         """

#     elif dataset_id == '3':
#         feature_cols = ['diff_14_13', 'diff_15_14', 'diff_16_15', 'diff_17_16', 'diff_18_17', 'diff_19_18', 'diff_20_19', 'diff_21_20', 'diff_22_21', 'diff_23_22', 'diff_24_23', 'diff_25_24']
#         query = """
#         SELECT b.code, MAX(b.field) AS field, u.title AS university, (SELECT ROUND(SUM(s.protimisi * s.plithos) / NULLIF(SUM(s.plithos), 0)) FROM statistics s WHERE s.code = b.code AND s.category = 1) AS avg_pref_success,
#         MAX(CASE WHEN b.year = 2014 AND b.cat_title = '90%% ΓΕΛ/ΕΠΑΛΒ ΓΕΝ.ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2013 AND b.cat_title LIKE '90%% ΓΕΝΙΚΗ%%ΣΕΙΡΑ%%' THEN b.vasitel END) AS diff_14_13,
#         MAX(CASE WHEN b.year = 2015 AND b.cat_title = '90%% ΓΕΛ/ΕΠΑΛΒ ΓΕΝ.ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2014 AND b.cat_title = '90%% ΓΕΛ/ΕΠΑΛΒ ΓΕΝ.ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_15_14,
#         MAX(CASE WHEN b.year = 2016 AND b.cat_title = 'ΓΕΛ ΓΕΝ.ΣΕΙΡΑ ΗΜ. (ΝΕΟ)' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2015 AND b.cat_title = '90%% ΓΕΛ/ΕΠΑΛΒ ΓΕΝ.ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_16_15,
#         MAX(CASE WHEN b.year = 2017 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2016 AND b.cat_title = 'ΓΕΛ ΓΕΝ.ΣΕΙΡΑ ΗΜ. (ΝΕΟ)' THEN b.vasitel END) AS diff_17_16,
#         MAX(CASE WHEN b.year = 2018 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2017 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_18_17,
#         MAX(CASE WHEN b.year = 2019 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2018 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_19_18,
#         MAX(CASE WHEN b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2019 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_20_19,
#         MAX(CASE WHEN b.year = 2021 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)' THEN b.vasitel END) AS diff_21_20,
#         MAX(CASE WHEN b.year = 2022 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2021 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_22_21,
#         MAX(CASE WHEN b.year = 2023 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2022 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_23_22,
#         MAX(CASE WHEN b.year = 2024 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2023 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_24_23,
#         MAX(CASE WHEN b.year = 2025 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2024 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_25_24
#         FROM base b JOIN dept d ON b.code = d.code JOIN university u ON d.uni_id = u.id
#         WHERE (b.year = 2013 AND b.cat_title LIKE '90%% ΓΕΝΙΚΗ%%ΣΕΙΡΑ%%') OR (b.year IN (2014, 2015) AND b.cat_title = '90%% ΓΕΛ/ΕΠΑΛΒ ΓΕΝ.ΣΕΙΡΑ ΗΜ.') OR (b.year = 2016 AND b.cat_title = 'ΓΕΛ ΓΕΝ.ΣΕΙΡΑ ΗΜ. (ΝΕΟ)') OR (b.year IN (2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025) AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.') OR (b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)')
#         GROUP BY b.code, u.title HAVING COUNT(DISTINCT b.year) = 13;
#         """

#     elif dataset_id == '4':
#         feature_cols = ['diff_20_19', 'diff_21_20', 'diff_22_21', 'diff_23_22', 'diff_24_23', 'diff_25_24']
#         query = """
#         SELECT b.code, MAX(b.field) AS field, u.title AS university, (SELECT ROUND(SUM(s.protimisi * s.plithos) / NULLIF(SUM(s.plithos), 0)) FROM statistics s WHERE s.code = b.code AND s.category = 1) AS avg_pref_success,
#         MAX(CASE WHEN b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2019 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_20_19,
#         MAX(CASE WHEN b.year = 2021 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)' THEN b.vasitel END) AS diff_21_20,
#         MAX(CASE WHEN b.year = 2022 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2021 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_22_21,
#         MAX(CASE WHEN b.year = 2023 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2022 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_23_22,
#         MAX(CASE WHEN b.year = 2024 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2023 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_24_23,
#         MAX(CASE WHEN b.year = 2025 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) - MAX(CASE WHEN b.year = 2024 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.' THEN b.vasitel END) AS diff_25_24
#         FROM base b JOIN dept d ON b.code = d.code JOIN university u ON d.uni_id = u.id
#         WHERE (b.year = 2019 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.') OR (b.year = 2020 AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ. (ΝΕΟ)') OR (b.year IN (2021, 2022, 2023, 2024, 2025) AND b.cat_title LIKE 'ΓΕΛ ΓΕΝ%%ΣΕΙΡΑ ΗΜ.')
#         GROUP BY b.code, u.title HAVING COUNT(DISTINCT b.year) = 7;
#         """
#     else:
#         raise ValueError("Μη έγκυρο Dataset ID")

#     # 4. Εκτέλεση και καθαρισμός δεδομένων
#     df = pd.read_sql(query, engine)
#     df = df.dropna(subset=feature_cols).fillna(0) 
#     data_for_clustering = df[feature_cols].copy()

#     # 5. K-Means
#     kmeans = KMeans(n_clusters=k_clusters, n_init='auto', random_state=42)
#     kmeans.fit(data_for_clustering)
#     df['Cluster'] = kmeans.labels_.astype(str)

#     # 6. Ανάλυση (Crosstabs)
#     field_analysis = pd.crosstab(df['Cluster'], df['field']).fillna(0).to_dict(orient='index')
#     pref_analysis = pd.crosstab(df['Cluster'], df['avg_pref_success']).fillna(0).to_dict(orient='index')

#     # 7. Έξοδος σε JSON
#     response = {
#         "status": "success",
#         "k": k_clusters,
#         "dataset": dataset_id,
#         "field_distribution": field_analysis,
#         "preference_distribution": pref_analysis
#     }
#     print(json.dumps(response))

# except Exception as e:
#     print(json.dumps({"status": "error", "message": str(e)}))


















# import sys
# import json
# import pandas as pd
# import os
# from sklearn.cluster import KMeans
# from sklearn.metrics import silhouette_score
# import warnings

# # Αγνοούμε τα warnings για να έχουμε καθαρό JSON
# warnings.filterwarnings('ignore') 

# try:
#     dataset_id = sys.argv[1]
#     k_input = int(sys.argv[2])

#     # 1. Αντιστοίχιση των ID με τα νέα, δικά σου ονόματα αρχείων
#     file_mapping = {
#         '1': 'dataset1.from2013.csv',
#         '2': 'dataset2.from2019.csv',
#         '3': 'dataset3.difsfrom2013.csv',
#         '4': 'dataset4.difsfrom2019.csv'
#     }

#     if dataset_id not in file_mapping:
#         raise ValueError("Μη έγκυρο Dataset ID")

#     filename = file_mapping[dataset_id]

#     # 2. Βρίσκουμε τον φάκελο 'datasets' και το σωστό αρχείο CSV
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(base_dir, 'datasets', filename)

#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Το αρχείο {filename} δεν βρέθηκε στον φάκελο datasets!")

#     # 3. Διαβάζουμε το CSV ακαριαία
#     df = pd.read_csv(file_path)

#     # 4. ΑΥΤΟΜΑΤΗ ανίχνευση στηλών (Zero-Code για το μέλλον)
#     if dataset_id in ['1', '2']:
#         feature_cols = [col for col in df.columns if col.startswith('base_')]
#     elif dataset_id in ['3', '4']:
#         feature_cols = [col for col in df.columns if col.startswith('diff_')]

#     # Καθαρίζουμε τυχόν κενά δεδομένα
#     df = df.dropna(subset=feature_cols).fillna(0) 
#     data_for_clustering = df[feature_cols].copy()

#     # 5. Αυτόματος υπολογισμός του k (Silhouette) ή χειροκίνητος
#     if k_input == 0:
#         best_k = 3
#         best_score = -1
#         for i in range(2, 9):
#             test_kmeans = KMeans(n_clusters=i, n_init='auto', random_state=42)
#             labels = test_kmeans.fit_predict(data_for_clustering)
#             score = silhouette_score(data_for_clustering, labels)
#             if score > best_score:
#                 best_score = score
#                 best_k = i
#         final_k = best_k
#     else:
#         final_k = k_input

#     # 6. Εκτέλεση του τελικού K-Means
#     kmeans = KMeans(n_clusters=final_k, n_init='auto', random_state=42)
#     kmeans.fit(data_for_clustering)
#     df['Cluster'] = kmeans.labels_.astype(str)

#     # 7. Στατιστική Ανάλυση (Crosstabs)
#     field_analysis = pd.crosstab(df['Cluster'], df['field']).fillna(0).to_dict(orient='index')
#     pref_analysis = pd.crosstab(df['Cluster'], df['avg_pref_success']).fillna(0).to_dict(orient='index')

#     # 8. Στέλνουμε τα αποτελέσματα στο Frontend
#     response = {
#         "status": "success",
#         "k": final_k,
#         "dataset": dataset_id,
#         "field_distribution": field_analysis,
#         "preference_distribution": pref_analysis
#     }
#     print(json.dumps(response))

# except Exception as e:
#     print(json.dumps({"status": "error", "message": str(e)}))











import sys
import json
import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import io
import base64


warnings.filterwarnings('ignore') 


def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')

try:
    dataset_id = sys.argv[1]
    k_input = int(sys.argv[2])

    # 1. Αντιστοίχιση των ID με τα νέα, δικά σου ονόματα αρχείων
    file_mapping = {
        '1': 'dataset1.from2013.csv',
        '2': 'dataset2.from2019.csv',
        '3': 'dataset3.difsfrom2013.csv',
        '4': 'dataset4.difsfrom2019.csv'
    }

    if dataset_id not in file_mapping:
        raise ValueError("Μη έγκυρο Dataset ID")

    filename = file_mapping[dataset_id]

    # 2. Βρίσκουμε τον φάκελο 'datasets' και το σωστό αρχείο CSV
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '../datasets', filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Το αρχείο {filename} δεν βρέθηκε στον φάκελο datasets!")

    # 3. Διαβάζουμε το CSV ακαριαία
    df = pd.read_csv(file_path)

    # 4. ΑΥΤΟΜΑΤΗ ανίχνευση στηλών (Zero-Code για το μέλλον)
    if dataset_id in ['1', '2']:
        feature_cols = [col for col in df.columns if col.startswith('base_')]
    elif dataset_id in ['3', '4']:
        feature_cols = [col for col in df.columns if col.startswith('diff_')]

   
    df = df.dropna(subset=feature_cols).fillna(0) 
    data_for_clustering = df[feature_cols].copy()

    # 5. Αυτόματος υπολογισμός του k (Silhouette) ή χειροκίνητος
    if k_input == 0:
        best_k = 3
        best_score = -1
        for i in range(2, 9):
            test_kmeans = KMeans(n_clusters=i, n_init='auto', random_state=42)
            labels = test_kmeans.fit_predict(data_for_clustering)
            score = silhouette_score(data_for_clustering, labels)
            if score > best_score:
                best_score = score
                best_k = i
        final_k = best_k
    else:
        final_k = k_input

    # 6. Εκτέλεση του τελικού K-Means
    kmeans = KMeans(n_clusters=final_k, n_init='auto', random_state=42)
    kmeans.fit(data_for_clustering)
    df['Cluster'] = kmeans.labels_.astype(str) 

    sse_value = float(kmeans.inertia_)
    sil_score = float(silhouette_score(data_for_clustering, kmeans.labels_))

    # 7. Στατιστική Ανάλυση (Crosstabs)
   
    if 'field' in df.columns:
        field_analysis = pd.crosstab(df['Cluster'], df['field']).fillna(0).to_dict(orient='index')
    else:
        field_analysis = {}

    if 'avg_pref_success' in df.columns:
        pref_analysis = pd.crosstab(df['Cluster'], df['avg_pref_success']).fillna(0).to_dict(orient='index')
    else:
        pref_analysis = {}


  
    # 8. ΠΑΡΑΓΩΓΗ ΝΕΩΝ ΓΡΑΦΗΜΑΤΩΝ 

    
    
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
    scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1], c=kmeans.labels_, cmap='Set1', s=30, alpha=0.7, edgecolor='k')
    plt.xlabel(f"Συνιστώσα 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    plt.ylabel(f"Συνιστώσα 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    pca_b64 = fig_to_base64(fig_pca)

    # Γ) HEATMAP Συσχετίσεων (Correlation Matrix) των μεταβλητών
    fig_heatmap = plt.figure(figsize=(10, 8))
    
    corr_matrix = data_for_clustering.corr()
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0)
    heatmap_b64 = fig_to_base64(fig_heatmap)


    # 9. Στέλνουμε ΟΛΑ τα αποτελέσματα στο Frontend
    response = {
        "status": "success",
        "k": final_k,
        "dataset": dataset_id,
        "field_distribution": field_analysis,
        "preference_distribution": pref_analysis,
        "parallel_coords": parallel_b64,
        "pca": pca_b64,                 
        "heatmap": heatmap_b64,
        "sse": sse_value,
        "silhouette": sil_score
    }
    
    print(json.dumps(response))

except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}))