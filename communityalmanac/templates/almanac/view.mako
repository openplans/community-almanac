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
<h2 class="almanac-title pngfix">${c.almanac.name}</h2>
<div id="map" style="width: 100%; height: 300px; border: 4px solid #d0c9b9;"></div>
% if c.pages:
<h3 id="frontispiece-pages">
  <span><strong>Table of Contents</strong>
    <em>${h.plural(c.npages, 'page', 'pages')}</em>
  </span></h3>
  <ul class="almanac-pages">
    % for page in c.pages:
    <li class="selfclear">
      <div class="almanac-meta">${page.creation_date_string}<br />
        <a href="${h.url_for('page_view', almanac=c.almanac, page=page)}#comments">
          ${h.plural(len(page.comments), 'Comment', 'Comments')}
        </a>
      </div>
      <h4>${h.link_to(page.name, h.url_for('page_view', almanac=c.almanac, page=page))} by ${page.author}</h4>
      <% first_image = page.first_image %>
      %if first_image is not None:
        <div class="page-first-image"><img src="${first_image.small_url}" /></div>
      %endif
      <div class="page-excerpt">${h.literal(page.first_story.excerpt())}</div>
    </li>
    % endfor
  </ul>
% endif
${self.tocnav(c.toc_pagination_data)}
<%def name="title()">
${c.almanac.name}
</%def>
<%def name="bookmark()">
<%doc>
<!-- We had decided not to show bookmark on almanac view pages. Leaving the markup in case we decide that we need to have the "bookmark in front" effect -->
<div id="backtoc">
  <a href="${h.url_for('almanac_view', almanac=c.almanac)}"><span>&laquo; ${c.almanac.name}</span></a>
</div>
</%doc>
</%def>
<%def name="extra_body()">
  <script type="text/javascript">
    var loadfunction = function() {
      var map = new OpenLayers.Map('map', {
        projection: new OpenLayers.Projection('EPSG:900913'),
        displayProjection: new OpenLayers.Projection('EPSG:4326'),
        maxExtent: new OpenLayers.Bounds(-14323800, 2299000, -7376800, 7191400),
        controls: [
          new OpenLayers.Control.Navigation({zoomWheelEnabled: false}),
          new OpenLayers.Control.PanZoom()
          ]
        });
        var baseLayer = new OpenLayers.Layer.Google('streets', {sphericalMercator: true, type: G_PHYSICAL_MAP});
        map.addLayer(baseLayer);
        var center = new OpenLayers.LonLat(${c.lng}, ${c.lat});
        center.transform(new OpenLayers.Projection('EPSG:4326'), map.getProjectionObject());
        var pagesLayer = new OpenLayers.Layer.GML('pages', "${h.url_for('pages_kml', almanac=c.almanac)}", {
          format: OpenLayers.Format.KML,
          projection: new OpenLayers.Projection('EPSG:4326'),
          styleMap: new OpenLayers.StyleMap({
            externalGraphic: '/js/img/page.png',
            graphicWidth: 28,
            graphicHeight: 16,
            graphicYOffset: 0
          })
        });
        map.addLayer(pagesLayer);
        map.setCenter(center, 12);
        
         // Big dirty hack!!!
		  var AlmaPopup = OpenLayers.Class(OpenLayers.Popup.FramedCloud, {
		  	fixedRelativePosition: true, relativePosition: "tl", 
		  	initialize:function(id, lonlat, contentSize, contentHTML, anchor, closeBox, 
		                        closeBoxCallback) {
		        OpenLayers.Popup.Framed.prototype.initialize.apply(this, arguments);
		    }
		  });
        var featureSelected = function(feature) {
          var popup = new AlmaPopup(null, feature.geometry.getBounds().getCenterLonLat(),
                                                          null, feature.attributes.description,
                                                          {size: new OpenLayers.Size(1, 1), offset: new OpenLayers.Pixel(-30, 75)},
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
    <input type="text" onfocus="if(this.value=='Search&hellip;') this.value='';" onblur="if(this.value=='') this.value='Search&hellip;';" tabindex="1" size="20" value="Search&hellip;" class="text" name="query" id="query"/>
    <input type="image" align="absmiddle" src="/img/search-submit.png" tabindex="2" value="Find" name="searchsubmit" id="searchsubmit"/>
  </form>
</div>
<div class="sidebar">
  <p class="kml-link"><a href="${h.url_for('pages_kml_link', almanac=c.almanac)}">View in Google Earth (KML)</a></p>
</div>
</%def>

<%def name="pagenav()">
${parent.pagenav(c.prev_page_url, c.prev_page_text, c.next_page_url, c.next_page_text)}
</%def>
