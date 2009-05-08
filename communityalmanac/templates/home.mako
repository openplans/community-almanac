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
<h2>Home page</h2>
% if c.almanacs:
  <h3>Almanacs</h3>
  <ul>
    % for almanac in c.almanacs:
    <li>${h.link_to(almanac.name, h.url_for('almanac_view', almanac=almanac))}</li>
    % endfor
  </ul>
% endif
<p>Right now, you can ${h.link_to('Add', h.url_for('almanac_create'))} an almanac</p>