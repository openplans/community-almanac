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
    <title>${self.title()}</title>
    <link rel="stylesheet" type="text/css" href="/style.css" />
  </head>
  <body>
    <div id="ill-sky">
    	<div id="ill-clouds">
    		<div id="ill-mountains">
    			<div id="ill-hills">
    				<div id="ill-foreground">
    					<div id="header" class="selfclear">
    						<h1 id="logo">${h.link_to('Community Almanac', h.url_for('home'))}</h1>
    						<p id="welcome">Wecome, <a href="#">Username</a>!</p>
    						<h3 id="tagline">The heart <span class="amp">&amp;</span> soul of <nobr>the place you live&hellip;</nobr></h3>
    					</div>
    				</div>
    			</div>
    		</div>
    	</div>
    </div>
    <div id="content">
    	<div id="wrap-a">
    		<div id="wrap-b">
    			<div id="nav-top">
    				<span class="prev"><a href="#">&laquo; Previous Page Name</a></span>
    				<span class="next"><a href="#">Next Page Name &raquo;</a></span>
            % if c.almanac:
    				<div id="backtoc">
              <a href="${h.url_for('almanac_view', almanac=c.almanac)}"><span>&laquo; ${c.almanac.name}</span></a>
    				</div>
            % endif
    			</div>
    			<div id="right-page">
    				${next.body()}
    			</div><!-- /#right-page -->

    			<div id="left-page" class="selfclear">
    				<div id="sidebar-1" class="sidebar">
    					<h3 id="add-page-bttn"><a href="#">Add a page to this almanac!</a></h3>
    					<form action="#" method="get" id="searchform">
    						<input type="text" onfocus="if(this.value=='Search&hellip;') this.value='';" onblur="if(this.value=='') this.value='Search&hellip;';" tabindex="1" size="20" value="Search&hellip;" class="text" name="s" id="s"/>
    						<input type="image" align="absmiddle" src="/img/search-submit.png" tabindex="2" value="Find" name="searchsubmit" id="searchsubmit"/>
    					</form>
    				</div>
    				<div id="sidebar-2" class="sidebar">
    					<h4>Sidebar 2</h4>
    					<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
    				</div>
    				<div id="sidebar-3" class="sidebar">
    					<h4>Sidebar 3</h4>
    					<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit.</p>
    					<p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>
    				</div>
    			</div><!-- /#left-page -->
    			<div id="nav-bottom">
    				<span class="prev"><a href="#">&laquo; Previous Page Name</a></span>
    				<span class="next"><a href="#">Next Page Name &raquo;</a></span>
    			</div>
    		</div><!-- /#wrap-b-->
    	</div><!-- /#wrap-a -->
    </div><!-- /#content-->
    <div id="footer">
    	<ul id="footer-nav">
    		<li><a href="#">About</a></li>
    		<li><a href="#">Contact</a></li>
    		<li><a href="#">Help</a></li>
    	</ul>
    </div>
    <script type="text/javascript" src="/js/jquery-1.3.2.min.js"></script>
    <script type="text/javascript" src="/js/almanac.js"></script>
  </body>
</html>
<%def name="title()">Community Almanac</%def>
