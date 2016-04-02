<?php
require '../vendor/autoload.php';
use \Firebase\JWT\JWT;

$config = require '../config.php';
$dbPath = '../data/node_data.sqlite'

$logger = new Katzgrau\KLogger\Logger('../log/');


if( $_POST['jwt'] ){

  try {

    $decoded = JWT::decode($_POST['jwt'], $config['jwt_key'], array('HS256'));
    http_response_code(202);
    readToken($decoded);

  } catch (Exception $e) {

    $logger->error("Token Error - " . $e->getMessage());
    http_response_code(401);

  }

} else {
  http_response_code(400);
}


function readToken($claims) {

  switch($claims->act) {
    case "push":
      dbPush($claims);
      break;
    case "start":
      dbReset($claims->nid);
      break;
    case "stop":
      break;
    default:
      http_response_code(422);
  }

}


function dbPush($data) {

  try {

    $dbh = new SQLite3(global $dbPath);

    //create new Table if it doesn't exist
    $query = "CREATE TABLE IF NOT EXISTS node_{$data->nid} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time DATETIME DEFAULT CURRENT_TIMESTAMP,
                rot NUMERIC,
                spd NUMERIC,
                row NUMERIC,
                lay NUMERIC,
                rdm NUMERIC,
                eta NUMERIC,
                tmp NUMERIC,
                bat NUMERIC,
                wsp NUMERIC,
                sli NUMERIC,
                mws NUMERIC,
              );";
    #$dbh->exec($query);

    #$esc_string = SQLite3::escapeString($data->pos);

    $query .= "INSERT INTO node_{$data->nid}
                (rot, spd, row, lay, rdm, eta, tmp, bat, wsp, sli, mws)
                VALUES ($data->rot,
                        $data->spd,
                        $data->row,
                        $data->lay,
                        $data->rdm,
                        $data->eta,
                        $data->tmp,
                        $data->bat,
                        $data->wsp,
                        $data->sli,
                        $data->mws,
                        );";
    $dbh->exec($query);

    http_response_code(201);

  } catch (Exception $e) {

    $logger->error("DB Error - " . $dbh->lastErrorMsg());
    http_response_code(500);

  } finally {

    $dbh->close();

  }

}

function dbReset($nid) {

  try {

    $dbh = new SQLite3(global $dbPath);

    $query = "DROP TABLE IF EXISTS node_{$nid};
              VACUUM;";

    $dbh->exec($query);

    http_response_code(200);

  } catch (Exception $e) {

    $logger->error("DB Error - " . $dbh->lastErrorMsg());
    http_response_code(500);

  } finally {

    $dbh->close();

  }

}

?>
