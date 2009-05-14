/*
# Community Almanac - A place for your stories.
# Copyright (C) 2009  Douglas Mayle, Robert Marianski,
# Andy Cochran, Chris Patterson

# This file is part of Community Almanac.

# Community Almanac is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Community Almanac is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Community Almanac.  If not, see <http://www.gnu.org/licenses/>.
*/
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

  $('ul.page-media-items').sortable({
    update: function(event, ui) {
      ui.item.parent().children().each(function(index) {
        if (this == ui.item.get(0)) {
          var content = $(this).find('div.mediacontent').get(0);
          $.post('/sort', {id: content.id, index: index})
        }
      });
    },
    handle: 'div.media-tab'
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
      newLi.appendTo('ul.page-media-items');
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
