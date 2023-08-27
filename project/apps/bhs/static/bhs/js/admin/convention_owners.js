window.addEventListener("load", function() {
  (function($){
      'use strict';

      $(document).ready(function() {
          $('select[name="organization"]').bind('change', update_convention_owners);           
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

  function update_convention_owners()
  {
    var organization_id = $('select[name="organization"]').find('option:selected').val();
    var $owners_field = $('select[name="owners"]');

    if ($owners_field.find('option:selected').length > 0) {
      $owners_field.val(null).trigger('change');
    }

    var url = '/organizations/organization/'+organization_id+'/default_owners';

    $.post(url, { pk: organization_id }, function(owners){
      Object.keys(owners).forEach(id => {
        console.log(id, owners[id]);
        $owners_field.select2("trigger", "select", {data: { id: id, text: owners[id] }});
      })
      $('select[name="organization"]').focus();
    });
  }

});