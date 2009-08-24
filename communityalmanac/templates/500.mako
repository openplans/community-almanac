<%inherit file="/base.mako" />
<%def name="sidebar()">
</%def>
<h1>Error</h1>

<h2>We're sorry, but something's gone wrong with the almanac.</h2>

<p>We are working on cleaning things up and we really appreciate your patience. If this keeps on happening please don't hesitate to ${h.link_to('contact', h.url_for('contact'), title='Contact us')} us.</p>

<%def name="body_class()">fivehundred</%def>
<%def name="title()">
Error
</%def>
