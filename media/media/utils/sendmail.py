# -*- coding: utf8 -*-

import os.path
import smtplib
import mimetypes

import email.MIMEBase  # import MIMEBase
import email.MIMEImage  # import MIMEImage
import email.MIMEMultipart  # import MIMEMultipart
import email.MIMEText  # import MIMEText


class SendEmail(object):

    def __init__(self, From='alert', password='maixun2410'):
        self.server = smtplib.SMTP("smtp.ym.163.com")
        self.From = From + "@maixunbytes.com"
        self.server.login(self.From, password)  # 仅smtp服务器需要验证时

        # 构造MIMEMultipart对象做为根容器  
        self.main_msg = email.MIMEMultipart.MIMEMultipart()
        self.main_msg['From'] = self.From

    def close(self):
        self.server.close()

    def __del__(self):
        self.close()

    def reset(self):
        """ 重置各种数据问题 """
        self.main_msg = email.MIMEMultipart.MIMEMultipart()
        self.main_msg['From'] = self.From

    def send(self, to='', subject='', text_msg='', attach=''):
        self.reset()

        # 构造MIMEText对象做为邮件显示内容并附加到根容器  
        text_msg = email.MIMEText.MIMEText(text_msg, _charset="utf-8")
        self.main_msg.attach(text_msg)

        # 构造MIMEBase对象做为文件附件内容并附加到根容器  
        if attach != '':
            ctype, encoding = mimetypes.guess_type(attach)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            file_msg = email.MIMEImage.MIMEImage(open(attach, 'rb').read(), subtype)

            basename = os.path.basename(attach)
            file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头
            self.main_msg.attach(file_msg)

        self.main_msg['To'] = to  # + '@maixunbytes.com'
        self.main_msg['Subject'] = subject
        self.main_msg['Date'] = email.Utils.formatdate()

        # 得到格式化后的完整文本  
        fullText = self.main_msg.as_string()

        # 用smtp发送邮件  
        # try:
        # self.server.sendmail(self.From, to + '@maixunbytes.com', fullText)
        self.server.sendmail(self.From, to, fullText)
