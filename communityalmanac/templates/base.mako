<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<!--
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
-->
  <head>
    <title>${self.title()} - Community Almanac</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="Content-Language" content="en-us" />
    <link type="text/css" rel="stylesheet" href="${h.url_for('/css/reset.css')}" />
    <link type="text/css" rel="stylesheet" href="${h.url_for('/css/style.css')}" />
    <link type="text/css" rel="stylesheet" href="${h.url_for('/css/openlayers.css')}" />
    <link type="text/css" rel="stylesheet" href="${h.url_for('/css/turn.css')}" />
    ${self.extra_head()}
  </head>
  <body 
  %if c.is_homepage:
  class="home"
  %elif self.attr.error_class:
  class="${self.attr.error_class}"
  %endif
  >
    <div id="ill-sky">
      <div id="ill-clouds">
        <div id="ill-mountains">
          <div id="ill-hills">
            <div id="ill-foreground">
              <div id="header" class="selfclear">
                <h1 id="logo"><a class="pngfix" href="${h.url_for('home')}">Community Almanac</a></h1>
                <% flash_messages = h.retrieve_flash_messages() %>
                %if flash_messages:
                  <div id="flash-messages">
                    <a id="flash-closer" href="#" title="Dismiss messages">Close</a>
                    <div id="flash-content">
                      %for flash_message in flash_messages:
                        <div>${flash_message}</div>
                      %endfor
                    </div><!-- /#flash-content -->
                  </div><!-- /#flash-messages -->
                %endif
                %if c.user:
                <div id="welcome">Welcome, ${c.user.username}! <a href="/logout">Sign Out</a></div>
                %else:
                <div id="login">
                  <form action="/do_login" method="post">
                    <input id="username" name="login" type="text" />
                    <input id="password" name="password" type="password" />
                    <input id="login-submit" type="submit" value="Log In"/>Not a member yet? <a href="/login#login-new">Sign Up!</a><br /><a href="/forgot">Forgot your password?</a></form><div class="tab"><a href="/login#login-returning">Login</a></div></div>
                %endif         
                <h3 id="tagline">The heart <span class="amp">&#038;</span> soul of <nobr>the place you live&hellip;</nobr></h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="content" class="selfclear">
      ${self.pagearea()}
    </div><!-- /#content-->
    <div id="footer" class="selfclear">
      <ul id="footer-nav">
        <li><a href="#">About</a></li>
        <li><a href="#">Contact</a></li>
        <li><a href="#">Help</a></li>
      </ul>
    </div>
    <script type="text/javascript" src="/js/jquery-1.3.2.min.js"></script>
    <script type="text/javascript" src="/js/jquery-ui-1.7.1.custom.min.js"></script>
    <script type="text/javascript" src="/js/almanac.js"></script>
    <script type="text/javascript" src="/js/turn.js"></script>
    <script type="text/javascript" src="/js/jquery.cycle-2.60.min.js"></script>
    <script type="text/javascript" src="/js/OpenLayers.js"></script>
    <script type="text/javascript"
            src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=${g.map_key}"></script>
    <script type="text/javascript">
  		$(document).ready(function(){
  			$('#target').fold({directory: '/img', side: 'right', turnImage: 'fold-sw.png', maxHeight: 135,	startingWidth: 24, startingHeight: 24});
      	$('div#login').hover(
      	  function () {
      	    $(this).animate({top: '0'},{queue:false,duration:500});
      	    $('#username').focus();
      	  }, 
      	  function () {
      	    $(this).animate({top: '-11.6em'},{queue:false,duration:500});	
      	  }
      	);
  		});
  	</script>
    ${self.extra_body()}
  </body>
</html>
<%def name="title()"></%def>
<%def name="extra_head()"></%def>
<%def name="extra_body()"></%def>
<%def name="bookmark()"></%def>
<%def name="pagenav(prev_page=None, next_page=None)">
%if prev_page:
<span class="prev"><a href="${h.url_for('page_view', almanac=c.almanac, page=prev_page)}">${prev_page.name}</a></span>
%endif
%if next_page:
<span class="next"><a href="${h.url_for('page_view', almanac=c.almanac, page=next_page)}">${next_page.name}</a></span>
%endif
</%def>
<%def name="sidebar()">
<div class="sidebar">
  % if c.almanac:
  <h3 id="add-page-bttn">
    ${h.link_to(u'Add a page to this almanac!', h.url_for('page_create', almanac=c.almanac))}
  </h3>
  % endif
  <form action="#" method="get" id="searchform">
    <input type="text" onfocus="if(this.value=='Search&hellip;') this.value='';" onblur="if(this.value=='') this.value='Search&hellip;';" tabindex="1" size="20" value="Search&hellip;" class="text" name="s" id="s"/>
    <input type="image" align="absmiddle" src="/img/search-submit.png" tabindex="2" value="Find" name="searchsubmit" id="searchsubmit"/>
  </form>
</div>
</%def>
<%def name="pagearea()">
<div id="wrap-a" class="selfclear">
  <div id="wrap-b">
    <div id="nav-top">
      <div id="target"></div>
      ${self.pagenav()}
      ${self.bookmark()}
    </div>
    <div id="right-page">
      ${next.body()}
    </div><!-- /#right-page -->
    <div id="left-page" class="selfclear">
      ${self.sidebar()}
    </div><!-- /#left-page -->
    <div id="nav-bottom">
      ${self.pagenav()}
    </div>
  </div><!-- /#wrap-b-->
</div><!-- /#wrap-a -->
</%def>
<%!
error_class = ""
prev_page_url = ""
prev_page = "Previous"
prev_page_class = "prev"
next_page_url = ""
next_page = "Next"
next_page_class = "next"
%>
