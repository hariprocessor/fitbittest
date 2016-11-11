
<?php
header("Content-Type: text/html; charset=UTF-8")  //UTF-8 설정
?>

<?php

//db연결
  mysql_connect("localhost", "root", "apmsetup") or die (mysql_error());
  mysql_select_db("fitbit");


  $sql = "SELECT * FROM fitbit";
    $result = mysql_query( $sql ) or die (mysql_error());

 // 출력할 테이블 컬럼명 텍스트 입력
    echo "
    <html>
    <head><title>FitBit</title></head>
    <body>
    <center>
    <H3>Content</H3>
    <table width='1000' border='1'>
    <tr>
    <td width='5%' align='center'>fitbit</td>
    <td width='20%' align='center'>gps</td>
    <td width='10%' align='center'>step</td>
    <td width='25%' align='center'>user</td>
    <td width='15%' align='center'>wifi</td>
     </tr>
";

 // 쿼리의 결과값이 있는 동안 반복을 통한 출력
    while($row = mysql_fetch_array($result))
    {
        echo("
        <tr>
        <td align='center'>$row[fitbit]</td>
        <td align='center'>$row[gps]</td>
        <td align='center'>$row[step]</td>
        <td align='center'>$row[user]</td>
        <td align='center'>$row[wifi]</td>
        </tr>
         ");
      }

 ?>
