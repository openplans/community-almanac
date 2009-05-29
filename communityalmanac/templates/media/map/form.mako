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
<div>
  <form class="media-item" method="post" action="${request.path_url}">
    <fieldset>
      <legend>Map</legend>
      %if c.map:
      <div id="pagemedia_${c.map.id}" style="width: 500px; height: 400px"></div>
      %else:
      <div id="map" style="width: 500px; height: 400px"></div>
      %endif
      <input type="hidden" id="feature-geometry" name="feature" />
      <input type="submit" value="Save" />
      %if c.map:
      <a class="media-cancel" href="${h.url_for('media_map_view', media_id=c.map.id)}">Cancel</a>
      %else:
      <a class="media-cancel" href="#">Cancel</a>
      %endif
    </fieldset>
  </form>
</div>
