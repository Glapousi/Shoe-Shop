<?php
header('Content-Type: application/json');


$dataset = isset($_GET['dataset']) ? escapeshellarg($_GET['dataset']) : escapeshellarg('1');
$k = isset($_GET['k']) ? intval($_GET['k']) : 3;


$python_executable = "C:\Python314\python.exe"; 


$script_path = __DIR__ . "\\kmeans.py";

$command = escapeshellcmd("$python_executable $script_path") . " $dataset $k 2>&1";
$output = shell_exec($command);

if ($output === null) {
    echo json_encode(["status" => "error", "message" => "Αποτυχία εκτέλεσης Python script. Ελέγξτε το path της Python."]);
} else {
    echo $output;
}
?>