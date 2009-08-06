# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <Style id="pageIcon">
    <IconStyle>
      <Icon>
        <href>${h.url_for('/js/img/page.png', qualified=True)}</href>
      </Icon>
    </IconStyle>
  </Style>
  %for page in c.pages:
    %for map_media in page.map_media:
      <Placemark>
        <name>${page.name}</name>
        <description>
          <![CDATA[
          <div>
            <a href="${h.url_for('page_view', almanac=page.almanac, page=page, qualified=True)}">${page.name}</a>
            <span>${h.plural(len(page.comments), 'comment', 'comments')}</span>
            <span>Updated ${page.updated_date_string}</span>
          </div>
          ]]>
        </description>
        <styleUrl>#pageIcon</styleUrl>
        <Point>
          <coordinates>${map_media.location_4326.centroid.x},${map_media.location_4326.centroid.y},0</coordinates>
        </Point>
      </Placemark>
    %endfor
  %endfor
</Document>
</kml>
