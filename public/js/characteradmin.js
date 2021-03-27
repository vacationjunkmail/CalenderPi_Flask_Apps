//more characters
document.querySelector("#characternext").addEventListener("click", (e) => { 
	//console.log(e.target);
	//console.log(e.target.id);
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
	//console.log(csrf_token.value)
    data = {"pageid":pageid};
    //console.log(data)
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
      .then(response => response.json())
        .then(res => {
            //console.log(res[0][0])
            //console.log(res[0][1])
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
					//adding edit row data
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
			//console.log(error)
            console.log("error happened")
        });
    
    document.getElementById("pageid").value=pageid;
	event.preventDefault();
});
//end more characters

