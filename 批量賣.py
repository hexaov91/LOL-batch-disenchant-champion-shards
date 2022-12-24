from lcu_driver import Connector


connector = Connector()

async def get_summoner_data(connection):
    data = await connection.request('GET', '/lol-summoner/v1/current-summoner')
    summoner = await data.json()
    print(f"displayName:    {summoner['displayName']}")
    print(f"summonerId:     {summoner['summonerId']}")
    print(f"puuid:          {summoner['puuid']}")
    print("-")

async def Sell(connection,bSellNotOwnedHero=False):
  loot = await connection.request('GET', '/lol-loot/v1/player-loot')
  loot = await loot.json()

  for i in loot:
    if i["disenchantLootName"] == "CURRENCY_champion":
        
        if i["itemStatus"] == "OWNED":
            itemCount=i["count"]
            data = [i["lootName"]]
            await connection.request('POST', f'/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat={itemCount}', data=data)
        elif bSellNotOwnedHero:
            itemCount=i["count"]
            data = [i["lootName"]]
            await connection.request('POST', f'/lol-loot/v1/recipes/CHAMPION_RENTAL_disenchant/craft?repeat={itemCount}', data=data)
            print(i["lootName"])
        #itemName=i["itemDesc"]



@connector.ready
async def connect(connection):
  await get_summoner_data(connection)
  await Sell(connection)

connector.start()

