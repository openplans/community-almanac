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
	<div id="intro" class="selfclear pngfix">
	  <div class="text">
		  <div class="panel-wrap">
				<div class="panel">
					<h3>What is a Community Almanac?</h3>
					<p>It's where you and your community share stories about the heart <span class="amp">&#038;</span> soul of the place you live. It's a lasting record of the place you love—the place you call home.</p>
					<h3>Anyone can contribute!</h3>
					<p>And it's free! Just find your community on the map and start adding to its almanac.</p>
					<p>If your community has no almanac, simply find your community on the map and add a page. Your new almanac will be created automatically.</p>
					<h3 class="start-by pngfix">Start by finding your community on the map.</h3>
					<p class="prevnext"><a class="next-panel" href="${h.url_for('almanac_create')}">Next &#187;</a></p>
				</div><!-- /.panel -->
				<div class="panel inactive">
					<h3>What makes your town special?</h3>
					<p>You do! Add pages and fill them with your content. Read other people's pages and post your replies. Get reacquainted with your town.</p>
					<h3>Make Local connections.</h3>
					<p>Community Almanac is a fun way to swap stories with your neighbors. Tell 'em about your favorite sledding hill or swimming hole, the best tree to climb or the coolest place to play stickball. Record memories from your life, and make connections in your community.</p>
					<h3 class="start-by pngfix">Start by finding your community on the map.</h3>
					<p class="prevnext"><a class="prev-panel" href="#">&#171; Previous</a> <a class="next-panel" href="#">Next &#187;</a></p>
				</div><!-- /.panel -->
				<div class="panel inactive">
					<h3>Share in all sorts of formats.</h3>
					<p>Adding text, pictures, audio, video and PDFs to pages is easy! Upload video of your grandfather speaking about his childhood or a recording of your friend singing at a local bar. Paste a poem you wrote while floating down the river in a canoe!</p>
					<h3>Connect stories with real places.</h3>
					<p>The mapping tools let you pinpoint locations in your community. Draw a map to show a street corner, bike trail, stretch of shore front, or even the course your canoe floated down that river.</p>
					<h3 class="start-by pngfix">Start by finding your community on the map.</h3>
					<p class="prevnext"><a class="prev-panel" href="#">&#171; Previous</a> <a class="next-panel" href="#">Next &#187;</a></p>
				</div><!-- /.panel -->
				<div class="panel inactive">
					<h3>It's community heart <span class="amp">&#038;</span> soul.</h3>
					<p>The Orton Family Foundation coined the term "community heart <span class="amp">&#038;</span> soul" to describe the people, places, history, traditions, issues, and values that make your community unique. Community Almanac's non-profit sponsors (<a href="http://www.orton.org/">Orton Family Foundation</a> and <a href="http://openplans.org/">The Open Planning Project</a>) want to help communities articulate, implement and steward their heart & soul.</p>
					<h3>And it's available totally free!</h3>
					<p>All you have to do is <a href="${h.url_for('user_register')}">sign up</a> for a free, no-strings-attached account.</p>
					<h3 class="start-by pngfix">Start by finding your community on the map.</h3>
					<p class="prevnext"><a class="prev-panel" href="#">&#171; Previous</a> <a class="next-signup" href="${h.url_for('user_register')}">Sign Up!</a></p>
				</div><!-- /.panel -->
			</div><!-- /.panel-wrap -->
		</div><!-- /.text -->
		<div class="map">
			<form id="almanac-geolocate" action="${h.url_for('geocode')}">
				<input id="almanac-name" type="text" value=""/>
				<a class="find-almanac" title="Find almanac" href="#">Locate</a>
			</form>
			<form id="almanac-create-form" action="${h.url_for('almanac_create')}" method="post">
				<div id="map"></div>
				<input id="almanac-center" type="hidden" name="almanac_center" value="" />
				<input id="almanac-authoritative" type="hidden" name="name" value="" />
				<input id="almanac-submit" class="disabled" disabled="disabled" type="submit" value="Add a Page" />
			</form>
		</div>
	</div><!-- /#intro -->
  ${self.recent_pages_snippet(c.pages)}
	% if c.almanacs:
	  <ul id="almanacs">
	    % for i, almanac in enumerate(c.almanacs):
      <li class="pngfix almanac-${i+1}"><a href="${h.url_for('almanac_view', almanac=almanac)}"><span class="almanac-name">${almanac.name} <span class="almanac-pagecount">(${h.plural(len(almanac.pages), 'page', 'pages')})</span></span><span class="almanac-timestamp">${almanac.updated_date_string}</span></a></li>
	    % endfor
	  </ul><!-- /#almanacs -->
	% endif
