from os import listdir,remove

def check_file_exists(image_dir,image_name):
	text_files = [f for f in listdir(image_dir) if f.endswith(image_name)]
	c = 0
	for file in text_files:
		remove("{}/{}".format(image_dir,file))
		c +=1
	return c
