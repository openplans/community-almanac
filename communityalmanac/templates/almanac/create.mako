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
<%inherit file="/base.mako" />
<form id="almanac-create-form" method="post" action="${h.url_for('almanac_create')}">
  <fieldset>
    <legend>Create Almanac</legend>
    <div class="selfclear">
      <label for="almanac-name">Name</label>
      <input type="text" name="name" id="almanac-name" value="${request.POST.get('name', u'')}" />
      <a class="find-almanac" href="#" title="Find almanac">Find almanac</a>
    </div>
    <div class="selfclear">
      <div id="map" style="width: 400px; height: 300px"></div>
    </div>
    <input id="almanac-center" type="hidden" name="almanac_center" value="" />
    <input class="indented-submit" type="submit" value="Add" />
  </fieldset>
</form>

<%def name="title()">Create Almanac - Community Almanac</%def>
<%def name="sidebar()">
<h2>What is a Community Almanac?</h2>
<p>It's where you and your community share stories about the heart &amp; soul of the place you live.  It's a lasting record of the place you love&emdash;the place you call home.</p>
<h2 class="userhint">Start by finding your community on the map.</h2>
<h2>Want to add your own pages?</h1>
<p>It's free! Just find your community on the map &amp; start contributing to its almanac.</p>
<p><a href="${h.url_for('tour')}">Learn more!</a></p>
</%def>
<%def name="extra_body()">
<% geocode_url = h.url_for('geocode') %>
<script type="text/javascript">
  var geocode_url = "${geocode_url}";
  $(document).ready(function() {
    function _geocode() {
      var location = $('#almanac-name').val();
      $.getJSON(geocode_url, {location: location}, function(data) {
        if (!data) {
          alert('no geocode - FIXME!');
        }
        else {
          var center = new OpenLayers.LonLat(data.lng, data.lat);
          center.transform(new OpenLayers.Projection('EPSG:4326'), map.getProjectionObject());
          map.setCenter(center, 12);
          var point_geometry = new OpenLayers.Geometry.Point(data.lat, data.lng);
          var formatter = new OpenLayers.Format.GeoJSON();
          var json = formatter.write(point_geometry);
          $('#almanac-center').val(json);
        }
      });
    }
    var form = $('#almanac-create-form');
    $('#almanac-name').focus(function() {
      form[0].onsubmit = function() { _geocode(); return false; };
    }).blur(function() {
      form[0].onsubmit = function() { return true; };
    });
    $('.find-almanac').click(function() {
      _geocode();
      return false;
    });
    map = new OpenLayers.Map('map', {
      restrict: true,
      projection: new OpenLayers.Projection('EPSG:900913'),
      displayProjection: new OpenLayers.Projection('EPSG:4326'),
      maxExtent: new OpenLayers.Bounds(-14323800, 2299000, -7376800, 7191400),
      controls: [
        new OpenLayers.Control.Navigation({zoomWheelEnabled: false}),
        new OpenLayers.Control.PanZoom()
        ],
      eventListeners: {
        "moveend": function(evt) {
            var geometry = map.getExtent().toGeometry();
            the_geometry = geometry;
          }
        }
      });
    var baseLayer = new OpenLayers.Layer.Google('streets', {sphericalMercator: true, type: G_PHYSICAL_MAP});
    map.addLayer(baseLayer);
    map.zoomToMaxExtent();
    });
</script>
</%def>
