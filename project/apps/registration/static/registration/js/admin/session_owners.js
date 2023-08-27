console.log('loaded...');
window.addEventListener("load", function() {
  (function($){
    'use strict';

    $(document).ready(function() {
      $('select[name="convention"]').bind('change', update_session_owners);
      $('select[name="session"]').bind('change', update_entry_owners);
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

  function update_session_owners()
  {
    var convention_id = $('select[name="convention"]').find('option:selected').val();
    var $owners_field = $('select[name="owners"]');

    if ($owners_field.find('option:selected').length == 0) {

      var url = '/bhs/convention/'+convention_id+'/default_owners';
  
      $.post(url, { pk: convention_id }, function(owners){
        Object.keys(owners).forEach(id => {
          console.log(id, owners[id]);
          $owners_field.select2("trigger", "select", {data: { id: id, text: owners[id] }});
        })
        $('select[name="convention"]').focus();
      });
    }
  }

  function update_entry_owners()
  {
    var session_id = $('select[name="session"]').find('option:selected').val();
    var $owners_field = $('select[name="owners"]');

    if ($owners_field.find('option:selected').length == 0) {

      var url = '/registration/session/'+session_id+'/default_owners';
  
      $.post(url, { pk: session_id }, function(owners){
        Object.keys(owners).forEach(id => {
          console.log(id, owners[id]);
          $owners_field.select2("trigger", "select", {data: { id: id, text: owners[id] }});
        })
        $('select[name="session"]').focus();
      });
    }
  }

});