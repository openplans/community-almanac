<%doc><!--
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
--></%doc>
<div>
  <form class="media-item" method="post" action="${request.path_url}">
    <fieldset>
      <legend>Map</legend>
      <div id="map" style="width: 500px; height: 400px"></div>
      <input type="hidden" id="feature-geometry" name="feature" />
      <input type="submit" value="Add" />
      <a class="media-cancel" href="#">Cancel</a>
    </fieldset>
  </form>
</div>
<script>
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
  var baseLayer = new OpenLayers.Layer.Google('streets', {sphericalMercator: true});
  map.addLayer(baseLayer);
  var center = new OpenLayers.LonLat(${c.lng}, ${c.lat});
  center.transform(new OpenLayers.Projection('EPSG:4326'), map.getProjectionObject());
  map.addLayer(featureLayer);
  map.addControl(toolbar);
  map.setCenter(center, 12);
</script>
