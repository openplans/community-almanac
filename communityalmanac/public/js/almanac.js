$(document).ready(function() {

  // add the title to the submit button form
  $('#submit-button-form').submit(function() {
      var title = $('#page-title').val();
      var newinput = $('<input type="hidden" name="name" value="' + title + '" />');
      newinput.appendTo($(this));
      return true;
  });

  // clicking on page title erases text already there
  $('#page-title').focus(function() {
      if ($(this).val() == "Page Name") {
        $(this).val("");
      }
  }).blur(function() {
      if ($(this).val() == "") {
        $(this).val("Page Name");
      }
  });

  var tools = [{
      link: $('#text-tool'),
      submitfn: submit_handler
    }, {
      link: $('#map-tool'),
      attach_form_behaviors: map_behaviors,
      submitfn: submit_handler
    }
  ];

  for (var i = 0; i < tools.length; i++) {
      var fn = function(i) {
        var tool = tools[i];
        var link = tool.link;
        var submitfn = tool.submitfn;
        var attach_form_behaviors = tool.attach_form_behaviors;

        // when somebody tries to add a particular media type, fetch the form from
        // the server, and attach the behavior to it
        link.click(function(e) {
          e.preventDefault();
          var url = $(this).attr('href');

          var formcontainer = $('#form-container');
          $.get(url, null, function(data) {
            formcontainer.empty();
            formcontainer.show();
            $(data).appendTo(formcontainer).hide().fadeIn('fast', function() {
              $(this).find('textarea').focus();
            });
            $('form.media-item a.media-cancel').click(function(e) {
              e.preventDefault();
              formcontainer.fadeOut('normal', function() { $(this).empty(); });
            });
            $('form.media-item').submit(submitfn);
            // attach custom behaviors if needed
            if (attach_form_behaviors) {
              attach_form_behaviors($(this));
            }
          });
        });
      }
      fn(i);
    }
});

function submit_handler(e) {
  e.preventDefault();
  var url = $(this).attr('action');
  var data = $('form.media-item').serialize();
  var formcontainer = $('#form-container');

  $.ajax({
    contentType: 'application/x-www-form-urlencoded',
    data: data,
    success: function(data, textStatus) {
      formcontainer.empty();
      var newLi = $('<li></li>');
      newLi.appendTo($('.session-data ul'));
      $('<div>' + data + '</div>').appendTo(newLi).hide().fadeIn('slow');
      },
    type: "POST",
    url: url
  });
};

function map_behaviors(formcontainer) {
  //var bounds = new OpenLayers.Bounds(
  //  -2.003750834E7,-2.003750834E7,
  //  2.003750834E7,2.003750834E7
  //);
  var map = new OpenLayers.Map('map', {
    projection: new OpenLayers.Projection('EPSG:900913'),
    displayProjection: new OpenLayers.Projection('EPSG:4326'),
    //maxExtent: bounds,
    //controls: [
    //    new OpenLayers.Control.Navigation({zoomWheelEnabled: false}),
    //    new OpenLayers.Control.PanZoom()
    //]
    });
  var baseLayer = new OpenLayers.Layer.Google('streets', {sphericalMercator: true});
  // XXX right now we have this dummy layer as a proof of concept
  var dummyLayer = new OpenLayers.Layer.Markers('dummy');
  // Center on 349 West 12th St. by default for now
  var center = new OpenLayers.LonLat(-74.006952, 40.738067);
  var storyIcon = new OpenLayers.Icon('/js/img/story_marker.png');
  var dummyMarker = new OpenLayers.Marker(center, storyIcon);
  dummyLayer.addMarker(dummyMarker);
  map.addLayers([baseLayer, dummyLayer]);
  var bounds = new OpenLayers.Bounds();
  bounds.extend(center);
  map.zoomToExtent(bounds);
  the_map = map;
  the_feature = dummyMarker;
}
