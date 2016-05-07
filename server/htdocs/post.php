<?php
require '../vendor/autoload.php';
use \Firebase\JWT\JWT;

$config = require '../config.php';
$dbPath = '../data/node_data.sqlite';

$logger = new Katzgrau\KLogger\Logger('../log/');

date_default_timezone_set('UTC');

if( isset($_POST['jwt']) ){

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
      webSocketPush($claims);
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

  global $logger;
  global $dbPath;

  try {

    $dbh = new SQLite3($dbPath);

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
                mws NUMERIC
              );";
    #$dbh->exec($query);

    #$esc_string = SQLite3::escapeString($data->pos);

    $query .= "INSERT INTO node_{$data->nid}
                (rot, spd, row, lay, rdm, eta, tmp, bat, wsp, sli, mws)
                VALUES ({$data->rot},
                        {$data->spd},
                        {$data->row},
                        {$data->lay},
                        {$data->rdm},
                        {$data->eta},
                        {$data->tmp},
                        {$data->bat},
                        {$data->wsp},
                        {$data->sli},
                        {$data->mws}
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
  global $logger;
  global $dbPath;

  try {

    $dbh = new SQLite3($dbPath);

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

function webSocketPush($data) {
  global $logger;

  try {

    $message = [];
    $message['nid'] = (int) $data->nid;
    $message['cap'] = "Node {$data->nid}";
    // 'time' and 'id' are created by the database - we just need 'time'
    $message['recent'] = ['time' => date('Y-m-d H:i:s', time())
                          ,'rot' => (int) $data->rot
                          ,'spd' => (float) $data->spd
                          ,'row' => (int) $data->row
                          ,'lay' => (int) $data->lay
                          ,'rdm' => (int) $data->rdm
                          ,'eta' => (int) $data->eta
                          ,'tmp' => (float) $data->tmp
                          ,'bat' => (int) $data->bat
                          ,'wsp' => (int) $data->wsp
                          ,'sli' => (int) $data->sli
                          ,'mws' => (int) $data->mws];

    $context = new ZMQContext();
    $socket = $context->getSocket(ZMQ::SOCKET_PUSH, 'st_pusher');
    $socket->connect("tcp://localhost:5555");

    $socket->send(json_encode($message));

  } catch (Exception $e) {

    $logger->error("Push Error - " . $e);

  }

}

?>
