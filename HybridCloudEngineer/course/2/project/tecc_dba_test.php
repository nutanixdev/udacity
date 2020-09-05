
  <html>
  <head>
    <title>TECC Test Web Application</title>
  </head>
  <body>
   <h1>TECC Test Web Application</h1>
  <?php
  try {
    $dbh = new PDO('mysql:host=DATABASE_ADDRESS;dbname=webapp', 'tecc_webuser', 'end-user-provided-password', array(
      PDO::ATTR_PERSISTENT => true,
      PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    ));

    // ensure there is at least 1 row of data for the app to read
    $data = $dbh->query("INSERT INTO tecc_dba_test (id, time, comment) VALUES (NULL, CURRENT_TIMESTAMP, "$_SERVER['SCRIPT_NAME']")");

    $data = $dbh->query('SELECT MAX(id) AS count FROM tecc_dba_test')->fetchAll(PDO::FETCH_COLUMN);
    $count = $data[0]; //print_r($data);
    $data = $dbh->query("SELECT time, comment FROM tecc_dba_test WHERE id = $count")->fetchAll(PDO::FETCH_ASSOC);
    $time = $data[0]['time'];
    $comment = $data[0]['comment'];

    echo "<p>Database records: $count</p>\n";
    echo "<p>Last comment: $comment, on: $time</p>\n";
    echo "<h3>Web docroot: $_SERVER['DOCUMENT_ROOT'], file: $_SERVER['SCRIPT_NAME']</h3>\n";

    $dbh = null;
  }
  catch (PDOException $e) {
    print "Error!: " . $e->getcomment() . "<br/>";
    print phpinfo();
    die();
  }
  ?></body>
  </html>
