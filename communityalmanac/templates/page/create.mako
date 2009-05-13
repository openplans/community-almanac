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
<h2>Create page</h2>
<form id="page-title-form"  method="post" action="${request.path_url}">
  <input id="page-title" type="text" name="name" value="Page Name" />
</form>
<ul class="page-media-tools">
  <li>${h.link_to('Text', h.url_for('media_story', almanac=c.almanac), id='text-tool')}</li>
  <li>${h.link_to('Map', h.url_for('media_map', almanac=c.almanac), id='map-tool')}</li>
</ul>
% if c.media_items:
<ul class="page-media-items">
  %for media_item in c.media_items:
    <li><div class="media-tab">drag</div><div class="media-controls"><a href="#">Edit</a><a href="#">Delete</a></div>${media_item}</li>
  %endfor
</ul>
% endif
<div id="form-container">
</div>
<form id="submit-button-form" method="post" action="${request.path_url}">
  <input type="submit" value="Publish" />
</form>

<%def name="title()">
Create Page - ${c.almanac.name} - Community Almanac
</%def>
<%def name="sidebar()">
<div class="sidebar">
  % if c.almanac:
  <h3 id="add-page-bttn">
    ${h.link_to(u'Publish this page!', h.url_for('page_create', almanac=c.almanac))}
  </h3>
  % endif
</div>
</%def>