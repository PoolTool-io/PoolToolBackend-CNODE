import websockets
import time
import json
import socket
import asyncio
import requests

from config import *
from pt_utils import * 
from fb_utils import fb_utils
from aws_utils import aws_utils

POOL_RANKING_PERIOD=60*58*5 # 5 hours ish

fb=fb_utils()
aws=aws_utils()

async def receive_message(ws):
    try:
        response = json.loads(await ws.recv())
        return response
    except:
        return False

async def send_message(ws, methodname, args):
    try:
        print(json.dumps({
            "type": "jsonwsp/request",
            "version": "1.0",
            "servicename": "ogmios",
            "methodname":methodname,
            "args":args
        }))
        await ws.send(json.dumps({
            "type": "jsonwsp/request",
            "version": "1.0",
            "servicename": "ogmios",
            "methodname":methodname,
            "args":args
        }))
        return  True
    except websockets.exceptions.ConnectionClosedError:
        return False
    except websockets.exceptions.ConnectionClosedOK:
        return False

    

async def update_pool_ranking(websocket):
    if not await send_message(websocket, "FindIntersect", { "points": ["origin"] }):
        return False
    response = await receive_message(websocket) 
    if not response:
        return False
    point = response['result']['IntersectionFound']['tip']
    print(point)
    if not await send_message(websocket,"Acquire",  {"point": point } ):
        return False
    response = await receive_message(websocket) 
    if not response:
        return False

    
    if not await send_message(websocket,"Query",  {"query": {"nonMyopicMemberRewards":[10000000000]} } ):
        return False
    response = await receive_message(websocket) 
    if not response:
        return False
    poolranks=[]
    for item in response['result']['10000000000']:
        poolId = convertBech32(item)
        poolranks.append({"p":poolId, "v":response['result']['10000000000'][item]})
    poolranks.sort(key=lambda x: x["v"], reverse=True)

    poolRanks = {}
    lastRankedPool = 0
    for pool in poolranks:
        if pool['v'] > 0:
            lastRankedPool = lastRankedPool + 1

    for idx, pool in enumerate(poolranks):
        if pool['v'] > 0:
            poolRanks[pool['p']] = idx + 1
        else:
            poolRanks[pool['p']] = lastRankedPool + 1
        
    
    latestpoolrank=str(int(time.time()))
    aws.dump_s3(poolRanks,"poolranks/poolranks"+latestpoolrank+".json")
    postDataToPT("savepoolranking",{"latestpoolrank":latestpoolrank})

    return True



async def main():
    pool_ranking=POOL_RANKING_PERIOD #every 1 hour
   
    
    while True:
        #init loop
        
        try:
            websocket = await websockets.connect('ws://localhost:1337')
        except:
            print("failed to open websocket.  retrying in 10 seconds")
            time.sleep(10)
            continue
        while True:

            

            print(" pool_ranking: ",pool_ranking)
            pool_ranking=pool_ranking-1
            if pool_ranking<=0:
                if not await update_pool_ranking(websocket):
                    print("update_pool_ranking failed.  pausing for 60 seconds before restarting")
                    time.sleep(60)
                    break
                else:
                    pool_ranking=POOL_RANKING_PERIOD
            
            time.sleep(1)

asyncio.run(main())