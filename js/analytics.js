let fieldChartInstance = null;
let prefChartInstance = null;

// Χρώματα για τα γραφήματα
const colors = [
    'rgba(255, 99, 132, 0.7)', 'rgba(54, 162, 235, 0.7)', 
    'rgba(255, 206, 86, 0.7)', 'rgba(75, 192, 192, 0.7)', 
    'rgba(153, 102, 255, 0.7)', 'rgba(255, 159, 64, 0.7)',
    'rgba(201, 203, 207, 0.7)', 'rgba(255, 99, 255, 0.7)', 
    'rgba(0, 200, 83, 0.7)', 'rgba(255, 87, 34, 0.7)',  
    'rgba(0, 74, 212, 0.7)' 
];

// Συνάρτηση για να εκτελεί την ανάλυση
function runAnalysis() {
    const algorithm = document.getElementById('algorithm').value;
    const dataset = document.getElementById('dataset').value;
    const k = document.getElementById('k').value;
    const linkage = document.getElementById('linkage').value;
    
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    let apiUrl = '';
    if (algorithm === 'kmeans') {
        apiUrl = `backend/kmeans_api.php?dataset=${dataset}&k=${k}`;
    } else if (algorithm === 'agglomerative') {
        apiUrl = `backend/agglomerative_api.php?dataset=${dataset}&k=${k}&linkage=${linkage}`; 
    }

    // Κλήση στο PHP API
    //fetch(`kmeans_api.php?dataset=${dataset}&k=${k}`)
    // fetch(apiUrl)
    //     .then(response => response.json())
    //     .then(data => {
    //         document.getElementById('loading').style.display = 'none';
    //         if(data.status === 'success') {
    //             document.getElementById('results').style.display = 'block';
    //             drawChart('fieldChart', data.field_distribution, 'Πεδίο', fieldChartInstance, (instance) => fieldChartInstance = instance);
    //             drawChart('prefChart', data.preference_distribution, 'Προτίμηση', prefChartInstance, (instance) => prefChartInstance = instance);
    //             if (algorithm === "agglomerative") {
    //                 if (data.dendrogram) {
    //                     document.getElementById("dendrogram").src = data.dendrogram;
    //                     document.getElementById("dendrogram_container").style.display = "block";
    //                 }
    //                 if (data.heatmap) {
    //                     document.getElementById("heatmap").src = data.heatmap;
    //                     document.getElementById("heatmap_container").style.display = "block";
    //                 }
    //             }
    //         } else {
    //             alert("Σφάλμα: " + data.message);
    //         }
    //     })
    //     .catch(err => {
    //         document.getElementById('loading').style.display = 'none';
    //         alert("Σφάλμα επικοινωνίας με τον server. Ελέγξτε την κονσόλα.");
    //         console.error(err);
    //     });
    // }
    // ... [το πάνω μέρος της runAnalysis μένει ίδιο] ...

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading').style.display = 'none';
            
            if(data.status === 'success') {
                document.getElementById('results').style.display = 'block';

                
                document.getElementById('sil_score_val').innerText = data.silhouette ? data.silhouette.toFixed(3) : "N/A";
                document.getElementById('sse_val').innerText = data.sse ? Math.round(data.sse).toLocaleString('el-GR') : "N/A";
                
                // --- 1. Parallel Coordinates ---
                if (data.parallel_coords) {
                    document.getElementById("parallel_img").src = data.parallel_coords;
                    document.getElementById("parallel_container").style.display = "block";
                } else {
                    document.getElementById("parallel_container").style.display = "none";
                }

                // --- 2. PCA ---
                if (data.pca) {
                    document.getElementById("pca_img").src = data.pca;
                    document.getElementById("pca_container").style.display = "block";
                } else {
                    document.getElementById("pca_container").style.display = "none";
                }

                // --- 3. Bar Charts (Υπάρχοντα) ---
                drawChart('fieldChart', data.field_distribution, 'Πεδίο', fieldChartInstance, (instance) => fieldChartInstance = instance);
                drawChart('prefChart', data.preference_distribution, 'Προτίμηση', prefChartInstance, (instance) => prefChartInstance = instance);

                // --- 4. Heatmap ---
               
                if (data.heatmap) {
                    document.getElementById("heatmap").src = data.heatmap;
                    document.getElementById("heatmap_container").style.display = "block";
                } else {
                    document.getElementById("heatmap_container").style.display = "none";
                }

                
                
            } else {
                alert("Σφάλμα: " + data.message);
            }
        })
        .catch(err => { console.error(err); });
}
// Γενική συνάρτηση για να ζωγραφίζει και τα δύο γραφήματα
function drawChart(canvasId, dataDict, legendPrefix, oldChartInstance, saveInstanceCallback) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    if (oldChartInstance) { oldChartInstance.destroy(); }

    const clusters = Object.keys(dataDict); 

    let allCategories = new Set();
    clusters.forEach(c => {
        Object.keys(dataDict[c]).forEach(cat => allCategories.add(cat));
    });
    const categoriesArray = Array.from(allCategories).sort(); 

    // Δημιουργία datasets για το Chart.js
    const chartDatasets = categoriesArray.map((category, index) => {
        return {
            label: `${legendPrefix} ${category}`,
            data: clusters.map(c => dataDict[c][category] || 0), 
            backgroundColor: colors[index % colors.length],
            borderWidth: 1
        };
    });

    const newChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: clusters.map(c => `Cluster ${c}`),
            datasets: chartDatasets
        },
        options: {
            responsive: true,
            scales: {
                x: { 
                    stacked: false,
                    title: {
                        display: true,
                        text: 'Ομάδες (Clusters)' 
                    }
                },
                y: { 
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Πλήθος Τμημάτων' 
                    }
                }
            }
        }
    });
    
    saveInstanceCallback(newChart);


}

