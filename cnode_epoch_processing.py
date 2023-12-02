from pt_utils import *
from config import *
from fb_utils import *
from nomemdecoder_util import *
from aws_utils import aws_utils
aws=aws_utils()
import time
fb=fb_utils()
# this will monitor the node and start epoch processing as soon as the node flips to the new epoch
print(DATABASESERVERURL)
def waitForNewEpoch():
    print("waiting for new epoch")
    epoch=None
    old_epoch=None
   
    while epoch == old_epoch:
        te = runcli(f"{cardanocli} query tip" + clisuffix2 )
        while te is None:
            print("could not get tip from node - is it offline?")
            time.sleep(30)
            te = runcli(f"{cardanocli} query tip" + clisuffix2 )
        if te is not None:
            tip=json.loads(te)
            epoch = firstSlotEpoch + math.floor((tip['slot'] -  firstSlot) / 432000)
            if old_epoch is None:
                old_epoch=epoch
            if old_epoch==epoch:
                time.sleep(30)
                
        print(epoch,old_epoch)    
    print("launch epoch processing")
    fb.updateFb(baseNetwork+"/epoch_processing",{"targetEpoch":int(epoch),"epochPricesDone":0,"epochParamsEpochDone":0,"waitStakeEpochDone":0,"rewardProcessingEpochDone":0})
    return epoch

def updateEpochPrices(epoch):
    block_production_epoch=epoch-2
    print(block_production_epoch)

    
    todayprices=ptGetPrices()
    print(baseNetwork)
    print(block_production_epoch)

    epoch_start_time=(block_production_epoch * 432000) + cardano_start_time
    epoch_reward_time=(2*432000)+epoch_start_time
    print(epoch_reward_time)

    print(todayprices)
    fb.updateFb(baseNetwork+"/epoch_processing",{"epochPricesDone":int(epoch)})
    fb.updateFb(baseNetwork+"/epoch_exchange_rates/"+str(block_production_epoch),{"rewardDate":int(epoch_reward_time),"adaPrices":todayprices['cardano']})

def postDataToPT(api,package):
    json_payload = json.dumps(package)
    # Set the headers to specify that we are sending JSON data
    headers = {'Content-Type': 'application/json'}
    # Send the POST request
    response = requests.post(DATABASESERVERURL+api, data=json_payload, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print('POST request successful: '+api)
        return True
    else:
        print('POST request failed')
        return False

def processLedgerState(epoch):
    filename = f"/{ledgerStateDirectory}ls{epoch}.cbor"
    print(filename)
    while not path.exists(ledgerStateDirectory + "ls"+str(epoch)+".cbor"):
        print("query ledger state",epoch)
        te = runcli(f"{cardanocli} query ledger-state --out-file /{ledgerStateDirectory}ls{epoch}.cbor {clisuffix}")
        print(te)
        if te != "":
            print("could not query ledger state")
            print(te)
            time.sleep(30)
        print("query ledger state: COMPLETE")

    #filename = f"testls424.cbor"
    decoder = Decoder()
    with open(filename, 'rb') as f:
        decoder.initialize_file_size(f)
        decoder.decode_item(f, [],True)
    pool_blocks=decoder.get_pool_blocks()
    snapshot_values=decoder.get_snapshot_values()
    epoch_params=decoder.get_epoch_params()
    aws.dump_s3(pool_blocks,"poolblocks/poolblocks"+str(epoch)+".json")
    aws.dump_s3(epoch_params,"epochparams/epochparams"+str(epoch)+".json")
    aws.dump_s3(snapshot_values,"ls/markSnapshot"+str(epoch)+".json")
    if postDataToPT("saveepochdata",{"epoch":epoch,"epoch_params":epoch_params,"pool_blocks":pool_blocks}):
        if postDataToPT("waitstakewritten",{"epoch":epoch,"waitstakewritten":True}):
            print("posted waitstake to pt")
            te = runcli(f"aws s3 cp {ledgerStateDirectory}ls{epoch}.cbor s3://data.pooltool.io/ls/ls{epoch}.cbor --profile s3writeprofile" )
            print(te)
            te= runcli(f"rm /{ledgerStateDirectory}/ls{epoch}.cbor")
            print(te)
        else:
            print("failed to post waitstake data to pooltool")
            exit()

        
    else:
        print("failed to post epoch data to pooltool")
        exit()
            





while True:
    epoch=waitForNewEpoch()
    # new epoch is different, launch epoch processing
    updateEpochPrices(epoch) # gather the prices and update fb
    processLedgerState(epoch) # process ledger state and write data to pooltool
    