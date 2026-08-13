<?php
header('Content-Type: application/json; charset=utf-8');


$dataset = isset($_GET['dataset']) ? $_GET['dataset'] : '1';
$k = isset($_GET['k']) ? intval($_GET['k']) : 0;
$linkage = isset($_GET['linkage']) ? $_GET['linkage'] : 'ward';


$python_executable = "C:\\Python314\\python.exe";  
$script_path = __DIR__ . "\\agglomerative.py";


$command = escapeshellcmd("\"$python_executable\" \"$script_path\" " . escapeshellarg($dataset) . " " . escapeshellarg($k) . " " . escapeshellarg($linkage));
$output = shell_exec($command);


if (!$output) {
    echo json_encode(["status" => "error", "message" => "Δεν ελήφθη έξοδος από το Python script."]);
    exit;
}


$data = json_decode($output, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    echo json_encode(["status" => "error", "message" => "Σφάλμα ανάλυσης JSON από Python."]);
    exit;
}


echo json_encode($data);
?>