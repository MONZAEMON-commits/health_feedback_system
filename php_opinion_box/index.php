<?php
$employee_id = $_GET['id'] ?? '';
?>
<!DOCTYPE html>
<html>
<body>
    <h2>投稿形式を選択</h2>

    <form action="form.php" method="post">

        <input type="hidden" name="employee_id" value="<?= $employee_id ?>">

        <label>
            <input type="radio" name="mode" value="anonymous" checked>
            匿名投稿（完全に匿名で投稿）
        </label><br>

        <label>
            <input type="radio" name="mode" value="semi">
            準匿名（性別・年代を入力）
        </label><br>

        <label>
            <input type="radio" name="mode" value="signed">
            署名（氏名・部署・年齢を入力）
        </label><br><br>
        <button type="submit">次へ</button>

    </form>
</body>
</html>
