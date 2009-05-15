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
  var featureLayer = new OpenLayers.Layer.Vector('feature');
  var onActivate = function() { featureLayer.destroyFeatures(); };
  var drawPoint = new OpenLayers.Control.DrawFeature(
    featureLayer, OpenLayers.Handler.Point,
    {'displayClass': 'olControlDrawFeaturePoint',
     'eventListeners': {'activate': onActivate}});
  var drawPath = new OpenLayers.Control.DrawFeature(
    featureLayer, OpenLayers.Handler.Path,
    {'displayClass': 'olControlDrawFeaturePath',
     'eventListeners': {'activate': onActivate}});
  var drawPolygon = new OpenLayers.Control.DrawFeature(
    featureLayer, OpenLayers.Handler.Polygon,
    {'displayClass': 'olControlDrawFeaturePolygon',
     'eventListeners': {'activate': onActivate}});
  var deactivateAllEditingControls = function() {
    drawPoint.deactivate();
    drawPath.deactivate();
    drawPolygon.deactivate();
  };
  var featureAdded = function(evt) {
    deactivateAllEditingControls();
    var formatter = new OpenLayers.Format.GeoJSON();
    var str = formatter.write(evt.feature.geometry);
    $('#feature-geometry').val(str);
  };
  featureLayer.events.on({featureadded: featureAdded});
  var panelControls = [
   new OpenLayers.Control.Navigation({zoomWheelEnabled: false}),
   new OpenLayers.Control.PanZoom(),
   drawPoint,
   drawPath,
   drawPolygon
  ];
  var toolbar = new OpenLayers.Control.Panel({
     displayClass: 'olControlEditingToolbar',
     defaultControl: panelControls[0]
  });
  toolbar.addControls(panelControls);

  map = new OpenLayers.Map('map', {
    projection: new OpenLayers.Projection('EPSG:900913'),
    displayProjection: new OpenLayers.Projection('EPSG:4326'),
    maxExtent: new OpenLayers.Bounds(-14323800, 2299000, -7376800, 7191400),
    });
  var baseLayer = new OpenLayers.Layer.Google('streets', {sphericalMercator: true, type: G_PHYSICAL_MAP});
  map.addLayer(baseLayer);
  map.addControl(toolbar);
  map.addLayer(featureLayer);
  var almanac_center_url = $('.almanac-center-url').attr('href');
  $.getJSON(almanac_center_url, {}, function(data) {
    var lng = data.lng;
    var lat = data.lat;
    var center = new OpenLayers.LonLat(lng, lat);
    center.transform(new OpenLayers.Projection('EPSG:4326'), map.getProjectionObject());
    map.setCenter(center, 12);
  });
}
