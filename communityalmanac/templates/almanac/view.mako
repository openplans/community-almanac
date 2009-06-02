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
% if c.almanac.pages:
  <h3 id="frontispiece-pages"><strong>Table of Contents</strong> ${len(c.almanac.pages)} pages</h3>
  <ul class="almanac-pages">
    % for page in c.almanac.pages:
    <li class="selfclear">
      <div class="almanac-meta">${page.creation_date_string}<br />
        <a href="${h.url_for('page_view', almanac=c.almanac, page=page)}#comments">
          <% n = len(page.comments) %>
          %if n == 1:
            1 Comment
          %else:
            ${n} Comments
          %endif
        </a>
      </div>
      <h4>${h.link_to(page.name, h.url_for('page_view', almanac=c.almanac, page=page))} by ${page.user.username}</h4>
      <div class="almanac-excerpt">${page.first_story.excerpt()}</div>
    </li>
    % endfor
  </ul>
% endif
<p id="almanac-pagination">Showing 11-20 of 23.</p>
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
    $(document).ready(function() {
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
        map.setCenter(center, 12);
    });
  </script>
</%def>
<%def name="sidebar()">
<div class="sidebar">
  % if c.almanac:
  <h3 id="add-page-bttn">
    ${h.link_to(u'Add a page to this almanac!', h.url_for('page_create', almanac=c.almanac))}
  </h3>
  % endif
  <form action="#" method="get" id="searchform">
    <input type="text" onfocus="if(this.value=='Search&hellip;') this.value='';" onblur="if(this.value=='') this.value='Search&hellip;';" tabindex="1" size="20" value="Search&hellip;" class="text" name="s" id="s"/>
    <input type="image" align="absmiddle" src="/img/search-submit.png" tabindex="2" value="Find" name="searchsubmit" id="searchsubmit"/>
  </form>
</div>
</%def>
<%!
prev_page_url = "#"
prev_page = "Pages 1-10"
next_page_url = "#"
next_page = "Pages 21-30"
%>
