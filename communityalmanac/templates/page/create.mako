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
<div id="form-container">
</div>
<ul class="page-media-items">
  % if c.media_items:
    %for media_item in c.media_items:
      <li>${media_item}</li>
    %endfor
  % endif
</ul>
<form id="submit-button-form" method="post" action="${request.path_url}">
  <div class="mini-page-media-tools">
    <h4>Add:</h4>
	  ${h.link_to('Text', h.url_for('media_story', almanac=c.almanac), id='mini-text-tool')}
		<a id="mini-image-tool" href="#" onclick="alert('not implemented');">Image</a>
	  ${h.link_to('Map', h.url_for('media_map', almanac=c.almanac), id='mini-map-tool')}
		<a id="mini-audio-tool" href="#" onclick="alert('not implemented');">Audio File</a>
		<a id="mini-pdf-tool" href="#" onclick="alert('not implemented');">PDF</a>
	</div><input type="submit" value="Publish" /><%doc>This button should read "Publish" when creating, and "done" otherwise</%doc>
</form>

<%def name="extra_body()">
  <script type="text/javascript">
    pageMapFeatures = ${c.map_features};
  </script>
</%def>

<%def name="title()">
Create Page - ${c.almanac.name} - Community Almanac
</%def>
<%def name="sidebar()">
<div class="sidebar">
  <%doc>
  This needs to be conditional on edit / create mode. For Edit, it should
  </%doc>
  % if c.almanac:
  <h3 id="add-page-bttn">
    ${h.link_to(u'Publish this page!', h.url_for('page_create', almanac=c.almanac))}
  </h3><%doc>This should read "Publish this page!" when creating, and "Done Editing" otherwise</%doc>
  % endif
  <h3 id="add-content">Add some content:</h3>
	<ul class="page-media-tools">
	  <li>${h.link_to('Text', h.url_for('media_story', almanac=c.almanac), id='text-tool')}</li>
		<li><a id="image-tool" href="#" onclick="alert('not implemented');">Image</a></li>
	  <li>${h.link_to('Map', h.url_for('media_map', almanac=c.almanac), id='map-tool')}</li>
		<li><a id="audio-tool" href="#" onclick="alert('not implemented');">Audio File</a></li>
		<li><a id="pdf-tool" href="#" onclick="alert('not implemented');">PDF</a></li>
	</ul>
</div>
</%def>
<%!
next_page_url = "#"
next_page = "Cancel Adding Page"
next_page_class = "cancel"
%>