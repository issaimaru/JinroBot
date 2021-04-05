# -*- coding: utf-8 -*-

#######################

#Created by Issaimaru

#Created at 2021-04-05

#######################


import random
import discord
import asyncio
from collections import Counter


class Jinro:
    async def run(message):
        GameSIGN = "\N{video game}"
        await message.add_reaction(GameSIGN)
        startmessage="ワンナイト人狼をプレイする人は一分間でこのメッセージにリアクションしてください"
        embed_GameStart = discord.Embed(title="ワンナイト人狼の参加者を募集中",description=startmessage+"\n参加者:[]",colour=0xff0000)
        embed_GameStart.set_thumbnail(url="https://pics.prcm.jp/1017ac6805b15/82016574/jpeg/82016574_220x220.jpeg")
        messagerid=await message.channel.send(embed=embed_GameStart)
        return  messagerid,embed_GameStart

    #受付のメッセージを送信する関数

    async def reaction_vote(payload,embed,attend,reaction_dic,mem,memid,client):
        if payload.message_id == attend.id and not payload.message_id in reaction_dic[payload.user_id]:#特定のメッセージに対するリアクションかつ一回もそのメッセージにリアクションしてない人かどうか
            reaction_dic[payload.user_id][payload.message_id] = payload.emoji
            message = await client.fetch_user(payload.user_id)#useridから情報を取得
            mem.append(message.name)
            memid.append(payload.user_id)
            color_message=0xff0000
            if (len(mem)>=3 and len(mem)<=6):color_message=0x4169e1

            startmessage="ワンナイト人狼をプレイする人は一分間でこのメッセージにリアクションしてください"
            embed.description=startmessage+"\n参加者:"+str(mem)
            embed.colour=color_message
            await attend.edit(embed=embed)

    #リアクションが追加されたときに実行する関数

    async def reaction_remove(payload,embed,attend,reaction_dic,mem,memid,client):
        if reaction_dic[payload.user_id][payload.message_id] == payload.emoji:
            del reaction_dic[payload.user_id][payload.message_id]
            message = await client.fetch_user(payload.user_id)#useridから情報を取得
            mem.remove(message.name)
            memid.remove(payload.user_id)
            color_message=0xff0000
            if (len(mem)>=3 and len(mem)<=6):color_message=0x4169e1

            startmessage="ワンナイト人狼をプレイする人は一分間でこのメッセージにリアクションしてください"
            embed.description=startmessage+"\n参加者:"+str(mem)
            embed.colour=color_message
            await attend.edit(embed=embed)

    #リアクションが削除されたときに実行する関数

    async def moderator(attend,embed,mem,memid,message,client,Jinro_list,Uranai_list,Kaitou_list,J_card,job_dic):
        embed.title="ワンナイト人狼の参加者募集終了!"
        embed.description="一分が経過し、受付が終了しました。"
        await attend.edit(embed=embed)

        if len(mem) < 3:
            await message.channel.send("人数が足りません!\nこのゲームをプレイするには最低３名は必要です!")
            return False,
            

        if len(mem) > 6:
            await message.channel.send("人数が多すぎます!ワンナイト人狼は3～6人用です!")
            return False,
        
        await message.channel.send("ゲームを開始します...")

        await Jinro.card(len(mem),J_card)#人数の分だけ村人を追加してやる
        job_dic=await Jinro.random(len(mem),J_card,mem,memid,Jinro_list,Uranai_list,Kaitou_list)
        
        await Jinro.send_message(len(mem),job_dic,memid,J_card,client)

        await message.channel.send("ユーザーの役職が決まりました！\n夜になるまでに役職を確認してください!")
        await asyncio.sleep(20)
        await message.channel.send("夜になりました。占い師の方は占ってください(30秒間)")
        return True,job_dic

    #受付終了～魔法使いの行動までを担当する関数





    async def card(number,j_card):
        for p in range(number-2):j_card.append("村人")

    #人数-2の分だけ村人を追加する関数

    async def random(number,j_card,mem,memberid,jinro_list,uranai_list,kaitou_list):
        j_dic={}
        for usernom in range(number):
            job=random.choice(j_card)
            j_dic[memberid[usernom]] = job
            if job == "人狼":jinro_list.append(mem[usernom])
            if job == "占い師":uranai_list.append(memberid[usernom])
            if job == "怪盗":kaitou_list.append(memberid[usernom])
            j_card.remove(job)
        return j_dic

    #ランダムに役職を決める関数

    async def send_message(number,job_dic,memid,j_card,client):
        for usernom in range(number):
            user = client.get_user(memid[usernom])
            job = job_dic[memid[usernom]]
            embed=discord.Embed(title="あなたの役職は" + job +"です")
            
            if (job=="人狼"):
                embed.set_thumbnail(url="https://pht.qoo-static.com/xpjm7LxwytTwf2gy2n0eVREppHxYC_hBKb_s67wCkqjQxh1egVdANpiM6cZZF1Unazw=w512")
                embed.colour=0x000000
                if (not "人狼" in j_card):embed.description="人狼の人は"+str(Jinro_list)+"です。\nばれないように頑張りましょう!"
                else:embed.description="人狼はあなた一人です!\nばれないように頑張りましょう!"

            if job == "村人":
                embed.description="あなたは特別な能力はありません"
                embed.set_thumbnail(url="https://cdn-ak.f.st-hatena.com/images/fotolife/M/MAABOU/20190225/20190225111336.jpg")
                embed.colour=0xff8c00

            if job == "占い師":
                embed.description="あなたは誰にも選ばれなかった２つの役職か、誰か一人のカードを見ることができます。\n夜になったら数字を打ち込んでください\n1:誰にも選ばれなかった２つの役職\n2:誰か一人のカード"
                embed.set_thumbnail(url="https://animeanime.jp/imgs/p/jtKDOVlKAvjRrNw8SXAVejagI61Nrq_oqaqr/286618.jpg")
                embed.colour=0xba55d3

            if job == "怪盗":
                embed.description="あなたは自分と誰か一人のカードを入れ替えることができます。\n夜になったら数字を打ち込んでください\n1:カードを入れ替える\n2:カードを入れ替えない"
                embed.set_thumbnail(url="https://pbs.twimg.com/media/DhlKk0dV4AAoT_0?format=jpg&name=large")
                embed.colour=0x0000ff
         
            await user.send(embed=embed)

    #役職を参加者に通知する関数


    async def Mahou_job(message,J_card,mem,memid,bools,job_dic,J_Uraned):
        if message.author.id in J_Uraned:return False

        embed=discord.Embed(title="天の声",colour=0xba55d3)
        embed.set_thumbnail(url="http://www.nihon-net.com/wp-content/uploads/2016/04/%E7%A5%9E%E6%A7%98.jpg")

        if bools==True:
            try:
                num=int(message.content)
                job=job_dic[memid[num]]
                embed.description="占った対象の役職は"+job+"です"
                await message.author.send(embed=embed)
                J_Uraned.append(message.author.id)
                return False
            except:
                embed.description="正しい数値を入力してください!"
                await message.author.send(embed=embed)
                return True
            
        elif message.content == "1":#もし選ばれなかった2つの役職を見るならば
            embed.description="誰にも選ばれなかった役職は"+str(J_card)+"です"
            await message.author.send(embed=embed)
            J_Uraned.append(message.author.id)
            return False
        elif message.content == "2":#もし誰か一人のカードを占うならば
            embed.description="占う人を選んでください...\n"
            for number in range(len(mem)):embed.description+=str(number)+":"+mem[number]+"\n"
            await message.author.send(embed=embed)
            return True

    #占い師の仕事の処理をする関数

    async def Kaitou_Job(message,mem,memid,bools,job_dic,jinro_list,J_Kaitoued):
        if message.author.id in J_Kaitoued:return False

        embed=discord.Embed(title="怪盗",colour=0x0000ff)
        embed.set_thumbnail(url="https://pbs.twimg.com/media/DhlKk0dV4AAoT_0?format=jpg&name=large")

        if bools==True:
            try:
                num=int(message.content)
                job=job_dic[memid[num]]
                if job=="人狼":#人狼以外の場合は特に処理が必要でないため必要ない
                    jinro_list.remove(mem[num])
                    job_dic[memid[num]]="怪盗"

                    find=memid.find(message.author.id)
                    jinro_list.append(mem[find])
                    job_dic[memid[find]]="人狼"
                embed.description="対象のカードを盗んでお前は"+job+"になったぜ!"
                await message.author.send(embed=embed)
                J_Kaitoued.append(message.author.id)
                return False
            
            except:
                embed.description="正しい数値を入力してくれないとわからないぞ！"
                await message.author.send(embed=embed)
                return True

        elif message.content == "1":
            embed.description="カードを盗みに行く人、誰にすっかな...!\n"
            for number in range(len(mem)):embed.description+=str(number)+":"+mem[number]+"\n"
            await message.author.send(embed=embed)
            return True
        elif message.content == "2":
            embed.description="やっぱ盗むのは犯罪だしだめだな、やめよう！"
            await message.author.send(embed=embed)
            J_Kaitoued.append(message.author.id)
            return False

     #怪盗の仕事をする関数


    async def Vote_Send(message,mem,memid,client):
        embed=discord.Embed(title="投票",description="5分が経過しました。誰が人狼かを投票してください!\n",colour=0x00bfff)
        embed.set_thumbnail(url="https://stg2-cdn.go2senkyo.com/articles/wp-content/uploads/2018/04/24185912/pixta_37438500_S-600x300.jpg")
        for num in range(len(mem)):embed.description+=str(num)+":"+mem[num]+"\n"
        embed.description+="無投票の場合:平和村"
        for userid in memid:
            usermessage=client.get_user(userid)
            await usermessage.send(embed=embed)
        return True

    #投票用メッセージを送りつける関数


    async def Votes_receive(message,mem,vote,voteuser):
        try:
            num=int(message.content)
            vote.append(mem[num])#投票された人を記録
            voteuser.append(message.author.id)
            await message.author.send("投票が完了しました!")
        except:await message.author.send("正しい番号を入力してください")

    #投票者を記録する関数

    async def Judge(message,vote,Jinro_list):
        embed=discord.Embed(title="結果発表",colour=0xdc143c)
        embed.set_thumbnail(url="https://i.ytimg.com/vi/xUgz9qpmdzg/maxresdefault.jpg")
        if not vote:
            embed.description="無投票でしたので平和村投票とみなされました\n"
            if not Jinro_list:
                embed.description+="平和村でした！全員勝利しました!"
            else:
                embed.description+="残念、平和村ではありませんでした!\n人狼サイドの勝利です!\n人狼:"+str(Jinro_list)
        else:
            user=Counter(vote).most_common()[0][0]
            num=Counter(vote).most_common()[0][1]
            embed.description=str(user)+"が"+str(num)+"票で選ばれました!\n"
            if not Jinro_list:embed.description+="残念、平和村でした！全員敗北です！"
            elif user in Jinro_list:embed.description+="選ばれた人は人狼でした！人間サイドの勝利です！\n人狼:"+str(Jinro_list)
            elif not user in Jinro_list:embed.description+="選ばれた人は人狼ではありません！人狼サイドの勝利です！\n人狼:"+str(Jinro_list)
        await message.channel.send(embed=embed)

    #結果を通知する関数
