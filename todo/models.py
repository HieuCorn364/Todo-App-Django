from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
from datetime import timedelta

class TODOO(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    )
    srno = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=100) 
    date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_sent = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.title} ({self.status})"

    @property
    def is_urgent(self):
        """Kiểm tra nếu todo sắp đến hạn (dưới 5 tiếng)."""
        if self.deadline and self.status == 'PENDING':
            time_left = self.deadline - timezone.now()
            return time_left <= timedelta(hours=5)
        return False

    @classmethod
    def get_progress_percentage(cls, user):
        """Tính phần trăm todo hoàn thành của user."""
        total_todos = cls.objects.filter(user=user).count()
        if total_todos == 0:
            return 0
        completed_todos = cls.objects.filter(user=user, status='COMPLETED').count()
        return round((completed_todos / total_todos) * 100, 2)

class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  
    attempts = models.IntegerField(default=0)  

    def save(self, *args, **kwargs):
        if not self.otp_code:  # Tự động tạo OTP
            self.otp_code = str(random.randint(100000, 999999))
        if not self.expires_at:  # Đặt thời hạn 5 phút
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        """Kiểm tra OTP đã hết hạn chưa."""
        return timezone.now() > self.expires_at

    def increment_attempts(self):
        """Tăng số lần thử sai."""
        self.attempts += 1
        self.save()