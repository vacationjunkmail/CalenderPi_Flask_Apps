$(function()
{
	const regex = /([a-z]+)_(\d{1,})/;

	function regex_function(str)
	{
		let m;
		m = regex.exec(str);
		return m;
	}
	
	var row=1;
	$(".add-row").click(function()
	{
		var new_name ='newrow'; //+new_row;
		var btn ="<span name='rm' id='newrow_"+row+"' class='btn btn-danger btn-sm rm'><i class='fa fa-minus'></i> Remove</span>";
        var html = "<tr id='newrow_"+row+"'><td colspan='2'><input type='textbox' name='"+new_name+"' id='newrow_"+row+"'>"+btn+"</td></tr>";
		$(html).insertAfter(this.closest('tr'));
		row +=1;
	});

	$('#data_tbl').on('click','.rm',function()
	{
		$('#'+this.id).remove();
		v = regex_function(this.id);

		if(typeof v === 'object' && v != null && v[1] =='row')
		{
			$.ajax(
			{
				url: '/games/admin/video_games/rm_char_remove/',
				data: {id: v[2]},
				type: 'GET',
				dataType: 'json',
				success: function(resp)
				{
					//console.log(resp);
				},
				error: function(err)
				{
					console.log(err);
				}
			});
		}
	});
});
