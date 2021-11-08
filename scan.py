import nmap,sys,time,queue,threading
q = queue.Queue()
res = {}

def logo():
	print(" ___  ___ __ _ _ __  _ __   ___ _ __ ")
	print("/ __|/ __/ _` | '_ \| '_ \ / _ \ '__|")
	print("\__ \ (_| (_| | | | | | | |  __/ |   ")
	print("\__|___/\___\__,_|_| |_|_| |_|\___|_|")

def icmp_scan(ip):
	'''icmp协议扫描主机存活'''
	global q
	nm = nmap.PortScanner()
	nm.scan(ip,arguments='-PE -sn')
	for host in nm.all_hosts():
		if nm[host].state() == 'up':
			q.put(host)

def port_scan(ip):
	'''端口扫描'''
	global q,res
	nm = nmap.PortScanner()
	nm.scan(ip,arguments='-Pn --open -sS')
	for host in nm.all_hosts():
		portlist=[]
		if len(nm[host].all_protocols()) != 0:
			for proto in nm[host].all_protocols():
				if len(nm[host][proto].keys()) != 0:
					for port in nm[host][proto].keys():
						portlist.append(port)
		res[host]={'port':portlist}


def system_scan(ip):
	'''操作系统扫描'''
	global res
	nm = nmap.PortScanner()
	nm.scan(ip,arguments='-O')
	if 'osmatch' in nm[ip]:
		for osmatch in nm[ip]['osmatch']:
			res[ip]['osmatch']=osmatch


def getip() -> str:
	'''获取队列中的ip'''
	ip=q.get()
	q.task_done()
	return ip


def output_res():
	'''输出最后的扫描结果'''
	global res
	print('\nresult:')
	for ip in res.keys():
		print('-'*40)
		print('ip:{}'.format(ip))
		print('port:',end="")
		for port in res[ip]['port']:
			 print(port,end="、")
		print('\nsystem:{}'.format(res[ip]['osmatch']['name']))





def main():
	global q,res
	if len(sys.argv) != 2:
		logo()
		print('start in {}\nERR:not found target ip\neg:python3 scanner.py 127.0.0.1'.format(time.asctime(time.localtime(time.time()))))
		sys.exit(1)

	logo()
	print('start in {}\n welcome to you use this to scan'.format(time.asctime(time.localtime(time.time()))))
	
	icmp_scan(sys.argv[1])
	while not q.empty():
		tasks=[]
		if q.qsize() >= 20:
			for i in range(20):
				thread = threading.Thread(target=port_scan,args=(getip(),))
				thread.start()
				tasks.append(thread)
			for i in range(20):
				tasks[i].join()
		else:
			for i in range(q.qsize()):
				thread=threading.Thread(target=port_scan,args=(getip(),))
				thread.start()
				tasks.append(thread)
			for i in range(len(tasks)):
				tasks[i].join()

	if q.empty():
		for ip in res.keys():
			q.put(ip)
	else:
		print('An unknown error occurred')
		sys.exit(1)

	while not q.empty():
		tasks=[]
		if q.qsize() >= 20:
			for i in range(20):
				thread = threading.Thread(target=system_scan,args=(getip(),))
				thread.start()
				tasks.append(thread)
			for i in range(20):
				tasks[i].join()
		else:
			for i in range(q.qsize()):
				thread=threading.Thread(target=system_scan,args=(getip(),))
				thread.start()
				tasks.append(thread)
			for i in range(len(tasks)):
				tasks[i].join()
	output_res()


if __name__ == '__main__':
	main()
