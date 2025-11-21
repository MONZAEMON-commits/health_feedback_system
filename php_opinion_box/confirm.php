<?php
$comment = htmlspecialchars($_POST['content'], ENT_QUOTES, 'UTF-8');
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
    <p>入力内容：<?= $comment?></p>
        <form action="submit.php" method="post">
            <input type="hidden" name="content" value="<?= htmlspecialchars($_POST['content'], ENT_QUOTES, 'UTF-8')?>">
            <input type="hidden" name="employee_id" value="<?= $_POST["employee_id"] ?>">
            <button type="submit">送信</button>
        </form>
    <br>
    <a href="form.php">戻る</a>
</body>
</html>