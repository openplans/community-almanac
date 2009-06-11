# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  %for page in c.almanac.pages:
    %for map_media in page.map_media:
      <Placemark>
        <name>${page.name}</name>
        <description>
          <![CDATA[
          <div>
            <a href="${h.url_for('page_view', almanac=c.almanac, page=page)}">${page.name}</a>
            <% n = len(page.comments) %>
            %if n == 1:
            <span>1 comment</span>
            %else:
            <span>${n} comments</span>
            %endif
            <span>Updated ${page.updated_date_string}</span>
          </div>
          ]]>
        </description>
        <Point>
          <coordinates>${map_media.location_4326.centroid.x},${map_media.location_4326.centroid.y},0</coordinates>
        </Point>
      </Placemark>
    %endfor
  %endfor
</Document>
</kml>
