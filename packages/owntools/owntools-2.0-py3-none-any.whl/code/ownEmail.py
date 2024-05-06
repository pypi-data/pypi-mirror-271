import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.utils import formataddr
from email.header import Header


class Email():
    """
        :my_email = ownEmail.Email(user,password,name,host)
        :my_email.make_msg(content="test", title=f'继续测试')
        :my_email.send_msg()
    """

    def __init__(self, user='285242442@qq.com', password='tpgdlmjmfqxybgdf', name="Neely", host='smtp.qq.com'):

        self._user = user
        self._password = password
        self._host = host
        self._msg = MIMEMultipart()  # 构建主体
        self._msg['From'] = formataddr([name, user])  # 发件人

    def make_normal_msg(self, content, title, receiver='285242442@qq.com'):

        self._msg = MIMEText(
            content,
            'plain',
        )

        self._receiver = receiver
        self._msg['From'] = formataddr([self._name, self._user])
        self._msg['To'] = formataddr(['Your name', self._receiver])
        self._msg['Subject'] = title

    def make_mult_mag(self, content="", title="", file_path="", image_path="", receiver_name="", receiver='285242442@qq.com'):

        self.receiver = receiver
        self._msg['To'] = formataddr([receiver_name, receiver])  # 收件人

        if file_path:
            _path = Path(file_path)
            self._msg['Subject'] = Header(title if title else _path.stem, 'utf-8')  # 邮件主题

            with open(_path, 'rb') as file:
                attchment = MIMEApplication(file.read())

            attchment.add_header('Content-Disposition', 'attachment', filename=_path.name)
            self._msg.attach(attchment)  # 添加附件到邮件

        if image_path:
            with open(image_path, 'rb') as file:
                msgimage = MIMEImage(file.read())  # 打开图片

            html_img = f'<p>{content}<br><img src="cid:image1"></br></p>'
            msgimage.add_header('Content-ID', '<image1>')  # 设置图片
            self._msg.attach(msgimage)
            self._msg.attach(MIMEText(html_img, 'html', 'utf-8'))  # 添加到邮件正文

        else:
            self._msg['Subject'] = Header(title, 'utf-8')  # 邮件主题
            self._msg.attach(MIMEText(content, 'html', 'utf-8'))  # 添加到邮件正文

    def send_msg(self):

        try:
            smtp = smtplib.SMTP_SSL(self._host, 465)
            _ = smtp.login(self._user, self._password)
            _ = smtp.sendmail(self._user, [self.receiver], self._msg.as_string())
            _ = smtp.quit()
            return True
        except Exception as e:
            print(e)
            return False
