import discord
import requests
import json
from core.models import Records
from discord.ext import commands
from collections import defaultdict
from asgiref.sync import sync_to_async
from django.db.models import Q

# intents是要求機器人的權限
intents = discord.Intents.all()

# command_prefix是前綴符號，可以自由選擇($, #, &...)
bot = commands.Bot(command_prefix = "%", intents = intents)

def selectUser(ctx):
    user_id = ctx.author.id
    debt =  Records.objects.get(DcID=user_id)

async def add(datas):
     for data in datas:
        tests =  Records.objects.filter(PokerID=data[0])
        async for test in tests:
            debt = Records(
                DcID = test.DcID,
                UserName = test.UserName,
                Account = test.Account,
                PokerID = test.PokerID,
                Total = data[1],
                WOL = True,
                Balance = data[1],
            )
            break
        await sync_to_async(debt.save, thread_sensitive=True)()

# 當機器人完成啟動
@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")

@bot.command()
async def NewGame(ctx, *, message):
    url = message + '/players_sessions'
    response = requests.get(url)

    total_net = 0
    try:
        # 檢查響應是否成功
        if response.status_code == 200:
            # 嘗試解析 JSON 字串
            try:
                data = json.loads(response.text)
            except json.JSONDecodeError:
                print("無法解析 JSON 字串")
            else:
                players_infos = data.get('playersInfos', {})  # 獲取 'playersInfos' 的值,如果不存在則返回空字典
                data = []
                # 遍歷 playersInfos 字典
                for player_id, player_info in players_infos.items():
                    Poker_ID = player_id
                    net = player_info['net'] / 100
                    money = round(net, 0)  # 四捨五入
                    total_net += money  # 計算總 net
                    data.append((Poker_ID, money))
                if total_net >= 0:
                    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
                    sorted_data[0] = (sorted_data[0][0], sorted_data[0][1] - total_net)
                    await add(sorted_data)
                elif total_net <= 0:
                    sorted_data = sorted(data, key=lambda x: x[1], reverse=False)
                    sorted_data[0] = (sorted_data[0][0], sorted_data[0][1] - total_net)
                    await add(sorted_data)
                await DebtRecord.pay_debts (ctx)

        else:
            print(f"請求失敗, 狀態碼: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

#取得誰該給誰錢
@bot.command()
async def result(ctx):
    await DebtRecord.pay_debts(ctx)

async def test2(creditor_id , debtor_id , amount):

    new_datas = []  # 建立一個新的列表來存放需要保留的資料

    amountx = amount
    amounty = amount
    creditor_qs = Records.objects.filter(DcID=creditor_id).exclude(Balance=0)
    debtor_qs = Records.objects.filter(DcID=debtor_id).exclude(Balance=0)

    async for debtor in debtor_qs:
        if amountx > -debtor.Balance:
            amountx += debtor.Balance
            debtor.Balance = 0
        elif amountx < -debtor.Balance:

            debtor.Balance += amountx
            amountx = 0
        elif amountx == -debtor.Balance:
            debtor.Balance = 0
            amountx = 0
        await sync_to_async(debtor.save, thread_sensitive=True)()

    async for creditor in creditor_qs:
        if amounty > creditor.Balance:
            amounty -= creditor.Balance
            creditor.Balance = 0
        elif amounty < creditor.Balance:
            creditor.Balance -= amounty
            amounty = 0
        elif amounty == creditor.Balance:
            creditor.Balance = 0
            amounty = 0
        await sync_to_async(creditor.save, thread_sensitive=True)()

    # 如果最後 amountx 和 amounty 都等於 0，則不將這一行資料加入新的列表中
    if amountx == 0 and amounty == 0:
        print("ok")
    else:
        data = {
            creditor_id,
            debtor_id,
            amount
        }
        new_datas.append(data)

    # 將新的資料列表寫回 debt_transfers.json 檔案
    with open('debt_transfers.json', 'w') as f:
        json.dump(new_datas, f, indent=4)

def save_debt_transfers_to_json():
    with open('debt_transfers.json', 'w') as f:
        json.dump(DebtRecord.debt_transfers_dict, f, indent=4)

class DebtRecord:
    debt_transfers_dict = []
    def __init__(self, who, total):
        self.who = who
        self.total = total

    @staticmethod
    async def fetch_all_records():

        try:
            records=[]
            # 取得所有債務記錄
            debts = Records.objects.all()
            async for debt in debts:
                    if debt.Balance != 0:
                        records.append(DebtRecord(debt.DcID, debt.Balance))
            return records

        except Exception as e:
            print(f"Error: {e}")

    @classmethod
    async def pay_debts(cls, ctx):
        records = await cls.fetch_all_records()

        await ctx.send(f"{ctx.guild.default_role} 大家注意了!") # 提及@everyone

        # 計算每個人的淨債務額
        net_debts = defaultdict(int)
        for record in records:
            net_debts[record.who] += record.total

        # 將所有人按照淨債務額從高到低排序
        sorted_net_debts = sorted(net_debts.items(), key=lambda x: x[1], reverse=True)

        # 轉移債務
        debt_transfers = []
        while sorted_net_debts:
            max_debtor_id, max_debt = sorted_net_debts[0]
            min_creditor_id, min_credit = sorted_net_debts[-1]

            # 債務最高的人將債務轉移給債權最高的人
            transfer_amount = min(-min_credit, max_debt)
            debt_transfers.append((max_debtor_id, min_creditor_id, transfer_amount))

            sorted_net_debts[0] = (max_debtor_id, max_debt - transfer_amount)
            sorted_net_debts[-1] = (min_creditor_id, min_credit + transfer_amount)

            # 移除淨債務額為0的人
            sorted_net_debts = [x for x in sorted_net_debts if x[1] != 0]

        DebtRecord.debt_transfers_dict.clear()
        # 輸出債務轉移記錄
        for debtor_id, creditor_id, amount in debt_transfers:
            # debtor = ctx.guild.get_member(debtor_id)
            await ctx.send(f"{creditor_id} pays {amount} to {debtor_id}")
            record = {
                'debtor_id': debtor_id,
                'creditor_id': creditor_id,
                'amount': amount
            }
            DebtRecord.debt_transfers_dict.append(record)
        save_debt_transfers_to_json()

# #總金額增減
# async def Settlement(conn, ID, money):
#     try:
#         # 查詢現有 Total
#         cursor = await conn.execute("SELECT Total FROM Debt WHERE ID = ?", (ID,))
#         now_Total = await cursor.fetchone()

#         # 檢查是否成功獲取到 Total
#         if now_Total:
#             now_Total = now_Total[0]
#             new_Total = now_Total + money
#             # 更新 Total
#             await conn.execute("UPDATE Debt SET Total = ? WHERE ID = ?", (new_Total, ID))
#             await conn.commit()
#         else:
#             logging.info(f"No data found for ID: {ID}")

#     except Exception as e:
#         logging.error(f"Error: {e}")
#         await conn.rollback()

# async def clear(conn,user_id):
#     await conn.execute("UPDATE Debt SET Total = 0 WHERE ID = ?", (user_id,))
#     await conn.commit()

# @bot.command()
# async def WOL(ctx, *, data):
#     user_id = ctx.author.id
#     user_message = str (data) + ","
#     await update(conn, user_id, user_message)
#     await Settlement(conn, user_id, int(data))
#     await ctx.send(f'小賭怡情大賭郭台銘: {data}')
# #傳送自己的紀錄
# @bot.command()
# async def SYR(ctx):
#     user_id = ctx.author.id
#     cursor = await conn.execute("SELECT Record FROM Debt WHERE ID = ?", (user_id,))
#     result = await cursor.fetchone()


#     if result:
#         lines = result[0].split(',')
#         await ctx.send("你的戰機：")  # 使用 strip() 去除每行首尾的空白字符
#         for line in lines:
#             await ctx.send(line.strip())  # 使用 strip() 去除每行首尾的空白字符
#     else:
#         await ctx.send("沒紀錄，趕緊去玩")

# #付完錢
# @bot.command()
# async def pay(ctx , * , message):
#     user_id = ctx.author.id
#     winner,data = message.split('/', 1)

#     if str.isdigit(data) :
#             for _ in list:
#                 winner, loser ,amount = _.split('/', 2)
#                 amount = int(amount)

#                 if  int(loser) == int(user_id) and abs(amount) == int(data) :
#                     if  amount>0:
#                         await Settlement(conn, loser,  int(amount))
#                         await Settlement(conn, winner, -int(amount))
#                     else:
#                         await Settlement(conn, loser, -int(amount))
#                         await Settlement(conn, winner, int(amount))
#                     member = ctx.guild.get_member(int(winner))
#                     await ctx.send("付款完成 可憐")
#                     await ctx.send(f"{member.mention}, 有人來還錢拉")
#                     await ctx.send("最新結果：")
#                     list.clear()
#                     await DebtRecord.pay_debts(conn,ctx)
#     else: await ctx.send("error")
# #列出所有人的Total
# @bot.command()
# async def SD(ctx):
#     cursor = await conn.execute("SELECT UserName, Total FROM Debt")
#     async for row in cursor:
#         name = row[0]
#         total = row[1]
#         await ctx.send(f"Name: {name}, Total: {total}")

# #show銀行帳戶
# @bot.command()
# async def account(ctx):
#     cursor = await conn.execute("SELECT Account, UserName FROM Debt")
#     results = await cursor.fetchall()
#     for account, username in results:
#         await ctx.send(f"{username}, 銀行帳戶: {account}")

# @bot.command()
# async def PayAll(ctx):
#     user_id = ctx.author.id
#     winners = []
#     mentions = []
#     for _ in list:
#         winner, loser ,amount = _.split('/', 2)
#         winners.append(winner)s
#         if  int(loser) == int(user_id):
#             if  int(amount)>0:
#                     await Settlement(conn, loser,  int(amount))
#                     await Settlement(conn, winner, -int(amount))

#     for a in winners:
#         member = ctx.guild.get_member(int(a))
#         if member:
#             mentions.append(member.mention)

#     if mentions:
#         await ctx.send(f"{' '.join(mentions)}, 有人來還錢拉")

#     await ctx.send("付款完成 可憐")
#     await ctx.send("最新結果：")
#     list.clear()
#     await DebtRecord.pay_debts(ctx)
