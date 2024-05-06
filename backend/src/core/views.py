from django.shortcuts import get_object_or_404, redirect, render
from .models import Records
from .forms import RecordsForm
from ninja import NinjaAPI, Schema
from django.http import JsonResponse
from django.core import serializers
from DC.DcRobot import *
import json

api = NinjaAPI()

#FastAPI#
class Tags(Schema):
    id: int
    DcID: str
    UserName: str
    Record: str
    Account: str
    PokerID: str
    Total: float
    WOL : bool

class Debts(Schema):
    debtors: str
    creditors: str
    amount: float

@api.get("/debts")
def get_debt(request):
    try:
        with open('debt_transfers.json', 'r') as f:
            data = json.load(f)
            return JsonResponse(data, safe=False)
    except FileNotFoundError:
        print("debt_transfers.json 文件不存在")
        return None

@api.delete("/debts", response=Debts)
async def delete_debt(request , data:Debts):
    json_data = data.dict()
    tag_data = Debts(**json_data)
    await test2(tag_data.creditors, tag_data.debtors, tag_data.amount )

@api.get("/records", response=list[Tags])
def get_record(request):
    record = Records.objects.all()
    return record

@api.post("/records", response=Tags)
def create_record(request, data: Tags):
    json_data = data.dict()
    tag_data = Tags(**json_data)
    record = Records(
        DcID = tag_data.DcID,
        UserName = tag_data.UserName,
        Record = tag_data.Record,
        Account = tag_data.Account,
        PokerID = tag_data.PokerID,
        Total = tag_data.Total,
        WOL = True,
    )
    record.save()
    return tag_data

@api.put("/records/{pk}", response=Tags)
def update_record(request, pk: int, data: Tags):
    record = Records.objects.get(id=pk)
    json_data = data.dict()
    tag_data = Tags(**json_data)

    if data:
        for attr, value in data.dict(exclude_unset=True).items():
            setattr(record, attr, value)
        record.save()
    return tag_data

@api.delete("/records/{pk}")
def delete_record(request, pk: int):
    record = Records.objects.get(id=pk)
    record.delete()
    json_data = serializers.serialize('json', [record])
    return JsonResponse(json.loads(json_data), safe=False)

#API methods
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