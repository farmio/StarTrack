<?PHP
//performance test
//$rustart = getrusage();

date_default_timezone_set('UTC');

require '../vendor/autoload.php';

$db_path = '../data/node_data.sqlite';

$logger = new Katzgrau\KLogger\Logger('../log/');

class Node extends SQLite3 {

  public function __construct() {
    global $db_path;
    $this->open($db_path);
  }

  public function __destruct() {
    $this->close();
  }

  public function getNodeTables() {
    //$query = "SELECT tbl_name FROM sqlite_master WHERE type = 'table' AND tbl_name LIKE 'node%'";
    $query = "SELECT tbl_name FROM sqlite_master WHERE tbl_name LIKE 'node%'";
    $result = $this->query($query);
    if ($result->fetchArray()[0] == null) {
      $logger->error("DB No matching Table found - " . $this->lastErrorMsg());
      return 0;
    } else {
      $result->reset();
      $nodes_data = array();
      while ($node_table = $result->fetchArray(SQLITE3_NUM)[0]) {
        $node_data = array();
        $nid = (int) str_replace('node_', '', $node_table);
        $node_data['nid'] = $nid;
        $node_data['cap'] = 'Node ' . $nid;
        $data = new NodeData($node_table);
        $node_data['records'] = $data->getLastN(600);
        $nodes_data[] = $node_data;
      }
      return $nodes_data;
    }
  }
}

class NodeData extends SQLite3 {

  private $table_name;

  public function __construct($table_name) {
    global $db_path;
    $this->table_name = $table_name;
    $this->open($db_path);
  }

  public function __destruct() {
    $this->close();
  }

  public function getLastN($lines) {
    try {
      $query = "SELECT * FROM {$this->table_name} LIMIT {$lines} OFFSET (SELECT COUNT(*) FROM {$this->table_name})-{$lines}";
      $result = $this->query($query);

      $table = array();
      while ($r = $result->fetchArray(SQLITE3_ASSOC)) {
        array_push($table, $r);
      };

      return $table;

    } catch (Exception $e) {
      $logger->error("DB Error - " . $this->lastErrorMsg());
    }
  }
}

$node = new Node();

echo(json_encode( $node->getNodeTables() ));

/*
//performance test
function rutime($ru, $rus, $index) {
    return ($ru["ru_$index.tv_sec"]*1000 + intval($ru["ru_$index.tv_usec"]/1000))
     -  ($rus["ru_$index.tv_sec"]*1000 + intval($rus["ru_$index.tv_usec"]/1000));
}

$ru = getrusage();
echo "This process used " . rutime($ru, $rustart, "utime") .
    " ms for its computations\n";
echo "It spent " . rutime($ru, $rustart, "stime") .
    " ms in system calls\n";
*/

// gibt Namen aller tables zurück
// SELECT tbl_name FROM sqlite_master WHERE type = 'table';
//
// letzten 10 rows von hinten - 10 mit COUNT vergleichen?!
// SELECT * FROM mytable LIMIT 10 OFFSET (SELECT COUNT(*) FROM mytable)-10;
//
// rows der letzten 4 minuten
// SELECT * FROM node_1 WHERE Time > datetime('now','-4 minutes');
// OFFSET ist weit schneller.
?>