</div>
<div id="shelf">
  <div id="almanac-pagination-footer">
    %if c.prev_page_url:
      <a class="prev" href="${c.prev_page_url}">&#171; ${c.prev_page_text}</a>
    %endif
    Showing ${c.showing_start}-${c.showing_end} Recently Updated Almanacs
    %if c.next_page_url:
      <a class="next" href="${c.next_page_url}">${c.next_page_text} &#187;</a>
    %endif
  </div>
</div><!-- /#shelf -->
<%def name="pagearea()">
      ${self.body()}
</%def>
<%def name="extra_body()">
<% geocode_url = h.url_for('geocode') %>
  <script type="text/javascript">
//<![CDATA[
var geocode_url = "${geocode_url}";
$(document).ready(function(){
	$('ul#almanacs li').hover(
	  function () {
	    $(this).animate({left: '-20px'},{queue:false,duration:500});
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
    window.map = map;
  var navControl = map.getControlsByClass('OpenLayers.Control.Navigation')[0];
  navControl.disableZoomWheel();
  var baseLayer = new OpenLayers.Layer.Google('google', {sphericalMercator: true, type: G_PHYSICAL_MAP});
  map.addLayer(baseLayer);
  var almanacLayer = new OpenLayers.Layer.GML('almanacs', "${h.url_for('almanacs_kml')}", {
    format: OpenLayers.Format.KML,
    projection: new OpenLayers.Projection('EPSG:4326'),
    styleMap: new OpenLayers.StyleMap({
      default: new OpenLayers.Style({
        externalGraphic: '/js/img/almanac_marker.png',
        graphicWidth: 28,
        graphicHeight: 16,
        graphicYOffset: 0,
      }),
      select: new OpenLayers.Style({
        externalGraphic: '/js/img/book-open.png',
        graphicWidth: 28,
        graphicHeight: 16,
        graphicYOffset: 0,
      })
    })
  });
  // In order to prevent features popping in and out of the map, we use a fixed set of features if the zoom is too high.
  var globalfeatures = [];
  function cacheFeatures() {
    if (globalfeatures.length != 0) {
      return;
    }
    for (var index = 0; index < almanacLayer.features.length; ++index) {
      globalfeatures.push(almanacLayer.features[index]);
    }
  };
  almanacLayer.events.on({'loadend': cacheFeatures});

  map.addLayer(almanacLayer);
  var curExtent = extent;
  var disableMoveEvents = false;
  var populateMap = function(evt) {
    if (disableMoveEvents) {
      return false;
    }
    // We have to combine both the geocode and the map update into a single step...
    var zoom = map.getZoom();
    if (zoom < 5) {
      replaceFeatures(almanacLayer, globalfeatures);
      return false;
    }

    var extent = map.getExtent();
    if (curExtent.bottom == extent.bottom &&
        curExtent.left == extent.left &&
        curExtent.right == extent.right &&
        curExtent.top == extent.top) {
      return false;
    }
    curExtent = extent;
    var geometry = extent.toGeometry();
    var formatter = new OpenLayers.Format.GeoJSON({
      'internalProjection': new OpenLayers.Projection("EPSG:900913"),
      'externalProjection': new OpenLayers.Projection("EPSG:4326")
    });
    var geojson = formatter.write(geometry);
    disableMoveEvents = true;
    _geocode(geojson);
    disableMoveEvents = false;
    return false;
  };
  map.zoomToExtent(extent);
  map.events.on({'moveend': populateMap});
  var AlmaPopup = OpenLayers.Class(OpenLayers.Popup.AnchoredBubble, {fixedRelativePosition: true, relativePosition: "tl", positionBlocks: OpenLayers.Popup.FramedCloud.prototype.positionBlocks});
  var featureSelected = function(feature) {
    var popup = new AlmaPopup(null, feature.geometry.getBounds().getCenterLonLat(),
                                                    new OpenLayers.Size(235, 85), feature.attributes.description,
                                                    {size: new OpenLayers.Size(1, 1), offset: new OpenLayers.Pixel(0, 0)},
                                                    true, function() { selectControl.unselect(feature); });
    feature.popup = popup;
    map.addPopup(popup);
  };
  var featureUnselected = function(feature) {
    map.removePopup(feature.popup);
    feature.popup.destroy();
    feature.popup = null;
  };
  var selectControl = new OpenLayers.Control.SelectFeature(almanacLayer, {
    onSelect: featureSelected, onUnselect: featureUnselected
  });
  map.addControl(selectControl);
  function replaceFeatures(layer, newfeatures) {
    // Remove old features
    for (var index=0; index<layer.features.length; ++index) {
        var oldf = layer.features[index];
        var found = false;
        for (var search=0; search<newfeatures.length; ++search) {
            var newf = newfeatures[search];
            if (newf.attributes.name == oldf.attributes.name) {
              // We found it... If the description changed, we'll remove it anyway.
              if (newf.attributes.description != oldf.attributes.description) {
                break;
              }
              found = true;
              break;
            }
        }
        if (!found) {
          layer.removeFeatures(oldf);
        }
    }
    // Add new features
    for (var index=0; index<newfeatures.length; ++index) {
        var newf = newfeatures[index];
        var found = false;
        for (var search=0; search<layer.features.length; ++search) {
            var oldf = layer.features[search];
            if (newf.attributes.name == oldf.attributes.name) {
              // We've handled this already, skip it.
              found = true;
              break;
            }
        }
        if (!found) {
          layer.addFeatures(newf);
        }
    }
  }
  selectControl.activate();
    function _geocode(bbox) {
      var location = bbox ? null : $('#almanac-name').val();
      $.getJSON(geocode_url, {location: location, bbox: bbox}, function(data) {
        if (data.layer) {
          // Undocumented function for loading the layer contents from a string.
          var options = {};
          if (almanacLayer.map && !almanacLayer.projection.equals(almanacLayer.map.getProjectionObject())) {
              options.externalProjection = almanacLayer.projection;
              options.internalProjection = almanacLayer.map.getProjectionObject();
          }
          var f = new almanacLayer.format(options);
          var newfeatures = f.read(data.layer);
          replaceFeatures(almanacLayer, newfeatures);
        }
        var zoom = map.getZoom();
        if (!data.lat || !data.lng || !data.authoritative_name || ((zoom < 7) && (!data.name_based))) {
          // Problem geocoding, we need to disable the submit button
          $('#almanac-submit').val('Add a Page').attr('disabled', 'disabled').addClass('disabled');
        }
        else {
          $('#almanac-authoritative').val(data.authoritative_name);
          $('#almanac-center').val(data.geojson);
          $('#almanac-submit').val('Add a Page to the ' + data.authoritative_name + ' Almanac').removeAttr('disabled').removeClass('disabled');
          if (data.name_based) {
            var center = new OpenLayers.LonLat(data.lng, data.lat);
            center.transform(new OpenLayers.Projection('EPSG:4326'), map.getProjectionObject());
            if (!disableMoveEvents) {
              var interfere = true;
              disableMoveEvents = true;
            } else {
              var interfere = false;
            }
            map.setCenter(center, 12);
            if (interfere) {
              disableMoveEvents = false;
            }
          } else {
            $('#almanac-name').val('');
          }
        }
        if (data.almanac) {
          for (var index=0; index<almanacLayer.features.length; ++index) {
            if (almanacLayer.features[index].attributes.name == data.authoritative_name) {
              selectControl.select(almanacLayer.features[index]);
            }
          }
        }
      });
    } // end geocode.
    var form = $('#almanac-geolocate');
    var submit_blocker = function() { _geocode(false); return false; };
    $('#almanac-name').focus(function() {
      form.bind('submit', submit_blocker);
    }).blur(function() {
      form.unbind('submit', submit_blocker);
    });
    $('.find-almanac').click(function() {
      _geocode(false);
      return false;
    });
    $('#almanac-name').focus();
});
//]]>
  </script>
</%def>

<%def name="body_class()">home</%def>
