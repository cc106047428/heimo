## 这里只是本人为了练手制作一个小爬虫
（本人代码能力较菜，请各位谅解,仅供个人学习参考使用）

### Markdown

源代码如下

```markdown
import requests as rq
import re
import sys
import socket
import urllib3
'''socket超时时间'''
socket.setdefaulttimeout(30)
'''关闭（不安全请求警告：正在发出未验证的HTTPS请求。强烈建议添加证书验证）警告'''
urllib3.disable_warnings()


class HttpRequest:
    def __init__(self,content):
        '''创建对象的同时设置相关设置'''
        self.__url = 'http://www.baidu.com/s'
        self.__content={'wd':content}
        self.__headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}

    def __requestOnce(self):
        '''第一次百度搜索获得http://www.baidu.com/link?=*'''
        try:
            self.__r = rq.get(self.__url,params=self.__content,headers=self.__headers,timeout=3)
            self.__r.encoding = 'utf-8'
        except:
            if str(self.__r.status_code) == '400':
                print(self.__r.status_code)
            else:
                print(self.__r.raise_for_status())
        else:
            self.__urlList1 = re.findall('https?://\w{3}\.\w{5}\.\w{3}/\w{4}\?\w{3}=[^"]*', self.__r.text)

    def __requestTwo(self):
        '''将百度搜索的获得的url进一步访问，获得跳转得到真实的url'''
        if hasattr(self,'_HttpRequest__urlList1'):
            '''urllist2用于接收跳转后真实的url，将是个2维列表'''
            self.__urlList2 = []
                # print(len(self.__urlList1))
            print('正在操作请等待:')
            while len(self.__urlList1):
                try:
                    '''给requests.get()传入 verify=False 避免ssl认证'''
                    self.__r = rq.get(self.__urlList1.pop(),headers=self.__headers,timeout=5,verify=False)
                    self.__r.encoding = 'utf-8'
                    print(len(self.__urlList1))
                except rq.exceptions.ConnectTimeout as err:
                    print('连接超时')
                except rq.exceptions.ReadTimeout as err:
                    print('读取、连接超时')
                except rq.exceptions.ConnectionError as err:
                    print('连接失败')
                else:
                    self.__urlList2.append(re.findall('https?://[\w./]*[\?\w=&]*', self.__r.text))
            print('操作完成')
            # for i in self.__urlList2:
            #     print(i)
        else:
            print('请优先进行requestOnce')
            sys.exit(0)

    def filterFuc(self):
        '''过滤函数
        1）希望过滤掉二元数组中重复的url（失败）
        2)希望过滤掉非目标的url（达成）
        3)将整合的目标url放入txt文件中(达成)
        '''
        self.__urlList3 = []
        '''一定程度上删除重复的url'''
        for i in range(len(self.__urlList2)):
            self.__urlList3.extend(self.__urlList2[i])
        del self.__urlList2
        self.__urlList3 = set(self.__urlList3)
        self.__urlList3 = list(self.__urlList3)
        '''获得目标的url，并写入文件'''
        for i in range(len(self.__urlList3)):
            tmp_list=self.__content['wd'].split(':')
            if tmp_list[1] in self.__urlList3[i]:
                self.writeToFile(self.__urlList3[i])


        # for i in range(len(self.__urlList2)):
        #     for j in range(len(self.__urlList2[i])):
        #         tmp_list=self.__content['wd'].split(':')
        #         if tmp_list[1] in self.__urlList2[i][j]:
        #             print(tmp_list[1])
        #             print(self.__urlList2[i][j])
        #             self.writeToFile(self.__urlList2[i][j])

    def writeToFile(self,content):
        with open('url.txt','a') as file:
            file.write(str(content))
            file.write('\n')

    def mainFuc(self):
        '''入口'''
        self.__requestOnce()
        self.__requestTwo()
        self.filterFuc()


if __name__ == '__main__':
    content = str(input('请输入希望搜索的信息：'))
    test = HttpRequest(content)
    test.mainFuc()
```


### 作用如下图
![image](https://user-images.githubusercontent.com/68406257/113649835-bc7b8c00-96c1-11eb-8f3b-fdd73070cecf.png)

### Support or Contact

如果有相关问题，可以咨询本人qq 1600964999
