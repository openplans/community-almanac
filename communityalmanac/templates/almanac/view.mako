<%inherit file="/base.mako" />
<h2>${c.almanac.name}</h2>
% if c.almanac.pages:
  <h3>Pages</h3>
  <ul>
    % for page in c.almanac.pages:
    <li>${h.link_to(page.name, h.url_for('page_view', almanac=c.almanac, page=page))}</li>
    % endfor
  </ul>
% endif

<p>${h.link_to('Add', h.url_for('page_create', almanac=c.almanac))} a page</p>

<%def name="title()">
${c.almanac.name} - Community Almanac
</%def>
