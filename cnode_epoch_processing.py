from pt_utils import *
from config import *
from fb_utils import *
import fast_abstracted_no_mem_decoder 
from aws_utils import aws_utils
from extraction_configs import *
import pickle
extraction_config = extraction_config_91babbage
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
    headers = {'Content-Type': 'application/json'}
    response = requests.post(DATABASESERVERURL+api, data=json_payload, headers=headers)

    if response.status_code == 200:
        print('POST request successful: '+api)
        return True
    else:
        print('POST request failed')
        return False

def processLedgerState(epoch=None):
    testmode=False
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

    start = time.time()
    decoder = fast_abstracted_no_mem_decoder.GenericCBORDecoder(extraction_config)
    with open(filename, 'rb') as f:
        decoder.initialize_file_size(f)
        decoder.decode_item(f, [],True)
    extracted_data = decoder.get_extracted_data()
    print(time.strftime("%H:%M:%S", time.gmtime(time.time()-start)))

    # file_path = 'large_dataset.pkl'
    # with open(file_path, 'rb') as file:
    #     extracted_data = pickle.load(file)

    # we need to preprocess the extracted data to get it in the right format
    if 'snapshot_values' in extracted_data:
        extracted_data['values'] = {}
        for key in extracted_data['snapshot_values']:
            extracted_data['values'][key] = {}
            extracted_data['values'][key]['v'] = extracted_data['snapshot_values'][key]['v']
            extracted_data['values'][key]['vk'] = extracted_data['snapshot_values'][key]['vk']
    if 'snapshot_delegations' in extracted_data:
        for key in extracted_data['snapshot_delegations']:
            if key in extracted_data['values']:
                extracted_data['values'][key]['dp'] = extracted_data['snapshot_delegations'][key]['v']
                extracted_data['values'][key]['dk'] = extracted_data['snapshot_delegations'][key]['dk']
            else:
                extracted_data['values'][key] = {}
                extracted_data['values'][key]['v']=0
                extracted_data['values'][key]['vk']=0
                extracted_data['values'][key]['dp'] = extracted_data['snapshot_delegations'][key]['v']
                extracted_data['values'][key]['dk'] = extracted_data['snapshot_delegations'][key]['dk']

    if 'snapshot_poolparams' in extracted_data:
        extracted_data['pool_params'] = {}
        for key in extracted_data['snapshot_poolparams']:
            extracted_data['pool_params'][key] = {}
            extracted_data['pool_params'][key]['pledge'] = extracted_data['snapshot_poolparams'][key]['pledge']
            extracted_data['pool_params'][key]['cost'] = extracted_data['snapshot_poolparams'][key]['cost']
            extracted_data['pool_params'][key]['own'] = extracted_data['snapshot_poolparams'][key]['owner_addresss']
            extracted_data['pool_params'][key]['ra'] = extracted_data['snapshot_poolparams'][key]['reward_address']
            extracted_data['pool_params'][key]['margin_num'] = extracted_data['snapshot_poolparams'][key]['margin_num']
            extracted_data['pool_params'][key]['margin_den'] = extracted_data['snapshot_poolparams'][key]['margin_den']
    
    try: 
        pool_blocks=extracted_data['pool_blocks']
    except:
        print("no pool blocks")
        pool_blocks=None
    snapshot_values={"values":extracted_data['values'], "pool_params":extracted_data['pool_params']}

   

    epoch_params = {
        'treasury': extracted_data['treasury'],
        'reserves': extracted_data['reserves'],
        'epoch_fees': extracted_data['epoch_fees'],
        'reward_pot': extracted_data['reward_pot'],
        'txFeeFixed': extracted_data['txFeeFixed'],
        'txFeePerByte': extracted_data['txFeePerByte'],
        'maxBlockSize': extracted_data['maxBlockSize'],
        'maxTxSize': extracted_data['maxTxSize'],
        'maxBhSize': extracted_data['maxBhSize'],
        'stakeAddressDeposit': extracted_data['stakeAddressDeposit'],
        'stakePoolDeposit': extracted_data['stakePoolDeposit'],
        'maxEpoch': extracted_data['maxEpoch'],
        'optimalPoolCount': extracted_data['optimalPoolCount'],
        'influence': extracted_data['influence']/extracted_data['influence_divisor'],
        'influence_divisor': extracted_data['influence_divisor'],
        'monetaryExpandRate': extracted_data['monetaryExpandRate']/extracted_data['monetaryExpandRate_divisor'],
        'monetaryExpandRate_divisor': extracted_data['monetaryExpandRate_divisor'],
        'treasuryGrowthRate': extracted_data['treasuryGrowthRate']/extracted_data['treasuryGrowthRate_divisor'],
        'treasuryGrowthRate_divisor': extracted_data['treasuryGrowthRate_divisor'],
        'protocolMajor': extracted_data['protocolMajor'],
        'protocolMinor': extracted_data['protocolMinor'],
        'minPoolCost': extracted_data['minPoolCost'],
        'decentralisation': 0,
    }
    extracted_data['epoch_params'] = epoch_params
    
    file_path = 'large_dataset.pkl'
    # Open the file in write-binary mode and save the dataset using pickle
    with open(file_path, 'wb') as file:
        pickle.dump(extracted_data, file, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Dataset successfully saved to {file_path}")


    

    if testmode:
        aws.dump_s3(pool_blocks,"poolblocks/testpoolblocks"+str(epoch)+".json")
        aws.dump_s3(epoch_params,"epochparams/testepochparams"+str(epoch)+".json")
        aws.dump_s3(snapshot_values,"ls/testmarkSnapshot"+str(epoch)+".json")
    else:
        aws.dump_s3(pool_blocks,"poolblocks/poolblocks"+str(epoch)+".json")
        aws.dump_s3(epoch_params,"epochparams/epochparams"+str(epoch)+".json")
        aws.dump_s3(snapshot_values,"ls/markSnapshot"+str(epoch)+".json")
    if testmode:
        print({"epoch":epoch,"epoch_params":epoch_params,"pool_blocks":pool_blocks})
    else:
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
    #processLedgerState(502)
    