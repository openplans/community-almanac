$(document).ready(function() {

  // add the title to the submit button form
  $('#submit-button-form').submit(function() {
      var title = $('#page-title').val();
      var newinput = $('<input type="hidden" name="name" value="' + title + '" />');
      newinput.appendTo($(this));
      return true;
  });

  // clicking on page title erases text already there
  $('#page-title').focus(function() {
      if ($(this).val() == "Page Name") {
        $(this).val("");
      }
  }).blur(function() {
      if ($(this).val() == "") {
        $(this).val("Page Name");
      }
  });

  var tools = [{
      link: $('#text-tool'),
      submitfn: submit_handler
    }, {
      link: $('#map-tool'),
                submitfn: submit_handler
    }
  ];

  for (var i = 0; i < tools.length; i++) {
      var fn = function(i) {
        var tool = tools[i];
        var link = tool.link;
        var submitfn = tool.submitfn;

        // when somebody tries to add a particular media type, fetch the form from
        // the server, and attach the behavior to it
        link.click(function(e) {
          e.preventDefault();
          var url = $(this).attr('href');

          var formcontainer = $('#form-container');
          $.get(url, null, function(data) {
            formcontainer.empty();
            formcontainer.show();
            $(data).appendTo(formcontainer).slideDown('fast');
            $('form.media-item a.media-cancel').click(function(e) {
              e.preventDefault();
              formcontainer.slideUp('fast').empty();
            });
            $('form.media-item').submit(submitfn);
          });
        });
      }
      fn(i);
    }
});

function submit_handler(e) {
  e.preventDefault();
  var url = $(this).attr('action');
  var data = $('form.media-item').serialize();
  var formcontainer = $('#form-container');

  $.ajax({
    contentType: 'application/x-www-form-urlencoded',
    data: data,
    success: function(data, textStatus) {
      formcontainer.empty();
      var newLi = $('<li></li>');
      newLi.appendTo($('.session-data ul'));
      $('<div>' + data + '</div>').appendTo(newLi).fadeIn('slow');
      },
    type: "POST",
    url: url
  });
};
