<?php
require '../vendor/autoload.php';
require '../jwt_key.php';
use \Firebase\JWT\JWT;


$logger = new Katzgrau\KLogger\Logger('../log/');

if( $_POST['jwt'] ){
  try {
    $decoded = JWT::decode($_POST['jwt'], $key, array('HS256'));
    $logger->info($_SERVER['REMOTE_ADDR'] . " - Temp: " . $decoded->temp . " Pos: " . $decoded->pos . " Spd: " . $decoded->spd);
  } catch (Exception $e) {
    $logger->error("Token Error - " . $e->getMessage());
  }
  try {
    $dbh = new SQLite3('../data/node_data.sqlite');

    //create new Table if it doesn't exist
    $query = "CREATE TABLE IF NOT EXISTS node_{$decoded->nid} (
                Time DATETIME DEFAULT CURRENT_TIMESTAMP,
                Speed NUMERIC,
                Position TEXT,
                Temperature NUMERIC)";
    $dbh->exec($query);

    $esc_string = SQLite3::escapeString($decoded->pos);
    $query = "INSERT INTO node_{$decoded->nid} (Speed, Position, Temperature) VALUES
      ({$decoded->spd}, '{$esc_string}', {$decoded->temp})";
    $dbh->exec($query);
  } catch (Exception $e) {
    $logger->error("DB Error - " . $dbh->lastErrorMsg());
  } finally {
    $dbh->close();
  }
}

?>
