import os, json, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

def load():
    try:
        with open("db.json") as f: return json.load(f)
    except: return {}

def save(d):
    with open("db.json","w") as f: json.dump(d,f)

def get(d,u):
    if str(u) not in d: d[str(u)]={"balance":1000}
    return d[str(u)]

def menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("💰 Solde",callback_data="solde"),InlineKeyboardButton("🎰 Jouer 500F",callback_data="play")],[InlineKeyboardButton("🎁 Bonus +1000",callback_data="bonus")]])

async def start(upd,ctx):
    d=load(); u=get(d,upd.effective_user.id); save(d)
    await upd.message.reply_text(f"🔥 ABJ Casino\n💰 Solde: {u['balance']} FCFA",reply_markup=menu())

async def daily(upd,ctx):
    d=load(); u=get(d,upd.effective_user.id); u["balance"]+=1000; save(d)
    await upd.message.reply_text(f"+1000 - Nouveau: {u['balance']}",reply_markup=menu())

async def btn(upd,ctx):
    q=upd.callback_query; await q.answer(); d=load(); u=get(d,q.from_user.id)
    if q.data=="solde":
        await q.edit_message_text(f"💰 Solde: {u['balance']} FCFA",reply_markup=menu())
    else:
        if q.data=="bonus":
            u["balance"]+=1000; t=f"🎁 Bonus +1000! Solde: {u['balance']}"
        else:
            if u["balance"]<500:
                await q.edit_message_text(f"❌ Pas assez - Solde: {u['balance']}",reply_markup=menu()); return
            r=random.randint(1,100)
            if r>50: u["balance"]+=500; t=f"🎉 Gagné {r}! +500 -> {u['balance']} FCFA"
            else: u["balance"]-=500; t=f"💸 Perdu {r} -500 -> {u['balance']} FCFA"
        save(d); await q.edit_message_text(t,reply_markup=menu())

app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("daily",daily))
app.add_handler(CallbackQueryHandler(btn))
app.run_polling()
