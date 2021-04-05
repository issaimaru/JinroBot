# -*- coding: utf-8 -*-

#######################

#Created by Issaimaru

#Created at 2021-04-05

#######################


import discord
import datetime
import time
import asyncio
import random
from Jinro import Jinro
from collections import defaultdict
from statistics import mode
user_reaction_dic = defaultdict(dict)

TOKEN = "ODExNzk0ODE4MDEwODQxMTA5.YC3Y1w.w4fvcnZip3j_bi7czNDiqY4rjlw"

intents = discord.Intents.default()
intents.members=True#membersがdefaultではFalseなのでTrueにする
client = discord.Client(intents=intents)

#グローバル変数
TIMEID=[]
Playing_check=False
J_Mahou=False
J_Uranayer=False
J_Kaitouyer=False
J_kaitou=False
Votes=False
J_member=[]
J_memberid=[]
J_Uraned=[]
J_kaitoued=[]
Jinro_list=[]
Uranai_list=[]
Kaitou_list=[]
Vote=[]
Voted=[]
J_attend=0
job_dic={}
J_card = ["人狼","人狼","占い師","怪盗"]


@client.event
async def on_ready():
    print("Botの起動が終わりました")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    Morning = ["おはよう","おはようございます","おはこんばにちは"]
    Hello = ["こんにちは","おはこんばにちは"]
    Night = ["おやすみなさい","おやすみね！","おやすみなさい!"]

    #挨拶メッセージ
    user_name = message.author.name
    if message.content in Morning: await message.channel.send(user_name + ",おはようございます!")
    if message.content in Hello: await message.channel.send(user_name + ",こんにちは!")
    if message.content in Night: await message.channel.send(user_name + ",おやすみなさい!")


    #時刻になったらお知らせ
    global TIMEID
    Timetxt = ["-T 予定を立てなさい!","-T 時間になったら呼んで","-T time"]
    if message.content in Timetxt or message.author.id in TIMEID:await TIMER(message)

    #人狼ゲーム
    Jinro_txt = ["-T 人狼がしたい","-T　人狼しようぜ","-T j"]
    global Playing_check,J_attend,embed_GameStart,J_Mahou,J_Kaitou,job_dic,J_member,J_memberid,Jinro_list,Kaitou_list,Uranai_list,J_card,J_Uraned,Votes,Vote,J_Kaitouyer,J_Kaitoued,J_Uranayer,Voted

    if message.content in Jinro_txt and Playing_check==False:
        await client.change_presence(activity=discord.Game(name="人狼の司会者", type=1))#ゲームアクティビティを変更する
        Playing_check=True
        returns=await Jinro.run(message)
        J_attend=returns[0]
        embed_GameStart=returns[1]
        await asyncio.sleep(60)#参加者募集時間
        Playing_check=False

        retu_two=await Jinro.moderator(J_attend,embed_GameStart,J_member,J_memberid,message,client,Jinro_list,Uranai_list,Kaitou_list,J_card,job_dic)
        J_Mahou=retu_two[0]
        if J_Mahou==False:
            await End(message)
            return
        job_dic=retu_two[1]
        await asyncio.sleep(30)#魔法使いの行動時間
        J_Mahou=False
        await message.channel.send("次に怪盗の方は行動してください(30秒間)")
        J_Kaitou=True
        await asyncio.sleep(30)#怪盗の行動時間
        J_Kaitou=False
        embed=discord.Embed(title="議論開始",description="昼になりました。\n参加者は議論を開始してください\n制限時間は5分間です",colour=0x7cfc00)
        embed.set_thumbnail(url="https://cdn-ak.f.st-hatena.com/images/fotolife/A/AnnieAreYou/20170111/20170111151052.jpg")
        await message.channel.send(embed=embed)
        await asyncio.sleep(60*5)#議論の時間
        Votes=await Jinro.Vote_Send(message,J_member,J_memberid,client)#投票用のメッセージを送りつける
        await asyncio.sleep(60)#投票する時間
        Votes=False
        await Jinro.Judge(message,Vote,Jinro_list)
        await asyncio.sleep(5)#結果発表を見る時間
        await End(message)

    elif message.content in Jinro_txt and (Playing_check==True or J_member):await message.channel.send("他の方がゲームをプレイ中です...")

    if J_Mahou==True and message.author.id in Uranai_list:J_Uranayer=await Jinro.Mahou_job(message,J_card,J_member,J_memberid,J_Uranayer,job_dic,J_Uraned)#魔法使いの処理
    if J_kaitou==True and message.author.id in Kaitou_list:J_Kaitouyer=await Jinro.Kaitou_Job(message,J_member,J_memberid,J_Kaitouyer,job_dic,Jinro_list,J_Kaitoued)#怪盗の処理

    if Votes==True and message.author.id in J_memberid and not message.author.id in Voted:await Jinro.Votes_receive(message,J_member,Vote,Voted)
    elif Votes==True and message.author.id in Voted:await message.author.send("あなたはすでに投票しています!")


