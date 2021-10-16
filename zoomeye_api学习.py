import requests
import sys
import json
import argparse

access_token = ""
ip_list=[]

def help():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-u','--user',type=str,help='input username')
	parser.add_argument('-p','--password',type=str,help='input password')
	args = parser.parse_args()
	return args


def login(u,p):
	user = u
	passwd = p
	data = {'username':user,'password':passwd}
	data_encode = json.dumps(data)
	try:
		r = requests.post('https://api.zoomeye.org/user/login',data=data_encode)
		r_decoded = json.loads(r.text)
		global access_token
		access_token = r_decoded['access_token']
	except Exception as e:
		print(e)
		sys.exit(1)


def api_Test():
	page = 1
	global access_token
	global ip_list
	headers = {'Authorization' : 'JWT ' + access_token,}
	try:
		r=requests.get('https://api.zoomeye.org/host/search?query=app:"apache web server 2.4.49 2.4.50"&facet=app,os&page=3',headers=headers)
		r_decoded = json.loads(r.text)
		for x in r_decoded['matches']:
			print(x['ip'])
			ip_list.append(x['ip'])
	except Exception as e:
		if str(e.message) == 'matches':
			print('[-] info : account was break, excceeding the max limitations')
		else:
			print(e)
		sys.exit(1)

def main():
	global ip_list
	args = help()
	login(args.user,args.password)
	api_Test()
	ip_list=tuple(ip_list)
	with open('url.txt','w') as file:
		for i in ip_list:
			file.write('http://'+i+'')
			file.write('\n')



if __name__ == '__main__':
	main()
