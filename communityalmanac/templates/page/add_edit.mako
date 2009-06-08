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
%if c.is_add:
<h2>Create page</h2>
%else:
<h2>Edit page</h2>
%endif
<form id="page-title-form"  method="post" action="${request.path_url}">
  %if c.is_add:
    <input id="page-title" type="text" name="name" value="Page Name" />
  %else:
    <input id="page-title" type="text" name="name" value="${c.page.name}" />
  %endif
</form>
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
    %if c.is_add:
	  ${h.link_to('Text', h.url_for('media_story_new', almanac=c.almanac), id='mini-text-tool')}
	  ${h.link_to('Image', h.url_for('media_image_new', almanac=c.almanac), id='mini-image-tool')}
	  ${h.link_to('Map', h.url_for('media_map_new', almanac=c.almanac), id='mini-map-tool')}
	  ${h.link_to('Audio', h.url_for('media_audio_new', almanac=c.almanac), id='mini-audio-tool')}
	  ${h.link_to('PDF', h.url_for('media_pdf_new', almanac=c.almanac), id='mini-pdf-tool')}
    %else:
	  ${h.link_to('Text', h.url_for('media_story_existing_new', almanac=c.almanac, page=c.page), id='mini-text-tool')}
	  ${h.link_to('Image', h.url_for('media_image_existing_new', almanac=c.almanac, page=c.page), id='mini-image-tool')}
	  ${h.link_to('Map', h.url_for('media_map_existing_new', almanac=c.almanac, page=c.page), id='mini-map-tool')}
	  ${h.link_to('Audio', h.url_for('media_audio_existing_new', almanac=c.almanac, page=c.page), id='mini-audio-tool')}
	  ${h.link_to('PDF', h.url_for('media_pdf_existing_new', almanac=c.almanac, page=c.page), id='mini-pdf-tool')}
    %endif
  </div>
  %if c.is_add:
  <input type="submit" value="Publish" /><%doc>This button should read "Publish" when creating, and "done" otherwise</%doc>
  %else:
  <input type="submit" value="Done" /><%doc>This button should read "Publish" when creating, and "done" otherwise</%doc>
  %endif

</form>

<%def name="extra_body()">
  <script type="text/javascript" src="/js/upload/ajaxupload.3.2.js"></script>
  <script type="text/javascript">
    pageMapFeatures = ${c.map_features};
  </script>
</%def>

<%def name="title()">
%if c.is_add:
Create Page - ${c.almanac.name}
%else:
Edit Page -  ${c.almanac.name}
%endif
</%def>
<%def name="sidebar()">
<div class="sidebar">
  <%doc>
  This needs to be conditional on edit / create mode. For Edit, it should
  </%doc>
  <h3 id="add-page-bttn">
    %if c.is_add:
    ${h.link_to(u'Publish this page!', h.url_for('page_create', almanac=c.almanac))}
    %else:
    ${h.link_to(u'Done editing', h.url_for('page_edit', almanac=c.almanac, page=c.page))}
    %endif
  </h3><%doc>This should read "Publish this page!" when creating, and "Done Editing" otherwise</%doc>
  <h3 id="add-content">Add some content:</h3>
	<ul class="page-media-tools">
    %if c.is_add:
	  <li>${h.link_to('Text', h.url_for('media_story_new', almanac=c.almanac), id='text-tool')}</li>
	  <li>${h.link_to('Image', h.url_for('media_image_new', almanac=c.almanac), id='image-tool')}</li>
	  <li>${h.link_to('Map', h.url_for('media_map_new', almanac=c.almanac), id='map-tool')}</li>
	  <li>${h.link_to('Audio', h.url_for('media_audio_new', almanac=c.almanac), id='audio-tool')}</li>
	  <li>${h.link_to('PDF', h.url_for('media_pdf_new', almanac=c.almanac), id='pdf-tool')}</li>
    %else:
	  <li>${h.link_to('Text', h.url_for('media_story_existing_new', almanac=c.almanac, page=c.page), id='text-tool')}</li>
	  <li>${h.link_to('Image', h.url_for('media_image_existing_new', almanac=c.almanac, page=c.page), id='image-tool')}</li>
	  <li>${h.link_to('Map', h.url_for('media_map_existing_new', almanac=c.almanac, page=c.page), id='map-tool')}</li>
	  <li>${h.link_to('Audio', h.url_for('media_audio_existing_new', almanac=c.almanac, page=c.page), id='audio-tool')}</li>
	  <li>${h.link_to('PDF', h.url_for('media_pdf_existing_new', almanac=c.almanac, page=c.page), id='pdf-tool')}</li>
    %endif
	</ul>
</div>
</%def>

<%def name="pagenav()">
  <span class="cancel">
  %if c.is_add:
    <a href="${h.url_for('almanac_view', almanac=c.almanac)}">Cancel Adding Page</a>
  %else:
    <a href="${h.url_for('page_view', almanac=c.almanac, page=c.page)}">Cancel Editing Page</a>
  %endif
  </span>
</%def>
