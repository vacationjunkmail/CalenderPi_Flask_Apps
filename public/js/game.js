$(function()
{	
	var new_row=1;
	$(".add-row").click(function()
	{
		var new_name ='newrow_'; //+new_row;
        var markup = "<tr id='newtrrow_"+new_row+"'><td colspan='2'><input type='textbox' name='"+new_name+"' id='"+new_name+"'></td></tr>";
        $("table tbody").append(markup);
		new_row +=1;
	});

	$('.rm').click(function()
	{
		$('#row_'+this.id).remove();
		
		$.ajax(
		{
			url: '/games/admin/video_games/rm_char/',
			data: {id: this.id},
			type: 'GET',
			dataType: 'json',
			success: function(resp)
			{
				console.log(resp);
			},
			error: function(err)
			{
				console.log(err);
				console.log('Error');
				console.log(err);
			}
		});

	});
});
