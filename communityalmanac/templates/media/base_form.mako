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
  %if c.media_item:
  <form class="edit-media-item" method="post" action="${request.path_url}">
  %else:
  <form class="add-media-item" method="post" action="${request.path_url}">
  %endif
    <fieldset>
      <legend>${c.legend}</legend>
      ${next.body()}
      <div class="media-item-actions selfclear">
      ${self.submit_button()}
      ${self.cancel_button()}
      </div>
    </fieldset>
  </form>
</div>

<%def name="submit_button()">
  <button class="media-save" type="submit"><span>Save</span></button>
</%def>

<%def name="cancel_button()">
  %if c.media_item:
  <a class="media-cancel" href="${c.view_url}"><span>Cancel</span></a>
  %else:
  <a class="media-cancel" href="#"><span>Cancel</span></a>
  %endif
</%def>
