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
<div class="wrap selfclear">
	<div id="intro" class="selfclear">
	  <div class="panel-wrap">
			<div class="panel">
				<h2>What is a Community Almanac?</h2>
				<p>It's where you and your community share stories about the heart <span class="amp">&#038;</span> soul of the place you live. It's a lasting record of the place you love—the place you call home.</p> 
				<p><strong>Start by finding your community on the map.</strong></p>
				<div id="add-pages-blurb" class="selfclear">
				  <img class="pngfix" src="/img/paper-icon-64.png" width="64" height="64" alt="Page icon" />
					<h3>Can I add my own pages?</h3>
					<p>Yes, and it's free! Just find your community on the map <span class="amp">&#038;</span> start contributing to its almanac.</p>
				</div>
				<div id="add-almanac-blurb" class="selfclear">
				  <img class="pngfix" src="/img/book-icon-64.png" width="64" height="64" alt="Almanac icon" />
					<h3>What if my town has no almanac?</h3>
					<p>Simply add a page for your community to start a new almanac.</p>
					<p class="selfclear"><a class="next-panel" href="${h.url_for('almanac_create')}">Learn more &#187;</a></p>
				</div>
			</div><!-- /.panel -->
			<div class="panel inactive">
				<h3>Anyone can contribute!</h3>
				<p>What makes your town a truly special place? You do. Add pages and fill them with your content. Read other people's pages and post your replies. Get reacquainted with your town.</p> 
				<h3>Make Local connections.</h3>
				<p>Community Almanac is a fun way to swap stories with your neighbors. Tell 'em about your favorite sledding hill or swimming hole, the best tree to climb or the coolest place to play stickball. Record memories from life, and make connections in your town. </p>
				<p><strong>Start by finding your community on the map.</strong></p>
				<p class="selfclear"><a class="prev-panel" href="#">&#171; Previous</a> <a class="next-panel" href="#">Learn more &#187;</a></p>
			</div><!-- /.panel -->
			<div class="panel inactive">
				<h3>Share in all sorts of formats.</h3>
				<p>Add text, pictures, maps, audio, video and PDFs to your pages. It's easy! Add a video of your grandfather speaking about his childhood.</p> 
				<h3>Connect stories with real places.</h3>
				<p>Community Almanac's mapping tools let you document particular places in your community. You can draw on a map to show a street corner, bike trail, stretch of shore front, or even the course your canoe floated down that river.</p>
				<p><strong>Start by finding your community on the map.</strong></p>
				<p class="selfclear"><a class="prev-panel" href="#">&#171; Previous</a> <a class="next-panel" href="#">Learn more &#187;</a></p>
			</div><!-- /.panel -->
			<div class="panel inactive">
				<h3>It's about community heart <span class="amp">&#038;</span> soul.</h3>
				<p>The Orton Family Foundation coined the term "community heart <span class="amp">&#038;</span> soul" to describe the people, places, history, traditions, issues (even feuds), values and other characteristics that make your town unique. Community Almanac's non-profit sponsors (Orton Family Foundation <span class="amp">&#038;</span> The Open Planning Project) want to help communities articulate, implement and steward their heart <span class="amp">&#038;</span> soul.</p> 
				<h3>And it's available totally free!</h3>
				<p>All you have to do is create a free, no-strings-attached login ID and password.</p>
				<p><strong>Start by finding your community on the map.</strong></p>
				<p class="selfclear"><a class="prev-panel" href="#">&#171; Previous</a></p>
			</div><!-- /.panel -->
		</div><!-- /.panel-wrap -->
		<div class="map">
			<form action="#" method="post">
				<input id="almanac-name" type="text" value="" name="name"/>
				<a class="find-almanac" title="Find almanac" href="#">Locate</a>
			</form>
      <div style="height: 350px; width: 500px" id="map"></div>
			<p>The map will go here. Right now, you can ${h.link_to('Add', h.url_for('almanac_create'))} an almanac</p>
		</div>
	</div><!-- /#intro -->
	<div id="recent-activity" class="pngfix">
	  <h2>Recently Updated Pages</h2><!-- should this link to a list of all pages sorted by update time? -->
	  <ul id="pages">
	    <li class="selfclear"><a class="page-title" href="#">Title of a page</a> <span class="page-timestamp">June 3, 2009</span> <a class="page-comments" href="#">7 comments</a> <span class="page-almanac">(Madison, WI)</span></li>
		  <li class="selfclear"><a class="page-title" href="#">Title of a page</a> <span class="page-timestamp">June 3, 2009</span> <a class="page-comments" href="#">7 comments</a> <span class="page-almanac">(Madison, WI)</span></li>
		  <li class="selfclear"><a class="page-title" href="#">Title of a page</a> <span class="page-timestamp">June 3, 2009</span> <a class="page-comments" href="#">7 comments</a> <span class="page-almanac">(Madison, WI)</span></li>
	  </ul><!-- /#pages -->
	</div><!-- /#recent-activity -->
	% if c.almanacs:
	  <h3 id="almanac-frontispiece"><span class="pngfix">23 Recently Updated Almanacs</span></h3>
	  <ul id="almanacs">
	    % for almanac in c.almanacs:
	    <li><a href="${h.url_for('almanac_view', almanac=almanac)}"><span class="almanac-name">${almanac.name}</span><span class="almanac-timestamp">June 15, 2009</span></a></li>
	    % endfor
	  </ul><!-- /#almanacs -->
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
	$('.panel-wrap').cycle({fx: 'fade', speed: 'fast', timeout: 0, next: '.next-panel', prev: '.prev-panel'
	});
  var extent = new OpenLayers.Bounds(-14323800, 2299000, -7376800, 7191400);
  map = new OpenLayers.Map('map', {
    projection: new OpenLayers.Projection('EPSG:900913'),
    displayProjection: new OpenLayers.Projection('EPSG:4326'),
    maxExtent: extent
    });
  var baseLayer = new OpenLayers.Layer.Google('google', {sphericalMercator: true, type: G_PHYSICAL_MAP});
  map.addLayer(baseLayer);
  var almanacLayer = new OpenLayers.Layer.GML('almanacs', "${h.url_for('almanacs_kml')}", {
    format: OpenLayers.Format.KML,
    projection: new OpenLayers.Projection('EPSG:4326'),
    styleMap: new OpenLayers.StyleMap({
      externalGraphic: '/js/img/almanac_marker.png',
      graphicWidth: 16,
      graphicHeight: 16,
      graphicYOffset: 0,
    })
  });
  map.addLayer(almanacLayer);
  almanacLayer.events.register('loadend', almanacLayer, function() {
    this.map.zoomToExtent(this.getDataExtent());
  });
  var curExtent = extent;
  var populateMap = function(evt) {
    var extent = map.getExtent();
    if (curExtent.bottom == extent.bottom &&
        curExtent.left == extent.left &&
        curExtent.right == extent.right &&
        curExtent.top == extent.top) {
      return;
    }
    curExtent = extent;
    var geometry = extent.toGeometry();
    var formatter = new OpenLayers.Format.GeoJSON({externalProjection: new OpenLayers.Projection('EPSG:4326'), internalProjection: new OpenLayers.Projection('EPSG:900913')});
    var geojson = formatter.write(geometry);
    almanacLayer.setUrl("${h.url_for('almanacs_kml')}" + '?extent=' + geojson);
  };
  map.zoomToExtent(extent);
  map.events.on({'moveend': populateMap});
});
//]]>
  </script>
</%def>
