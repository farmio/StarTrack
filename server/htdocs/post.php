<?php
require '../vendor/autoload.php';
require '../jwt_key.php';
use \Firebase\JWT\JWT;


$logger = new Katzgrau\KLogger\Logger('../log/');

if( $_POST['jwt'] ){
  try {
    $decoded = JWT::decode($_POST['jwt'], $key, array('HS256'));
    $logger->info($_SERVER['REMOTE_ADDR'] . " - " . $decoded->temp);
  } catch (Exception $e) {
    $logger->error("Token Error - " . $e->getMessage());
  }
  try {
    $db = sqlite_open('../data/node_data.sqlite', 0666, $error);
    $query = "SELECT * FROM sqlite_master WHERE name ='node_" . $decoded->nid . "' and type='table'";
    $result = sqlite_exec($db, $query, $error);
    if (!$result) {
      //create new Table if it doesn't exist
      $query = 'CREATE TABLE node_' . $decoded->nid . ' (
                  Time DATETIME DEFAULT CURRENT_TIMESTAMP,
                  Speed NUMERIC,
                  Postiton TEXT,
                  Temperature NUMERIC)';
      if(!$db->queryExec($query, $error)) {
        $logger->error("DB Error creating table - " . $error);
        exit();
      } else {
        $logger->notice("DB new table created: node_" . $decoded->nid);
      }
    }

    $query = 'INSERT INTO node_' . $decoded->nid . ' (Speed, Postiton, Temperature) VALUES
      (' . $decoded->spd . ', ' . $decoded->pos . ', ' . $decoded->temp . ')';
    $result = sqlite_exec($db, $query, $error);
  } catch (Exception $e) {
    $logger->error("DB Error - " . $error);
  } finally {
    sqlite_close($db);
  }
}

?>
