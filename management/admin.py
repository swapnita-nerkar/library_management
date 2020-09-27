from django.contrib import admin

# Register your models here.
from .models import Book, Student, Issue, Language, Department

admin.site.register(Department)

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'summary', 'language', 'total_copies', 'available_copies']

admin.site.register(Book, BookAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_no', 'name', 'department', 'contact_no', 'total_books_due', 'email']

admin.site.register(Student, StudentAdmin)

class IssueAdmin(admin.ModelAdmin):
    list_display = ['student', 'book', 'issue_date', 'return_date']

admin.site.register(Issue, IssueAdmin)

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Language, LanguageAdmin)

