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
<%inherit file="/media/base_form.mako" />
%if c.media_item:
  Download <a href="${c.media_item.url}">${c.media_item.filename}</a>
%endif
<div id="${c.file_id}" class="upload-bttn">Choose File</div>
<div class="upload-status"></div>

<%def name="submit_button()">
<a id="submit-upload-file" class="media-save" href="#"><span>Upload</span></a>
</%def>
