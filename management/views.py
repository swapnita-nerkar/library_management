from django.contrib.auth.forms import UserCreationForm
from django.contrib.sitemaps.views import index
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import date
from django.views.generic import TemplateView, ListView
from django.views.generic.base import View
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import *

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime


def index(request):
    return render(request,'index.html',)

#def index(request):
    #return render(request,'index.html',)

#class BookListView(ListView):
    #model = Book

def BookListView(request):
    book_list = Book.objects.all()
    return render(request, 'catalog/book_list.html', locals())

@allowed_users(allowed_roles=['admin', 'students'])
def student_BookListView(request):
    #student = Student.objects.get(roll_no=request.user)
    issue = Issue.objects.all()
    book_list = []
    for i in issue:
        book_list.append(i.book)
    return render(request, 'catalog/book_list.html', locals())

@allowed_users(allowed_roles=['admin', 'students'])
def BookDetailView(request, pk):
    book = get_object_or_404(Book, id=pk)
    try:
        stu = Student.objects.get(roll_no=request.user)
    except:
        pass
        return render(request, 'catalog/book_detail.html', locals())

@login_required
@allowed_users(allowed_roles=['admin'])
def BookCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())

@login_required
@allowed_users(allowed_roles=['admin'])
def BookUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Book.objects.get(id=pk)
    form = BookForm(instance=obj)
    if request.method == 'POST':
        form = BookForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())

@login_required
@allowed_users(allowed_roles=['admin'])
def BookDelete(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = get_object_or_404(Book, pk=pk)
    obj.delete()
    return redirect('index')

@login_required
@allowed_users(allowed_roles=['admin', 'students'])
def student_request_issue(request, pk):
    obj = Book.objects.get(id=pk)
    stu = Student.objects.get(name=request.user.first_name)
    s = get_object_or_404(Student, name=str(request.user.first_name))
    if s.total_books_due < 10:
        message = "book has been issued, You can collect book from library"
        a = Issue()
        a.student = s
        a.book = obj
        a.issue_date = datetime.datetime.now()
        obj.available_copies = obj.available_copies - 1
        obj.save()
        stu.total_books_due = stu.total_books_due+1
        stu.save()
        a.save()
    else:
        message = "you have exceeded limit."
    return render(request, 'catalog/result.html', locals())

@login_required
@allowed_users(allowed_roles=['admin', 'students'])
def view_issued_book_view(request):
    issued_books = models.IssuedBook.objects.all()
    li = []
    for ib in issued_books:
        issue_date=str(ib.issue_date.day)+'-'+str(ib.issue_date.month)+'-'+str(ib.issue_date.year)
        return_date=str(ib.return_date.day)+'-'+str(ib.return_date.month)+'-'+str(ib.return_date.year)
        #fine calculation
        days = (date.today() - ib.issue_date)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d-15
            fine = day*10

        books = list(models.Book.objects.filter(isbn=ib.isbn))
        students = list(models.StudentExtra.objects.filter(enrollment=ib.department))
        i = 0
        for l in books:
            t = (students[i].get_name, students[i].department, books[i].name, books[i].author, issue_date, return_date, fine)
            i = i+1
            li.append(t)

    return render(request, 'catalog/view_issued_book.html', {'li': li})

@login_required
@allowed_users(allowed_roles=['admin', 'students'])
def StudentCreate(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            s = form.cleaned_data['roll_no']
            form.save()
            u = User.objects.get(username=s)
            s = Student.objects.get(roll_no=s)
            u.email = s.email
            u.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
@allowed_users(allowed_roles=['admin'])
def StudentUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Student.objects.get(id=pk)
    form = StudentForm(instance=obj)
    if request.method == 'POST':
        form = StudentForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect(index)
    return render(request, 'catalog/form.html', locals())


@login_required
@allowed_users(allowed_roles=['admin'])
def StudentDelete(request, pk):
    obj = get_object_or_404(Student, pk=pk)
    obj.delete()
    return redirect('index')

@login_required
@allowed_users(allowed_roles=['admin', 'students'])
def ret(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Issue.objects.get(id=pk)
    book_pk = obj.book.id
    student_pk = obj.student.id
    student = Student.objects.get(id=student_pk)
    student.total_books_due = student.total_books_due-1
    student.save()

    book = Book.objects.get(id=book_pk)
    book.available_copies = book.available_copies+1
    book.save()
    obj.delete()
    return redirect('index')

@login_required
@allowed_users(allowed_roles=['admin', 'students'])
def StudentList(request):
    students = Student.objects.all()
    return render(request, 'catalog/student_list.html', locals())

@login_required
@allowed_users(allowed_roles=['admin', 'students'])
def StudentDetail(request, pk):
    student = get_object_or_404(Student, id=pk)
    books = Issue.objects.filter(student=student)
    return render(request, 'catalog/student_detail.html', locals())

@unauthenticated_user
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('index')

            group = Group.ojects.get(name='students')
            user.groups.add(group)

    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })

def pie_chart(request):
    labels = []
    data = []

    queryset = Book.objects.order_by('-available_copies')[:]
    for book in queryset:
        labels.append(book.title)
        data.append(book.available_copies)

    return render(request, 'graphs/pie_chart.html', {
        'labels': labels,
        'data': data,
    })
