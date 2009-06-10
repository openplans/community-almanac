<%inherit file="/base.mako" />
<%def name="sidebar()">
</%def>
<h1>Oh no! Where's the page?</h1>
<p>We can't seem to find what you're looking for. There could be a typo in your address. Or perhaps the page has moved. You could go back to the Community Almanac <a href="${h.url_for('home')}">home</a> or try a search...</p>
<form action="#" method="get" id="searchform">
  <input type="text" onfocus="if(this.value=='Search&hellip;') this.value='';" onblur="if(this.value=='') this.value='Search&hellip;';" tabindex="1" size="20" value="Search&hellip;" class="text" name="s" id="s"/>
  <input type="image" align="absmiddle" src="/img/search-submit.png" tabindex="2" value="Find" name="searchsubmit" id="searchsubmit"/>
</form>
<p>If it turns out that a link is broken, we'd like to know. Please <a href="#" onclick="alert('not implemented');">contact us</a>.</p>
<%!
error_class = "fourhundred"
%>