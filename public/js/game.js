//https://www.codexworld.com/inline-table-edit-delete-jquery-ajax-php-mysql/
$(function()
{
	const regex = /([a-z]+)_(\d{1,})/;

	function regex_function(str)
	{
		let m;
		m = regex.exec(str);
		return m;
	}
	
	function emptyFunction(str)
	{
		$('#character_search').val('');		
		$(str).empty();
	}

	function add_row_function(str_id,str_name)
	{
		var html = "<tr id='row_"+str_id+"'><td colspan='2' >"+str_name+" <span name='rm' id='row_"+str_id+"' class='btn btn-danger btn-sm rm'><i class='fa fa-minus'></i>Remove</span></td></tr>";	
		return html;
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

	$(".add-character").click(function()
	{
		form_data = {character_name:$('#character_search').val(),game_id:$('#id').val()};
		$.ajax(
		{
			url: '/games/admin/video_games/add_new_character/',
			data: form_data,
			type: 'POST',
			success: function(resp)
			{
				r_id = resp['character_id'];
				r_name = resp['character_name']
				var html_row = add_row_function(r_id,r_name);
				$(html_row).insertAfter('#character_data');
				//console.log(resp);
				emptyFunction('#searchResult');	
			},
			error: function(err)
			{
				console.log(err);
			}
		});//insert end
	});

	$('#data_tbl').on('click','.rm',function()
	{
		$('#'+this.id).remove();
		v = regex_function(this.id);
		game_id = $('#id').val(); 
		if(typeof v === 'object' && v != null && v[1] =='row')
		{
			$.ajax(
			{
				url: '/games/admin/video_games/rm_char/',
				data: {id: v[2],game_id:game_id},
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

	//AutoComplete
	$("#character_search").keyup(function(){
    	var search = $(this).val().trim();
        if(search != "" && search.length >= 2){

            $.ajax({
                url: '/games/charactersearch/',
                type: 'post',
                data: {search:search, type:1},
                dataType: 'json',
                success:function(response){
                	var form_id = '#searchResult';
                    var len = response.length;
                    $(form_id).empty();
                    for( var i = 0; i<len; i++){
                        var id = response[i]['id'];
                        var name = response[i]['name'];
                        $(form_id).append("<li value='"+id+"'>"+name+"</li>");
                    }

                    // binding click event to li
                    $(form_id + " li").bind("click",function(){
						$('#character_search').val($(this).text());
						$('#char_id').val($(this).val());
						$(form_id).empty();
						var data = {game_id:$('#id').val(),character_id:$(this).val(),character_name:$(this).text()};
						$.ajax(
						{
							url: '/games/admin/video_games/add_character/',
							data: data,
							type: 'POST',
							success: function(resp)
							{
								r_id = resp['character_id'];
								r_name = resp['character_name']
								var html = "<tr id='row_"+r_id+"'><td colspan='2' >"+r_name+" <span name='rm' id='row_"+r_id+"' class='btn btn-danger btn-sm rm'><i class='fa fa-minus'></i>Remove</span></td></tr>";
								$(html).insertAfter('#character_data');
								$('#character_search').val('');
							},
							error: function(err)
							{
								console.log(err);
							}
						});//insert end
                    });
                }
            });
        }
    });

	//Being of CharacterEdit
	$(".edit_character").keyup(function()
	{
		console.log("test");
		console.log(this);
	});
	
	//End of Character Edit

	//Edit Character Button 
	$('.editBtn').on('click',function(){
        //hide edit span
        $(this).closest("tr").find(".editSpan").hide();
        
        //show edit input
        $(this).closest("tr").find(".editInput").show();
        
        //hide edit button
        $(this).closest("tr").find(".editBtn").hide();
        
        //show edit button
        $(this).closest("tr").find(".saveBtn").show();
		
		//show cancel button
		$(this).closest("tr").find(".cancelBtn").show();
        
    });
	//End of Edit Character Button

	//Cancel Character Button
	$('.cancelBtn').on('click',function(){
		$(this).closest("tr").find(".editSpan").show();
		$(this).closest("tr").find(".editInput").hide();
		$(this).closest("tr").find(".editBtn").show();
		$(this).closest("tr").find(".cancelBtn").hide();
		$(this).closest("tr").find(".saveBtn").hide();
	});
	//End of Cancel Character Button

    $('.saveBtn').on('click',function(){
		$('#message').hide();	
		$('#message').empty();
		$("#message").removeClass();
        var trObj = $(this).closest("tr");
        var ID = $(this).closest("tr").attr('id');
        var inputData = $(this).closest("tr").find(".editInput");//.serialize();
		var data = {};
		$(this).closest("tr").find(".editInput").each(function()
		{
			data[this.name]=this.value;
		});
		//save action
        $.ajax({
            type:'POST',
            url:'/games/admin/characters/edit_characters/',
            dataType: "json",
			data:data,
            success:function(resp){
				if(Array.isArray(resp.msg))
				{
					for(var i = 0; i<resp.msg.length; i++){
						//console.log(resp.msg[i][0]+":"+resp.msg[i][2]);
						$('#message').append("<strong>"+resp.msg[i][0]+":</strong> "+resp.msg[i][2]+"<br/>");
						$('#message').addClass('alert alert-danger');
					}
				}
				else
				{
					$("#message").append("<strong>"+resp.msg+"</strong>").addClass('alert alert-success');
				}
				$('#message').show();
				trObj.find(".editSpan.character_name").text(data['character_name']);
				trObj.find(".editSpan.display_order").text(data['display_order']);

                trObj.find(".editInput").hide();
                trObj.find(".saveBtn").hide();
				trObj.find(".cancelBtn").hide();
                trObj.find(".editSpan").show();
                trObj.find(".editBtn").show();				
            },
			error:function(err){
				console.log(err);
			}
        });
		//end of save action

	});
});
