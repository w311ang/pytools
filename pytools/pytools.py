import os

qpass=''
qfrom=''

def update(**kw):
  global qpass,qfrom
  if 'qpass' in kw:
    qpass=kw['qpass']
  if 'qfrom' in kw:
    qfrom=kw['qfrom']

def qmail(fromName,content,subject,html=False,to=None):
  import smtplib
  from email.mime.text import MIMEText
  from email.utils import formataddr

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

def jmail(fromName,subject,content,html=False,to=None,md=False):
  import smtplib
  from email.mime.text import MIMEText
  from email.utils import formataddr
  import requests
  from pytools import _aes as aes
  import json
  import os
  from markdown import markdown

  key=os.getenv('jmail')
  js=requests.get('https://raw.githubusercontent.com/w311ang/pytools/package/jmail.txt').text
  js=aes.AESCipher(key).decrypt(js)
  if (not qpass) and (not qfrom):
    js=json.loads(js)
    rqpass=js['qpass']
    rqfrom=js['qfrom']
    update(qpass=rqpass,qfrom=rqfrom)

  if md==True:
    content=content.replace('\n','\n\n')
    content=markdown(content)
    html=True

  qmail(fromName,content,subject,html=html,to=to)

def echo(str):
  import os

  os.system("echo '%s'"%str)

def pickledump(var,path):
  import pickle
  import os, sys

  openpath=os.path.join(os.path.split(os.path.realpath(sys.argv[0]))[0],path)
  with open(openpath,'wb') as f:
    pickle.dump(var,f)

def pickleread(path,*args):
  import pickle
  import os, sys

  theback=args[0]
  openpath=os.path.join(os.path.split(os.path.realpath(sys.argv[0]))[0],path)
  try:
    with open(openpath,'rb') as f:
      return pickle.load(f)
  except FileNotFoundError:
    return theback

def jsondump(var,path):
  import json
  import os, sys

  openpath=os.path.join(os.path.split(os.path.realpath(sys.argv[0]))[0],path)
  js=json.dumps(var)
  with open(openpath,'w') as f:
    f.write(js)

def jsonread(path,*args):
  import json
  import os, sys

  theback=args[0]
  openpath=os.path.join(os.path.split(os.path.realpath(sys.argv[0]))[0],path)
  try:
    with open(openpath,'rb') as f:
      text=f.read()
    return json.loads(text)
  except FileNotFoundError:
    return theback

def execCmd(cmd,viewErr=False):
    import subprocess

    stderr=None if viewErr else subprocess.PIPE
    cmd=cmd.split()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=stderr, text=True)
    try:
      outs, errs = proc.communicate(timeout=15)
    except TimeoutExpired:
      print('%s: TimeoutExpired'%cmd[0])
      proc.kill()
      outs, errs = proc.communicate()

    return outs

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
    import platform    # For getting the operating system name
    import subprocess  # For executing a shell command

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

def kill(name,force=True):
    import psutil
    import os

    pid=get_pid(name)
    if pid!=[]:
        for i in pid:
            if not force:
              p=psutil.Process(i)
              p.terminate()
            else:
              r=os.popen('taskkill /f /pid %s 2>&1'%i).read()
              return r
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
  import dns.resolver

  answers = dns.resolver.resolve(domain, 'A')
  for answer in answers:
    return answer.to_text()

def bypassCC(session):
  session.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 10; ONEPLUS A5010) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36'})

passed=[]

def pas(host,pw,remember=False):
  import requests
  from bs4 import BeautifulSoup
  from urllib.parse import urlparse

  s=requests.Session()
  bypassCC(s)
  s.verify=False
  requests.packages.urllib3.disable_warnings()
  with s.get('http://'+host) as web:
    homeurl=web.url
    urlp=urlparse(homeurl)
    domain=urlp.hostname
    port=urlp.port
    url='https://%s:%s'%(domain,port)
  try:
    hometext=s.get(url).text
  except urllib3.exceptions.ProtocolError:
    print('https连接错误，可能已验证')

  if (not url in passed) and ('<title>SakuraFrp 访问认证</title>' in hometext):
    with s.get(url) as web:
      text=web.text
      soup=BeautifulSoup(text,features='lxml')
      csrf=soup.find('input',{'name':'csrf'}).get('value')
      ip=soup.find('input',{'name':'ip'}).get('value')
    with s.post(url,data={'pw':pw,'csrf':csrf,'ip':ip,'persist_auth':'on' if remember==True else 'off'}) as web:
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

def tomd5(string):
  import hashlib

  hl = hashlib.md5()
  hl.update(string.encode(encoding='utf-8'))
  return hl.hexdigest()

def isnewday(path='isnewday.txt'):
  import time

  today=time.strftime("%y%m%d", time.localtime())
  try:
    with open(path) as f:
      thatday=f.read()
  except FileNotFoundError:
    thatday=None
  with open(path,'w') as f:
    f.write(today)
  if today==thatday:
    return False
  #elif thatday==None:
  #  return None
  else:
    return True

