class app_queries():
	def game_update():
		return 'update games.video_games set name=%s,console_id=%s,small_image=%s,large_image=%s,header_image=%s,game_description=%s where id=%s'
	def select_game():
		return 'select * from games.video_games where id = %s;'
	def base_index(base):
		query = '''select * from games.{} limit 50'''.format(base)
		return query
