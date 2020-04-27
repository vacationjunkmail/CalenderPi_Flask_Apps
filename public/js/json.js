$(document).ready(function() 
{
	$('#calendar').fullCalendar(
	{
      		header: 
		{
		        left: 'prev,next today',
		        center: 'title',
		        right: 'month,agendaWeek,agendaDay,listWeek'
		},
      		//defaultDate: '2018-03-12',
		editable: true,
      		navLinks: true, // can click day/week names to navigate views
      		eventLimit: true, // allow "more" link when too many events
      		events: 
		{
		        //url: '/get_calendar_data/',
			url: '/calendar_data',
		        error: function(e) 
			{
			          $('#script-warning').empty();
			          $('#script-warning').show();
			          $('#script-warning').append(e.responseText);
		        }
		},
	      	loading: function(bool) 
		{
		        $('#loading').toggle(bool);
      		}
	});

});
