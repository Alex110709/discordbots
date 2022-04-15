import discord, random, asyncio, requests
from random import randint
from random import randrange
from re import I
from discord.utils import get


client = discord.Client()
prefix = "p!"
idA, moneyA, timeA = [], [], []

try:
    f = open("UserData.txt", "r")
except:
    f = open("UserData.txt", "w")
    f.close()
    f = open("UserData.txt", "r")
while True:
    line = f.readline()
    if not line:
        break
    line = line.split(",")
    idA.append(line[0])
    moneyA.append(int(line[1]))
    timeA.append(int(line[2]))
f.close()


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


@client.event
async def on_message(message):
    cmd = message.content.split(" ")[0]
    args = message.content.split(" ")[1:]
    ID = str(message.author.id)

    if cmd == prefix + "도움말":
        embed = discord.Embed(title="명령어", description="봇 명령어", color=0x62C1CC)
        embed.add_field(name="PTX", value="ptXcash,도박 <ptX cash>, 올인, 랭킹, 송금 <ptX cash> <@대상>, 주가", inline=True)
        await message.channel.send("", embed=embed)

    if cmd == prefix + "ptXcash":
        if ID in idA:  # ID가 있을 때
            embed = discord.Embed(title="",description=format(moneyA[idA.index(ID)], ",d") + " QD ptX cash",color=0x118811,)
            await message.channel.send(embed=embed)
        elif not ID in idA:  # ID가 없을 때
            embed = discord.Embed(title="", description="0QD ptX cash", color=0x118811)
            await message.channel.send(embed=embed)

    if cmd == prefix + "올인":
        if not ID in idA or moneyA[idA.index(ID)] <= 0:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="ptX cash이 부족합니다.", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        give = random.randrange(2, 10)  # 성공확률 : 4/9
        count = await message.channel.send("배수 정하는 중 ...")
        await asyncio.sleep(2)
        await count.edit(content="만약 성공하면 건 ptX cash의 " + str(give) + "배 를 얻어요")
        await asyncio.sleep(2)
        if give % 2 == 0:
            moneyA[idA.index(ID)] *= give
            await count.edit(
                content="올인 성공! 현재 ptX cash: " + format(moneyA[idA.index(ID)], ",d") + "QD ptX cash"
            )
        elif give % 2 != 0:
            moneyA[idA.index(ID)] = 0
            await count.edit(
                content="올인 실패... 현재 ptX cash: " + format(moneyA[idA.index(ID)], ",d") + "QD ptX cash"
            )

    if cmd == prefix + "도박":
        if len(args) != 1:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: !도박 ptX cash", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if args[0].isdecimal() == False:  # 숫자가 입력되지 않았을 때
            embed = discord.Embed(title="", description="숫자만 입력해 주세요!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        args[0] = int(args[0])
        if not ID in idA or moneyA[idA.index(ID)] - args[0] < 0:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="ptX cash가 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= args[0]
        give = random.randrange(2, 10)  # 성공확률 4/9
        count = await message.channel.send("배수 정하는 중 ...")
        await asyncio.sleep(2)
        await count.edit(content="만약 성공하면 건 ptX cash의 " + str(give) + "배 를 얻어요")
        await asyncio.sleep(2)
        if give % 2 == 0:
            moneyA[idA.index(ID)] += give * args[0]
            await count.edit(
                content="도박 성공! 현재 ptX cash: " + format(moneyA[idA.index(ID)], ",d") + "QD ptXcash"
            )
        elif give % 2 != 0:
            await count.edit(
                content="도박 실패... 현재 ptX cash: " + format(moneyA[idA.index(ID)], ",d") + "QD ptXcash"
            )
    if cmd == prefix + "랭킹":
        rank, rankA = "", []  # 모든 id와 ptX cash을 담아 정렬할 2차원 배열 rankA
        for i in range(0, len(idA)):
            rankA.append([idA[i], moneyA[i]])
        rankA = sorted(rankA, reverse=True, key=lambda x: x[1])
        for i in range(0, 10):
            try:
                rank += (str(i + 1)+ "위 <@"+ rankA[i][0]+ "> : "+ format(rankA[i][1], ",d")+ "\n")
            except:
                break
        embed = discord.Embed(title="ptX cash 랭킹", description=rank, color=0xD8AA2D)
        await message.channel.send(embed=embed)

    if cmd == prefix + "송금":
        if len(args) != 2 or args[0][3:-1] in idA:  # 만약 인자 수가 잘못됬거나 순서가 바뀌었을 때
            embed = discord.Embed(title="오류", description="사용법: !송금 ptX cash @유저이름", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not args[1][3:-1] in idA:  # 송금대상의 ID가 없을 때
            embed = discord.Embed(title="오류", description="송금대상이 등록된 ID가 아닙니다", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA:  # 송금자의 ID가 없을 때
            embed = discord.Embed(title="오류", description="ptX cash이 부족합니다", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if args[0].isdecimal() == False:  # 숫자가 입력되지 않았을 때
            embed = discord.Embed(title="오류", description="숫자를 입력해주세요", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if moneyA[idA.index(ID)] < int(args[0]):  # 잔액이 부족할 때
            embed = discord.Embed(title="오류", description="ptX cash이 부족합니다", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        else:  # 모든 이상이 없을 때
            moneyA[idA.index(ID)] -= int(args[0])
            moneyA[idA.index(str(args[1][3:-1]))] += int(args[0])
            embed = discord.Embed(title="", description="송금을 성공하였습니다", color=0x118811)
            await message.channel.send(embed=embed)

    if cmd == prefix + "한강":
        page = requests.get(
            "https://hangang.winsub.kr/", headers={"User-Agent": "Mozilla/5.0"}
        )
        msg = ":droplet: 현재 한강 물 온도 : "
        msg += page.text[244:252]
        embed = discord.Embed(title="", description=msg, color=0x2EFEF7)
        await message.channel.send(embed=embed)

    if cmd == prefix + "주가":
        f=open("wnrk.txt","rt")
        for x in range(2):
         q=f.readline()
        print(q)
        f.close()
        f=open("wnrk.txt","rt")
        for x in range(3):
            w=f.readline()
        print(w)
        f.close()
        f=open("wnrk.txt","rt")
        for x in range(4):
             e=f.readline()
        print(e)
        f.close()
        f=open("wnrk.txt","rt")
        for x in range(5):
         r=f.readline()
        print(r)
        f.close()
        f=open("wnrk.txt","rt")
        for x in range(6):
            t=f.readline()
        print(t)
        f.close()
        f=open("wnrk.txt","rt")
        for x in range(7):
             y=f.readline()
        print(y)
        f.close()
        f=open("wnrk.txt","rt")
        for x in range(8):
             u=f.readline()
        print(u)

        f=open("wnrk.txt","rt")
        for x in range(9):
             i=f.readline()
        print(i)
        f.close()
        await message.channel.send("소스 코퍼레이션:"+str(q)+"SP카드:"+str(w)+"화이트 전자:"+str(e)+"엑따 대리:"+str(r)+"KOIKO(코이코):"+str(t)+"SP의 사업장:"+str(y)+"비코서버:"+str(u)+"피시톤 X의 사업장:"+str(i)  +  "    $$***QD단위***$$")

    if cmd == prefix + "가입":
        f = open("UserData.txt", "w")  # 바뀐 데이터 저장
        for i in range(0, len(idA), 1):
            f.write(str(idA[i]) + "," + str(moneyA[i]) + "," + str(timeA[i]) + "\n")
        f.close()
        print(ID, cmd)

    if cmd == prefix + "주가변동":
            from re import I
            from random import randint

            f=open("wnrk.txt","rt")
            for x in range(2):
             q=f.readline()
            print(q)
            f.close()
            f=open("wnrk.txt","rt")
            for x in range(3):
                w=f.readline()
            print(w)
            f.close()
            f=open("wnrk.txt","rt")
            for x in range(4):
                 e=f.readline()
            print(e)
            f.close()
            f=open("wnrk.txt","rt")
            for x in range(5):
                 r=f.readline()
            print(r)
            f.close()
            f=open("wnrk.txt","rt")
            for x in range(6):
                t=f.readline()
            print(t)
            f.close()
            f=open("wnrk.txt","rt")
            for x in range(7):
                 y=f.readline()
            print(y)
            f.close()
            f=open("wnrk.txt","rt")
            for x in range(8):
                 u=f.readline()
            print(u)

            f=open("wnrk.txt","rt")
            for x in range(9):
             i=f.readline()
            print(i)
            f.close()
            q = int(q)
            print(q)
            print(type(q))

            w = int(w)
            print(w)
            print(type(w))

            e = int(e)
            print(e)
            print(type(e))

            r = int(r)
            print(r)
            print(type(r))


            t = int(t)
            print(t)
            print(type(t))

            y = int(y)
            print(y)
            print(type(y))

            u = int(u)
            print(u)
            print(type(u))

            i = int(i)
            print(i)
            print(type(i))

            for _ in range(1):
                value = randrange(-100,100)
            value = int(value)
            q = int(q) + int(value)
            for _ in range(1):
                value = randrange(-100,100)
            value = int(value)
            w = int(w) + int(value)
            for _ in range(1):
                value = randrange(-100,100)
            value = int(value)
            e = int(e) + int(value)
            for _ in range(1):
                value = randrange(-100,100)
            value = int(value)
            r = int(r) + int(value) 
            for _ in range(1):
                value = randrange(-100,100)
            value = int(value)
            t = int(t) + int(value)
            for _ in range(1):
                value = randrange(-100,100)
            value = int(value)
            y = int(y) + int(value)
            for _ in range(1):
                value = randrange(-100,100)
            value = int(value)
            u = int(u) + int(value)
            for _ in range(1):
                value = randrange(10,1000)
            value = int(value)
            i = int(i) + int(value)
            f=open("wnrk.txt","x")
            f.write("============주가==============\n")
            f.write(str(q)+"\n")
            f.write(str(w)+"\n")
            f.write(str(e)+"\n")
            f.write(str(r)+"\n")
            f.write(str(t)+"\n")
            f.write(str(y)+"\n")
            f.write(str(u)+"\n")
            f.write(str(i)+"\n")
            f.close()
            f=open("wnrk.txt","rt")
            while True:
                c = f.read()
                if c == '':
                    break
                print(c)
            f.close()
            await message.channel.send("변동됨")

    if cmd == prefix + "1234":
        await message.chan4nel.send("4321")


client.run("OTIzNDY2Nzc5Mzg3MzkyMDMw.YcQbdQ.HflK4ygUq3yev07a__oOXNu5KWQ")
