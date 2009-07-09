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
<form method="post" action="${request.path_url}">
  <fieldset>
    <legend>Contact us</legend>
    <div class="selfclear">
      <label for="name">Name</label>
      <input id="name" type="text" name="name" value="${request.POST.get('name', '')}" />
    </div>
    <div class="selfclear">
      <label for="email">Email</label>
      <input id="email" type="text" name="email" value="${request.POST.get(email, '')}" />
    </div>
    <div class="selfclear">
      <label id="message" for="message">Message</label>
      <textarea name="message" rows="8" cols="30">${request.POST.get('message', '')}</textarea>
    </div>
    <input class="indented-submit" type="submit" value="Send" />
</form>
