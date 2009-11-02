# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:georss="http://www.georss.org/georss">
  <title>${c.almanac.name} Community Almanac Feed</title>
  % if c.query and c.name:
  <link href="${h.url_for('pages_atom_search', almanac_slug=c.slug, query=c.query, qualified=True)}" rel="self" />
  <id>${h.url_for('pages_atom_search', almanac_slug=c.slug, query=c.query, qualified=True)}</id>
  % elif c.name:
  <link href="${h.url_for('pages_atom', almanac_slug=c.slug, qualified=True)}" rel="self" />
  <id>${h.url_for('pages_atom', almanac_slug=c.slug, qualified=True)}</id>
  % else:
  <link href="${h.url_for('all_pages_atom_search', query=c.query, qualified=True)}" rel="self" />
  <id>${h.url_for('all_pages_atom_search', query=c.query, qualified=True)}</id>
  % endif
  <link href="${h.url_for('home', qualified=True)}" />
  <updated>${h.rfc3339(c.almanac.modified)}</updated>
  %for page in c.pages:
    <entry>
      <id>${h.url_for('page_view', almanac=page.almanac, page=page, qualified=True)}</id>
      <author>
        <name>${page.author}</name>
      </author>
      <title>${page.name}</title>
      <link rel="alternate" href="${h.url_for('page_view', almanac=page.almanac, page=page, qualified=True)}" />
      <content type="html">
        <![CDATA[
        <div>
          <a href="${h.url_for('page_view', almanac=page.almanac, page=page, qualified=True)}">${page.name}</a>
          <span>${h.plural(len(page.comments), 'comment', 'comments')}</span>
          <span>Updated ${page.updated_date_string}</span>
        </div>
        ]]>
      </content>
      <updated>${h.rfc3339(page.modified)}</updated>
      %for map_media in page.map_media[:1]:
        <georss:point>${map_media.location_4326.centroid.x},${map_media.location_4326.centroid.y},0</georss:point>
      %endfor
    </entry>
  %endfor
</feed>
