from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import TODOO, EmailOTP
from datetime import timedelta

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')

        try:
            validate_email(emailid)
        except ValidationError:
            messages.error(request, "Email không hợp lệ!")
            return redirect('/')

        if User.objects.filter(email=emailid).exists():
            messages.error(request, "Email đã được sử dụng!")
            return redirect('/')

        if not fnm or len(pwd) < 6:
            messages.error(request, "Tên không được để trống và mật khẩu phải dài ít nhất 6 ký tự!")
            return redirect('/')

        my_user = User.objects.create_user(username=fnm, email=emailid, password=pwd)
        my_user.is_active = False
        my_user.save()

        otp = EmailOTP.objects.create(user=my_user)  # Tự động tạo OTP và expires_at
        send_mail(
            subject='Xác nhận tài khoản Todo App',
            message=f'Xin chào {fnm},\n\nMã OTP xác nhận tài khoản của bạn là: {otp.otp_code}\nMã này có hiệu lực trong 5 phút.',
            from_email=None,
            recipient_list=[emailid],
            fail_silently=False,
        )

        request.session['otp_user_id'] = my_user.id
        messages.success(request, "Mã OTP đã được gửi đến email của bạn!")
        return redirect('verify_otp')

    return render(request, 'signup.html')

def verify_otp(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, "Phiên xác thực không hợp lệ!")
        return redirect('/')

    try:
        user = User.objects.get(id=user_id)
        otp_obj = EmailOTP.objects.get(user=user)
    except (User.DoesNotExist, EmailOTP.DoesNotExist):
        messages.error(request, "Lỗi hệ thống, vui lòng thử lại!")
        return redirect('/')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        if otp_obj.is_expired():
            otp_obj.delete()
            messages.error(request, "Mã OTP đã hết hạn! Vui lòng đăng ký lại.")
            return redirect('/')

        if entered_otp == otp_obj.otp_code:
            user.is_active = True
            user.save()
            otp_obj.delete()
            del request.session['otp_user_id']
            messages.success(request, "Xác thực thành công! Bạn có thể đăng nhập.")
            return redirect('loginn')
        else:
            otp_obj.increment_attempts()
            if otp_obj.attempts >= 3:
                otp_obj.delete()
                messages.error(request, "Bạn đã nhập sai OTP quá 3 lần! Vui lòng đăng ký lại.")
                return redirect('/')
            messages.error(request, f"Mã OTP không đúng! Còn {3 - otp_obj.attempts} lần thử.")

    return render(request, 'OTP.html', {'email': user.email})

def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        user = authenticate(request, username=fnm, password=pwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Chào mừng {fnm}!")
                return redirect('todopage')
            else:
                messages.error(request, "Tài khoản chưa được kích hoạt! Vui lòng xác thực email.")
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
        return redirect('loginn')
    return render(request, 'loginn.html')

def todo(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        if title:
            TODOO.objects.create(
                title=title.strip(),
                user=user,
                deadline=deadline if deadline else None
            )
            messages.success(request, "Thêm nhiệm vụ thành công!")
            return redirect('todopage')
        else:
            messages.error(request, "Tiêu đề không được để trống!")

    res = TODOO.objects.filter(user=user).order_by('-date')
    progress_percentage = TODOO.get_progress_percentage(user)  
    return render(request, 'todo.html', {
        'res': res,
        'user': user,
        'progress_percentage': progress_percentage
    })

def edit_todo(request, srno):
    try:
        todo = TODOO.objects.get(srno=srno, user=request.user)
        if request.method == 'POST':
            title = request.POST.get('title')
            deadline = request.POST.get('deadline')
            if title:
                todo.title = title.strip()
                todo.deadline = deadline if deadline else None
                todo.save()
                messages.success(request, "Cập nhật nhiệm vụ thành công!")
                return redirect('todopage')
            else:
                messages.error(request, "Tiêu đề không được để trống!")
        return render(request, 'edit_todo.html', {'user': request.user, 'todo': todo})
    except TODOO.DoesNotExist:
        messages.error(request, "Nhiệm vụ không tồn tại!")
        return redirect('todopage')

def delete_todo(request, srno):
    try:
        todo = TODOO.objects.get(srno=srno, user=request.user)
        todo.delete()
        messages.success(request, "Xóa nhiệm vụ thành công!")
    except TODOO.DoesNotExist:
        messages.error(request, "Nhiệm vụ không tồn tại!")
    return redirect('todopage')

def toggle_todo(request, srno):
    try:
        todo = TODOO.objects.get(srno=srno, user=request.user)
        todo.status = 'COMPLETED' if todo.status == 'PENDING' else 'PENDING'
        todo.save()
        messages.success(request, f"Đã cập nhật trạng thái cho '{todo.title}'!")
    except TODOO.DoesNotExist:
        messages.error(request, "Nhiệm vụ không tồn tại!")
    return redirect('todopage')

def logoutt(request):
    logout(request)
    messages.success(request, "Đăng xuất thành công!")
    return redirect('loginn')