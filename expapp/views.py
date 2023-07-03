from django.shortcuts import render,redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login  as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            new_expense = expense.save(commit=False)
            new_expense.user = request.user
            new_expense.save()

    expenses = Expense.objects.filter(user=request.user)
    total_exp = expenses.aggregate(total=Sum('amount'))

    last_year = datetime.date.today() - datetime.timedelta(days=365)
    yearly_expenses = expenses.filter(date__gt=last_year)
    yearly_sum = yearly_expenses.aggregate(total=Sum('amount'))

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    monthly_expenses = expenses.filter(date__gt=last_month)
    monthly_sum = monthly_expenses.aggregate(total=Sum('amount'))

    last_week = datetime.date.today() - datetime.timedelta(days=7)
    weekly_expenses = expenses.filter(date__gt=last_week)
    weekly_sum = weekly_expenses.aggregate(total=Sum('amount'))

    daily_sums = expenses.values('date').order_by("date").annotate(sum=Sum('amount'))
    category_sums = expenses.values('category').order_by("category").annotate(sum=Sum('amount'))

    expense_form = ExpenseForm()
    return render(request, 'trakapp/index.html', {
        'expense_form': expense_form,
        'expenses': expenses,
        'total_exp': total_exp,
        'yearly_sum': yearly_sum,
        'monthly_sum': monthly_sum,
        'weekly_sum': weekly_sum,
        'daily_sums': daily_sums,
        'category_sums': category_sums
    })


def edit(request,id):
    expense=Expense.objects.get(id=id)
    
    expense_form = ExpenseForm(instance=expense)
    if request.method =="POST":
        expense=Expense.objects.get(id=id)
        form =ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request,"trakapp/edit.html",{"expense_form": expense_form})


def delete(request,id):
    if request.method == 'POST' and 'delete' in request.POST:
        expense=Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')





def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,'trakapp/register.html',{'form': form})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Use the renamed login method
                return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'trakapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')
