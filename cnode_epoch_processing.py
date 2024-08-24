from pt_utils import *
from config import *
from fb_utils import *
import fast_abstracted_no_mem_decoder 
from aws_utils import aws_utils
from extraction_configs import *
import hashlib
import pickle
import time
import zlib

aws=aws_utils()
import time
fb=fb_utils()
query_utxo=True
query_mark_snapshot=False
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
            epoch = tip['epoch']
            era = tip['era']
            if old_epoch is None:
                old_epoch=epoch-1
            if old_epoch==epoch:
                time.sleep(30)
                
        print(epoch,old_epoch)    
    print("launch epoch processing")
    fb.updateFb(baseNetwork+"/epoch_processing",{"targetEpoch":int(epoch),"epochPricesDone":0,"epochParamsEpochDone":0,"waitStakeEpochDone":0,"rewardProcessingEpochDone":0})
    return epoch,era

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

def processLedgerState(epoch=None,era=None):
    if era=="Babbage":
        print("Babbage")
        if query_utxo:
            extraction_config = action_config_91babbage_utxo_set
        elif query_mark_snapshot:
            extraction_config = extraction_config_91babbage
        else:
            exit()
    elif era=="Conway":
        print("Conway")
        if query_utxo:
            extraction_config = action_config_91conway_utxo_set
        elif query_mark_snapshot:
            extraction_config = extraction_config_91conway
        else:
            exit()
    else:
        print("era not recognized")
        exit()

    testmode=True
    filename = f"/{ledgerStateDirectory}ls{epoch}.cbor"
    print(filename)
    start = time.time()
    if False and path.exists(ledgerStateDirectory + "ls"+str(epoch)+".cbor"):
        print("ledger state exists")
        file_path = 'large_dataset.pkl'
        with open(file_path, 'rb') as file:
            extracted_data = pickle.load(file)
    else:
        while not path.exists(ledgerStateDirectory + "ls"+str(epoch)+".cbor"):
            print("query ledger state",epoch)
            te = runcli(f"{cardanocli} query ledger-state --out-file /{ledgerStateDirectory}ls{epoch}.cbor {clisuffix}")
            print(te)
            if te != "":
                print("could not query ledger state")
                print(te)
                time.sleep(30)
            print("query ledger state: COMPLETE")

        
        decoder = fast_abstracted_no_mem_decoder.GenericCBORDecoder(extraction_config)
        with open(filename, 'rb') as f:
            decoder.initialize_file_size(f)
            decoder.decode_item(f, [],True)
        extracted_data = decoder.get_extracted_data()
        totalutxo = decoder.get_total_utxo()
    print(time.strftime("%H:%M:%S", time.gmtime(time.time()-start)))

    

    # we need to preprocess the extracted data to get it in the right format
    if query_mark_snapshot: # process snapshot data
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

        exit()

        print(f"Dataset successfully saved to {file_path}")
        if testmode:
            # aws.dump_s3(pool_blocks,"poolblocks/testpoolblocks"+str(epoch)+".json")
            # aws.dump_s3(epoch_params,"epochparams/testepochparams"+str(epoch)+".json")
            # aws.dump_s3(snapshot_values,"ls/testmarkSnapshot"+str(epoch)+".json")
            pass
        else:
            aws.dump_s3(pool_blocks,"poolblocks/poolblocks"+str(epoch)+".json")
            aws.dump_s3(epoch_params,"epochparams/epochparams"+str(epoch)+".json")
            aws.dump_s3(snapshot_values,"ls/markSnapshot"+str(epoch)+".json")
        if testmode:
            print({"epoch":epoch,"epoch_params":epoch_params,"pool_blocks":pool_blocks})
        # else:
        #     if postDataToPT("saveepochdata",{"epoch":epoch,"epoch_params":epoch_params,"pool_blocks":pool_blocks}):
        #         if postDataToPT("waitstakewritten",{"epoch":epoch,"waitstakewritten":True}):
        #             print("posted waitstake to pt")
        #             te = runcli(f"aws s3 cp {ledgerStateDirectory}ls{epoch}.cbor s3://data.pooltool.io/ls/ls{epoch}.cbor --profile s3writeprofile" )
        #             print(te)
        #             te= runcli(f"rm /{ledgerStateDirectory}/ls{epoch}.cbor")
        #             print(te)
        #         else:
        #             print("failed to post waitstake data to pooltool")
        #             exit()
        #     else:
        #         print("failed to post epoch data to pooltool")
        #         exit()
        
    
    if query_utxo: # process utxo data
        extracted_data['total_utxo'] = totalutxo
        pool_stake={}
        pool_delegator_stake = {}
        for stake_key,data in extracted_data['delegation_and_rewards'].items():
            stake_key_bin = bytes.fromhex(stake_key)
            if 'delegation' in data:
                if data['delegation'] not in pool_stake:
                    pool_stake[data['delegation']] = 0
                if data['delegation'] not in pool_delegator_stake:
                    pool_delegator_stake[data['delegation']] = {}
                if stake_key not in pool_delegator_stake[data['delegation']]:
                    
                    pool_delegator_stake[data['delegation']][stake_key_bin] = 0
                
                if stake_key in extracted_data['utxo_stake_set']:
                    pool_stake[data['delegation']] += extracted_data['utxo_stake_set'][stake_key]
                    pool_delegator_stake[data['delegation']][stake_key_bin] = extracted_data['utxo_stake_set'][stake_key]
                if 'rewards' in data:
                    pool_stake[data['delegation']] += data['rewards']
                    pool_delegator_stake[data['delegation']][stake_key_bin] += data['rewards']


        pool_data = {}
        for pool_id, data in extracted_data['live_poolparams'].items():
            pool_id_bin = bytes.fromhex(pool_id)
            pool_data[pool_id_bin]={"cp":0,"ap":0,"dl":{},"ls":0}
            pool_data[pool_id_bin]["cp"] = data['pledge']
            for pool_owner_stake_key in data['owner_addresss']:
                pool_owner_stake_key_bin = bytes.fromhex(pool_owner_stake_key)
                if pool_id in pool_delegator_stake and pool_owner_stake_key_bin in pool_delegator_stake[pool_id]:
                    pool_data[pool_id_bin]["ap"] += pool_delegator_stake[pool_id][pool_owner_stake_key_bin]
                
            if pool_id in pool_stake:
                pool_data[pool_id_bin]["ls"] = pool_stake[pool_id]
            if pool_id in pool_delegator_stake:
                pool_data[pool_id_bin]["dl"] = pool_delegator_stake[pool_id]


        # Pickle the data
        pickled_data = pickle.dumps({"pool_data":pool_data,"treasury":extracted_data['treasury'],"reserves":extracted_data['reserves']})

        # Compress the pickled data
        compressed_data = zlib.compress(pickled_data)

        hash_object = hashlib.sha256(pickled_data)
        hash_digest = hash_object.hexdigest()
        print(f"Hash of pickled data: {hash_digest}")
        # Saving to a file
        with open('compressed_data.pkl', 'wb') as file:
            file.write(compressed_data)
        
        current_timestamp = int(time.time())

        # te = subprocess.run([f"/usr/local/bin/aws s3 cp /home/user/compressed_data.pkl s3://data.pooltool.io/livedata/{current_timestamp}.pkl --profile s3writeprofile"], shell=True, capture_output=True, text=True)
        # if te.returncode != 0:
        #     print(f"Error: {te.stderr}")
        #     print("unable to write data to s3.  we will pause for 30 seconds before re-running everything")
        #     time.sleep(30)
        # else:
        #     print(f"Dataset successfully saved")
        
        # # print the time taken in H:M:s
        # print(f"Time taken: {time.strftime('%H:%M:%S', time.gmtime(time.time()-time_start))}")
        # # execute the loop at most once every 30 minutes, so delay such that we get to 30 minute cycle time:
        # print("current time: "+time.strftime('%H:%M:%S', time.gmtime(time.time())))
        # time_to_sleep = 1800 - (time.time()-time_start)
        # if time_to_sleep < 0:
        #     time_to_sleep = 0

        # print("sleeping for: "+time.strftime('%H:%M:%S', time.gmtime(time_to_sleep)))
        # print("next cycle will start at: "+time.strftime('%H:%M:%S', time.gmtime(time.time()+time_to_sleep)))
        # time.sleep(time_to_sleep)

    

    
            
    exit()




while True:
    epoch,era=waitForNewEpoch()
    # new epoch is different, launch epoch processing
    #updateEpochPrices(epoch) # gather the prices and update fb
    processLedgerState(epoch,era) # process ledger state and write data to pooltool
    #processLedgerState(502)
    