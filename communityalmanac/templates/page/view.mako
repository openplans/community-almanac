<%doc><!--
# Community Almanac - A place for your stories.
# Copyright (C) 2009  Douglas Mayle, Robert Marianski,
# Andy Cochran, Chris Patterson

# This file is part of Community Almanac.

# Community Almanac is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Community Almanac is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Community Almanac.  If not, see <http://www.gnu.org/licenses/>.
--></%doc>
<%inherit file="/base.mako" />
<h2 class="page-title">${c.page.name}</h2>
<div class="page-meta">By ${c.page.author} | ${c.page.creation_date_string} | <a href="#comments">${h.plural(len(c.page.comments), 'Comment', 'Comments')}</a></div>
<a href="${h.url_for('page_edit', almanac=c.almanac, page=c.page)}" title="Edit Page">Edit</a>
%if c.media_items:
  <div>
    <ul class="page-items">
      %for media_item in c.media_items:
        <li class="page-item">${media_item}</li>
      %endfor
    </ul>
  </div>
%endif

<div class="comments-head selfclear">
  <% n = len(c.page.comments) %>
  <h3 id="comments">
    ${h.plural(len(c.page.comments), 'Comment', 'Comments')}
    <a class="comment-link" href="#comment">Leave a comment</a>
  </h3>
</div>

% for comment in c.page.comments:
<div class="comment">
  <p class="meta">
    <span>
    %if comment.website:
      <a href="${comment.website}">${comment.fullname} says:</a>
    %else:
      ${comment.fullname} says:
    %endif
    </span> ${comment.creation.strftime('%H:%M %B %d, %Y')}
  </p>
  <p>${comment.text}</p>
</div>
% endfor

<div class="comments-footer">
  <h3 id="comment-bttn"><a class="comment-link" href="#">Leave a comment…</a></h3>
  <form action="${h.url_for('page_view', almanac=c.almanac, page=c.page)}" method="post" id="comment-form" style="display: none;">
    <div class="form-row">
      <label for="fullname">Full Name <span class="required">* </span></label>
      <input type="text" class="textType" id="fullname" name="fullname" size="20" value=""/>
    </div>
    <div class="form-row">
      <label for="email">Email <span class="required">* </span><span class="note">(will not be displayed)</span></label>
      <input type="text" class="textType" id="email" name="email" size="20" value=""/>
    </div>
    <div class="form-row">
      <label for="website">Website</label>
      <input type="text" class="textType" id="website" name="website" size="20" value=""/>
    </div>
    <div class="form-row">
      <label for="body">Comment <span class="required">* </span></label>
      <textarea cols="60" name="text" rows="15"></textarea>
    </div>
    %if g.captcha_enabled and not c.user:
      <div class="form-row">
        <input type="hidden" name="recaptcha_marker_field" />
        ${c.captcha_html}
      </div>
    %endif
    <div class="form-row">
      <h3 id="comment-submit"><a class="comment-link" href="${h.url_for('page_view', almanac=c.almanac, page=c.page)}">Add your Comment</a></h3>
    </div>
  </form>
</div>

<%def name="extra_body()">
  <script type="text/javascript">
    pageMapFeatures = ${c.map_features};
    flowplayerElts = ${c.flow_data};
  </script>
  <script type="text/javascript" src="/js/flowplayer/flowplayer-3.1.1.min.js"></script>
</%def>

<%def name="title()">
${c.page.name} - ${c.almanac.name}
</%def>
<%def name="bookmark()">
<div id="backtoc" class="pngfix">
  <a href="${h.url_for('almanac_view', almanac=c.almanac)}"><span>&laquo; ${c.almanac.name}</span></a>
</div>
</%def>

<%def name="pagenav()">
<%
if c.prev_page:
    ptext = h.literal('&#171; ' +c.prev_page.name)
    purl = h.url_for('page_view', almanac=c.almanac, page=c.prev_page)
else:
    ptext = purl = None
if c.next_page:
    ntext = h.literal(c.next_page.name + ' &#187;')
    nurl = h.url_for('page_view', almanac=c.almanac, page=c.next_page)
else:
    ntext = nurl = None
%>
${parent.pagenav(purl, ptext, nurl, ntext)}
</%def>
