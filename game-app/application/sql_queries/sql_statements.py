class app_queries():
	def game_update():
		return 'update games.video_games set name=%s,console_id=%s,small_image=%s,large_image=%s,header_image=%s,game_description=%s where id=%s'
	def update_console():
		return 'update games.game_console set console_name=%s,console_shortname=%s,twitter=%s,facebook=%s  where id = %s'
	def update_character():
		return 'update games.characters set `name`= %s,display_order=%s where id = %s;'
	def select_game():
		return 'select * from games.video_games where id = %s;'
	def base_index(base):
		query = '''select * from games.{} limit 50 offset %s;'''.format(base)
		return query
	def select_characters():
		query ='''select c.id,c.name from games.video_game_and_characters as v inner join games.characters as c on c.id=v.character_id where v.video_game_id=%s'''
		return query
	def delete_character():
		return 'delete from games.video_game_and_characters where character_id = %s and video_game_id = %s;'
	def character_check():
		return 'select id,`name` from games.characters where lower(name) like %s;'
	def insert_new_character():
		return 'insert into games.characters(name)values(%s)'
	def insert_video_game_and_character():
		return 'insert into games.video_game_and_characters(video_game_id,character_id)values(%s,%s);'
	def get_character():
		return 'select * from games.characters where `name` = %s;'
	def get_console():
		return '''select * from games.game_console where id = %s;'''
	def insert_comment():
		return '''insert into games.video_game_comments(game_id,comment)values(%s,%s);'''
	def delete_comment():
		return '''delete from games.video_game_comments where id =%s and game_id=%s;'''
	def select_comments():
		return '''select id, comment,status from games.video_game_comments where game_id=%s order by id asc;'''
	def next_game():
		return '''select id from games.video_games where id > %s limit 1;'''
