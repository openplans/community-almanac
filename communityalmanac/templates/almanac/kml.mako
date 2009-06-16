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
          <a class="almanac-title" href="${h.url_for('almanac_view', almanac=almanac)}">${almanac.name}</a>
          <% n = len(almanac.pages) %>
          %if n == 1:
          <span class="almanac-pagecount"> 1 page</span>
          %else:
          <span class="almanac-pagecount">${n} pages</span>
          %endif
          <span class="almanac-timestamp">Updated ${almanac.updated_date_string}</span>
          <a class="addpage" href="${h.url_for('page_create', almanac=almanac)}">Add page</a>
        </div>
        ]]>
      </description>
      <Point>
        <coordinates>${almanac.location_4326.x},${almanac.location_4326.y},0</coordinates>
      </Point>
    </Placemark>
  %endfor
</Document>
</kml>
