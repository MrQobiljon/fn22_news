from django.contrib.auth import login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

from .models import News, Category, Comment
from .forms import RegisterForm, LoginForm

# Create your views here.


@login_required
def index(request):
    newses = News.objects.filter(is_active=True)
    news_banner = newses.filter(is_banner=True).last()
    news_top_story = newses.order_by("-views").first()
    latest_newses = newses.order_by("-created")[:8]
    categories = Category.objects.all()

    context = {
        "news_banner": news_banner,
        'news_top_story': news_top_story,
        'latest_newses': latest_newses,
        'categories': categories
    }
    return render(request, "app/index.html", context)


@login_required
@permission_required("app.view_news")
def detail(request, pk):
    news = News.objects.get(pk=pk)
    context = {
        "news": news
    }
    return render(request, "app/detail.html", context)


def save_comment(request: WSGIRequest, news_id):
    news = News.objects.get(id=news_id)
    Comment.objects.create(
        user=request.user,
        news=news,
        text=request.GET.get("text")
    )
    messages.success(request, "Commentratiya saqlandi!!!")

    page = request.META.get("HTTP_REFERER", "home")
    return redirect(page)



def register(request: WSGIRequest):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Siz ro'yxatdan muvaffaqiyatli o'tdingiz!\n"
                                      "Login parolni terib saytga kiring!")
            return redirect("login")
        else:
            print(form.error_messages, "**********************************")
    else:
        form = RegisterForm()
    context = {
        "form": form
    }
    return render(request, "register.html", context)



def user_login(request: WSGIRequest):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Saytga hush kelibsiz! {user.username}")
            return redirect("home")
        else:
            pass
            # messages.error(request, f"{form.errors}")
    else:

        form = LoginForm()
    context = {
        "form": form
    }
    return render(request, "login.html", context)


@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, "Siz saytdan chiqdingiz!!!")
    return redirect("login")


@login_required
@permission_required("app.can_deliver_pizzas", "login", raise_exception=True)
def change_news(request):
    return HttpResponse("O'zgartirish")


@login_required
def send_message_to_email(request: WSGIRequest):
    if request.user.is_staff:
        if request.method == 'POST':
            title = request.POST.get("title")
            text = request.POST.get("text")

            users = User.objects.all()

            send_mail(
                title,
                text,
                settings.EMAIL_HOST_USER,
                [user.email for user in users],
                fail_silently=False,
            )
            messages.success(request, "Habar yuborildi!!!❤")

        return render(request, "app/send_message.html")
    else:
        page = request.META.get("HTTP_REFERER", "home")
        return redirect(page)