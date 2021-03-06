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
<h2>Add page to ${c.almanac.name}</h2>
%else:
<h2>Edit page</h2>
%endif
<form id="page-title-form"  method="post" action="${request.path_url}">
  ${h.literal(c.behalf)}
  <input id="page-title" type="text" name="name" value="${c.page.name or u'Page Name'}" />
</form>
<ul class="page-media-items">
  % if c.media_items:
    %for media_item in c.media_items:
      <li class="page-item">${media_item}</li>
    %endfor
  % endif
</ul>
<form id="submit-button-form" method="post" action="${request.path_url}">
  <div class="mini-page-media-tools">
    <h4>Add:</h4>
    %if c.is_add:
	  ${h.link_to('Text', h.url_for('media_story_new', almanac=c.almanac), id='mini-text-tool', onclick='return false;', title='Text')}
	  ${h.link_to('Image', h.url_for('media_image_new', almanac=c.almanac), id='mini-image-tool', onclick='return false;', title='Image')}
	  ${h.link_to('Map', h.url_for('media_map_new', almanac=c.almanac), id='mini-map-tool', onclick='return false;', title='Map')}
	  ${h.link_to('MP3', h.url_for('media_audio_new', almanac=c.almanac), id='mini-audio-tool', onclick='return false;', title='MP3')}
	  ${h.link_to('PDF', h.url_for('media_pdf_new', almanac=c.almanac), id='mini-pdf-tool', onclick='return false;', title='PDF')}
	  ${h.link_to('Embed Video', h.url_for('media_video_new', almanac=c.almanac), id='mini-video-tool', onclick='return false;', title='Embed Video')}
    %else:
	  ${h.link_to('Text', h.url_for('media_story_existing_new', almanac=c.almanac, page=c.page), id='mini-text-tool', onclick='return false;', title='Text')}
	  ${h.link_to('Image', h.url_for('media_image_existing_new', almanac=c.almanac, page=c.page), id='mini-image-tool', onclick='return false;', title='Image')}
	  ${h.link_to('Map', h.url_for('media_map_existing_new', almanac=c.almanac, page=c.page), id='mini-map-tool', onclick='return false;', title='Map')}
	  ${h.link_to('MP3', h.url_for('media_audio_existing_new', almanac=c.almanac, page=c.page), id='mini-audio-tool', onclick='return false;', title='MP3')}
	  ${h.link_to('PDF', h.url_for('media_pdf_existing_new', almanac=c.almanac, page=c.page), id='mini-pdf-tool', onclick='return false;', title='PDF')}
	  ${h.link_to('Embed Video', h.url_for('media_video_existing_new', almanac=c.almanac, page=c.page), id='mini-video-tool', onclick='return false;', title='Embed Video')}
    %endif
  </div>
  %if c.is_add:
  <input type="submit" value="Publish" /><%doc>This button should read "Publish" when creating, and "done" otherwise</%doc>
  %else:
  <input type="submit" value="Done" /><%doc>This button should read "Publish" when creating, and "done" otherwise</%doc>
  %endif

</form>

<%def name="extra_body()">
  <script type="text/javascript" src="/js/tinymce/tiny_mce.js"></script>
  <script type="text/javascript">
    pageMapFeatures = ${c.map_features};
    flowplayerElts = ${c.flow_data};
    %if c.is_add:
        sortUrl = "${h.url_for('media_item_temppage_sort', almanac=c.almanac)}";
    %else:
        sortUrl = "${h.url_for('media_item_sort', almanac=c.almanac, page=c.page)}";
    %endif
    pageNameEditUrl = "${h.url_for('page_save_name', page_id=c.page.id)}";
    var form = $('#page-title-form');
    var submit_blocker = function() { return false; };
    $('#page-title').focus(function() {
      form.bind('submit', submit_blocker);
    }).blur(function() {
      form.unbind('submit', submit_blocker);
    });
    tinyMCE.init({
      mode : "none",
      theme : "advanced",
      onchange_callback : function(inst) {tinyMCE.triggerSave();},
      theme_advanced_buttons1: "bold,italic,underline,strikethrough,separator,undo,redo,separator,numlist,bullist,separator",
      theme_advanced_buttons2: "",
      theme_advanced_buttons3: "",
      theme_advanced_toolbar_location: "bottom",
      theme_advanced_toolbar_align: "left",
      plugins : "paste",
      paste_auto_cleanup_on_paste : true,
      paste_remove_styles : true
    });
  </script>
  <script type="text/javascript" src="/js/upload/ajaxupload.3.2.js"></script>
  <script type="text/javascript" src="/js/flowplayer/flowplayer-3.1.1.min.js"></script>
  <script type="text/javascript" src="/js/jquery.scrollTo-1.4.2-min.js"></script>
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
	  <li>${h.link_to('Text', h.url_for('media_story_new', almanac=c.almanac), id='text-tool', onclick='return false;')}</li>
	  <li>${h.link_to('Image', h.url_for('media_image_new', almanac=c.almanac), id='image-tool', onclick='return false;')}</li>
	  <li>${h.link_to('Map', h.url_for('media_map_new', almanac=c.almanac), id='map-tool', onclick='return false;')}</li>
	  <li>${h.link_to('MP3', h.url_for('media_audio_new', almanac=c.almanac), id='audio-tool', onclick='return false;')}</li>
	  <li>${h.link_to('PDF', h.url_for('media_pdf_new', almanac=c.almanac), id='pdf-tool', onclick='return false;')}</li>
	  <li>${h.link_to('Embed Video', h.url_for('media_video_new', almanac=c.almanac), id='video-tool', onclick='return false;')}</li>
    %else:
	  <li>${h.link_to('Text', h.url_for('media_story_existing_new', almanac=c.almanac, page=c.page), id='text-tool', onclick='return false;')}</li>
	  <li>${h.link_to('Image', h.url_for('media_image_existing_new', almanac=c.almanac, page=c.page), id='image-tool', onclick='return false;')}</li>
	  <li>${h.link_to('Map', h.url_for('media_map_existing_new', almanac=c.almanac, page=c.page), id='map-tool', onclick='return false;')}</li>
	  <li>${h.link_to('MP3', h.url_for('media_audio_existing_new', almanac=c.almanac, page=c.page), id='audio-tool', onclick='return false;')}</li>
	  <li>${h.link_to('PDF', h.url_for('media_pdf_existing_new', almanac=c.almanac, page=c.page), id='pdf-tool', onclick='return false;')}</li>
	  <li>${h.link_to('Embed Video', h.url_for('media_video_existing_new', almanac=c.almanac, page=c.page), id='video-tool', onclick='return false;')}</li>
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
<%def name="bookmark()">
<div id="backtoc">
  <a href="${h.url_for('almanac_view', almanac=c.almanac)}"><span>&laquo; ${c.almanac.name}</span></a>
</div>
</%def>
