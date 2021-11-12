import os 

dirname = input('请输入目录路径:')
filename = input('请输入所需要查找文件的名称:')
basedir = 'C:\\Users\\root\\Desktop\\'+dirname
resdir=[]

if str(os.getcwd()) != basedir:
	os.chdir('{}'.format(basedir))


def find_file(dir,file) -> bool:
	global resdir
	if file in os.listdir(dir):
		resdir.append(dir+'\\'+file)
		return True
	return False

def nest_fuc(dir='')->bool:
	global basedir,dirname,filename
	
	
	if dir != '':
		os.chdir(dir) 

	if str(os.getcwd()) == basedir:
		if find_file(os.getcwd(),filename):
			return True

		for i in os.listdir(os.getcwd()):
			if os.path.isdir('{}\\{}'.format(basedir,i)):
				if nest_fuc('{}\\{}'.format(basedir,i)):
					return True
	else:
		if find_file(os.getcwd(),filename):
			return True

		for i in os.listdir(os.getcwd()):
			if os.path.isdir('{}\\{}'.format(os.getcwd(),i)):
				if nest_fuc('{}\\{}'.format(os.getcwd(),i)):
					return True
		os.chdir('../')

if nest_fuc(basedir):
	print('get it')
	print('result:',resdir.pop())
else:
	print('not found anything')
