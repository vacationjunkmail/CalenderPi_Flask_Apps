$(document).ready(function(){
		var csrftoken = "{{ csrf_token () }}";
		$('form').on('submit',function(event) 
		{
			event.preventDefault();
			$.ajax(
			{
				url: '/calendar/add/',
				data: $('form').serialize(),
				type: 'POST',
				beforeSend:function(xhr,settings)
				{
					var csrftoken = $('meta[name=csrf-token]').attr('content');
					//if (!/^(GET|HEAD|OPTIONS|TRACE|POST)$/i.test(settings.type) && !this.crossDomain) 
					//{
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
					//}
				},
				success: function(response) {
					console.log(response);
				},
				error: function(error) 
				{
					console.log(error);
				}
			});      
		});
	});