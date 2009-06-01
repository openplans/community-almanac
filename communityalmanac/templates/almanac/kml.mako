# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  %for almanac in c.almanacs:
    <Placemark>
      <name>${almanac.name}</name>
      <description>
        <![CDATA[
        <div>
          <a href="${h.url_for('almanac_view', almanac=almanac)}">${almanac.name}</a>
          <% n = len(almanac.pages) %>
          %if n == 1:
          <span>1 page</span>
          %else:
          <span>${n} pages</span>
          %endif
          <span>Updated ${almanac.updated_date_string}</span>
          <a href="${h.url_for('page_create', almanac=almanac)}">Add page</a>
        </div>
        ]]>
      </description>
      <Point>
        <coordinates>${almanac.location.y},${almanac.location.x},0</coordinates>
      </Point>
    </Placemark>
  %endfor
</Document>
</kml>