def addpush(content):
  import requests
  import os

  apiurl=os.getenv('pushapiurl')
  pw=os.getenv('pushpw')

  from pytools.pytools import bypassCC
  s=requests.Session()
  bypassCC(s)
  with s.get(apiurl+'/add',params={'content':content,'pw':pw}) as resp:
    try:
      json=resp.json()
    except:
      raise Exception('json解析失败: '+resp.text)
    status=json['status']
    if status=='OK':
      return status
    else:
      raise Exception('推送失败: '+json)

def serverchen(title,content,key=''):
  import os
  import httpx
  key=os.environ['sckey'] if not key else key
  resp=httpx.get('https://sctapi.ftqq.com/%s.send'%key,params={'title':title,'desp':content}).json()
  assert resp['code']==0, resp['message']
  return resp

def base64encode(s):
  import base64
  return base64.b64encode(s.encode('utf-8')).decode('utf-8')

def base64decode(b):
  import base64
  return base64.b64decode(b).decode('utf-8')

def find_nearest(array, value):
    import numpy as np
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def set_exit_handler(func):
    # https://danielkaes.wordpress.com/2009/06/04/how-to-catch-kill-events-with-python/
    # https://stackoverflow.com/questions/25104119/python-save-sets-to-file-on-windows-shutdown
    import os, sys
    if os.name == "nt":
        try:
            import win32api
            win32api.SetConsoleCtrlHandler(func, True)
        except ImportError:
            version = ".".join(map(str, sys.version_info[:2]))
            raise Exception("pywin32 not installed for Python " + version)
    else:
        import signal
        signal.signal(signal.SIGTERM, func)


def getpath(file):
    # https://stackoverflow.com/questions/53587322/how-do-i-include-files-with-pyinstaller
    import sys
    import os
    if getattr(sys, 'frozen', False):     
        path = os.path.join(sys._MEIPASS, file)
    else:
        path = file
    return path

def checkPgmPortOpen(pgmName, port):
    from pytools.pytools import get_pid
    import psutil

    port=int(port)
    for pid in get_pid(pgmName):
        proc = psutil.Process(pid)
        for i in proc.connections():
            if i.laddr.port==port:
                return True
    return False

def sec2time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def get_parent_process(ok_names, limit=10):
    '''Walk up the process tree until we find a process we like.

    Arguments:
        ok_names: Return the first one of these processes that we find
    '''

    import psutil
    import os

    depth = 0
    this_proc = psutil.Process(os.getpid())
    next_proc = parent = psutil.Process(this_proc.ppid())
    while depth < limit:

        if next_proc.name() in ok_names:
            return True, next_proc.name()

        try:
            next_proc = psutil.Process(next_proc.ppid())
        except psutil.NoSuchProcess:
            break
        depth += 1

    return False, parent.name()

def ifPowerOf2(n):
    return (n & (n-1) == 0) and n != 0

def ifOnePlusTwoPlusThree(n):
    count=1 #range从0开始
    sum=0
    while sum<n:
      count+=1
      sum=0
      for i in range(1,count):
          sum+=i
    if sum>n:
        return False
    elif sum==n:
        return True

def ifPgmRunning(ok_name):
    import psutil

    pids=psutil.pids()
    for pid in pids:
        p=psutil.Process(pid)
        name=p.name()
        if name==ok_name:
           return True
    return False

def paste(text,syntax='text'):
  import httpx

  resp=httpx.post('https://paste.ubuntu.com',data={"poster":"None","syntax":syntax,"content":text})
  return 'https://paste.ubuntu.com'+resp.headers['location']

def secretlog(secret):
  from pytools._aes import AESCipher
  import os

  key=os.environ['jmail']
  crypted=AESCipher(key).encrypt(secret)
  return paste(crypted.decode('utf-8'))

def opts2dic(opts):
  import re

  dic={}
  for opt, arg in opts:
    opt=re.sub(r'^--',opt,'')
    opt=re.sub(r'^-',opt,'')
    dic[opt]=arg
  return dic

def tgsend(msg,token=os.getenv('tgtoken'),chatid=os.getenv('tgchatid')):
  import httpx

  resp=httpx.post(f'https://api.telegram.org/bot{token}/sendMessage',
    data={
      'disable_web_page_preview':'true',
      'parse_mode':'Markdown',
      'chat_id':chatid,
      'text':msg
    }
  )
  json=resp.json()
  ok=json['ok']
  if not ok:
    raise Exception(f'发送Telegram失败!\n{json}')
  else:
    print('发送Telegram成功')

def isMpFork():
  '''
  Mp=Multiprocessing
  '''
  import sys

  if __name__=='__mp_main__':
    return True
  elif '--multiprocessing-fork' in sys.argv:
    return True
  else:
    return False

def termuxClipboardGet():
  return execCmd('termux-clipboard-get')
