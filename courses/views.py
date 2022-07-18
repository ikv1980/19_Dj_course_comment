from django.views.generic import ListView, DetailView, CreateView
# from requests import post
from .models import Course, Lesson, Comment
from django.shortcuts import render, redirect
from .forms import CourseForm, CommentForm
from django.contrib import messages
from cloudipsp import Api, Checkout
import time


secret_key = 'test'

def tarrifsPage(request):
    api = Api(merchant_id=1397120,
              secret_key=secret_key)
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": 1500,
        "order_desc": "Покупка подписки на сайте",
        "order_id": str(time.time())
    }
    url = checkout.url(data).get('checkout_url')
    return render(request, 'courses/tarrifs.html', {'title': 'Тарифы на сайте', 'url': url})


class HomePage(ListView):
    model = Course
    template_name = 'courses/home.html'
    context_object_name = 'courses'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(HomePage, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница сайта'
        return ctx

# Курсы
class ListCourses(ListView):
    model = Course
    template_name = 'courses/courses.html'
    context_object_name = 'courses'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(ListCourses, self).get_context_data(**kwargs)
        ctx['title'] = 'Список курсов на сайте'
        return ctx


class CourseDetailPage(DetailView):
    model = Course
    template_name = 'courses/course-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CourseDetailPage, self).get_context_data(**kwargs)
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        ctx['title'] = course
        ctx['lessons'] = Lesson.objects.filter(course=course).order_by('number')
        return ctx

# Вывод детальной информации об уроке + комментарии
class LessonDetailPage(DetailView):
    model = Course
    template_name = 'courses/lesson-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LessonDetailPage, self).get_context_data(**kwargs)
        lesson = Lesson.objects.filter(slug=self.kwargs['lesson_slug']).first()

        lesson.video = lesson.video.split("=")[1]
        
        ctx['title'] = lesson
        ctx['lesson'] = lesson
        ctx['form'] = CommentForm
        # Для комментариев
        ctx['comments'] = Comment.objects.filter(post=lesson).order_by('-id')
        ctx['n'] = len(Comment.objects.filter(post=lesson))
        return ctx


    def post(self, request, *args, **kwargs):
        lesson = Lesson.objects.filter(slug=self.kwargs['lesson_slug']).first()
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.post = lesson
            form.save()
            url = self.kwargs['slug'] + '/' + self.kwargs['lesson_slug']
            return redirect('/course/' + url)


# Первый способ создания нового курса
class CreateCourse(CreateView):
    model = Course
    template_name = 'courses/add-course.html'
    fields = ['slug', 'title', 'desc', 'image']
    success_url = '/'


# Второй способ создания нового курса с выводом сообщения об успехе
def AddCourse(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            course = form.cleaned_data.get('title')
            messages.success(request, f'Курс {course} был успешно добавлен!')
            return redirect('home')
    else:
        form = CourseForm()

    data = {
            'title': 'Добавление курса',
            'form': form
        }

    return render(request, 'courses/add-course.html', data)
