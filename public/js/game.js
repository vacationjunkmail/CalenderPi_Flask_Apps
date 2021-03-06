//https://www.codexworld.com/inline-table-edit-delete-jquery-ajax-php-mysql/
$(function()
{
	const regex = /([a-z]+)_(\d{1,})/;

	//var csrf_token = $(".csrf_token").text();
	var csrf_token = $("input[name='csrf_token'").val();
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

	$("#previous,#next").click(function(event)
	{
		var pageid = parseInt($("#pageid").val());
		if(this.id == "next"){
			pageid=pageid+50;
			$("#previous").show();
		}
		else if(this.id == "previous")
		{
			if(pageid >0)
			{
				pageid=pageid-50;
			}
			else
			{
				pageid=0;
			}
		}
		else
		{
			console.log("Something happened....search is reset");
		}
		if(pageid==0)
		{
			$("#previous").hide();
		}
		//ajax call to route to get new data
		form_data = {pageid:pageid};
		$.ajax(
		{
			url: '/games/admin/video_games/',
			data: form_data,
			type: 'POST',
			beforeSend: function(xhr, settings) {
            	if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
               		xhr.setRequestHeader("X-CSRFToken", csrf_token);
            	}
				else {
					console.log(settings.type);
				}	
        	},
			success: function(resp)
			{
				$("#data_row").empty();
				
				for(var i = 0; i<resp[0][1].length; i++){
					id=resp[0][1][i].id
					cid=resp[0][1][i].console_id
					lbx=' data-lightbox="data_'+id+'" data-title="'+resp[0][1][i].name+'"';
					imgclass=" class='btn btn-default btn-sm'"
					e='<td><a href="/games/admin/video_games/'+id+'/'+pageid+'/" role="button" class="btn btn-default btn-sm">Edit</a></td>'
					n='<td>'+resp[0][1][i].name+'</td>'
					s='<td><a href="/public/images/'+resp[1][cid]+'/small/'+resp[0][1][i].small_image+'"'+lbx+imgclass+'>Small Image</a></td>'
					l='<td><a href="/public/images/'+resp[1][cid]+'/large/'+resp[0][1][i].large_image+'"'+lbx+imgclass+' >Large Image</a></td>'
					c='<td>'+resp[1][cid]+'</td>'
					if(resp[0][1][i].header_image == '' || resp[0][1][i].header_image == null)
					{
						h='<td></td>'
					}
					else
					{
						h='<td><a href="/public/images/'+resp[1][cid]+'/header/'+resp[0][1][i].header_image+'"'+lbx+imgclass+' >Header Image</a></td>'
					}
					line='<tr id="'+id+'">"'+e+n+s+l+c+h+'"</tr>'
					$("#data_row").append(line)	
				}
			},
			error: function(err)
			{
				console.log("Error")
				console.log(err);
			}
		});//End of ajax post
		
		$("#pageid").val(pageid);
		event.preventDefault();
	});

	var row=1;
	$(".add-row").click(function()
	{
		var new_name ='newrow'; //+new_row;
		var btn ="<span name='rm' id='newrow_"+row+"' class='btn btn-danger btn-sm rm'><i class='fa fa-minus'></i> Remove</span>";
        var html = "<tr id='newrow_"+row+"'><td colspan='2'><input type='textbox' name='"+new_name+"' id='newrow_"+row+"'>"+btn+"</td></tr>";
		$(html).insertAfter(this.closest('tr'));
		row +=1;
	});

	$(".add-comment").click(function()
	{
		form_data = {comment:$('#comment').val(),game_id:$('#id').val()};
		$.ajax(
		{
			url: '/games/admin/video_games/add_comment/',
			data: form_data,
			type: 'POST',
			beforeSend: function(xhr, settings) {
            	if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
               		xhr.setRequestHeader("X-CSRFToken", csrf_token);
            	}
				else {
					console.log(settings.type);
				}	
        	},
			success: function(resp)
			{
				$("<tr><td colspan='2' id='commentid_"+resp['comment_id']+"'>"+form_data.comment+"</td></tr>").insertAfter('#game_thoughts');
				$('#comment').val('');
				
			},
			error: function(err)
			{
				console.log("Error")
				console.log(err);
			}	
		});//insert end

	});

	$(".add-character").click(function()
	{
		form_data = {character_name:$('#character_search').val(),game_id:$('#id').val()};
		$.ajax(
		{
			url: '/games/admin/video_games/add_new_character/',
			data: form_data,
			type: 'POST',
			beforeSend: function(xhr, settings) {
            	if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
               		xhr.setRequestHeader("X-CSRFToken", csrf_token);
            	}
				else {
					console.log(settings.type);
				}	
        	},
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
			csrf_token = $("input[name='csrf_token'").val();
            $.ajax({
                url: '/games/charactersearch/',
                type: 'post',
                data: {search:search, type:1},
                dataType: 'json',
		beforeSend: function(xhr, settings) {
			if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrf_token);
            		}
			else{
				console.log(settings.type);
			}	
       		},
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
			$(form_id + " li").bind("click",function()
			{
				$('#character_search').val($(this).text());
				$('#char_id').val($(this).val());
				$(form_id).empty();
				var data = {game_id:$('#id').val(),character_id:$(this).val(),character_name:$(this).text()};
				$.ajax(
				{
					url: '/games/admin/video_games/add_character/',
					data: data,
					type: 'POST',
					beforeSend: function(xhr, settings) {
			            	if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
						xhr.setRequestHeader("X-CSRFToken", csrf_token);
		            		}
					else {
						console.log(settings.type);
					}	
				},
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
	$('#character_tbl').on('click','.editBtn',function(){ 
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
	$('#character_tbl').on('click','.cancelBtn',function(){
		$(this).closest("tr").find(".editSpan").show();
		$(this).closest("tr").find(".editInput").hide();
		$(this).closest("tr").find(".editBtn").show();
		$(this).closest("tr").find(".cancelBtn").hide();
		$(this).closest("tr").find(".saveBtn").hide();
	});
	//End of Cancel Character Button

    $('#character_tbl').on('click','.saveBtn',function(){
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
			beforeSend: function(xhr, settings) {
            	if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                	xhr.setRequestHeader("X-CSRFToken", csrf_token);
            	}
				else{
					console.log(settings.type);
				}	
        	},
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


function validate(r)
{
	if(!r.ok)
	{
		throw Error('Danger Will Robinson');
	}
	return r;
}

function getdata(r)
{
	return r.json()
}

function dsp_data(results)
{
	document.getElementById("data_row").innerHTML="";
	for(var i = 0; i<results.length; i++)
	{
		row = ''
		row+="<tr><td><a href='/games/admin/video_games/"+results[i]['id']+"/0/' role='button' class='btn btn-default btn-sm'>Edit</a></td><td>"+results[i]['name']+"</td>";
		row+="<td><a href='/public/images/"+results[i]['console_shortname']+"/small/"+results[i]['small_image']+"' data-lightbox='data_"+i+"' data-title='"+results[i]['name']+"' class='btn btn-default btn-sm'>Small Image</a></td>";
		row+="<td><a href='/public/images/"+results[i]['console_shortname']+"/large/"+results[i]['large_image']+"' data-lightbox='data_"+i+"' data-title='"+results[i]['name']+"' class='btn btn-default btn-sm'>Large Image</a></td><td>"+results[i]['console_shortname']+"</td>";
		if(results[i]['header_image'])
		{ 
			row+="<td><a href='/public/images/"+results[i]['console_shortname']+"/header/"+results[i]['header_image']+"' data-lightbox='data_"+i+"' data-title='"+results[i]['name']+"' class='btn btn-default btn-sm'>Header Image</a></td>";
		}
		else 
		{
			row+="<td></td>";
		}
		row+="</tr>";
		document.getElementById("data_row").innerHTML+=row;
	}
}

function showerror(error)
{
	console.log("An error occured:\n",error);
}

//document.querySelector("#search_game_btn").addEventListener("click",(e) =>{
const search_game = document.querySelector("#search_game_btn");

if(search_game)
{
	search_game.addEventListener("click",(e) =>{
	form_data = {'search':document.getElementById("search_game").value};

	var csrf_token = document.getElementById("csrf_token").value;

	document.getElementById("search_game").innerHTML="";
	//let loader = "<div class='loading'></div>";
	let loader = '<div class="loading_image"><img alt ="" src="/public/images/loader.gif "></div>';
	document.getElementById("data_row").innerHTML+=loader;

	var url = "/games/admin/search_video_games/";
	fetch(url,{
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
			'X-CSRF-TOKEN':csrf_token,
		},
		body:JSON.stringify(form_data),
		credentails: 'include'
	})
	.then(validate)
	.then(getdata)
	.then(dsp_data)
	.catch(showerror)
	
	event.preventDefault();
	});
}

function fade (show) {
	var para = document.getElementById("show_message");
  	if(show) {
    	para.classList.remove("hide");
    	para.classList.add("show");
  	} else {
    	para.classList.remove("show");
    	para.classList.add("hide");
	}
}
