$(function(){
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
				console.log('Error');
			}
		});

	});
});
