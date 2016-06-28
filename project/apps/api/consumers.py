from django.core.mail import send_mail


def send_invite(message):
    result = send_mail(
        message.content.get('subject'),
        'Foobar bat baz',
        'admin@barberscore.com',
        [
            'dbinetti@gmail.com',
        ],
    )
    return result
