import os
import scan
import writer
import time
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from collections import Counter

class Witness:

	def __init__(self):
		self.common_ports = [80, 443, 8443, 8080]
		self.image_dir = './images/'
		self.urls_to_filenames = {}
		# self.make_browser()
		self.max_retries = 3

	def make_browser(self, headless=True):
		options = Options()
		options.headless = headless
		options.keep_alive = False
		options.accept_untrusted_certs = True
		options.add_argument('--allow-running-insecure-content')
		options.add_argument('--ignore-certificate-errors')
		self.driver = webdriver.Firefox(options = options)

	def parse_input_file(self, input_file):
		""" Read domains from an input file. 
		"""
		f = open(input_file, 'r')
		domains = f.readlines()
		domains = [d.replace("\n", "") for d in domains if d]
		domains = [d.lstrip() for d in domains if d]
		domains = [d.rstrip() for d in domains if d]
		domains = sorted(list(set(domains)))
		return domains

	def capture(self, input_file):
		""" Screenshot all URLs of the given domain and write results to viewer.html
		"""
		domains = self.parse_input_file(input_file)
		self.make_browser()
		self.urls = []
		assert(len(domains) > 0), 'Error: file at path {} is empty, no domains loaded.'.format(input_file)
		# print("initializing...", end="\r")
		num_domains = len(domains)
		domain_ctr = 0
		for domain in domains:
			domain_ctr += 1
			domain_prct = int(100.*float(domain_ctr)/float(num_domains))
			print("scanning {} ({}/{}) [ {} %]".format(domain, domain_ctr, num_domains, domain_prct), end='\r')
			self.urls = self.urls + scan.get_urls(domain, ports=self.common_ports)
		print("")
		exception_ctr = Counter()
		num_urls = len(self.urls)
		url_ctr = 0
		for u in self.urls:
			url_ctr += 1
			url_prct = int(100.*(float(url_ctr)/float(num_urls)))
			print("capturing {} ({}/{}) [ {} %]".format(u, url_ctr, num_urls, url_prct), end='\r')
			try:
				self.screenshot_url(u)
			except Exception as e:
				# print("error capturing {}".format(u))
				if exception_ctr[u] < self.max_retries:
					exception_ctr[u] += 1
					# print("... retry ({}/{})".format(exception_ctr[u], self.max_retries))
					self.driver.quit()
					self.make_browser()
		self.driver.quit()
		print("\nwriting viewer.html")
		self.write()
		print("archiving viewer")
		self.archive()
		print("archived to {}".format(self.archive_path))
		# open viewer in browser 
		print("opening viewer.html")
		self.make_browser(headless=False)
		self.driver.get(os.path.abspath(self.archive_path+"/viewer.html"))

	def write(self):
		# write results
		writer.write_viewer(self.urls_to_filenames, self.image_dir)

	def archive(self):
		""" archive image files and viewer
		"""
		ts = int(time.time())
		archive_path = "./archives/"+str(ts)
		self.archive_path = archive_path		
		os.mkdir(archive_path)
		os.mkdir(archive_path+"/images")
		os.rename("viewer.html", archive_path+"/viewer.html")
		image_files = os.listdir("./images")
		for ifn in image_files:
			if not '.png' in ifn:
				continue
			os.rename("./images/"+ifn, archive_path+"/images/"+ifn)

	def screenshot_url(self, url):
		""" Take a screenshot of the URL.
		"""
		self.driver.get(url)
		sleep(1)
		screenshot_filename = Witness.url_to_filename(url)
		self.urls_to_filenames[url] = screenshot_filename
		# print(screenshot_filename)
		self.driver.get_screenshot_as_file(self.image_dir + screenshot_filename)

	@staticmethod
	def url_to_filename(url):
		""" Generate a screenshot filename from a URL.
		"""
		# print("creating filename from {}".format(url))
		screenshot_filename = url.replace(":","_")
		screenshot_filename = screenshot_filename.replace('/', '')
		screenshot_filename = screenshot_filename.replace('.','_')
		screenshot_filename = screenshot_filename + '.png'
		return screenshot_filename

if __name__ == "__main__":
	w = Witness()
	assert(len(sys.argv) == 2), "Error: please supply filepath with domain names as argument (e.g. python witness.py ./domains.txt)"
	assert(os.path.exists(sys.argv[1])), "Error: supplied filepath {} does not exist.".format(sys.argv[1])
	w.capture(sys.argv[1])