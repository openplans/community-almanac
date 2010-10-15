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
<form id="user_register" method="post" action="${h.url_for('user_register')}">
  <fieldset>
    <legend>Sign Up!</legend>
    <div class="selfclear">
      <%doc> We use the unintuitive 'login' for username so that we can register and log in at the same time.</%doc>
      <label for="user-login">Username</label>
      <input type="text" name="login" id="user-login" value="${request.POST.get('login', u'')}" />
    </div>
    <div class="selfclear">
      <label for="Email Address">Email Address</label>
      <input type="text" name="email_address" id="email_address" value="${request.POST.get('email_address', u'')}" />
    </div>
    <div class="selfclear">
      <label for="password">Password</label>
      <input type="password" name="password" id="password" value="${request.POST.get('password', u'')}" />
    </div>
    <div class="selfclear">
      <label for="password_repeat">Retype Password</label>
      <input type="password" name="password_repeat" id="password_repeat" />
    </div>
    <input type="hidden" name="came_from" value="${request.params.get('came_from', '')}"/>

    %if g.captcha_enabled:
    <div class="form-row">
      <input type="hidden" name="recaptcha_marker_field" />
      ${c.captcha_html}
    </div>
    %endif


    <input class="indented-submit" type="submit" value="Add" />
  </fieldset>
</form>

<%def name="title()">User Signup</%def>
<%def name="sidebar()">
<h2>What is a Community Almanac?</h2>
<p>It's where you and your community share stories about the heart & soul of the place you live.  It's a lasting record of the place you love—the place you call home.</p>
<h2 class="userhint">Start by finding your community on the map.</h2>
<h2>Want to add your own pages?</h1>
<p>It's free! Just find your community on the map &amp; start contributing to its almanac.</p>
<p><a href="${h.url_for('tour')}">Learn more!</a></p>
</%def>
