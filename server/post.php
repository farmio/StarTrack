<?php
use \Firebase\JWT\JWT;

$key = "example_key";

$logger = new Katzgrau\KLogger\Logger('../log/');

if( $_POST["jwt"] ){
  try {
    $decoded = JWT::decode($_POST["jwt"], $key, array('HS256'));
    $logger->info($_SERVER['REMOTE_ADDR'] . " - " . $decoded);
  } catch (Exception $e) {
    echo $e->getMessage();
  }
}

?>
