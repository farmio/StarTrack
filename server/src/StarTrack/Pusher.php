<?php
namespace StarTrack;
use Ratchet\ConnectionInterface;
use Ratchet\Wamp\WampServerInterface;

class Pusher implements WampServerInterface {
    /**
     * A lookup of all the nodes clients have subscribed to
     */
    protected $subscribedNodes = array();
    protected $clients;

    public function __construct() {
        $this->clients = new \SplObjectStorage;
    }

    public function onSubscribe(ConnectionInterface $conn, $node) {
        $this->subscribedNodes[$node->getId()] = $node;
    }

    /**
     * @param string JSON'ified string we'll receive from ZeroMQ
     */
    public function onNodePush($jsonPayload) {
        //echo($jsonPayload);
        /*
        $payload = json_decode($jsonPayload, true);
        var_dump($payload);
        var_dump($this->subscribedNodes);
        // If the lookup node object isn't set there is no one to publish to
        if (!array_key_exists($payload['cap'], $this->subscribedNodes)) {
            return;
        }

        $node = $this->subscribedNodes[$payload['cap']];

        // re-send the data to all the clients subscribed to that category
        $node->broadcast($payload);
        */
        //like a chat...
        foreach ($this->clients as $client) {
            echo("Sending to client: {$client->resourceId}\n");
            $client->send($jsonPayload);
        }
    }
    public function onUnSubscribe(ConnectionInterface $conn, $node) {
      //var_dump($conn);
      echo("Subscription!! {$node}\n");
    }
    public function onOpen(ConnectionInterface $conn) {
      $this->clients->attach($conn);
      echo "New connection! ({$conn->resourceId})\n";
    }
    public function onClose(ConnectionInterface $conn) {
      $this->clients->detach($conn);
      echo "Connection {$conn->resourceId} closed!\n";
    }
    public function onCall(ConnectionInterface $conn, $id, $node, array $params) {
        // In this application if clients send data it's because the user hacked around in console
        echo("Call... \n");
        $conn->callError($id, $node, 'You are not allowed to make calls')->close();
    }
    public function onPublish(ConnectionInterface $conn, $node, $event, array $exclude, array $eligible) {
        // In this application if clients send data it's because the user hacked around in console
        echo("Publish ^^ \n");
        $conn->close();
    }
    public function onError(ConnectionInterface $conn, \Exception $e) {
      echo($e);
    }
}
