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
from scipy.cluster.hierarchy import linkage, dendrogram

warnings.filterwarnings('ignore')

try:
    dataset_id = sys.argv[1]
    linkage_method = sys.argv[2] if len(sys.argv) > 2 else 'ward'
    file_mapping = {
        '1': 'dataset1.from2013.csv', '2': 'dataset2.from2019.csv',
        '3': 'dataset3.difsfrom2013.csv', '4': 'dataset4.difsfrom2019.csv'
    }

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '../datasets', file_mapping[dataset_id])
    df = pd.read_csv(file_path)

    # Επιλογή στηλών
    if dataset_id in ['1', '2']:
        feature_cols = [c for c in df.columns if c.startswith('base_')]
    else:
        feature_cols = [c for c in df.columns if c.startswith('diff_')]

    data = df.dropna(subset=feature_cols).fillna(0)[feature_cols].copy()

    # Παραγωγή ΜΟΝΟ του Δενδρογράμματος
    fig = plt.figure(figsize=(10, 5))
    Z = linkage(data, method=linkage_method)
    
    # Ζωγραφίζουμε το δέντρο
    dendrogram(Z, link_color_func=lambda k: '#1f77b4') 
    plt.title("Δενδρόγραμμα – Επιλέξτε το ιδανικό k")
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    
    dendrogram_b64 = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')

    print(json.dumps({"status": "success", "dendrogram": dendrogram_b64}))

except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}))