<%inherit file="/base.mako" />
<%def name="sidebar()">
</%def>
<h1>Oh no! Where's the page?</h1>
<p>We can't seem to find what you're looking for. There could be a typo in your address. Or perhaps the page has moved. You could go back to the Community Almanac <a href="${h.url_for('home')}">home</a> or try a search...</p>
  <form action="${h.url_for('site_search', query='form')}" method="post" id="searchform">
    <input type="text" onfocus="if(this.value=='Search&hellip;') this.value='';" onblur="if(this.value=='') this.value='Search&hellip;';" tabindex="1" size="20" value="Search&hellip;" class="text" name="query" id="query"/>
    <input type="image" align="absmiddle" src="/img/search-submit.png" tabindex="2" value="Find" name="searchsubmit" id="searchsubmit"/>
  </form>
<p>If it turns out that a link is broken, we'd like to know. Please <a href="/contact">contact us</a>.</p>

<%def name="body_class()">fourhundred</%def>
<%def name="title()">
Oh no! Where's the page?
</%def>
