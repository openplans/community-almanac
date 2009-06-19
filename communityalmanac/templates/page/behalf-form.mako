<label for="on_behalf_of">On behalf of</label>
%if c.page.on_behalf_of:
  <input id="on_behalf_of" type="text" name="on_behalf_of" value="${c.page.on_behalf_of}" />
%else:
  <input id="on_behalf_of" type="text" name="on_behalf_of" value="" />
%endif
<a id="behalf-save" href="${request.url}"><img src="/img/tick.png" /></a>
<a id="behalf-cancel" href="${h.url_for('behalf', page_id=c.page.id)}"><img src="/img/cancel-icon.png" /></a>
