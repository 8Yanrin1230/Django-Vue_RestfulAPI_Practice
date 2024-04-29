from django.shortcuts import get_object_or_404, redirect, render
from .models import Debt
from .forms import DebtForm
from ninja import NinjaAPI, Schema
import json
from django.http import JsonResponse
from django.core import serializers

api = NinjaAPI()

#FastAPI#
class Tags(Schema):
    id: int
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

@api.post("/debts", response=Tags)
def create_debt(request, data: Tags):
    json_data = data.dict()
    tag_data = Tags(**json_data)
    debt = Debt(
        DcID = tag_data.DcID,
        UserName = tag_data.UserName,
        Record = tag_data.Record,
        Account = tag_data.Account,
        PokerID = tag_data.PokerID,
        PokerID2 = tag_data.PokerID2,
        Total = tag_data.Total,
    )
    debt.save()
    return tag_data

@api.put("/debts/{pk}", response=Tags)
def update_debt(request, pk: int, data: Tags):
    debt = Debt.objects.get(id=pk)
    json_data = data.dict()
    tag_data = Tags(**json_data)

    if data:
        for attr, value in data.dict(exclude_unset=True).items():
            setattr(debt, attr, value)
        debt.save()
    return tag_data

@api.delete("/debts/{pk}")
def delete_debt(request, pk: int):
    debt = Debt.objects.get(id=pk)
    debt.delete()
    json_data = serializers.serialize('json', [debt])
    return JsonResponse(json.loads(json_data), safe=False)


#API methods#s
# def home(request):
#     form = DebtForm()
#     Debts = Debt.objects.all()

#     if request.method == "POST":
#         form = DebtForm(request.POST)
#         if form.is_valid():
#             form.save()

#     context = {
#         "Debt": Debts,
#         "form": form
#     }
#     return render(request,'index.html',context)

# def update(request, pk):
#     Debts = Debt.objects.get(id = pk)
#     form = DebtForm(instance=Debts)

#     if request.method == "POST":
#         form = DebtForm(request.POST, instance=Debts)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     context = {
#         'Debt': Debts,
#         'form': form
#     }
#     return render(request, 'update.html', context)

# def delete(request, pk):
#     Debts = get_object_or_404(Debt, pk=pk)
#     form = DebtForm(instance=Debts)

#     if request.method == "POST":
#         form = DebtForm(request.POST, instance=Debts)
#         Debts.delete()
#         return redirect('/')
#     context = {
#         'form': form
#     }
#     return render(request, 'delete.html', context)
