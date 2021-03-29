qpass=''
qfrom=''

def update(**kw):
  global qpass,qfrom
  if 'pass' in kw:
    qpass=kw['qpass']
  if 'from' in kw:
    qfrom=kw['qfrom']

def qmail(fromName,content,subject):
  import smtplib
  from email.mime.text import MIMEText
  from email.utils import formataddr
   
  my_sender=qfrom    # 发件人邮箱账号
  my_pass = qpass              # 发件人邮箱密码
  my_user=qfrom      # 收件人邮箱账号，我这边发送给自己
  def mail():
      msg=MIMEText(content,'plain','utf-8')
      msg['From']=formataddr([fromName,my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
      msg['To']=formataddr([my_user,my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
      msg['Subject']=subject                # 邮件的主题，也可以说是标题
   
      server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
      print(my_sender,my_pass)
      server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
      server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
      server.quit()  # 关闭连接
  mail()
  print('邮件已发送')
