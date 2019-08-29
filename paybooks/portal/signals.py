import django.dispatch
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMessage

leave_signal = django.dispatch.Signal(providing_args=["apply","from_date","to_date"])


@receiver(leave_signal)
def send_mail_on_leave(sender, **kwargs):
    mail_id = sender.email
    if kwargs['apply'] == 'applied':
        email = EmailMessage(
            'Leave applied from '+kwargs['from_date'] + ' to '+ kwargs['to_date'] + ' by ' + str(sender),
            'Hello Admin \n \n Please Approve the leave requests, by logging to Admin portal -> Leave Monitor'
            ' \n \n Best Regards, \n Admin Management Team',
            settings.EMAIL_HOST_USER, to=['chundurimounica@gmail.com'],cc=[mail_id], )
        email.send()
    elif kwargs['apply'] == 'cancel':
        email = EmailMessage(
            'Leave cancelled from ' + kwargs['from_date'] + ' to ' + kwargs['to_date'] + ' by ' + str(sender),
            'Hello Admin \n \n Please Approve the leave requests, by logging to Admin portal -> Leave Monitor'
            ' \n \n Best Regards, \n Admin Management Team',
            settings.EMAIL_HOST_USER, to=['chundurimounica@gmail.com'],cc=[mail_id], )
        email.send()
