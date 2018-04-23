from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = '[慕学在线网]注册激活链接'
        email_body = '请点击下面的链接激活您的帐号:http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'update_email':
        email_title = '[慕学在线网]邮箱修改验证码'
        email_body = '您的验证码是:{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])


def random_str(randomLength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomLength):
        str += chars[random.randint(0,length)]
    return str