@client.event
async def on_raw_reaction_add(payload):
    global J_attend,user_reaction_dic,embed_GameStart,J_member,J_memberid
    if J_attend==0 or Playing_check==False:return
    await Jinro.reaction_vote(payload,embed_GameStart,J_attend,user_reaction_dic,J_member,J_memberid,client)

@client.event
async def on_raw_reaction_remove(payload):
    global J_attend,user_reaction_dic,embed_GameStart,J_member,J_memberid
    if J_attend==0 or Playing_check==False:return
    await Jinro.reaction_remove(payload,embed_GameStart,J_attend,user_reaction_dic,J_member,J_memberid,client)


async def End(message):
    global Playing_check,J_Mahou,J_Uranayer,J_Kaitouyer,J_kaitou,Votes,J_member,J,memberid,J_Uraned,J_Kaitoued,Jinro_list,Uranai_list,Kaitou_list,Vote,Voted,J_attend,job_dic,J_card
    Playing_check=False
    J_Mahou=False
    J_Uranayer=False
    J_Kaitouyer=False
    J_kaitou=False
    Votes=False
    J_member=[]
    J_memberid=[]
    J_Uraned=[]
    J_kaitoued=[]
    Jinro_list=[]
    Uranai_list=[]
    Kaitou_list=[]
    Vote=[]
    Voted=[]
    J_attend=0
    job_dic={}
    J_card = ["人狼","人狼","占い師","怪盗"]
    #すべてのグローバル変数を初期値に戻す
    await client.change_presence(activity=None)
    await message.channel.send("人狼ゲームが正常終了しました!")

async def TIMER(message):
    global TIMEID
    if not message.author.id in TIMEID:
        OKSIGN = "\N{OK Hand Sign}"
        await message.add_reaction(OKSIGN)
        TIMEID.append(message.author.id)#予定を立てるようBOTに指示した人のidを記録する
        return

    if message.author.id in TIMEID:
        try:
            plan=(message.content).split("-")
            x = []
            for p in plan:x.append(int(p))
            time_plan = datetime.datetime(x[0],x[1],x[2],x[3],x[4],x[5])#秒数まで指定
            time_real = datetime.datetime.now()#現在時刻
            if time_plan<time_real :raise TimeWarning("現在時刻よりも過去の時間設定になっています!")
            time_sleep = (time_plan - time_real).seconds#待つ秒数を設定する
            TIMEID.clear()#予定は一人しかできない
            await asyncio.sleep(time_sleep)#指定された時間まで待つ
            await message.channel.send("予定の時刻になりました!")

        except TimeWarning as e:
            await message.channel.send(e)

        except:await message.channel.send("予定を立てる構文が間違っている可能性があります\n正しい表記の例:2019-08-31-18-00-00\n(例は2019年8月31日18時00分00秒)")

class TimeWarning(Exception):pass


client.run(TOKEN)#指定のトークンのBOTを起動させる
