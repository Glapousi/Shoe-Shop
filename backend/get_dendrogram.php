<?php
header('Content-Type: application/json; charset=utf-8');

$dataset = isset($_GET['dataset']) ? $_GET['dataset'] : '1';
$linkage = isset($_GET['linkage']) ? $_GET['linkage'] : 'ward';
$python_executable = "C:\\Python314\\python.exe";  
$script_path = __DIR__ . "\\generate_dendrogram.py";

$command = escapeshellcmd("\"$python_executable\" \"$script_path\" " . escapeshellarg($dataset) . " " . escapeshellarg($linkage));
$output = shell_exec($command);

echo $output;
?>