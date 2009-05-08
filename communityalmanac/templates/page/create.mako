<%inherit file="/base.mako" />
<h2>Create page</h2>
<form id="page-title-form"  method="post" action="${request.path_url}">
    <input id="page-title" type="text" name="title" value="Page Name" />
  </form>
  <ul class="page-media-tools">
    <li>${h.link_to('Text', h.url_for('page_form_text'), id='text-tool')}</li>
    <li>${h.link_to('Map', h.url_for('page_form_map'), id='map-tool')}</li>
  </ul>
  <div class="session-data">
    <ul>
      <li>(Stub for session data)</li>
    </ul>
  </div>
  <div id="form-container">
  </div>
  <form id="submit-button-form" method="post" action="${request.path_url}">
    <input type="submit" value="Publish" />
  </form>
</div>