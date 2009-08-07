# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <NetworkLink>
    % if c.query:
    <name>&quot;${c.query}&quot; in ${c.name}</name>
    % else:
    <name>${c.name}</name>
    % endif
    <visibility>1</visibility>
    <open>0</open>
    % if c.query:
    <description>Pages about &quot;${c.query}&quot; in the ${c.name} almanac</description>
    % else:
    <description>Pages in the ${c.name} almanac</description>
    % endif
    <refreshVisibility>0</refreshVisibility>
    <flyToView>1</flyToView>
    <Link>
      % if c.query:
      <href>${h.url_for('pages_kml_search', almanac_slug=c.slug, query=c.query, qualified=True)}</href>
      % else:
      <href>${h.url_for('pages_kml', almanac_slug=c.slug, qualified=True)}</href>
      % endif
    </Link>
  </NetworkLink>
</kml>
