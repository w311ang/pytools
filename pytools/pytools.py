import os
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from pytools import _aes as aes
import pickle
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from bs4 import BeautifulSoup
import dns.resolver
from urllib.parse import urlparse

qpass=''
qfrom=''

def update(**kw):
  global qpass,qfrom
  if 'qpass' in kw:
    qpass=kw['qpass']
  if 'qfrom' in kw:
    qfrom=kw['qfrom']

def qmail(fromName,content,subject,html=False,to=None):
  to=qfrom if not to else to
  if html:
    type='html'
  else:
    type='plain'
   
  my_sender=qfrom    # 发件人邮箱账号
  my_pass = qpass              # 发件人邮箱密码
  my_user=to      # 收件人邮箱账号，我这边发送给自己
  def mail():
      msg=MIMEText(content,type,'utf-8')
      msg['From']=formataddr([fromName,my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
      msg['To']=formataddr([my_user,my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
      msg['Subject']=subject                # 邮件的主题，也可以说是标题
   
      server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
      #print(my_sender,my_pass)
      server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
      server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
      server.quit()  # 关闭连接
  mail()
  print('邮件已发送')

def jmail(fromName,subject,content,html=False,to=None):
  key=os.getenv('jmail')
  js=requests.get('https://raw.githubusercontent.com/w311ang/pytools/main/jmail.txt').text
  js=aes.AESCipher(key).decrypt(js)
  if (not qpass) and (not qfrom):
    js=json.loads(js)
    rqpass=js['qpass']
    rqfrom=js['qfrom']
    update(qpass=rqpass,qfrom=rqfrom)
  qmail(fromName,content,subject,html=html,to=to)

def echo(str):
  os.system("echo '%s'"%str)

def pickledump(var,path):
  with open(path,'wb') as f:
    pickle.dump(var,f)

def pickleread(path,*args):
  theback=args[0]
  try:
    with open(path,'rb') as f:
      return pickle.load(f)
  except FileNotFoundError:
    return theback

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def getListOfProcessSortedByCpu():
    '''
    Get list of running process sorted by Memory Usage
    '''
    import psutil

    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['cpu'] = proc.cpu_percent(interval=0.5) / psutil.cpu_count()
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['cpu'], reverse=True)

    return listOfProcObjects

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def get_pid(name):
    '''
     作用：根据进程名获取进程pid
    '''
    import psutil

    re=[]
    pids = psutil.process_iter()
    #print("[" + name + "]'s pid is:")
    for pid in pids:
        if(pid.name() == name):
            re.append(pid.pid)
    return re

def kill(name):
    import psutil

    pid=get_pid(name)
    if pid!=[]:
        for i in pid:
            p=psutil.Process(i)
            p.terminate()
    else:
        return 'not running'

def cookie2dic(rawdata):
  from http.cookies import SimpleCookie

  rawdata = 'Cookie: '+rawdata
  cookie = SimpleCookie()
  cookie.load(rawdata)

  # Even though SimpleCookie is dictionary-like, it internally uses a Morsel object
  # which is incompatible with requests. Manually construct a dictionary instead.
  cookies = {}
  for key, morsel in cookie.items():
    cookies[key] = morsel.value
  return cookies

def getip(domain):
  answers = dns.resolver.resolve(domain, 'A')
  for answer in answers:
    return answer.to_text()

passed=[]

def pas(host,pw):
  s=requests.Session()
  s.verify=False
  requests.packages.urllib3.disable_warnings()
  with s.get('http://'+host) as web:
    hometext=web.text
    homeurl=web.url
    urlp=urlparse(homeurl)
    domain=urlp.hostname
    port=urlp.port
    url='https://%s:%s'%(domain,port)
    
  if (not url in passed) and ('<title>SakuraFrp 访问认证</title>' in hometext):
    with s.get(url) as web:
      text=web.text
      soup=BeautifulSoup(text,features='lxml')
      csrf=soup.find('input',{'name':'csrf'}).get('value')
      ip=soup.find('input',{'name':'ip'}).get('value')
    with s.post(url,data={'pw':pw,'csrf':csrf,'ip':ip}) as web:
      #print(web.request.body)
      text=web.text
      soup=BeautifulSoup(text,features='lxml')
      notice=soup.find('div',{'class':'notice'}).string
      notice=notice.strip()
      print(notice)
      if '认证成功' in notice:
        passed.append(url)
      return notice
  else:
    print('已验证过')
