window.addEventListener("load", function() {
  (function($){
      'use strict';

      $(document).ready(function() {
          $('input[name="_buildconvention"]').bind('click', build_convention);           
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

  function build_convention()
  {
    // Validate information needed for child elements
    if (is_valid_for_building()) {
      var convention_id = $('.field-id .readonly').text();

      var build_url = '/bhs/convention/'+convention_id+'/build';

      $.post(build_url, { pk: convention_id }, function(data){
        alert('The build has finished. This page will now refresh.');
        location.reload();
      });
    }
  }

  function is_valid_for_building()
  {
    // Kinds = kinds
    // Open date = open_date
    // Close date = close_date
    // Start date = start_date
    // End date = end_date
    // Timezone = timezone

    var fields = [
      'kinds',
      'open_date',
      'close_date',
      'start_date',
      'end_date',
      'timezone'
    ];

    var valid = true;

    $.each(fields, function(i, field_name){
      var $field = $('#convention_form :input[name="'+field_name+'"]');
      var field_value = $field.val();
      var field_label = $field.prev('label').text().replace(':', '');

      if (field_value.length == 0) {
        valid = false;
        alert('Please set and save the "'+ field_label +'" value before attempting to build again.');
        $field.focus();
        $('[name="_buildconvention"]').hide(); // hide button to avoid a resubmit without saving the entry
        return false;
      }
    });

    return valid;
  }
});