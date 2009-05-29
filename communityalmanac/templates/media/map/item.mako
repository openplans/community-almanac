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
% if c.editable:
<div class="media-tab">drag</div>
<div class="media-content">
  <div class="media-controls">
    <a class="media-edit" href="${h.url_for('media_map_edit', media_id=c.map.id)}">Edit</a>
    <a class="media-delete" href="${h.url_for('media_map_delete', media_id=c.map.id)}">Delete</a>
  </div>
  <div style="width: 500px; height: 400px" class="mediacontent map" id="pagemedia_${c.map.id}">
  </div>
</div>
% else:
  <div style="width: 500px; height: 400px" class="mediacontent map" id="pagemedia_${c.map.id}">
  </div>
%endif