// Συνάρτηση για να ανακτά το προτεινόμενο k από τον server
function fetchBestK() {
    const datasetId = document.getElementById('dataset').value;
    const algorithm = document.getElementById('algorithm').value;
    const kInput = document.getElementById('k');

   
    kInput.disabled = true;

   
    fetch(`backend/get_best_k.php?dataset_id=${datasetId}&algorithm=${algorithm}`)
        .then(response => response.json())
        .then(data => {
            if (data.best_k) {
                kInput.value = data.best_k;
            }
            kInput.disabled = false; 
        })
        .catch(error => {
            console.error('Σφάλμα κατά την ανάκτηση του προτεινόμενου k:', error);
            kInput.disabled = false;
        });
}

    // Όταν φορτώσει η σελίδα, συνδέουμε το dropdown με τη συνάρτηση 
   
document.addEventListener('DOMContentLoaded', () => {
    const datasetSelect = document.getElementById('dataset');
    const algorithmSelect = document.getElementById('algorithm');
    if (datasetSelect) {
       
        datasetSelect.addEventListener('change', fetchBestK);
        algorithmSelect.addEventListener('change', fetchBestK);
        
        fetchBestK(); 
    }
});


function showDendrogram() {
    const dataset = document.getElementById('dataset').value;
    const linkage = document.getElementById('linkage').value;
    document.getElementById('loading2').style.display = 'block';
    
   
    fetch(`backend/get_dendrogram.php?dataset=${dataset}&linkage=${linkage}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('loading2').style.display = 'none';
            if(data.status === 'success') {
                
                
                document.getElementById("modal_dendrogram_img").src = data.dendrogram;
                
                
                document.getElementById("dendroModal").style.display = "block";
                
               
                const dendrogram_btn = document.getElementById('execute_btn');
                dendrogram_btn.disabled = false;
                dendrogram_btn.style.opacity = '1';
                dendrogram_btn.style.cursor = 'pointer';
                
            } else {
                alert("Σφάλμα: " + data.message);
            }
        })
        .catch(err => {
            document.getElementById('loading2').style.display = 'none';
            alert("Σφάλμα σύνδεσης");
            console.error(err);
        });
}

// Συνάρτηση για να κλείνει το pop-up από το X
function closeModal() {
    document.getElementById("dendroModal").style.display = "none";
}

// Αν ο χρήστης κάνει κλικ στο σκοτεινό φόντο ΕΞΩ από το pop-up, να κλείνει
window.addEventListener('click', function(event) {
    const modal = document.getElementById("dendroModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
});



// Συνάρτηση για να ενημερώνει την κατάσταση του UI ανάλογα με τον αλγόριθμο
function updateUIState() {
    const algorithm = document.getElementById('algorithm').value;
    const executeBtn = document.getElementById('execute_btn');
    const dendroBtn = document.getElementById('dendrogram_btn');
    const linkageContainer = document.getElementById('linkage_container');

    if (algorithm === 'kmeans') {
       
        dendroBtn.style.display = 'none';
        linkageContainer.style.display = 'none';
        executeBtn.disabled = false;
        executeBtn.style.opacity = '1';
        executeBtn.style.cursor = 'pointer';
    } else if (algorithm === 'agglomerative') {
        
        dendroBtn.style.display = 'inline-block';
        linkageContainer.style.display = 'block';
        executeBtn.disabled = true;
        executeBtn.style.opacity = '0.5'; 
        executeBtn.style.cursor = 'not-allowed';
    }
}



// Όταν φορτώσει η σελίδα, συνδέουμε τα dropdown με τις συναρτήσεις
document.addEventListener('DOMContentLoaded', () => {
    const datasetSelect = document.getElementById('dataset');
    const algorithmSelect = document.getElementById('algorithm');
    const linkageSelect = document.getElementById('linkage'); 

    if (datasetSelect) {
        datasetSelect.addEventListener('change', fetchBestK);
        datasetSelect.addEventListener('change', updateUIState); 
    }
    
    if (algorithmSelect) {
        algorithmSelect.addEventListener('change', fetchBestK);
        algorithmSelect.addEventListener('change', updateUIState); 
    }

    if (linkageSelect) {
        linkageSelect.addEventListener('change', updateUIState); 
    }

  
    if (datasetSelect && algorithmSelect) {
        fetchBestK(); 
        updateUIState(); 
    }
});
