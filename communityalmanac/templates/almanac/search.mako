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
<h3 class="search-title">
  ${h.plural(c.npages, 'result', 'results')} in ${c.almanac.name} for: <strong>${c.query}</strong>
</h3>
<div id="map" style="width: 100%; height: 300px; border: 4px solid #d0c9b9;"></div>
% if c.pages:
  <ul class="almanac-pages">
    % for page in c.pages:
      <%include file="/page/extract.mako" args="page=page, almanac_link=False"/>
    % endfor
  </ul>
% endif
${self.tocnav(c.pagination_data)}
<%def name="title()">
${c.almanac.name}
</%def>
<%def name="bookmark()">
<div id="backtoc" class="pngfix">
  <a href="${h.url_for('almanac_view', almanac=c.almanac)}"><span>&laquo; ${c.almanac.name}</span></a>
</div>
</%def>
<%def name="extra_body()">
  <script>
    var loadfunction = function() {
      map = new OpenLayers.Map('map', {
        projection: new OpenLayers.Projection('EPSG:900913'),
        displayProjection: new OpenLayers.Projection('EPSG:4326'),
        maxExtent: new OpenLayers.Bounds(-14323800, 2299000, -7376800, 7191400),
        controls: [
          new OpenLayers.Control.Navigation({zoomWheelEnabled: false}),
          new OpenLayers.Control.PanZoom()
          ],
        });
        var baseLayer = new OpenLayers.Layer.Google('streets', {sphericalMercator: true, type: G_PHYSICAL_MAP});
        map.addLayer(baseLayer);
        var center = new OpenLayers.LonLat(${c.lng}, ${c.lat});
        center.transform(new OpenLayers.Projection('EPSG:4326'), map.getProjectionObject());
        var pagesLayer = new OpenLayers.Layer.GML('pages', "${h.url_for('pages_kml_search', almanac=c.almanac, query=c.query)}", {
          format: OpenLayers.Format.KML,
          projection: new OpenLayers.Projection('EPSG:4326'),
          styleMap: new OpenLayers.StyleMap({
            externalGraphic: '/js/img/page.png',
            graphicWidth: 28,
            graphicHeight: 16,
            graphicYOffset: 0,
          })
        });
        map.addLayer(pagesLayer);
        map.setCenter(center, 12);
        var featureSelected = function(feature) {
          var popup = new OpenLayers.Popup.AnchoredBubble(null, feature.geometry.getBounds().getCenterLonLat(),
                                                          new OpenLayers.Size(100, 100), feature.attributes.description,
                                                          {size: new OpenLayers.Size(1, 1), offset: new OpenLayers.Pixel(-64, -126)},
                                                          true, function() { selectControl.unselect(feature); });
          feature.popup = popup;
          map.addPopup(popup);
        };
        var featureUnselected = function(feature) {
          map.removePopup(feature.popup);
          feature.popup.destroy();
          feature.popup = null;
        };
        var selectControl = new OpenLayers.Control.SelectFeature(pagesLayer, {
          onSelect: featureSelected, onUnselect: featureUnselected
        });
        map.addControl(selectControl);
        selectControl.activate();
    };
if ($.browser.msie) {
  $(window).load(loadfunction);
} else {
  $(document).ready(loadfunction);
}
  </script>
</%def>
<%def name="sidebar()">
<div class="sidebar">
  % if c.almanac:
  <h3 id="add-page-bttn">
    ${h.link_to(u'Add a page to this almanac!', h.url_for('page_create', almanac=c.almanac))}
  </h3>
  % endif
  <form action="${h.url_for('almanac_search', almanac=c.almanac, query='form')}" method="post" id="searchform">
    <input type="text" onfocus="if(this.value=='Search&hellip;') this.value='';" onblur="if(this.value=='') this.value='Search&hellip;';" tabindex="1" size="20" value="${c.query if c.query else 'Search&hellip;'}" class="text" name="query" id="query"/>
    <input type="image" align="absmiddle" src="/img/search-submit.png" tabindex="2" value="Find" name="searchsubmit" id="searchsubmit"/>
  </form>
  <p class="kml-link"><a href="${h.url_for('pages_kml_search_link', almanac=c.almanac, query=c.query)}">View in Google Earth (KML)</a></p>
</div>
<div class="sidebar">
  ${self.recent_pages_snippet(c.latest_pages)}
</div>
</%def>

<%def name="pagenav()">
</%def>
