<?php
$employee_id = $_REQUEST['employee_id'] ?? '';
$mode = $_POST['mode'] ?? '';
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="css/style.css">
    <title>ご意見入力</title>

    <script>
        function validateForm() {
            const text = document.querySelector('textarea[name="content"]').value;

            // 空白・改行のみの場合を弾く
            if (text.trim().length === 0) {
                alert("空白のみの入力はできません。内容を入力してください。");
                return false;
            }
            return true;
        }
    </script>
</head>

<body>
    <h2>ご意見入力フォーム</h2>

    <form action="confirm.php" method="post" onsubmit="return validateForm();">
        <input type="hidden" name="employee_id" value="<?= $employee_id ?>">
        <input type="hidden" name="mode" value="<?= $mode ?>">

        <textarea name="content" rows="5" cols="40" required></textarea>

        <label>カテゴリ</label>
        <select name="tag" required>
            <option value="">選択してください</option>
            <option value="業務改善">業務改善</option>
            <option value="人間関係">人間関係</option>
            <option value="設備・環境">設備・環境</option>
            <option value="安全性">安全性</option>
            <option value="その他">その他</option>
        </select>

        <br><br>
        <button type="submit">確認</button>
    </form>
</body>
</html>