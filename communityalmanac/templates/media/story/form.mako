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
  %if c.story:
  <form class="edit-media-item" method="post" action="${request.path_url}">
  %else:
  <form class="add-media-item" method="post" action="${request.path_url}">
  %endif
    <fieldset>
      <legend>Text</legend>
      %if c.story:
      <textarea name="body">${c.story.text}</textarea>
      %else:
      <textarea name="body"></textarea>
      %endif
      <input type="submit" value="Save" />
      %if c.story:
      <a class="media-cancel" href="${h.url_for('media_story_view', media_id=c.story.id)}">Cancel</a>
      %else:
      <a class="media-cancel" href="#">Cancel</a>
      %endif
    </fieldset>
  </form>
</div>
