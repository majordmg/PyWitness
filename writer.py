""" Writes screenshot results to a viewer.html file.
"""

def write_viewer(urls_to_filenames, image_dir):
	""" 
		urls_to_filenames : a dict of URL -> screenshot filename
		image_dir : the directory in which screenshot files are saved
	"""
	assert(urls_to_filenames), "exception in write_viewer: urls_to_filenames is empty"
	with open("viewer.html", 'w') as f:
		for url, filename in urls_to_filenames.items():
			f.write('<h1><a href={} target="_blank">{}</a></h1>\n'.format(url, url))
			f.write('<img src={} style="width:500px;"/>\n'.format(image_dir+filename))
		f.write("</html>\n")


