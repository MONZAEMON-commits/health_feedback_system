<?php
$employee_id = $_POST['employee_id'] ?? '';
$mode = $_POST['mode'] ?? '';
$content = htmlspecialchars($_POST['content'], ENT_QUOTES, 'UTF-8');
$tag = $_POST['tag'] ?? '';
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ご意見箱内容確認</title>
</head>
<body>
    <h2>ご意見箱内容確認</h2>
    <p>以下の内容で送信してよろしいですか？</p>
    <p>投稿形式：<?= [
    'anonymous' => '匿名',
    'semi'      => '準匿名',
    'signed'    => '署名'
    ][$mode] ?? '' ?></p>
    <p>入力内容：<?= $content?></p>
    <p>カテゴリ：<?=$tag?></p>
        <form action="submit.php" method="post">
            <input type="hidden" name="mode" value="<?= $mode ?>">
            <input type="hidden" name="content" value="<?= htmlspecialchars($_POST['content'], ENT_QUOTES, 'UTF-8')?>">
            <input type="hidden" name="employee_id" value="<?= $_POST["employee_id"] ?>">
            <input type="hidden" name="tag" value="<?= $tag ?>">
            <button type="submit">送信</button>
        </form>
    <br>
    <a href="form.php">戻る</a>
</body>
</html>