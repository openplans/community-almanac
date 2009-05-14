# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  % for page in c.almanac.pages:
    % for map in page.maps:
      <Placemark>
        <name>${c.almanac.name}</name>
        <description>
          <![CDATA[
          <div><a href="${h.url_for('page_view', almanac=c.almanac, page=page)}">${page.name}</a></div>
          ]]>
        </description>
        <Point>
          <coordinates>${map.location.y},${map.location.x},0</coordinates>
        </Point>
      </Placemark>
    % endfor
  % endfor
</Document>
</kml>
