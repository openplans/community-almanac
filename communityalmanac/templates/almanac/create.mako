<%inherit file="/base.mako" />
<form method="post" action="${h.url_for('almanac_create')}">
  <fieldset>
    <legend>Create Almanac</legend>
    <div class="selfclear">
      <label for="almanac-name">Name</label>
      <input type="text" name="name" id="almanac-name" value="${request.POST.get('name', u'')}" />
    </div>
    <input class="indented-submit" type="submit" value="Add" />
  </fieldset>
</form>

<%def name="title()">Create Almanac</%def>
