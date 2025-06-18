from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from todo.models import TODOO

class Command(BaseCommand):
    help = 'Gửi email nhắc nhở cho các todo sắp đến hạn'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        twenty_five_hours_later = now + timedelta(hours=24)
        todos = TODOO.objects.filter(
            status='PENDING',
            deadline__lte=twenty_five_hours_later,
            deadline__gt=now,
            reminder_sent=False
        )

        for todo in todos:
            send_mail(
                subject='Nhắc nhở: Nhiệm vụ sắp đến hạn!',
                message=f'Xin chào {todo.user.username},\n\nNhiệm vụ "{todo.title}" của bạn sẽ đến hạn vào {todo.deadline.strftime("%d/%m/%Y %H:%M")}.\nVui lòng hoàn thành sớm!\n\nTrân trọng,\nTodo App',
                from_email=None,
                recipient_list=[todo.user.email],
                fail_silently=True,
            )
            todo.reminder_sent = True
            todo.save()
            self.stdout.write(self.style.SUCCESS(f'Gửi email nhắc nhở cho {todo.user.email} về task "{todo.title}"'))