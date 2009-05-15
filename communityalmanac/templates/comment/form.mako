<div class="comments-footer">
  <h3 id="comment-bttn"><a class="comment-link" href="#">Leave a comment…</a></h3>
  <form action="${h.url_for('comment_form', almanac=c.almanac, page=c.page)}" method="post" id="comment-form" style="display: none;">
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
      <textarea cols="60" name="the-comment" rows="15"></textarea>
    </div>
    <div class="form-row">
      <h3 id="comment-submit"><a class="comment-link" href="#">Add Comment</a></h3>
    </div>
  </form>
</div>
