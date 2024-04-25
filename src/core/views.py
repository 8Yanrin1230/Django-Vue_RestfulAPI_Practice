from django.shortcuts import get_object_or_404, redirect, render
from .models import Debt
from .forms import DebtForm


def home(request):
    form = DebtForm()
    Debts = Debt.objects.all()

    if request.method == "POST":
        form = DebtForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        "Debt": Debts,
        "form": form
    }
    return render(request,'index.html',context)

def update(request, pk):
    Debts = Debt.objects.get(id = pk)
    form = DebtForm(instance=Debts)

    if request.method == "POST":
        form = DebtForm(request.POST, instance=Debts)
        if form.is_valid():
            form.save()
            return redirect('/home')
    context = {
        'Debt': Debts,
        'form': form
    }
    return render(request, 'update.html', context)

def delete(request, pk):
    Debts = get_object_or_404(Debt, pk=pk)
    form = DebtForm(instance=Debts)

    if request.method == "POST":
        form = DebtForm(request.POST, instance=Debts)
        Debts.delete()
        return redirect('/home')
    context = {
        'form': form
    }
    return render(request, 'delete.html', context)

