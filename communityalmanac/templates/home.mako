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
<div class="wrap">
	<div id="intro" class="selfclear">
	  <div class="text">
			<h2>What is a Community Almanac?</h2>
			<p>It's where you and your community share stories about the heart & soul of the place you live. It's a lasting record of the place you love—the place you call home.</p> 
			<p><strong>Start by finding your community on the map.</strong></p>
			<div id="add-pages-blurb" class="selfclear">
			  <img class="pngfix" src="/img/paper-icon-64.png" width="64" height="64" alt="Page icon" />
				<h3>Can I add my own pages?</h3>
				<p>Yes, and it's free! Just find your community on the map & start contributing to its almanac.</p>
			</div>
			<div id="add-almanac-blurb" class="selfclear">
			  <img class="pngfix" src="/img/book-icon-64.png" width="64" height="64" alt="Almanac icon" />
				<h3>What if my town has no almanac?</h3>
				<p>Simply add a page for your community to start a new almanac.</p>
				<p><a href="#">Learn more!</a></p>
			</div>
		</div><!-- /.text -->
		<div class="map">
			<form action="#" method="post">
				<input id="almanac-name" type="text" value="" name="name"/>
				<a class="find-almanac" title="Find almanac" href="#">Find almanac</a>
			</form>
			<div id="map">
			<p>The map will go here. Right now, you can ${h.link_to('Add', h.url_for('almanac_create'))} an almanac</p>
			</div>
		</div>
	</div><!-- /#intro -->
	% if c.almanacs:
	  <h3>Almanacs</h3>
	  <ul id="almanacs">
	    % for almanac in c.almanacs:
	    <li><a href="${h.url_for('almanac_view', almanac=almanac)}"<span>${almanac.name}</span></a></li>
	    % endfor
	  </ul>
	% endif
</div>
<div id="shelf">
showing recently updated almanacs
</div>
<%def name="pagearea()">
      ${self.body()}
</%def>
<%def name="extra_body()">
  <script type="text/javascript">
//<![CDATA[
$(document).ready(function(){ 
	$('ul#almanacs li').hover(
	  function () {
	    $(this).animate({left: '-50px'},{queue:false,duration:500});	
	  }, 
	  function () {
	    $(this).animate({left: '0px'},{queue:false,duration:500});	
	  }
	);
});
//]]>
  </script>
</%def>