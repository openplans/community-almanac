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
<h2>${c.page.name}</h2>
%if c.media_items:
  <div class="session-data">
    <ul>
      %for media_item in c.media_items:
        <li>${media_item}</li>
      %endfor
    </ul>
  </div>
%endif

<%def name="title()">
${c.page.name} - ${c.almanac.name} - Community Almanac
</%def>
<%def name="bookmark()">
<div id="backtoc">
  <a href="${h.url_for('almanac_view', almanac=c.almanac)}"><span>&laquo; ${c.almanac.name}</span></a>
</div>
</%def>
<%def name="bookmark()">
<span class="prev"><a href="#">&laquo; Previous Page Name</a></span>
<span class="next"><a href="#">Next Page Name &raquo;</a></span>
</%def>