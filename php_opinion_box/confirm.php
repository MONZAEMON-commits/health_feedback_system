<?php
// POST 受け取り
$employee_id = $_POST['employee_id'] ?? '';
$mode        = $_POST['mode'] ?? '';
$raw_content = $_POST['content'] ?? '';
$tag         = $_POST['tag'] ?? '';

// PHP側でも空白・改行のみをチェック（サーバー側の最終防衛ライン）
if (trim($raw_content) === "") {
    // 空白のみ → 入力画面に戻す
    header("Location: form.php?error=empty");
    exit;
}

// XSS対策
$comment = htmlspecialchars($raw_content, ENT_QUOTES, 'UTF-8');
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="css/style.css">
    <title>ご意見確認</title>
</head>

<body>
    <h2>ご意見内容の確認</h2>
    <p>以下の内容で送信してよろしいですか？</p>

    <p><strong>入力内容：</strong><br><?= $comment ?></p>
    <p><strong>カテゴリ：</strong><?= htmlspecialchars($tag, ENT_QUOTES, 'UTF-8') ?></p>

    <form action="submit.php" method="post">
        <input type="hidden" name="employee_id" value="<?= $employee_id ?>">
        <input type="hidden" name="mode" value="<?= $mode ?>">
        <input type="hidden" name="content" value="<?= $comment ?>">
        <input type="hidden" name="tag" value="<?= $tag ?>">

        <button type="submit">送信</button>
    </form>

    <br>
    <a href="form.php">戻る</a>
</body>
</html>