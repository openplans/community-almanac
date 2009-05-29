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
        applyDisplayFeatureMapBehavior(feature_data);
      };
      fn(i);
    }
  }

  // add sortable behavior
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

  // behavior when adding a media type
  $('ul.page-media-tools li a').click(function(e) {
    e.preventDefault();
    var link = $(this);
    var url = link.attr('href');

    var formcontainer = $('#form-container');
    $.getJSON(url, null, function(data) {
      formcontainer.empty();
      formcontainer.show();
      var html = data.html;
      $(html).appendTo(formcontainer).hide().fadeIn('fast', function() {
        $(this).find('textarea').focus();
      });
      link.effect('transfer', {to: '#form-container'}, 1000);
      applyDrawFeatureMapBehavior(data);
    });
  });

  var _removeMediaItemForm = function() {
    // Helper function to remove the media form at the top of the page
    // This will get called when new media items are added or cancelled
    $('#form-container').children().each(function() {
      $(this).fadeOut('slow', function() {
        $(this).remove();
      });
    });
  };

  // behavior when cancelling the edit of a new media item
  $('#form-container a.media-cancel').live('click', function(e) {
    e.preventDefault();
    _removeMediaItemForm();
  });

  // behavior when saving a new media item
  $('#form-container form input[type=submit]').live('click', function(e) {
    e.preventDefault();
    var formcontainer = $('#form-container');
    var form = $('#form-container form');
    var url = form.attr('action');
    var data = form.serialize();

    $.ajax({
      contentType: 'application/x-www-form-urlencoded',
      data: data,
      success: function(data, textStatus) {
        _removeMediaItemForm();
        $('<li></li>').append($(data.html)).appendTo('ul.page-media-items').hide().effect('pulsate', {times: 2}, 1000, function() {
          applyDisplayFeatureMapBehavior(data);
        });
      },
      type: "POST",
      dataType: 'json',
      url: url
    });
  });

  // register live events for the media items
  $('ul.page-media-items li .media-controls .media-edit').live('click', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    var li = $(this).closest('li');
    $.getJSON(url, {}, function(data) {
      var newli = $('<li></li>').append($(data.html));
      li.replaceWith(newli);
      newli.find('textarea').focus();
      applyDrawFeatureMapBehavior(data);
    });
  });

  $('ul.page-media-items li .media-controls .media-delete').live('click', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    var li = $(this).closest('li');
    $.ajax({
      contentType: 'application/x-www-form-urlencoded',
      data: {},
      success: function(data, textStatus) {
        li.fadeOut('slow', function() {
          $(this).remove();
        });
      },
      type: "POST",
      dataType: 'json',
      url: url
    });
  });

  // media item live edit
  $('ul.page-media-items form.media-item input[type=submit]').live('click', function(e) {
    e.preventDefault();
    var form = $(this).closest('form.media-item');
    var postUrl = form.attr('action');
    var getUrl = $(this).next().attr('href');
    var data = form.serialize();
    var li = form.closest('li');

    $.ajax({
      contentType: 'application/x-www-form-urlencoded',
      data: data,
      success: function(data, textStatus) {
        $.getJSON(getUrl, {}, function(data) {
          var newli = $('<li></li>').append($(data.html));
          li.replaceWith(newli);
          newli.hide().fadeIn('slow');
          applyDisplayFeatureMapBehavior(data);
        });
      },
      type: "POST",
      dataType: 'json',
      url: postUrl
    });
  });

  // media item live cancel
  $('ul.page-media-items a.media-cancel').live('click', function(e) {
    e.preventDefault();
    var url = $(this).attr('href');
    var li = $(this).closest('li');
    $.getJSON(url, {}, function(data) {
      var newli = $('<li></li>').append($(data.html));
      li.replaceWith(newli);
      newli.hide().fadeIn('slow');
      applyDisplayFeatureMapBehavior(data);
    });
  });

});

function applyDisplayFeatureMapBehavior(data) {
  var geometryJson = data.geometry;
  if (!geometryJson) {
    return;
  }
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

function applyDrawFeatureMapBehavior(data) {
  if (!(data.lng && data.lat) && !data.geometry) {
    return;
  }
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

  var map_id = data.map_id ? data.map_id : 'map';
  map = new OpenLayers.Map(map_id, {
    projection: new OpenLayers.Projection('EPSG:900913'),
    displayProjection: new OpenLayers.Projection('EPSG:4326'),
    maxExtent: new OpenLayers.Bounds(-14323800, 2299000, -7376800, 7191400),
    });
  var baseLayer = new OpenLayers.Layer.Google('google', {sphericalMercator: true, type: G_PHYSICAL_MAP});
  map.addLayer(baseLayer);
  map.addControl(toolbar);
  // if this is an edit on an existing feature, we should displaly that feature too
  if (data.geometry) {
    var geometryJson = data.geometry;
    var formatter = new OpenLayers.Format.GeoJSON();
    var feature = formatter.read(geometryJson)[0];
    var bounds = feature.geometry.getBounds();
    featureLayer.addFeatures([feature]);
    map.addLayer(featureLayer);
    map.zoomToExtent(bounds);
  }
  // otherwise we center on the almanac
  else {
    var lng = data.lng;
    var lat = data.lat;
    var center = new OpenLayers.LonLat(lng, lat);
    map.addLayer(featureLayer);
    center.transform(new OpenLayers.Projection('EPSG:4326'), map.getProjectionObject());
    map.setCenter(center, 12);
  }
}
