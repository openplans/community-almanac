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
<form id="request_reset" method="post" action="${h.url_for('user_requestreset')}">
  <fieldset>
    <legend>Forgotten username or password</legend>
    <div class="selfclear">
      <%doc> We use the unintuitive 'login' because the user can enter username or password into this field.</%doc>
      <label for="user-login">Username or Email Address</label>
      <input type="text" name="login" id="user-login" value="${request.POST.get('login', u'')}" />
    </div>
    <input class="indented-submit" type="submit" value="Send Details" />
  </fieldset>
</form>

<%def name="title()">Forgotten Username or Password</%def>
