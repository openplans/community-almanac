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
    <%page args="page, almanac_link"/>
    <li class="selfclear">
      <div class="almanac-meta">
        %if almanac_link:
        <a href="${h.url_for('almanac_view', almanac=page.almanac)}" class="almanac-link">
          ${page.almanac.name}
        </a><br />
        %endif
        ${page.creation_date_string}<br />
        <a href="${h.url_for('page_view', almanac=page.almanac, page=page)}#comments" class="comments-link">
          ${h.plural(len(page.comments), 'Comment', 'Comments')}
        </a>
      </div>
      <h4>${h.link_to(page.name, h.url_for('page_view', almanac=page.almanac, page=page))} by ${page.author}</h4>
      <% first_image = page.first_image %>
      %if first_image is not None:
        <div class="page-first-image">${h.link_to(h.literal('<img src="%s" />' % first_image.small_url), h.url_for('page_view', almanac=page.almanac, page=page))}</div>
      %endif
      <div class="page-excerpt">${h.literal(page.first_story.excerpt())}</div>
    </li>
