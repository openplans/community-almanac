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
      <div id="map" style="width: 500px; height: 400px"></div>
      <input type="hidden" id="feature-geometry" name="feature" />
      <input type="submit" value="Add" />
      <a class="media-cancel" href="#">Cancel</a>
      <a style="display: none" class="almanac-center-url" href="${h.url_for('almanac_center', almanac=c.almanac)}"></a>
    </fieldset>
  </form>
</div>
