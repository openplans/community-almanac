# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <NetworkLink>
    % if c.query and c.name:
    <name>&quot;${c.query}&quot; in ${c.name}</name>
    % elif c.name:
    <name>${c.name}</name>
    % else:
    <name>&quot;${c.query}&quot; in the Community Almanac</name>
    % endif
    <visibility>1</visibility>
    <open>0</open>
    % if c.query and c.name:
    <description>Pages about &quot;${c.query}&quot; in the ${c.name} almanac</description>
    % elif c.name:
    <description>Pages in the ${c.name} almanac</description>
    % else:
    <description>Pages about &quot;${c.query}&quot; in the Community Almanac</description>
    % endif
    <refreshVisibility>0</refreshVisibility>
    <flyToView>1</flyToView>
    <Link>
      % if c.query and c.name:
      <href>${h.url_for('pages_kml_search', almanac_slug=c.slug, query=c.query, qualified=True)}</href>
      % elif c.name:
      <href>${h.url_for('pages_kml', almanac_slug=c.slug, qualified=True)}</href>
      % else:
      <href>${h.url_for('all_pages_kml_search', query=c.query, qualified=True)}</href>
      % endif
    </Link>
  </NetworkLink>
</kml>
