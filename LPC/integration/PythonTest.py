from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib
from django.http import request

__author__ = 'teddy'

class Email(object):

    def __init__(self, smtp_server, sender, password):
        self.smtpserver = smtp_server
        self.sender = sender
        self.password = password
        self.msg = MIMEMultipart()
        self.smtp = smtplib.SMTP()

    def set_email_header(self, receiver, subject):
        self.msg['From'] = self.sender
        self.msg['To'] = receiver
        self.msg['Subject'] = subject

    def set_email_body(self, cont):
        body = MIMEText('%s' % cont, 'html', 'utf-8')
        self.msg.attach(body)

    def send_email(self, receiver, subject, cont):
        # login_smtp_server = getattr(settings, 'LOGIN_SMTP_SERVER', False)
        # do not need to login to smtp server by default
        login_smtp_server='10.96.170.16'
        (code, resp) = self.smtp.connect(self.smtpserver)
        print 'connect, %s, %s' % (code, resp)
        self.smtp.docmd('ehlo', self.sender)
        print self.sender, self.password
        if self.smtpserver not in ["localhost", "127.0.0.1"] and\
                login_smtp_server:
            (code, resp) = self.smtp.login(self.sender, self.password)
            print 'login, %s, %s' % (code, resp)
        self.set_email_header(receiver, subject)
        self.set_email_body(cont)
        self.smtp.sendmail(self.sender, receiver, self.msg.as_string())
        self.smtp.quit()

if __name__ == '__main__':
    # aa=[];
    # aa.append("aaa")
    # aa.append('bbb')
    # print(aa.__len__())

    # test_List=[1,2,3];
    # result=[];
    # for i, test in enumerate(test_List):
    #     result.append(test)
    try:
        query = request.GET
        receiver = query.get('email')
        cont = json.loads(request.body)
        print(receiver)
    except Exception as e:
        print('Receiver or Content is None')
         # rest_utils.JSONResponse("Receiver or Content is None", 500)
    if receiver is None:
         # rest_utils.JSONResponse("Receiver or Content is None", 500)
        print('Receiver or Content is None')

    value_list = []
    for key in ['alarm_name', 'alarm_resource', 'alarm_meter',
                'alarm_description', 'previous', 'current', 'reason']:
        value = cont.get(key)
        if value:
            value_list.append(value)
        else:
            value_list.append('')

    subject = "Easystack Alarm Notification  (alarm name:%s)" % value_list[0]
    alarm_mail = """
    <html>
        <head></head>
        <body>
        <p>
        <b>Alarm Info</b><br>
        alarm_name: %s<br>
        alarm_resource: %s<br>
        alarm_meter: %s<br>
        alarm_description: %s<br>
        </p>
        <p>
        <b>Alarm State Transition</b><br>
         From '%s' To '%s'<br>
        <p>
        <b>Reason</b><br>
        %s<br>
        </p>
       </body>
    </html>""" % tuple(value_list)

    SMTP_SERVER = '10.96.170.16'
    SENDER = 'cloudmonitor@lenovo.com'
    SMTP_PW = 'qwer-1234'

    # server = getattr(settings, 'SMTP_SERVER', SMTP_SERVER)
    # sender = getattr(settings, 'SENDER', SENDER)
    # # password = getattr(settings, 'SMTP_PW', None)
    email = Email(SMTP_SERVER, SENDER, SMTP_PW)
    email.send_email(receiver, subject, alarm_mail)
    result="Successfully send the mail"
    # jsonResult= rest_utils.JSONResponse("Successfully send the mail", 202)
    print(result)