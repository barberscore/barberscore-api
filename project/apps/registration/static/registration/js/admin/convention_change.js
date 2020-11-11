window.addEventListener("load", function() {
  (function($){
      'use strict';

      $(document).ready(function() {
          $('#id_convention').bind('change', populate_convention);           
      });

  })(django.jQuery);

  var $ = django.jQuery.noConflict();

  function populate_convention()
  {
    var convention_id = $('#id_convention').val();
    var status = $('#id_status').val();

    $.getJSON("/bhs/convention/"+convention_id, function(json){
      if (status == 0) {
        update_form_fields(json);
      } else if (status == 2 || status == 4) {
        if (confirm('Would you like to update the fields with the data from the selected convention?')) {
          update_form_fields(json);
        }
      }
    });
  }

  function update_form_fields(json) {
    var excluded_fields = ['status'];

    $('#session_form :input').each(function(index, field){
        var field_name = $(field).attr('name');

        if (!excluded_fields.includes(field_name)) {
          if (json.data.attributes[field_name] && $(field).attr('type') != 'hidden' && $(field).attr('type') != 'undefined') {
            $(field).val(json.data.attributes[field_name]);
          }
        }
    });
  }
});