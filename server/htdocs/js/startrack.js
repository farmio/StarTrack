var starTrack = (function() {
  var colors = ['#7777ff', '#ff7f0e', '#2ca02c'];
  function nodeColor(nid) {    //get a color based on id
    return colors[nid % colors.length];
  }

  var time_format = d3.time.format.utc("%Y-%m-%d %H:%M:%S");

  return {    //public methods
    initData : function() {   //ajax call gets initial data from db
      var jsonData = $.ajax({
          url: "get.php",
          dataType: "json",
          async: false
          }).responseText;

      var obJSON = JSON && JSON.parse(jsonData) || $.parseJSON(jsonData);
      var result = [];

      obJSON.forEach(function(obj) {
        var node_data = [];
        obj.records.forEach(function(dataset) {
          node_data.push({x: time_format.parse(dataset.time), y: dataset.spd})
        })
        result.push({values: node_data
                    ,key: obj.cap
                    ,nid: obj.nid
                    ,color: nodeColor(obj.nid)
                    })
      })
      console.log(result)
      //return array of series objects: [{key: 'Name',nid: NID, values: [{x: 1, y: 1}, ...]', color: '#123456'}, ...]
      return result;
    }
  };

})();

/*These lines are all chart setup.  Pick and choose which chart features you want to utilize. */
nv.addGraph(function() {
  var chart = nv.models.lineWithFocusChart()
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
  var myData = starTrack.initData();   //You need data...

  d3.select('#chart svg')    //Select the <svg> element you want to render the chart in.
      .datum(myData)         //Populate the <svg> element with chart data...
      .call(chart);          //Finally, render the chart!

  //Update the chart when window resizes.
  nv.utils.windowResize(function() { chart.update() });
  return chart;
});
