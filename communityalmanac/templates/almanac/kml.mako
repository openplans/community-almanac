# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <Style id="almanacIcon">
    <IconStyle>
      <Icon>
        <href>${h.url_for('/js/img/almanac_marker.png', qualified=True)}</href>
      </Icon>
    </IconStyle>
  </Style>
  %for almanac in c.almanacs:
    <Placemark>
      <name>${almanac.name}</name>
      <description>
        <![CDATA[
        <div>
          <a class="almanac-title" href="${h.url_for('almanac_view', almanac=almanac, qualified=True)}">${almanac.name}</a>
          <span class="almanac-pagecount">${h.plural(len(almanac.pages), 'page', 'pages')}</span>
          <span class="almanac-timestamp">Updated ${almanac.updated_date_string}</span>
          <a class="addpage" href="${h.url_for('page_create', almanac=almanac, qualified=True)}">Add page</a>
        </div>
        ]]>
      </description>
      <styleUrl>#almanacIcon</styleUrl>
      <Point>
        <coordinates>${almanac.location_4326.x},${almanac.location_4326.y},0</coordinates>
      </Point>
    </Placemark>
  %endfor
</Document>
</kml>
