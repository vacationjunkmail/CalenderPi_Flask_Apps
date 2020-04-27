$(document).ready(function() 
{
	$('#calendar').fullCalendar(
	{
      		header: 
		{
		      	left:'prev,next today',
			center: 'title',
			right: 'month,basicWeek,basicDay'
		},
		//defaultDate: '2018-10-12',
		navLinks: true,
      		editable: true,
      		eventLimit: true, // allow "more" link when too many events
      		/*events:
		{
      			url: '/calendar_data/',
			dataType:"json",
			type: "GET",
			contentType: "application/json",
			success: function(d)
			{
				alert(d);	
				
			},
			error: function()
			{
				$('#calendar-warning').show()
			}
      		}
     		*/ 
		events: function(start, end, callback) 
		{
			$.ajax(
			{
				url: '/calendar_data/',
				dataType: 'json',
				//contentType: "application/json",
				type: "GET",		
				data: 
				{
					start: start.unix(),
					end: end.unix()
				},
				success: function(response) 
				{
					console.log(response.data.length);
					//alert(response.data.length);
					var events = [];
					console.log(response.data[0].title);
					for(var i = 0; i < response.data.length; i++)
					{
						//alert(response.data[i].title);
						$('#test').val(response.data[i].title);					
					}
					callback(events);
				}
			});
		}
	});
});
