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
%if c.editable:
<div class="media-tab">drag</div>
<div class="media-content">
  <div class="media-controls">
    ${self.media_edit_controls()}
  </div>
  <div class="mediacontent ${c.type}" id="pagemedia_${c.story.id}">
    ${next.body()}
  </div>
</div>
% else:
<div class="mediacontent ${c.type}" id="pagemedia_${c.story.id}">
  ${next.body()}
</div>
%endif

<%def name="media_edit_controls()">
  <a class="media-edit" href="${c.edit_url}">Edit</a>
  <a class="media-delete" href="${c.delete_url}">Delete</a>
</%def>
