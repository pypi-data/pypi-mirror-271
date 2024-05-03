import smtplib
from email.mime.text import MIMEText
from email.header import Header
import base64

def send_mail(subject, content, receiver='cyzhelper@qq.com', sender='cyzhelper@qq.com', passward='idzeantfoqclcdgi', \
               from_nike_name='default', to_nike_name='default'):
    
    mail_host = "smtp.qq.com"

    if from_nike_name == 'default':
        from_nike_name = sender.split('@')[0]
    from_nike_name = base64.b64encode(from_nike_name.encode('utf-8')).decode()
    from_nike_name = '=?utf-8?b?' + from_nike_name + '?='

    if to_nike_name == 'default':
        to_nike_name = receiver.split('@')[0]
    to_nike_name = base64.b64encode(to_nike_name.encode('utf-8')).decode()
    to_nike_name = '=?utf-8?b?' + to_nike_name + '?='

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(from_nike_name + " <" + sender + ">")  #邮件发送者姓名
    message['To'] = Header(to_nike_name + " <" + receiver + ">")    #邮件接收者姓名

    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465) #建立smtp连接，qq邮箱必须用ssl边接，因此边接465端口
        # smtpObj.set_debuglevel(1)
        smtpObj.login(sender, passward)  #登陆
        smtpObj.sendmail(sender, receiver, message.as_string())  #发送
        smtpObj.quit()
        print('发送成功！！')
    except smtplib.SMTPException as e:
        print('发送失败！！')


if __name__ == '__main__':
    print('this is a use demo')
    subject = '嘎嘎gaga'
    content = 'gagaga gagagaga嘎嘎\n' + 'gaga! gaga!'
    send_mail(subject, content)
    # mail(subject, content, 'receiver@qq.com', 'sender@qq.com', 'passward')

'''
qq邮箱官网教程

POP3/SMTP 设置方法
用户名/帐户： 你的QQ邮箱完整的地址

密码： 生成的授权码

电子邮件地址： 你的QQ邮箱的完整邮件地址

接收邮件服务器： pop.qq.com，使用SSL，端口号995

发送邮件服务器： smtp.qq.com，使用SSL，端口号465或587
'''