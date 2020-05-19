class app_queries():
	def game_update():
		return 'update games.video_games set name=%s,console_id=%s,small_image=%s,large_image=%s,header_image=%s,game_description=%s where id=%s'
	def select_game():
		return 'select * from games.video_games where id = %s;'
	def base_index(base):
		query = '''select * from games.{} limit 50'''.format(base)
		return query
	def select_characters():
		query ='''select c.id,c.name from games.video_game_and_characters as v inner join games.characters as c on c.id=v.character_id where v.video_game_id=%s'''
		return query
	def delete_character():
		return 'delete from games.video_game_and_characters where character_id = %s;'
