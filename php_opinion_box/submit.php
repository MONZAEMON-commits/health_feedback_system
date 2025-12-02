<?php
// POST 受け取り
$employee_id = $_POST['employee_id'] ?? '';
$mode        = $_POST['mode'] ?? '';
$content     = $_POST['content'] ?? '';
$tag         = $_POST['tag'] ?? '';

// 空白チェック（最終）
if (trim($content) === '') {
    header("Location: form.php?error=empty");
    exit;
}

// タイムスタンプ
$timestamp = date('Y-m-d H:i:s');

// 保存先ディレクトリとファイル名
$directory = __DIR__ . '/opinions';
$csv_path  = $directory . '/opinion_box.csv';

// ① フォルダが無ければ作る
if (!is_dir($directory)) {
    mkdir($directory, 0777, true);
}

// ② CSVファイルが無ければ作る
if (!file_exists($csv_path)) {
    // 初回だけヘッダー行も書いておくと綺麗（任意）
    file_put_contents($csv_path, "timestamp,employee_id,mode,content,tag\n");
}

// ③ 書き込み開始
$fp = fopen($csv_path, 'a');
if ($fp === false) {
    die("CSVファイルのオープンに失敗しました。");
}

// 排他ロックで安全に書き込む
flock($fp, LOCK_EX);
fputcsv($fp, [$timestamp, $employee_id, $mode, $content, $tag]);
flock($fp, LOCK_UN);
fclose($fp);

// 完了画面へ
header("Location: success.php");
exit;
?>