<?php
$employee_id = $_POST['employee_id'] ?? '';
$content     = $_POST['content'] ?? '';
$timestamp = date('Y-m-d H:i:s');
$csv_file = __DIR__ . '/opinion_box.csv';  // テスト用のCSV

$fp = fopen($csv_file, 'a');  // a = 追記モード
fputcsv($fp, [$timestamp,$employee_id, $content]);
fclose($fp);
?>
