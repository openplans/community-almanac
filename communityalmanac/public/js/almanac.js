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

  // on pages, have the add a comment link unhide the form
  $("#comment-form").hide();
  $("#comment-bttn").click(function() {
    $("#comment-form").slideDown("fast");
    $(this).slideUp("normal");
    return false;
    });
  // and have the comment link submit the form itself
  $('#comment-submit a.comment-link').click(function() {
    $('#comment-form').submit();
    return false;
  });

  // click on the sidebar publish button submits the form
  var addPageBtn = $('#add-page-bttn a');
  // but only on the create page, because the id is reused
  // for the button style
  if (addPageBtn.text() == 'Publish this page!') {
    addPageBtn.click(function() {
      $('#submit-button-form').submit();
      return false;
    });
  }

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

  // page title input on page create should be focused by default
  $('#page-title').focus();

  // display media maps from session or database
  if (window.pageMapFeatures) {
    for (var i = 0; i < pageMapFeatures.length; i++) {
      var fn = function(i) {
        var feature_data = pageMapFeatures[i];
        map_display_behaviors(feature_data);
      };
      fn(i);
    }
  }

  $('ul.page-media-items').sortable({
    update: function(event, ui) {
      ui.item.parent().children().each(function(index) {
        if (this == ui.item.get(0)) {
          var content = $(this).find('div.mediacontent').get(0);
          $.post('/sort', {id: content.id, index: index})
          $(this).effect('bounce', {times: 2});
        }
      });
    },
    handle: 'div.media-tab'
  });

  // add the edit/delete behaviors
  $('.mediacontent.text').prev().find('a.media-edit').each(function(e) {
    // the function expects a json object
    // so we'll construct that here
    config = {id: $(this).parent().next().attr('id') };
    addtext_display_behaviors(config);
    return false;
  });

  var tools = [{
      link: $('#text-tool'),
      submitfn: submit_handler,
      post_behaviorfn: addtext_display_behaviors
    }, {
      link: $('#map-tool'),
      attach_form_behaviors: map_behaviors,
      submitfn: submit_handler,
      post_behaviorfn: map_display_behaviors
    }
  ];

  for (var i = 0; i < tools.length; i++) {
    var fn = function(i) {
      var tool = tools[i];
      var link = tool.link;
      var submitfn = tool.submitfn;
      var attach_form_behaviors = tool.attach_form_behaviors;
      var post_behaviorfn = tool.post_behaviorfn;

      // when somebody tries to add a particular media type, fetch the form from
      // the server, and attach the behavior to it
      link.click(function(e) {
        e.preventDefault();
        var url = $(this).attr('href');

        var formcontainer = $('#form-container');
        $.getJSON(url, null, function(data) {
          formcontainer.empty();
          formcontainer.show();
          var html = data.html;
          $(html).appendTo(formcontainer).hide().fadeIn('fast', function() {
            $(this).find('textarea').focus();
          });
          link.effect('transfer', {to: '#form-container'}, 1000);
          $('form.media-item a.media-cancel').click(function(e) {
            e.preventDefault();
            formcontainer.fadeOut('fast', function() { $(this).empty(); });
          });
          $('form.media-item').submit(function(e) { submitfn(e, $(this).attr('action'), data, post_behaviorfn); });
          // attach custom behaviors if needed
          if (attach_form_behaviors) {
            attach_form_behaviors(data);
          }
        });
      });
    }
    fn(i);
  }
});

function submit_handler(e, url, jsonobj, post_behaviorfn) {
  e.preventDefault();
  var data = $('form.media-item').serialize();
  var formcontainer = $('#form-container');

  $.ajax({
    contentType: 'application/x-www-form-urlencoded',
    data: data,
    success: function(data, textStatus) {
      formcontainer.empty();
      $('<li></li>').append($(data.html)).appendTo('ul.page-media-items').hide().effect('pulsate', {times: 2}, 1000);
      if (post_behaviorfn) {
          post_behaviorfn(data);
      }
    },
    type: "POST",
    dataType: 'json',
    url: url
  });
}

function map_display_behaviors(data) {
  var geometryJson = data.geometry;
  var map_id = data.map_id;
  var formatter = new OpenLayers.Format.GeoJSON();
  var feature = formatter.read(geometryJson)[0];
  var bounds = feature.geometry.getBounds();
  var map = new OpenLayers.Map(map_id, {
    projection: new OpenLayers.Projection('EPSG:900913'),
    displayProjection: new OpenLayers.Projection('EPSG:4326'),
    maxExtent: new OpenLayers.Bounds(-14323800, 2299000, -7376800, 7191400),
    });
  var baseLayer = new OpenLayers.Layer.Google('google', {sphericalMercator: true, type: G_PHYSICAL_MAP});
  map.addLayer(baseLayer);
  var featureLayer = new OpenLayers.Layer.Vector('features');
  featureLayer.addFeatures([feature]);
  map.addLayer(featureLayer);
  map.zoomToExtent(bounds);
}

function map_behaviors(data) {
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
  var baseLayer = new OpenLayers.Layer.Google('google', {sphericalMercator: true, type: G_PHYSICAL_MAP});
  map.addLayer(baseLayer);
  map.addControl(toolbar);
  map.addLayer(featureLayer);
  var lng = data.lng;
  var lat = data.lat;
  var center = new OpenLayers.LonLat(lng, lat);
  center.transform(new OpenLayers.Projection('EPSG:4326'), map.getProjectionObject());
  map.setCenter(center, 12);
}

function addtext_display_behaviors(data) {
  var eltid = data.id;
  var elt = $('#' + eltid);
  var mediaContent = elt.parent();
  the_content = mediaContent;
  var mediaControls = mediaContent.find('.media-controls');
  $(mediaControls).find('.media-edit').click(function() {
    var url = $(this).attr('href');
    $.getJSON(url, {media_id: eltid}, function(data) {
      mediaContent.children().each(function() {
        $(this).css('display', 'none');
      });
      $(data.html).appendTo(mediaContent).hide().fadeIn('slow');
    });
    return false;
  });
}
