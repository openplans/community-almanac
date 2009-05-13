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
<h2>${c.almanac.name}</h2>
% if c.almanac.pages:
  <h3>Pages</h3>
  <ul>
    % for page in c.almanac.pages:
    <li>${h.link_to(page.name, h.url_for('page_view', almanac=c.almanac, page=page))}</li>
    % endfor
  </ul>
% endif

<%def name="title()">
${c.almanac.name} - Community Almanac
</%def>
<%def name="bookmark()">
<div id="backtoc" class="pngfix">
  <a href="${h.url_for('almanac_view', almanac=c.almanac)}"><span>&laquo; ${c.almanac.name}</span></a>
</div>
</%def>
<%!
prev_page_url = "#"
prev_page = "Pages 1-10"
next_page_url = "#"
next_page = "Pages 21-30"
%>
