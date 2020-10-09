import smtplib
from email.mime.text import MIMEText

HOST = "smtp.gmail.com"     # 定义smtp主机
SUBJECT = "官网流量数据报表"      # 定义邮件主题
TO = "123456@qq.com"                # 定义邮件收件人
FROM = "knowing@gmail.com"           # 定义邮件发件人
text = "Python rules them all!"         # 邮件内容

# 创建一个MIMEText对象，分别指定HTML内容,类型(文本或html),字符编码
msg = MIMEText("""                      
<table width="800" border="0" cellspacing="0" cellpadding="4">
    <tr>
        <td bgcolor="#CECFAD" height="20" style="font-size: 14px">* 官网数据
            <a href="baidu.com">更多 >></a>
        </td>
        <tr>
    </tr>
    <tr>
        <td bgcolor="#EFEBDE" height="100" style="font-size: 13px">
            1) 日访问量 : <span style="color:red">152433</span> 访问次数 : 23651  页面浏览量 : 45123 点击数 : 545122 数据流量 : 504MB<br>
            2) 状态码信息<br>
            &nbsp;&nbsp;500:105     404:3264    503:214<br>
            3) 访客浏览器信息<br>
            &nbsp;&nbsp;IE:50%  firefox:10% chrome:30% other:10%<br>
            4) 页面信息<br>
            &nbsp;&nbsp;/index.php 42153<br>
            &nbsp;&nbsp;/view.php 21451<br>
            &nbsp;&nbsp;/login.php 5112<br>
        </td>
    </tr>
</table>
""", "html", "utf-8")
msg['Subject'] = SUBJECT            # 邮件主题
msg['From'] = FROM                  # 邮件发件人，邮件头部可见
msg['To'] = TO                      # 邮件收件人，邮件头部可见

try:
    server = smtplib.SMTP_SSL(HOST)                 # 创建一个SMTP()对象
    server.connect(HOST, "465")              # 通过connect 方法链接smtp主机
    server.login(FROM, "mypassword")
    server.sendmail(FROM, [TO], msg.as_string())       # 邮件发送
    server.quit()
    print("邮件发送成功!")
except Exception as e:
    print("失败: {}".format(str(e)))
