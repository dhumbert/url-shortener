jQuery(document).ready(function($){
	if ($('a.delete-url').length) {
		$('a.delete-url').button();
		$('a.delete-url').click(function(){
			$row = $(this).closest('tr');
			$(this).button('loading');
			var url = $(this).attr('href');
			
			$.delete_(url, {}, function(){
				$row.fadeOut('fast');
			});
			
			return false;
		});
	}
});


function _ajax_request(url, data, callback, type, method) {
    if (jQuery.isFunction(data)) {
        callback = data;
        data = {};
    }
    return jQuery.ajax({
        type: method,
        url: url,
        data: data,
        success: callback,
        dataType: type
        });
}

jQuery.extend({
    put: function(url, data, callback, type) {
        return _ajax_request(url, data, callback, type, 'PUT');
    },
    delete_: function(url, data, callback, type) {
        return _ajax_request(url, data, callback, type, 'DELETE');
    }
});