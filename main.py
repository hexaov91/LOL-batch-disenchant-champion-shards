from lcu_driver import Connector


connector = Connector()

#async def get_summoner_data(connection):
#    data = await connection.request('GET', '/lol-summoner/v1/current-summoner')
#    summoner = await data.json()
#    print(f"displayName:    {summoner['displayName']}")
#    print(f"summonerId:     {summoner['summonerId']}")
#    print(f"puuid:          {summoner['puuid']}")
#    print("-")

async def Sell(connection,bSellNotOwnedHero=False,bSellHaveMasteryToken=False):
  loot = await connection.request('GET', '/lol-loot/v1/player-loot')
  loot = await loot.json()
  SkipSellList=[]

  if not bSellHaveMasteryToken:
    for i in loot:
      bIsHeroShard = i["disenchantLootName"] == "CURRENCY_champion"
      bIsMasteryToken = "CHAMPION_TOKEN" in i["lootName"]

      if bIsMasteryToken:
          SkipSellList.append(i["itemDesc"])
  #print(SkipSellList)

  for i in loot:
    bIsHeroShard = i["disenchantLootName"] == "CURRENCY_champion"
    bIsMasteryToken = "CHAMPION_TOKEN" in i["lootName"]

    if bIsHeroShard:
        if i["itemStatus"] == "OWNED" and (i["itemDesc"] not in SkipSellList):
            itemCount=i["count"]
            data = [i["lootName"]]
            await connection.request('POST', f'/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat={itemCount}', data=data)
        elif bSellNotOwnedHero: #未擁有英雄
            itemCount=i["count"]
            data = [i["lootName"]]
            await connection.request('POST', f'/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat={itemCount}', data=data)
        else:
           print(i["itemDesc"])





@connector.ready
async def connect(connection):
  #await get_summoner_data(connection)
  await Sell(connection)

connector.start()

