""" Contains scanning functions.
"""
import socket 

def get_urls(domain_name, ports=[80, 443, 8443, 8080]):
	""" Scan the domain for common web ports and return a full URL for each open port / protocol.
	"""
	''' too slow with nmap
	# create ports argument for nmap
	str_ports = [str(_) for _ in ports]
	nm_ports = ','.join(str_ports)
	# scan ports with nmap
	nm = nmap.PortScanner()
	s = nm.scan(domain_name, nm_ports)
	# parse nmap results to assemble full urls
	urls = []
	for ip, rdict in s['scan'].items():
		for port, port_dict in rdict['tcp'].items():
			if port_dict['state'] == 'open':
				# infer protocol
				# protocol = port_dict['name'] -- this turns out to be unreliable
				if '4' in str(port):
					protocol = 'https'
				else:
					protocol = 'http'
				# assemble url
				url = "{}://{}:{}".format(protocol, domain_name, str(port))
				urls.append(url)
	return urls
	'''
	urls = []
	for p in ports:
		if p == 80 or p == 8080:
			protocol = 'http://'
		else:
			protocol = 'https://'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		result = s.connect_ex((domain_name, p))
		if result == 0:
			new_url = protocol + domain_name + ":" + str(p)
			urls.append(new_url)
		s.close()
	return urls


if __name__ == '__main__':
	d = 'example.com'
	urls = get_urls(d)
	print(urls)