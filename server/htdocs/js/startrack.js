(function(window, document, undefined) {
  var chart;
  var chartData;
  var recent = [];

  var time_format = d3.time.format.utc("%Y-%m-%d %H:%M:%S");

  var colors = ['#7777ff', '#ff7f0e', '#2ca02c'];
  function nodeColor(nid) {    //get a color based on id
    return colors[nid % colors.length];
  }

  function initData() {   //ajax call gets initial data from db
    var jsonData = $.ajax({
        url: "get.php",
        dataType: "json",
        async: false
        }).responseText;

    var obJSON = jsonDecode(jsonData);
    var result = [];

    obJSON.forEach(function(obj) {
      var node_data = [];
      obj.records.forEach(function(dataset) {
        dataset.time = time_format.parse(dataset.time);
        node_data.push({x: dataset.time, y: dataset.spd})
      });
      result.push({values: node_data
                  ,key: obj.cap
                  ,nid: obj.nid
                  ,color: nodeColor(obj.nid)
                });
      //console.log(obj.records.slice(-1));
      recent[obj.nid] = obj.records.slice(-1);
    })
    //console.log(result);
    console.log(recent);
    //return array of series objects: [{key: 'Name',nid: NID, values: [{x: 1, y: 1}, ...]', color: '#123456'}, ...]
    return result;
  };

  function pushData(latest) {
    latest.recent.time = time_format.parse(latest.recent.time);
    recent[latest.nid] = [latest.recent];
    console.log(recent);
    chartAddPoint(latest.nid, latest.recent.spd, latest.recent.time);
  }

  /*These lines are all chart setup.  Pick and choose which chart features you want to utilize. */
  nv.addGraph(function() {
    chart = nv.models.lineWithFocusChart()
                  .margin({left: 100, bottom: 50})  //Adjust chart margins to give the x-axis some breathing room.
                  //.useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                  //.transitionDuration(350)  //how fast do you want the lines to transition?
                  .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
                  ;

    chart.xAxis     //Chart x-axis settings
        .rotateLabels(-45)
        .tickFormat(function(d) {   //different format for tooltip and axis
            if (this === window) return d3.time.format("%Y-%m-%d %H:%M:%S")(new Date(d));
            return d3.time.format("%H:%M")(new Date(d));
          })
        .showMaxMin(0);             //showMaxMin would use tooltip format

    chart.yAxis     //Chart y-axis settings
        .axisLabel('Speed m/h')
        .tickFormat(d3.format('.02f'));

    chart.x2Axis    //Focus x-axis settings
        .tickFormat(function(d) {
            return d3.time.format("%H:%M")(new Date(d))
          });

    chart.y2Axis    //Focus y-axis settings
        .showMaxMin(0)
        //.tickFormat(d3.format('.02f'));

    chart.xScale(d3.time.scale());

    /* Done setting the chart up? Time to render it!*/
    chartData = initData();   //You need data...

    d3.select('#chart svg')  //Select the <svg> element you want to render the chart in.
                  .datum(chartData)         //Populate the <svg> element with chart data...
                  .call(chart);          //Finally, render the chart!

    //Update the chart when window resizes.
    nv.utils.windowResize(function() { chart.update() });
    //console.log(chartData)
    return chart;
  });

  function chartAddPoint(nid, yValue, xValue) {   // adds new point (with x: Date.now)
    xValue = xValue || new Date(Date.now());
    var point = {x: xValue, y: yValue};
    chartData.find(function (d) {
      return d['nid'] === nid;
      }).values.push(point);
    chart.update();
  }

  function jsonDecode(jsonData) {
    var obJSON = JSON && JSON.parse(jsonData) || $.parseJSON(jsonData);
    return obJSON;
  }

  // for testing...

  function buttonClicked(bid) {
    var randInt = function() {
      return Math.floor((Math.random() * 10) + 1)
    };
    chartAddPoint(bid, randInt());
  }

  function socketConnect() {
    try{

    	var socket;
    	var host = "wss://" + window.location.host + ":443/socket/";
      var socket = new WebSocket(host);

      console.log('Socket Status: '+socket.readyState);

      socket.onopen = function(){
     		 console.log('Socket Status: '+socket.readyState+' (open)');
      }

      socket.onmessage = function(msg){
     		 console.log('Received: '+msg.data);
         try {
           var json = jsonDecode(msg.data);
           pushData(json);
         } catch(e) {
           return
         }
      }

      socket.onclose = function(){
     		 console.log('Socket Status: '+socket.readyState+' (Closed)');
      }

    } catch(exception){
     	message('<p>Error'+exception);
    }
  }

  function message(msg){
	   console.log(msg);
  }

/*
var connection = new autobahn.Connection({
         url: 'wss://' + window.location.host + ':8080/socket',
         realm: 'realm1'
      });

connection.onopen = function (session) {

   // 1) subscribe to a topic
   function onevent(args) {
      console.log("Event:", args[0]);
   }
   session.subscribe('Node 2', onevent);

   // 2) publish an event
   session.publish('com.myapp.hello', ['Hello, world!']);

   // 3) register a procedure for remoting
   function add2(args) {
      return args[0] + args[1];
   }
   session.register('com.myapp.add2', add2);

   // 4) call a remote procedure
   session.call('com.myapp.add2', [2, 3]).then(
      function (res) {
         console.log("Result:", res);
      }
   );
};
*/



  $(document).ready(function() {
    $('#button1').click(function() {buttonClicked(1)})
    $('#button2').click(function() {buttonClicked(2)})
    $('#button3').click(function() {buttonClicked(3)})
    //$('#button4').click(function() {buttonClicked(4)})

    if(!("WebSocket" in window)){
		  $('<p>You need a browser that supports WebSockets for live updates.</p>').appendTo('#container');
	  } else {
      //The user has WebSockets
	    socketConnect();
      //connection.open();
	  }
  });

})(window, document);
