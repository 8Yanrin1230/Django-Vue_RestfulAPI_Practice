from django.shortcuts import get_object_or_404, redirect, render
from .models import Debt
from .forms import DebtForm
from ninja import NinjaAPI, Schema
from typing import Optional

api = NinjaAPI()

#FastAPI#
class Tags(Schema):
    DcID: str
    UserName: str
    Record: str
    Account: str
    PokerID: str
    PokerID2: str
    Total: float

@api.get("/debts", response=list[Tags])
def get_debt(request):
    debt = Debt.objects.all()
    return debt

@api.post("/debts", response=list[Tags])
def create_debt(request, data: Tags):
    debt = Debt(DcID=data.DcID, UserName=data.UserName, Record=data.Record, Account=data.Account, PokerID=data.PokerID, PokerID2=data.PokerID2, Total=data.Total)
    debt.save()
    return debt

@api.put("/debts/{pk}", response=list[Tags])
def update_debt(request, pk: int, data: Optional[Tags] = None):
    debt = Debt.objects.get(id=pk)
    if data:
        for attr, value in data.dict(exclude_unset=True).items():
            setattr(debt, attr, value)
        debt.save()
    return debt

@api.delete("/debts/{pk}")
def delete_debt(request, pk: int):
    debt = Debt.objects.get(id=pk)
    debt.delete()
    return debt


#API methods#s
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
            return redirect('/')
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
        return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'delete.html', context)
