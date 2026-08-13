<?php

header('Content-Type: application/json');


$dataset_id = isset($_GET['dataset_id']) ? $_GET['dataset_id'] : '1';
$algorithm = isset($_GET['algorithm']) ? $_GET['algorithm'] : 'kmeans';


$best_k_values = [
    '1' => [
        'kmeans' => 3, 
        'agglomerative' => 4  
    ],
    '2' => [
        'kmeans' => 3, 
        'agglomerative' => 4
    ],
    '3' => [
        'kmeans' => 6, 
        'agglomerative' => 4
    ],
    '4' => [
        'kmeans' => 5, 
        'agglomerative' => 5
    ]
];


$best_k = 3; 

if (isset($best_k_values[$dataset_id]) && isset($best_k_values[$dataset_id][$algorithm])) {
    $best_k = $best_k_values[$dataset_id][$algorithm];
}

echo json_encode(['best_k' => $best_k]);
?>