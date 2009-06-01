# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  %for almanac in c.almanacs:
    <Placemark>
      <name>${almanac.name}</name>
      <description>
        <![CDATA[
        <div><a href="${h.url_for('almanac_view', almanac=almanac)}">${almanac.name}</a></div>
        ]]>
      </description>
      <Point>
        <coordinates>${almanac.location.y},${almanac.location.x},0</coordinates>
      </Point>
    </Placemark>
  %endfor
</Document>
</kml>
