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
<div id="about-page-text">
	<h1>What is a Community Almanac?</h1>
	<p>It's where you and your community share stories about the heart <span class="amp">&#038;</span> soul of the place you live. It's a lasting record of the place you love&#8212;the place you call home.</p>

	<h4>Anyone can contribute!</h4>
	<p>And it's free! Just <a href="/">find your community</a> and start adding to its almanac&#8212;written stories, photos, videos—anything you'd like to share.</p>
	<p>If your community has no almanac yet, simply find the your city or town on the map and add a page. Your new almanac will be created automatically.</p>

	<h4>What makes your town special?</h4>
	<p>Is it a special place? A person? A quirky custom? Share your perspective! Add pages and fill them with your content. Read other people's pages and post your replies. Get reacquainted with your town.</p>

	<h4>Make Local connections.</h4>
	<p>Community Almanac is a fun way to swap stories with your neighbors. Tell them about your favorite sledding hill or swimming hole, the best tree to climb or the coolest place to play stickball. Record memories from your life, and make connections in your community.</p>

	<h4>Share in all sorts of formats.</h4>
	<p>It's easy! Post text, pictures, audio, video and/or PDFs, kind of like a digital scrapbook. Upload video of your grandfather speaking about his childhood, or a recording of your friend singing at a local bar. Paste a poem you wrote while floating down the river in a canoe!</p>

	<h4>Connect stories with real places.</h4>
	<p>Community Almanac mapping tools let you show particular places in your community. Draw on the map to point out Main street, or the place you took that photo, or maybe even the course your canoe floated down that river.</p>

	<h4>It's community heart <span class="amp">&#038;</span> soul.</h4>
	<p>Community Almanac's non-profit sponsors (<a href="http://www.orton.org/">Orton Family Foundation</a> and <a href="http://openplans.org/">The Open Planning Project</a>) want to help communities articulate, implement and steward their heart <span class="amp">&#038;</span> soul. The Orton Family Foundation coined the term "Community Heart <span class="amp">&#038;</span> Soul" to describe the people, places, history, traditions, issues, and values that make your community unique.</p>

	<h4>And it's totally free!</h4>
	<p>Just <a href="${h.url_for('user_register')}">sign up</a> for a free, no-strings-attached account.</p>

	<h3>Ready to get started?</h3>
	<p>Just <a href="/">find your community</a> and start adding to its almanac!
</div>

<%def name="sidebar()">
<div class="sidebar">
%if c.latest_pages:
${self.recent_pages_snippet(c.latest_pages)}
%endif
</div>
</%def>
