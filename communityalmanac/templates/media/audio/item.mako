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
<%inherit file="/media/base_item.mako" />
<div style="height: 30px" class="mediacontent audio" id="pagemedia_${c.audio.id}">
  <a href="${c.audio_url}">Audio</a>
</div>

<%def name="media_edit_controls()">
  <a class="media-edit" href="${h.url_for('media_audio_edit', media_id=c.audio.id)}">Edit</a>
  <a class="media-delete" href="${h.url_for('media_audio_delete', media_id=c.audio.id)}">Delete</a>
</%def>
