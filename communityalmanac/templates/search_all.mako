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
  ${h.plural(c.npages, 'result', 'results')} for: <strong>${c.query_global}</strong>
</h3>
% if c.pages:
  <ul class="almanac-pages">
    % for page in c.pages:
      <%include file="/page/extract.mako" args="page=page, almanac_link=True"/>
    % endfor
  </ul>
% endif
${self.tocnav(c.pagination_data)}
<%def name="title()">
Search results
</%def>
<%def name="sidebar()">
<div class="sidebar">
  <p class="kml-link"><a href="${h.url_for('all_pages_kml_search_link', query=c.query_global)}">View in Google Earth (KML)</a></p>
</div>
<div class="sidebar">
  ${self.recent_pages_snippet(c.latest_pages)}
</div>
</%def>

<%def name="pagenav()">
</%def>
