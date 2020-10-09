
HOST = "smtp.gmail.com"     # 定义smtp主机
SUBJECT = "Test email from Python"      # 定义邮件主题
TO = "123456789@qq.com"                # 定义邮件收件人
FROM = "knwoing@gmail.com"           # 定义邮件发件人
text = "Python rules them all!"         # 邮件内容
BODY = ''.join((                    # 组装sendmail方法的邮件主机内容，各段以"\r\n"进行分隔
            f"FROM: {FROM}\r\n",
            f"To: {TO}\r\n",
            f"Subject: {SUBJECT}\r\n",
            "\r\n",
            text + '\r\n'
))
print(BODY)
server = smtplib.SMTP_SSL(HOST)                 # 创建一个SMTP()对象
server.connect(HOST, "465")              # 通过connect 方法链接smtp主机
server.login(FROM, "mypassword")
server.sendmail(FROM, [TO], BODY)       # 邮件发送
server.quit()
