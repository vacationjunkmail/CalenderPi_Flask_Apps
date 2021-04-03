/*document.querySelector("#find-char").addEventListener("click", (e) => {

	alert("asdfa");
	event.preventDefault();
});
*/
function validate(r){
	if(!r.ok)
	{
		throw Error('This was an error');
	}
	return r;
}
function getdata(r)
{
	return  r.json()
}

function createtbl(results)
{
	document.getElementById("data_row").innerHTML="";
	document.getElementById("search_value").innerHTML="";
	var tbl="";
	if(results[0][1]){
		results = results[0][1];
	}
	for(var i=0;i<results.length; i++)
	{
		tbl+="<tr><td>"+results[i]['id']+"<input type='hidden' id='id' name='id' value='"+results[i]['id']+"' class='editInput'></td>";
		tbl+="<td><span class='editSpan character_name'> "+results[i]['name']+"</span> <input type='text' class='editInput form-control input-sm' name='character_name' id='character_name' value='"+results[i]['name']+"' style='display:none;' > </td>";
		tbl+="<td><span class='editSpan display_order'>"+results[i]['display_order']+"</span><input type='text' name='display_order' id='display_order' value='"+results[i]['display_order']+"' class='editInput form-control input-sm' style='display:none;'></td>";
		tbl+="<td><div class='btn-group btn-group-sm'><button type='button' class='btn btn-sm btn-default editBtn' style='float: none;'><span class='glyphicon glyphicon-pencil'></span></button><button type='button' class='btn btn-sm btn-default cancelBtn' style='float: none; display:none;'><span class='glyphicon glyphicon-ban-circle'></span></button></div><button type='button' class='btn btn-sm btn-success saveBtn' style='float: none; display: none;'>Save</button><button type='button' class='btn btn-sm btn-danger confirmBtn' style='float: none; display: none;'>Confirm</button></td></tr>";
	}
	
	document.getElementById("data_row").innerHTML=tbl ;
}

function shwerror(error)
{
	console.log("An error occured:\n",error);
}

function associated_characters_games(results)
{
	var modal_data="Associated with no games;";
	if(results.length)
	{
		modal_data = "";
		for(var i=0;i<results.length;i++){
			modal_data+=results[i]['game_name']+" on "+results[i]['console_shortname']+"<br />";
			//modal_data+=results;
		}
	}
	document.getElementById("modal_body").innerHTML=modal_data;
}

function getmore(d)
{
	document.getElementById("modal_body").innerHTML="";
	document.getElementById("modal_title").innerHTML=d.dataset.gamename;
	data = {'data':d.id};
	fetch('/games/associated_characters_games/',
	{
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
			'X-CSRF-TOKEN':csrf_token.value
		},
		body:JSON.stringify(data),
		credentials: 'include'
	})
	.then(validate)
	.then(getdata)
	.then(associated_characters_games)
	.catch(shwerror)
	//document.getElementById("modal_body").innerHTML="changed";
}

function getchar()
{
	data = {'search': document.getElementById("search_value").value};
	
	fetch('/games/charactersearch/',
	{
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
			'X-CSRF-TOKEN':csrf_token.value
		},
		body:JSON.stringify(data),
		credentials: 'include'
	})
	.then(validate)
	.then(getdata)
	.then(createtbl)
	.catch(shwerror)
}

//more characters
document.querySelector("#characternext").addEventListener("click", (e) => { 
	var pageid = parseInt(document.getElementById("pageid").value);
	if(e.target.id == "characternext"){
		pageid=pageid+50;
		//$("#previous").show();
	}
	else if(e.target.id == "characterprevious")
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
    data = {"pageid":pageid};
	var url = '../characters/50/';
    fetch(url, {
    	method: 'POST', 
        headers: {
        	'Content-Type': 'application/json',
          	'X-CSRF-TOKEN': csrf_token.value
        },
        body: JSON.stringify(data),
        credentials: 'include'
	})
	.then(validate)
	.then(getdata)
	.then(createtbl)
	.catch(shwerror)	
    /*.then(response => response.json())
        .then(res => {
            data = res[0][1]
            col = res[0][0]
            var data_row='';
            var data_col='';
            var value = '';
            if(data.length > 0)
			{
				document.getElementById("data_row").innerHTML="";
				for(var a=0;a<data.length; a++)
				{
					data_row='<tr>';
					for(var b=0;b<col.length; b++)
					{
						value=data[a][col[b]];				
						data_row+='<td>';
						if(col[b] == 'id'){
							data_row+=value;
							data_row+='<input type="hidden" name="id" id="id" value="'+value+'" class="editInput" />';
						} else if(col[b] == 'name') {
							data_row+='<span class="editSpan character_name">'+value+'</span>';
							data_row+='<input type = "text" class="editInput form-control input-sm" name="character_name" id="character_name" value="'+value+'" style="display: none;" />';
						} else if(col[b] == 'display_order'){
							data_row+='<span class="editSpan display_order">'+value+'</span>';
							data_row+='<input type="text" name="display_order" id="display_order" value="'+value+'" class="editInput form-control input-sm" style="display:none;" />';
						}
						
						data_row+='</td>';
					}
					data_row+='<td> <div class="btn-group btn-group-sm">'+
					'<button type="button" class="btn btn-sm btn-default editBtn" style="float: none; display: inline-block;"><span class="glyphicon glyphicon-pencil"></span></button>'+
					'<button type="button" class="btn btn-sm btn-default cancelBtn" style="float: none; display:none;"><span class="glyphicon glyphicon-ban-circle"></span></button>'+
					'</div>'+
					'<button type="button" class="btn btn-sm btn-success saveBtn" style="float: none; display: none;">Save</button>'+
					'<button type="button" class="btn btn-sm btn-danger confirmBtn" style="float: none; display: none;">Confirm</button>'+
					'</td>';
					data_row+='</tr>';
					document.getElementById("data_row").innerHTML += data_row;
				}	
			}
        })
        .catch((error) => {
            console.log("error happened")
        });
    	*/
    document.getElementById("pageid").value=pageid;
	event.preventDefault();
});
//end more characters

