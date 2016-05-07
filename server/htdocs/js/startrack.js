(function(window, document, undefined) {
  var chart;
  var chartData;
  var recent = {};

  var dot_threshold = {
    speed: {
      min: 9,
      max: 25
    },
    timer: {
      warning: 60,
      alarm: 120
    }
  }

  var time_format = d3.time.format.utc("%Y-%m-%d %H:%M:%S");

  //var colors = ['#7777ff', '#ff7f0e', '#2ca02c'];
  //var colors = ['#D65076', '#DD4124', '#006E51', '#EFC050', '#4C6A92', '#9B2335', '#009B77', '#B76BA3', '#034F84', '#B93A32', '#79C753', '#955251', '#92B6D5'];
  var colors = ['#7B5141', '#FF7F0E', '#2CA02C', '#A02128', '#154889', '#F7BA0B', '#904684']
  function nodeColor(nid) {    //get a color based on id
    return colors[nid % colors.length];
  }
  var dot_colors = {
    red: 'linear-gradient(to bottom, #F70000, #C1121C)',
    green: 'linear-gradient(to bottom, #48A43F, #008754)',
    orange: 'linear-gradient(to bottom, #DD7907, #E15501)',
    blue: 'linear-gradient(to bottom, #40B3FF, #09F)'
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
    setInterval(updatePanelTimer, 1000);
  });

// ################################
// ## Panels ######################
// ################################

  function recentPanel(nid, data) {
    console.log(data)
    var panel = $('<div class="panel panel-default"></div>')
        .append($('<div class="panel-heading"></div>')
          .css('background-color', convertHex(nodeColor(nid), 75))
          .css('color', '#ffffff')
          .append($('<h3 class="panel-title"></h3>')
            .text(data.cap))
          )
        .append($('<table class="table table-striped">\
                      <colgroup>\
                        <col style="width:35%">\
                        <col style="width:55%">\
                        <col style="width:10%">\
                      </colgroup>\
                    </table>')
          .append($('<tr></tr>')
            .addClass('st-speed')
            .data('speed', data['spd'])
            .append($('<td>Speed</td>')
                   ,$('<td>' + data['spd'] + ' m/h</td>')
                   ,$('<td class="st-dot-parent"> <div class="st-dot"> </div></td>'))
            )
          .append($('<tr></tr>')
            .addClass('st-timer')
            .data('updated', data['time'])
            .append($('<td>Last update</td>')
                   ,$('<td class="st-timer-display">' + panel_timer(data['time']) + '</td>')
                   ,$('<td class="st-dot-parent"> <div class="st-dot"></div> </td>'))
            )
          .append(hideableRows(data))
          );
    return panel;
  }

  function hideableRows(data) {
    var hideables = [];
    var hideableCols = [
       ['Finished in', panel_time_format(data['eta']) ]
      ,['Distance', data['rdm'] + ' m']
      ,['Temperature', data['tmp'] + ' &deg;C']
      ,['Reel', 'Count: ' + data['rot'] + '<br>Layer: ' + data['lay'] + '<br>Row: ' + data['row'] ]
    ];
    hideableCols.forEach(function(col) {
      hideables.push($('<tr></tr>')
        .addClass('hideable')
        .append($('<td></td>')
          .html(col[0]))
        .append($('<td colspan="2"></td>')
          .html(col[1]))
      )}
    );
    return hideables;
  }

  function showRecent() {
    $('#panel-row').empty();
    console.log('showRecent: recent: ', recent)
    $.each(recent, function(key, data) {
      console.log('showRecent: key: ', key);
      $('#panel-row')
        .append($('<div></div>')
          .addClass('col-xs-12 col-sm-6 col-md-4')
          .append($('<a href="#expand" class="link-panel"></a>')
            .append(recentPanel(key, data))
          )
        );
    });
    setExpandPanel();
  }

  function setExpandPanel() {
    $('.link-panel').each(function() {
      $(this).click(function() {
        $(this).find('.hideable').each(function() {
          $(this).css('display') === 'none' ? $(this).css('display', 'table-row') : $(this).css('display', 'none')
        });
        //console.log();
        return false;
      });
    })
  }

  function panel_timer(last) {
    return panel_time_format(seconds_offset(last));
  }

  function panel_time_format(seconds) {
    return seconds < 60 ? (seconds + ' sec')
            : seconds < 600 ? (Math.floor(seconds / 60) + ' min ' + (seconds % 60) + ' sec')
              : seconds < 3600 ? (Math.floor(seconds / 60) + ' min')
                : seconds < 36000 ? (Math.floor(seconds / 3600) + ' h ' + Math.floor((seconds % 3600) / 60) + ' min')
                  : (Math.floor(seconds / 3600) + ' h');
  }

  function speed_dot_color(speed) {
    var color;
    switch(true) {
      case (speed < dot_threshold.speed.min):
        color = dot_colors.red;
        break;
      case (speed > dot_threshold.speed.min):
        color = dot_colors.red;
        break;
      default:
        color = dot_colors.green;
        break;
    }
    return color;
  }

  function timer_dot_color(seconds) {
    var color;
    switch(true) {
      case (seconds > dot_threshold.timer.alarm):
        color = dot_colors.red;
        break;
      case (seconds > dot_threshold.timer.warning):
        color = dot_colors.orange;
        break;
      default:
        color = dot_colors.green;
        break;
    }
    return color;
  }

  //every second
  function updatePanelTimer() {
    $('.st-timer').each(function() {
      var seconds = seconds_offset($(this).data('updated'));
      $(this).find('.st-timer-display').text(panel_time_format(seconds));
      $(this).find('.st-dot').css('background', timer_dot_color(seconds));
    })
  }

// ################################
// ## Chart #######################
// ################################

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

// ################################
// ## Helpers #####################
// ################################

  function jsonDecode(jsonData) {
    var obJSON = JSON && JSON.parse(jsonData) || $.parseJSON(jsonData);
    return obJSON;
  }

  function seconds_offset(time) {
    return Math.floor((Date.now() - time) / 1000);
  }

  function convertHex(hex,opacity) {
    hex = hex.replace('#','');
    r = parseInt(hex.substring(0,2), 16);
    g = parseInt(hex.substring(2,4), 16);
    b = parseInt(hex.substring(4,6), 16);
    result = 'rgba('+r+','+g+','+b+','+opacity/100+')';
    return result;
  }

// ################################
// ## Socket ######################
// ################################

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

  function pushData(latest) {
    latest.recent.time = time_format.parse(latest.recent.time);
    latest.recent.cap = latest.cap;
    recent[latest.nid] = latest.recent;
    console.log('pushData: ', recent);
    showRecent();
    chartAddPoint(latest.nid, latest.recent.spd, latest.recent.time);
  }

// ################################
// ## Database ####################
// ################################

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
      //console.log(obj.records);
      recent[obj.nid] = {};
      recent[obj.nid] = obj.records[obj.records.length - 1];
      recent[obj.nid].cap = obj.cap;
    })

    showRecent();
    //return array of series objects: [{key: 'Name',nid: NID, values: [{x: 1, y: 1}, ...]', color: '#123456'}, ...]
    return result;
  };

})(window, document);
