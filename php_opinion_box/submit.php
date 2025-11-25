<?php
$employee_id = $_POST['employee_id'] ?? '';
$mode = $_POST['mode'] ?? '';
$content     = $_POST['content'] ?? '';
$tag = $_POST['tag'] ?? '';
$timestamp = date('Y-m-d H:i:s');
$csv_file = __DIR__ . '/opinion_box.csv';  // テスト用のCSV

$fp = fopen($csv_file, 'a');  // a = 追記モード
fputcsv($fp, [$timestamp,$employee_id,$mode, $content, $tag]);
fclose($fp);
header("Location: success.php");
exit;
?>
