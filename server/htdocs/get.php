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
      $node_data = array();
      while ($node_table = $result->fetchArray(SQLITE3_NUM)[0]) {
        array_push($node_data, new NodeData($node_table));
      }
      return $node_data;
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

      //var_dump($result->fetchArray(SQLITE3_ASSOC));

      $table = array('cols' => array(
          // Labels for your chart, these represent the column titles.
          array('label' => 'Time', 'type' => 'datetime'),
          array('label' => 'Temperature', 'type' => 'number')
        ),
        'rows' => array());

      // hardcoded Timezones here
      $db_timezone = new DateTimeZone('UTC');
      $user_timezone = new DateTimeZone('Europe/Vienna');

      // Extract the information from $result
      while ($r = $result->fetchArray(SQLITE3_ASSOC)) {
        // assumes dates are patterned 'yyyy-MM-dd hh:mm:ss'
        $db_time = new DateTime($r['Time'], $db_timezone);
        $db_time->setTimeZone($user_timezone);

        $java_time = $db_time->format('Y-m-d H:i:s');

        preg_match('/(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})/', $java_time, $match);
        $year = (int) $match[1];
        $month = (int) $match[2] - 1; // convert to zero-index to match javascript's dates
        $day = (int) $match[3];
        $hours = (int) $match[4];
        $minutes = (int) $match[5];

        $seconds = (int) $match[6];

        array_push($table['rows'], array('c' => array(
          array('v' => "Date($year, $month, $day, $hours, $minutes, $seconds)"),
          array('v' => (float) $r['Temperature'])
        )));

      }

      // convert data into JSON format
      $jsonTable = json_encode($table);

      return $jsonTable;

    } catch (Exception $e) {
      $logger->error("DB Error - " . $this->lastErrorMsg());
    }
  }
}

$node = new Node();
$nodes = $node->getNodeTables();
//var_dump($nodes);
echo($nodes[0]->getLastN(600));

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
