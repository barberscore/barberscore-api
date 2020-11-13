window.addEventListener("load", function() {
  (function($){
      'use strict';

      $(document).ready(function() {
          $('input[name="_buildcontests"]').bind('click', build_contests);           
      });

  })(django.jQuery);

  var $ = django.jQuery.noConflict();

  $.ajaxSetup({ 
       beforeSend: function(xhr, settings) {
           function getCookie(name) {
               var cookieValue = null;
               if (document.cookie && document.cookie != '') {
                   var cookies = document.cookie.split(';');
                   for (var i = 0; i < cookies.length; i++) {
                       var cookie = django.jQuery.trim(cookies[i]);
                       // Does this cookie string begin with the name we want?
                       if (cookie.substring(0, name.length + 1) == (name + '=')) {
                           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                           break;
                       }
                   }
               }
               return cookieValue;
           }
           if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
               // Only send the token to relative URLs i.e. locally.
               xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
           }
       } 
  });

  function build_contests()
  {
    var session_id = $('#id_entries-__prefix__-session').val();
    var kind = $('#id_kind').val();

    if (!kind) {
      alert("Please set the \"Kind\" of Session for this Entry.");
      $('#id_kind').focus();
    } else {
      var build_url = '/registration/session/'+session_id+'/build';

      $.post(build_url, { pk: session_id }, function(data){
        alert('The build has finished. This page will now refresh.');
        location.reload();
      });
    }
  }
});