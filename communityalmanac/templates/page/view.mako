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
<h2>${c.page.name}</h2>
%if c.media_items:
  <div class="session-data">
    <ul>
      %for media_item in c.media_items:
        <li>${media_item}</li>
      %endfor
    </ul>
  </div>
%endif

<div class="comments-head selfclear">
  <% n = len(c.page.comments) %>
  <h3>
    %if n == 1:
      1 comment
    %else:
      ${len(c.page.comments)} Comments
    %endif
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
    <div class="form-row">
      <h3 id="comment-submit"><a class="comment-link" href="${h.url_for('page_view', almanac=c.almanac, page=c.page)}">Add Comment</a></h3>
    </div>
  </form>
</div>

<%def name="title()">
${c.page.name} - ${c.almanac.name} - Community Almanac
</%def>
<%def name="bookmark()">
<div id="backtoc" class="pngfix">
  <a href="${h.url_for('almanac_view', almanac=c.almanac)}"><span>&laquo; ${c.almanac.name}</span></a>
</div>
</%def>
<%!
prev_page_url = "#"
prev_page = "Next Page Name"
next_page_url = "#"
next_page = "Previous Page Name"
%>
