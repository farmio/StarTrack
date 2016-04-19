(function(window, document, undefined) {
  var chart;
  var chartData;
  var recent = {};

  var time_format = d3.time.format.utc("%Y-%m-%d %H:%M:%S");

  // '#7777ff', '#ff7f0e', '#2ca02c'      '#f07c4a'
  // orange: ('#f0ad4e',) '#f4ac5e', '#f6b876'
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
      console.log(obj.records);
      recent[obj.nid] = {};
      recent[obj.nid] = obj.records[obj.records.length - 1];
      recent[obj.nid].cap = obj.cap;


    })
    //console.log(result);
    //console.log("init recent: " + recent);
    showRecent();
    //return array of series objects: [{key: 'Name',nid: NID, values: [{x: 1, y: 1}, ...]', color: '#123456'}, ...]
    return result;
  };

// is this pushing an array or an object?
  function pushData(latest) {
    latest.recent.time = time_format.parse(latest.recent.time);
    latest.recent.cap = latest.cap;
    recent[latest.nid] = latest.recent;
    console.log('pushData: ', recent);
    showRecent();
    chartAddPoint(latest.nid, latest.recent.spd, latest.recent.time);
  }

  function recentPanel(nid, data) {
    console.log(data)
    var panel = $('<div></div>')
      .addClass('col-sm-4')
      .append($('<div></div>')
        .addClass('panel panel-default')
        //.css('border-color', nodeColor(nid))
        //.css('background', nodeColor(nid))
        .append($('<div></div>')
          .addClass('panel-heading')
          .css('background-color', convertHex(nodeColor(nid), 75))
          .css('color', '#ffffff')
          .append($('<h3></h3>')
            .addClass('panel-title')
            .text(data.cap)
          )
        ).append($('<div></div>')
          .addClass('panel-body')
          .append($('<p><b>Speed: </b>' + data['spd'] + ' m/h</p>'))
          .append($('<p><b>Last update: </b>' + time_format(data['time']) + ' that was before ' + (data['time'] - Date.now()) + ' seconds.</p>'))
        )
      );
    return panel;
  }

  function showRecent() {
    $('#panel-row').empty();
    console.log('showRecent: recent: ', recent)
    $.each(recent, function(key, data) {
      console.log('showRecent: key: ', key);
      $('#panel-row').append(recentPanel(key, data));
    });
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

  function convertHex(hex,opacity) {
    hex = hex.replace('#','');
    r = parseInt(hex.substring(0,2), 16);
    g = parseInt(hex.substring(2,4), 16);
    b = parseInt(hex.substring(4,6), 16);
    result = 'rgba('+r+','+g+','+b+','+opacity/100+')';
    return result;
  }

  function socketConnect() {
    try{

    	var socket;
    	var host = "wss://" + window.location.host + ":443/socket/";
      var socket = new WebSocket(host);

      console.log('Socket Status: '+socket.readyState);

      socket.onopen = function(){
     		 console.log('Socket Status: '+socket.readyState+' (open)');
         $('#info-container').text('Live updates ready.');
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
         $('#info-container').html('No connection to Websocket. <a href="#reconnect" id="ws-reconnect">Try to reconnect.</a>');
         $('#ws-reconnect').click(function() {
           $('#info-container').text('Establishing websocket connection...');
           socketConnect();
           return false;    //prevents link form being followed by browser
         });
      }

    } catch(exception){
     	message('<p>Error'+exception);
    }
  }

  function message(msg){
	   console.log(msg);
  }


  $(document).ready(function() {
    if(!("WebSocket" in window)){
		  $('#info-container').text('You need a browser that supports WebSockets for live updates.');
	  } else {
      //The user has WebSockets
      $('#info-container').text('Establishing websocket connection...');
	    socketConnect();
      //connection.open();
	  }
  });

  // for testing...

  function buttonClicked(bid) {
    var randInt = function() {
      return Math.floor((Math.random() * 10) + 1)
    };
    chartAddPoint(bid, randInt());
  }

})(window, document);
