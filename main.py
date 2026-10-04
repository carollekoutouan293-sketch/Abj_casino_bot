import os,json,random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application,CommandHandler,CallbackQueryHandler
TOKEN=os.getenv("BOT_TOKEN")
def load():
 try:
  with open("db.json") as f: return json.load(f)
 except: return {}
def save(d):
 with open("db.json","w") as f: json.dump(d,f)
def get(d,u):
 if str(u) not in d: d[str(u)]={"balance":10000}
 return d[str(u)]
def menu(): return InlineKeyboardMarkup([[InlineKeyboardButton("Dice",callback_data="dice"),InlineKeyboardButton("Solde",callback_data="solde")]])
async def start(upd,ctx):
 d=load(); u=get(d,upd.effective_user.id); save(d)
 await upd.message.reply_text(f"ABJ Casino - {u['balance']} jetons /daily",reply_markup=menu())
async def daily(upd,ctx):
 d=load(); u=get(d,upd.effective_user.id); u["balance"]+=1000; save(d)
 await upd.message.reply_text(f"+1000 - {u['balance']}",reply_markup=menu())
async def btn(upd,ctx):
 q=upd.callback_query; await q.answer(); d=load(); u=get(d,q.from_user.id)
 if q.data=="solde": await q.edit_message_text(f"Solde {u['balance']}",reply_markup=menu())
 else:
  if u["balance"]<500: await q.edit_message_text("Pas assez",reply_markup=menu()); return
  r=random.randint(1,100)
  if r>50: u["balance"]+=500; t=f"Gagne {r} +500"
  else: u["balance"]-=500; t=f"Perdu {r} -500"
  save(d); await q.edit_message_text(f"{t} - {u['balance']}",reply_markup=menu())
app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("daily",daily))
app.add_handler(CallbackQueryHandler(btn))
app.run_polling()
