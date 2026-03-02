from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
from .models import Book
from .form import BookForm
from django.contrib.auth.decorators import login_required

def home(request):
    books = Book.objects.all()
    return render(request, "home.html", {"books": books})

def book_list(request):
    books = Book.objects.all()
    return render(request, "home.html", {"books": books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "book_details.html", {"book": book})

@login_required
def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        book = form.save(commit = False)
        book.owner = request.user
        book.save()
        return redirect('book_list')
    return render(request, 'book_form.html', {'form': form})

@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if book.owner != request.user and not request.user.is_staff:
        return redirect('book_list')
    
    form = BookForm(request.POST or None, isinstance=book)
    if form.is_valid():
        form.save()
        return redirect('book_detail', pk=pk)
    return render(request, 'book_form.html', {'form': form})

@login_required
def buy_book(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'buy_book.html', {'book': book})