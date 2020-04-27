$(function() 
{
	$.ajax(
	{
		url: '/calendar_data/',
		success: function(data) 
		{
			console.log(data);
			//alert(data.events);
			var events = [];
			//alert(JSON.stringify(data));
			for(var i = 0; i < data.length; i++)
			{
				console.log(data[i].title);
			}
			//callback(events);
		}
	});
});
