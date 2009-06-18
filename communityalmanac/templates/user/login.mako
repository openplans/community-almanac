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
<h2>Log In</h2>
<div id="login-new" class="js-toggle">
<form id="user_register" method="post" action="${h.url_for('user_register')}">
<fieldset>
  <legend>New Users</legend>
  <a class="js-toggler rightwise" href="#login-returning">Already have an account?</a>
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
    <label for="password_repeat">Confirm Password</label>
    <input type="password" name="password_repeat" id="password_repeat" />
  </div>
  <input type="hidden" name="came_from" value="${request.params.get('came_from', '')}" />
  <input class="indented-submit" type="submit" value="Add" />
  </fieldset>
</form>
</div>
<div id="login-returning" class="js-toggle">
<form action="/do_login" method="post" name="login">
  <fieldset>
    <legend>Returning Users</legend>
    <a class="js-toggler rightwise" href="#login-new">New user?</a>
    <div class="selfclear">
      <%doc> We use the unintuitive 'login' for username so that we can register and log in at the same time.</%doc>
      <label for="user-login">Username</label>
      <input type="text" name="login" id="user-login" value="${request.POST.get('login', u'')}" />
    </div>
    <div class="selfclear">
      <label for="password">Password:</label>
      <input type="password" name="password" />
    </div>
  % if request.params.get('came_from'):
  <input type="hidden" name="came_from" value="${request.params.get('came_from')}" />
  % endif
    <input class="indented-submit" type="submit" value="Login!" />
  </fieldset>
</form>
<form action="/do_login" method="POST">
<label for="openid">OpenID URL</label>
<input type="openid" name="openid" />
<input type="submit" value="Login with OpenID" />
</form>
</div>
<%def name="extra_body()">
<script type="text/javascript">
/* <![CDATA[ */
    // This gorgeous function originally written by Dan Phiffer (http://phiffer.org/)
    <%doc>
      [TODO] - do we want to move this into a standalone file? It seems like it could be broadly useful.
    </%doc>
    function hrefToID(href) {
      var start = href.indexOf('#');
      var length = href.length - start;
      return href.substr(start + 1, length);
    }
    function sectionhider(except) {
      $(".js-toggle").hide();
      $("#" + except).show();
    }
      $(document).ready(function(){
        $(".js-toggler").click(function () {
          sectionhider(hrefToID(this.href));
          });
        sectionhider('${c.active_section}');
      });
/* ]]> */
</script>
</%def>
