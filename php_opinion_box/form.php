<?php
$employee_id = $_POST['id'] ?? '';
$mode = $_POST['mode'] ?? '';
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ご意見入力</title>
</head>
<body>
    <h2>ご意見入力フォーム</h2>

    <form action="confirm.php" method="post">
        <input type="hidden" name="employee_id" value="<?= $employee_id ?>">
        <input type="hidden" name="mode" value="<?= $mode ?>">
        <textarea name="content" rows="5" cols="40"></textarea>
        <br><br>
        <button type="submit">確認</button>
    </form>
</body>
</html>
