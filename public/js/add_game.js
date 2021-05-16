/*var el = document.querySelector('.more_details');
el.style.display = 'none';
*/

/*document.querySelector(".add-new-game").addEventListener("click",(e) =>{
	el.style.display = '';
	var new_game_btn = document.querySelector('#new_game_btn_row');
	new_game_btn.style.display = 'none';
	var title = document.getElementById("title").value;
	var console_id = document.getElementById("console_id").value;
	var small_image = document.getElementById("small_image").value;
	var large_image = document.getElementById("large_image").value;
	var header_image = document.getElementById("header_image").value;

	data = {'title':title,'console_id':console_id,'small_image':small_image,'large_image':large_image,'header_image':header_image};
	console.log(data);

	event.preventDefault();
	document.getElementById("id").value="thisid";
});
*/
var ready = (callback) => 
{
	if(document.readyState != "loading") callback();
	else document.addEventListener("DOMContentLoaded", callback);
	
}
/* Jquery like ready state 
	https://tobiasahlin.com/blog/move-from-jquery-to-vanilla-javascript/
*/
ready(() =>{
	
var csrf_token = document.getElementById("csrf_token").value;
console.log(csrf_token)
	var el = document.querySelector('.more_details');
	el.style.display = 'none';
	document.querySelector(".add-new-game").addEventListener("click",(e) =>{
		el.style.display = '';
		var new_game_btn = document.querySelector('#new_game_btn_row');
		new_game_btn.style.display = 'none';
		var title = document.getElementById("title").value;
		var console_id = document.getElementById("console_id").value;
		var small_image = document.getElementById("small_image").value;
		var large_image = document.getElementById("large_image").value;
		var header_image = document.getElementById("header_image").value;

		form_data = {'title':title,'console_id':console_id,'small_image':small_image,'large_image':large_image,'header_image':header_image};

		//event.preventDefault();
		document.getElementById("id").value="thisid";

		url = "/games/admin/video_games/add_new_game";
		fetch(url,{
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRF-TOKEN':csrf_token,
			},
			body:JSON.stringify(form_data),
			credentials:'include'
		})
		.then(validate)
		.then(getdata)
		.then(do_something)
		.catch(handle_error)

	});
	event.preventDefault();

});
