%if c.user:
  %if c.page.on_behalf_of:
    <div class="page-meta"><p>On <a class="on_behalf_of" href="${h.url_for('behalf-form', page_id=c.page.id)}">behalf</a> of ${c.page.on_behalf_of}</p></div>
  %else:
  <div class="page-meta"><p>By ${c.user.username} (<a class="on_behalf_of" href="${h.url_for('behalf-form', page_id=c.page.id)}">on behalf of</a>)</p></div>
  %endif
%endif
