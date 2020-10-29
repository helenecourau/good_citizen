$(document).ready(function() {
	$('form').on('submit', function(event) {
		$.done(function(data) {
			test();
		})
	})
})