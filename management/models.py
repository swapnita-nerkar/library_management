from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from twilio.rest import Client

class Department(models.Model):
    department = models.CharField(max_length=200, help_text="Enter a book of Department (e.g. IT, CSE, etc.)")
    class Meta:
        ordering=('-department',)
    def __str__(self):
        return self.department

class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    pic = models.ImageField(blank=True, null=True, upload_to='book_image')

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

# Twilio app sms........
    def save(self, *args, **kwargs):
        if self.available_copies < 10:
            account_sid = 'AC546670f460126b5f8f3e38abd463318f'
            auth_token = 'f0508a7e323e5db606deb914b9a42ae7'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=f"Available books of {self.title} are less than 10, i.e - {self.available_copies} Add books",
                from_='+12056569196',
                to='+91 8850422367'
            )

            print(message.sid)
        return super().save(*args, **kwargs)


def create_user(sender, *args, **kwargs):
    if kwargs['created']:
        user = User.objects.create(username=kwargs['instance'],password="dummypass")

class Student(models.Model):
    roll_no = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=10)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    contact_no = models.CharField(max_length=10)
    total_books_due=models.IntegerField(default=0)
    email = models.EmailField(unique=True)
    pic = models.ImageField(blank=True, upload_to='profile_image')
    def __str__(self):
        return str(self.roll_no)

post_save.connect(create_user, sender=Student)

class Issue(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.student.name+" Issued "+self.book.title
