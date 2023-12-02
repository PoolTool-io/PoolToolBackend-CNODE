import binascii
import os 
class Decoder:

    def __init__(self):
        self.file_size=0
        self.pool_blocks = {}
        self.pool_id = ''
        self.capturing_pool_blocks = False
        self.snapshot_values = {"values": {}, "pool_params": {}}
        self.capturing_mark_snapshot_values_count = False
        self.capturing_mark_snapshot_values = False
        self.capturing_mark_snapshot_delegations = False
        self.capturing_mark_snapshot_pool_params = False
        self.capturing_mark_snapshot_pool_params_owner_addresses = False
        self.capturing_mark_snapshot_owner_array_length = False
        self.capturing_mark_snapshot_owner_array_length_value = 0
        self.capturing_mark_snapshot_key = 0
        self.mark_snapshot_values_counter = 0
        self.capturing_mark_snapshot_pool_params_waiting_for_next = 0
        self.snapshot_value_1 = None
        self.snapshot_value_2 = None
        self.epoch_params = {}
    
    def initialize_file_size(self, f):
        self.file_size=os.fstat(f.fileno()).st_size
    
    def get_epoch_params(self):
        return self.epoch_params
    
    def get_snapshot_values(self):
        return self.snapshot_values
    
    def get_pool_blocks(self):
        return self.pool_blocks

    def decode_item(self, f, hierarchy=[], top_level=True):
        if len(hierarchy)==2 and hierarchy[0]==2 and hierarchy[1]==1:
            self.capturing_pool_blocks=True
        if self.capturing_pool_blocks and len(hierarchy)==1 and hierarchy[0]==3:
            self.capturing_pool_blocks=False
            print("Done capturing pool blocks")
        if len(hierarchy)==4 and hierarchy[0]==4 and hierarchy[1]==3 and hierarchy[2]==1 and hierarchy[3]==1:
            self.capturing_mark_snapshot_values=True
            self.capturing_mark_snapshot_values_count=True
            self.mark_snapshot_values_counter=0
            self.capturing_mark_snapshot_key=0
        if len(hierarchy)==4 and hierarchy[0]==4 and hierarchy[1]==3 and hierarchy[2]==1 and hierarchy[3]==2:
            print("Done capturing mark snapshot values.  We have "+str(len(self.snapshot_values["values"]))+" addresses")
            self.capturing_mark_snapshot_values_count=True
            self.mark_snapshot_values_counter=0
            self.capturing_mark_snapshot_values=False
            self.capturing_mark_snapshot_delegations=True
            self.capturing_mark_snapshot_key=0
            
        if len(hierarchy)==4 and hierarchy[0]==4 and hierarchy[1]==3 and hierarchy[2]==1 and hierarchy[3]==3:
            print("Done capturing mark snapshot delegations.  We have "+str(len(self.snapshot_values["values"]))+" addresses")
            self.capturing_mark_snapshot_delegations=False
            self.capturing_mark_snapshot_pool_params=True
            self.capturing_mark_snapshot_values_count=True
            self.capturing_mark_snapshot_pool_params_waiting_for_next=1
            self.mark_snapshot_values_counter=0
            self.capturing_mark_snapshot_key=0
            
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==3 and  hierarchy[2]==2:
            print("done capturing mark snapshot pool params.  We have "+str(len(self.snapshot_values["pool_params"]))+" pools")
            self.capturing_mark_snapshot_pool_params=False
            self.capturing_mark_snapshot_values_count=False
            self.capturing_mark_snapshot_delegations=False
            
        read_byte = f.read(1)
        if not read_byte:  # The file has ended
            print("End of file")
            return
        
        initial_byte = ord(read_byte)
        major_type = initial_byte >> 5
        length_or_value = initial_byte & 0x1F
        if length_or_value > 23:
            # If the length or value is above 23, it's encoded in the next 1-8 bytes
            if length_or_value == 24:
                length_or_value = ord(f.read(1))
            elif length_or_value == 25:
                length_or_value = int.from_bytes(f.read(2), 'big')
            elif length_or_value == 26:
                length_or_value = int.from_bytes(f.read(4), 'big')
            elif length_or_value == 27:
                length_or_value = int.from_bytes(f.read(8), 'big')
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==1 and hierarchy[2]==1:
            self.epoch_params["treasury"]=length_or_value
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==1 and hierarchy[2]==2:
            self.epoch_params["reserves"]=length_or_value
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==3 and hierarchy[2]==4:
            self.epoch_params["epoch_fees"]=length_or_value
            self.epoch_params["decentralisation"]=0
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==3:
            self.epoch_params["maxBlockSize"]=length_or_value
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==5:
            self.epoch_params["maxBhSize"]=length_or_value
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==8:
            self.epoch_params["maxEpoch"]=length_or_value  
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==9:
            self.epoch_params["optimalPoolCount"]=length_or_value
        if len(hierarchy)==5 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==10 and hierarchy[3]==1 and hierarchy[4]==1:
            self.epoch_params["influence"]=length_or_value
        if len(hierarchy)==5 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==10 and hierarchy[3]==1 and hierarchy[4]==2:
            self.epoch_params["influence"]=self.epoch_params["influence"]/length_or_value      
        if len(hierarchy)==5 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==11 and hierarchy[3]==1 and hierarchy[4]==1:
            self.epoch_params["monetaryExpandRate"]=length_or_value
        if len(hierarchy)==5 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==11 and hierarchy[3]==1 and hierarchy[4]==2:
            self.epoch_params["monetaryExpandRate"]=self.epoch_params["monetaryExpandRate"]/length_or_value          
        if len(hierarchy)==5 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==12 and hierarchy[3]==1 and hierarchy[4]==1:
            self.epoch_params["treasuryGrowthRate"]=length_or_value
        if len(hierarchy)==5 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==12 and hierarchy[3]==1 and hierarchy[4]==2:
            self.epoch_params["treasuryGrowthRate"]=self.epoch_params["treasuryGrowthRate"]/length_or_value       
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==13:
            self.epoch_params["protocolMajor"]=length_or_value
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==4 and hierarchy[2]==14:
            self.epoch_params["protocolMinor"]=length_or_value
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==6 and hierarchy[2]==2:
            self.epoch_params["reward_pot"]=length_or_value
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==6 and hierarchy[2]==13:
            self.epoch_params["protocolMajorEM1"]=length_or_value
        if len(hierarchy)==3 and hierarchy[0]==4 and hierarchy[1]==6 and hierarchy[2]==14:
            self.epoch_params["protocolMinorEM1"]=length_or_value

        if major_type in [0, 1]:  # unsigned integer, negative integer
            if self.capturing_pool_blocks:
                self.pool_blocks[self.pool_id]=length_or_value
            if self.capturing_mark_snapshot_values:
                if self.capturing_mark_snapshot_key==0:
                    self.snapshot_value_1=length_or_value
                    self.capturing_mark_snapshot_key=1
                elif self.capturing_mark_snapshot_key==2:
                    self.snapshot_values['values'][self.snapshot_value_2]={"vk":self.snapshot_value_1,"v":length_or_value}
                    self.mark_snapshot_values_counter-=1
                    self.capturing_mark_snapshot_key=0
            if self.capturing_mark_snapshot_delegations:
                if self.capturing_mark_snapshot_key==0:
                    self.snapshot_value_1=length_or_value
                    self.capturing_mark_snapshot_key=1
            if self.capturing_mark_snapshot_pool_params:
                
                if self.capturing_mark_snapshot_key==2:
                    self.snapshot_values['pool_params'][self.pool_id]["pledge"]=length_or_value
                    self.capturing_mark_snapshot_key=3
                elif self.capturing_mark_snapshot_key==3:
                    self.snapshot_values['pool_params'][self.pool_id]["cost"]=length_or_value
                    self.capturing_mark_snapshot_key=4
                elif self.capturing_mark_snapshot_key==4:
                    self.snapshot_values['pool_params'][self.pool_id]["margin_num"]=length_or_value
                    self.capturing_mark_snapshot_key=5
                elif self.capturing_mark_snapshot_key==5:
                    self.snapshot_values['pool_params'][self.pool_id]["margin_den"]=length_or_value
                    self.capturing_mark_snapshot_key=6
        elif major_type == 2:  # byte string
            if f.tell() + length_or_value > self.file_size:
                raise EOFError('Byte string extends beyond end of file:' + str(length_or_value) + ' bytes at position ' + str(f.tell()) + ' of ' + str(self.file_size))
            value=f.read(length_or_value)
            if self.capturing_pool_blocks:
                self.pool_id=binascii.hexlify(value).decode('utf-8')
            if self.capturing_mark_snapshot_values:
                if self.capturing_mark_snapshot_key==1:
                    self.snapshot_value_2=binascii.hexlify(value).decode('utf-8')
                    self.capturing_mark_snapshot_key=2
            if self.capturing_mark_snapshot_delegations:
              #  print("byte string: ")
              #  print(value)
                if self.capturing_mark_snapshot_key==1:
                    self.snapshot_value_2=binascii.hexlify(value).decode('utf-8')
               #     print("keyvalue")
               #     print(self.snapshot_value_2)
                    self.capturing_mark_snapshot_key=2
                elif self.capturing_mark_snapshot_key==2:
                    self.snapshot_values['values'][self.snapshot_value_2]["dk"]=self.snapshot_value_1
                    self.snapshot_values['values'][self.snapshot_value_2]["dp"]=binascii.hexlify(value).decode('utf-8')
                #    print("pool")
                #    print(self.snapshot_values['values'][self.snapshot_value_2]["dp"])
                    self.capturing_mark_snapshot_key=0
                    self.mark_snapshot_values_counter-=1

            if self.capturing_mark_snapshot_pool_params:
                if (self.capturing_mark_snapshot_pool_params_waiting_for_next==hierarchy[4] and self.capturing_mark_snapshot_key==8) or (self.capturing_mark_snapshot_pool_params_waiting_for_next==1 and self.capturing_mark_snapshot_key==0):
                    self.pool_id=binascii.hexlify(value).decode('utf-8')
                    self.snapshot_values['pool_params'][self.pool_id]={}
                    self.snapshot_values['pool_params'][self.pool_id]["own"]=[]
                    self.capturing_mark_snapshot_key=1
                elif self.capturing_mark_snapshot_key==1:
                    self.capturing_mark_snapshot_key=2
                elif self.capturing_mark_snapshot_key==6:
                    self.snapshot_values['pool_params'][self.pool_id]["ra"]=binascii.hexlify(value).decode('utf-8')
                    self.capturing_mark_snapshot_key=7
                    self.capturing_mark_snapshot_pool_params_owner_addresses=True
                    self.mark_snapshot_values_counter-=1
                    self.capturing_mark_snapshot_owner_array_length=True
                elif self.capturing_mark_snapshot_key==7:
                    if self.capturing_mark_snapshot_owner_array_length_value>0:
                        self.snapshot_values['pool_params'][self.pool_id]["own"].append(binascii.hexlify(value).decode('utf-8'))
                        self.capturing_mark_snapshot_owner_array_length_value-=1
                        if self.capturing_mark_snapshot_owner_array_length_value==0:
                            self.capturing_mark_snapshot_pool_params_owner_addresses=False
                            self.capturing_mark_snapshot_key=8
                            self.capturing_mark_snapshot_pool_params_waiting_for_next=hierarchy[4]+1
                    else:
                        self.capturing_mark_snapshot_pool_params_owner_addresses=False
                        self.capturing_mark_snapshot_key=8
                        self.capturing_mark_snapshot_pool_params_waiting_for_next=hierarchy[4]+1
            
        elif major_type == 4:  # array
            if length_or_value == 31:
                # Indefinite length array
                i=0
                while True:
                    # Read the next item
                    byte = f.read(1)
                    if byte == b'\xff':  # break marker
                        break
                    else:
                        f.seek(-1, 1)
                    self.decode_item(f, hierarchy + [i+1], True)
                    i+=1
            else:
                if self.capturing_mark_snapshot_owner_array_length: #this works so long as owner array stays as a fixed length array
                    self.capturing_mark_snapshot_owner_array_length_value=length_or_value
                    self.capturing_mark_snapshot_owner_array_length=False
                for i in range(length_or_value):
                    self.decode_item(f, hierarchy + [i + 1], False)
        elif major_type == 6:  # semantic tag
            self.decode_item(f, hierarchy + [1], False)
        elif major_type == 7:  # floating point numbers and simple values
            if self.capturing_mark_snapshot_delegations:
                print("floating point: ")
                print(length_or_value)
            pass
        
        elif major_type == 5:  # map
            if length_or_value == 31:
                # Indefinite length map
                i=0
                while True:
                    # Read the next item
                    byte = f.read(1)
                    if byte == b'\xff':  # break marker
                        break
                    else:
                        f.seek(-1, 1)
                    self.decode_item(f, hierarchy + [i+1], True)
                    i+=1
            else:
                if self.capturing_mark_snapshot_values_count:
                    self.mark_snapshot_values_counter=length_or_value
                    self.capturing_mark_snapshot_values_count=False
                for i in range(length_or_value):
                    self.decode_item(f, hierarchy + [i + 1], False)  # Decode the key
                    self.decode_item(f, hierarchy + [i + 1], False)  # Decode the value
        elif major_type == 3:  # text string
            value=f.read(length_or_value)
            if self.capturing_mark_snapshot_delegations:
                print("text: ")
                print(value)
        else:
            raise ValueError('Unknown major type: ' + str(major_type))
        
        
        