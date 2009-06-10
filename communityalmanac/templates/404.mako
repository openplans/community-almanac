<%inherit file="/base.mako" />
<%def name="sidebar()">
</%def>
<h1>Oh no! Where's the page?</h1>
<p>We can't seem to find what you're looking for. There could be a typo in your address. Or perhaps the page has moved. You could go back to the Community Almanac <a href="${h.url_for('home')}">home</a> or try a search...</p>

<p>If it turns out that a link is broken, we'd like to know. Please <a href="#" onclick="alert('not implemented');">contact us</a>.</p>
<%!
error_class = "fourhundred"
%>