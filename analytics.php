
<?php
$last_year = "2026"; 
$csv_file = __DIR__ . '/datasets/dataset2.from2019.csv'; 

if (file_exists($csv_file)) {
    if (($handle = fopen($csv_file, "r")) !== FALSE) {
        // Διαβάζουμε ΜΟΝΟ την πρώτη γραμμή (τα headers)
        $headers = fgetcsv($handle, 1000, ",");
        fclose($handle);

        if (!empty($headers)) {
            $max_year = 0;
            // Ψάχνουμε σε όλα τα headers για τη λέξη "base_"
            foreach ($headers as $header) {
                if (strpos($header, 'base_') === 0) {
                    // Αφαιρούμε το 'base_' για να κρατήσουμε μόνο τον αριθμό του έτους
                    $year_num = intval(str_replace('base_', '', $header));
                    if ($year_num > $max_year) {
                        $max_year = $year_num;
                    }
                }
            }
            if ($max_year > 0) {
                $last_year = $max_year;
            }
        }
    }
}
?>

<!DOCTYPE html>
<html lang="el">

<head>
    <meta charset="UTF-8">
    <title>Ανάλυση K-Means</title>
    <link rel="stylesheet" href="css/analytics.css">
    <!-- Φορτώνουμε το Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
</head>
<body>
    <nav>
        <div class="nav-bar">
            <div class="logo">vaseis-app</div>
            <div class="back"><a href="index.php">Επιστροφή στην Αρχική</a></div>
        </div>
    </nav>
<div class="container">
    <h2>Ανάλυση Βάσεων </h2>
    
    <div class="controls">
        <div class="control-group">
            <div class="control-group">
                <label for="algorithm">Αλγόριθμος:</label>
                <select id="algorithm" class="control-input">
                    <option value="kmeans">K-Means</option>
                    <option value="agglomerative">Agglomerative (Hierarchical)</option>
                </select>
            </div>
            <div class="control-group" id="linkage_container" >
                <label for="linkage">Μέθοδος Σύνδεσης (Linkage):</label>
                <select id="linkage" class="control-input" style="padding: 8px;">
                    <option value="ward">Ward (Ελαχιστοποίηση Διακύμανσης)</option>
                    <option value="complete">Complete (Μέγιστη Απόσταση)</option>
                    <option value="average">Average (Μέση Απόσταση)</option>
                    <option value="single">Single (Ελάχιστη Απόσταση)</option>
                </select>
            </div>
            <br>
            <label for="dataset">Επιλογή Δεδομένων:</label>
            <select id="dataset" style="padding: 8px;">
                <option value="1">Dataset 1: Βάσεις 2013-<?php echo $last_year; ?></option>
                <option value="2">Dataset 2: Βάσεις 2019-<?php echo $last_year; ?></option>
                <option value="3">Dataset 3: Διαφορές Βάσεων 2013-<?php echo $last_year; ?></option>
                <option value="4">Dataset 4: Διαφορές Βάσεων 2019-<?php echo $last_year; ?></option>
            </select>
        </div>
        
        <div class="control-group">
            <label for="k">Αριθμός Ομάδων:</label>
            <input type="number" id="k" min="2" max="10" value="<?php echo isset($_GET['k']) ? $_GET['k'] : 3; ?>" style="padding: 8px; width: 60px;">
        </div>
        
        <button id="execute_btn" onclick="runAnalysis()">Εκτέλεση Αλγορίθμου</button>
        <button id="dendrogram_btn" onclick="showDendrogram()" style="display: none;">Δενδρόγραμμα</button>
    </div>

    <div id="loading" class="loading">
        <img src="https://i.gifer.com/ZZ5H.gif" alt="loading" width="30"> <br>
        Εκτέλεση Αλγορίθμου... Παρακαλώ περιμένετε!
    </div>

    <div id="loading2" class="loading">
        <img src="https://i.gifer.com/ZZ5H.gif" alt="loading" width="30"> <br>
        Δενδρόγραμμα σε επεξεργασία... Παρακαλώ περιμένετε!
    </div>

    <div id="results" class="charts-wrapper">

        <div style="display: flex; gap: 20px; margin-bottom: 30px;">
            <div class="chart-container" style="flex: 1; text-align: center; margin-bottom: 0;">
                <h4 style="margin: 0 0 10px 0; color: #666;">Silhouette Score</h4>
                <div id="sil_score_val" style="font-size: 28px; font-weight: bold; color: #0056b3;">-</div>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #888;"></p>
            </div>
            <div class="chart-container" style="flex: 1; text-align: center; margin-bottom: 0;">
                <h4 style="margin: 0 0 10px 0; color: #666;">Sum of Squared Errors (SSE)</h4>
                <div id="sse_val" style="font-size: 28px; font-weight: bold; color: #0056b3;">-</div>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #888;"></p>
            </div>
        </div>
        
        <div id="parallel_container" class="chart-container" style="display:none;">
            <h3>Parallel Coordinates</h3>
            <img id="parallel_img" src="" alt="Parallel Coordinates Chart">
        </div>

        <div id="pca_container" class="chart-container" style="display:none;">
            <h3>Ανάλυση Κύριων Συνιστωσών (PCA - 2D)</h3>
            <img id="pca_img" src="" alt="PCA Plot">
        </div>

        <div class="chart-container">
            <h3>Κατανομή Επιστημονικών Πεδίων ανά Ομάδα (Cluster)</h3>
            <canvas id="fieldChart"></canvas>
        </div>
        
        <div class="chart-container">
            <h3>Μέση Προτίμηση Επιτυχόντων ανά Ομάδα (Cluster)</h3>
            <canvas id="prefChart"></canvas>
        </div>

        <div id="heatmap_container" class="chart-container" style="display:none;">
            <h3>Heatmap Αποστάσεων / Συσχετίσεων</h3>
            <img id="heatmap" src="" alt="Heatmap">
        </div>

    </div>
<div id="dendroModal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <h3>Επιλογή Ιδανικού k από το Δενδρόγραμμα</h3>
            <p style="color: #666; margin-bottom: 20px;">Μελετήστε το γράφημα, κλείστε αυτό το παράθυρο και εισάγετε το k στο πεδίο.</p>
            <img id="modal_dendrogram_img" src="" alt="Dendrogram" style="max-width: 100%; height: auto; border-radius: 8px;">
        </div>
    </div>
<script src="/vaseis-app/js/analytics.js"></script>

</body>
</html>