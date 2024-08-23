import binascii
import os
import struct


class GenericCBORDecoder:

    def __init__(self, extraction_config):
        self.file_size = 0
        self.extraction_config = extraction_config
        self.extracted_data = {}
        self.context = {}
        self.current_key = None
        self.buffer = b""
        self.buffer_pos = 0
        self.chunk_size = 4096  # Adjust this as needed
        self.last_byte = None
        self.terminate = False

    def initialize_file_size(self, f):
        self.file_size = os.fstat(f.fileno()).st_size

    def get_extracted_data(self):
        return self.extracted_data

    def process_value(self, value, config, context):
        action = config.get('action', 'store')
        if action == "mark_completed":
            # iterate over all configs and set the completed flag to true through this exact config.
            for c in self.extraction_config:
                c['completed']=True
                if c == config:
                    break
        if action == "terminate":
            self.terminate = True

        context_key=config.get('context_key',None)

        if action == 'capture_simple_delegation_map' and context_key=='pool_id':
            self.extracted_data[config['key']][self.current_key]=value
            self.current_key = None

        elif action == 'capture_simple_delegation_map' and context_key=='stake_key':
            if config['key'] not in self.extracted_data:
                self.extracted_data[config['key']] = {}
            if value is not None:
                self.current_key = value

        if action == 'capture_snapshot_value' and context_key=='stake_key':
            if config['key'] not in self.extracted_data:
                self.extracted_data[config['key']] = {}
            if value is not None:
                if value not in self.extracted_data[config['key']]:
                    self.extracted_data[config['key']][value]={"vk":self.current_key}
                self.current_key = value
        elif action == 'capture_snapshot_value' and context_key=='value':
            if self.current_key not in self.extracted_data[config['key']]:
                self.extracted_data[config['key']][self.current_key]={}
            self.extracted_data[config['key']][self.current_key]['v']=value
        elif action == 'capture_snapshot_value' and context_key=='vk':
            #since this comes first, we don't have a key yet, so store the data in self.current_key and use when we get the key
            self.current_key = value

        if action == 'capture_snapshot_delegation' and context_key=='stake_key':
            if config['key'] not in self.extracted_data:
                self.extracted_data[config['key']] = {}
            if value is not None:
                if value not in self.extracted_data[config['key']]:
                    self.extracted_data[config['key']][value]={"dk":self.current_key}
                self.current_key = value
        elif action == 'capture_snapshot_delegation' and context_key=='pool_id':
            if self.current_key not in self.extracted_data[config['key']]:
                self.extracted_data[config['key']][self.current_key]={}
            self.extracted_data[config['key']][self.current_key]['v']=value
        elif action == 'capture_snapshot_delegation' and context_key=='dk':
            #since this comes first, we don't have a key yet, so store the data in self.current_key and use when we get the key
            self.current_key = value
            



        if action == 'capture_simple_map' and self.current_key is not None:
            self.extracted_data[config['key']][self.current_key]=value
            self.current_key = None

        elif action == 'capture_simple_map' and self.current_key==None:
            if config['key'] not in self.extracted_data:
                self.extracted_data[config['key']] = {}
            if value is not None:
                self.current_key = value
        elif action == 'capture_delegation_and_rewards_map':
            if 'delegation_and_rewards' not in self.extracted_data:
                self.extracted_data['delegation_and_rewards'] = {}
            if context_key=='stake_key':
                self.current_key = value
                self.extracted_data['delegation_and_rewards'][self.current_key]={}
            elif context_key=='rewards':
                self.extracted_data['delegation_and_rewards'][self.current_key]["rewards"]=value
            elif context_key=='delegation':
                self.extracted_data['delegation_and_rewards'][self.current_key]['delegation']=value
        elif action == 'store':
            self.extracted_data[config['key']] = value
        
        elif action == 'capture_pool_params_map' and context_key=='pool_id':
            if config['key'] not in self.extracted_data:
                self.extracted_data[config['key']] = {}
            self.current_key = value
            self.extracted_data[config['key']][self.current_key]={}
        elif action == 'capture_pool_params_map' and context_key!='pool_id':
            if 'type' in config and config['type']=='objectinarray':
                if context_key in self.extracted_data[config['key']][self.current_key]:
                    self.extracted_data[config['key']][self.current_key][context_key].append(value)
                else:
                    self.extracted_data[config['key']][self.current_key][context_key]=[value]
            else:
                self.extracted_data[config['key']][self.current_key][context_key]=value
        
        
        
        elif action == 'capture_utxo_set':
            if 'utxo_set' not in self.extracted_data:
                self.extracted_data['utxo_set'] = {}
            if context_key=='input':
                self.current_key= value
            elif context_key=='index':
                self.current_key = str(self.current_key)+"#"+str(value)
                self.extracted_data['utxo_set'][self.current_key]={"address":'',"lovelace":0,"policies":{},"datum":None,"referenceScript":None}
            elif context_key=='amount':
                self.extracted_data['utxo_set'][self.current_key]["lovelace"]=value
            elif context_key=='address':
                self.extracted_data['utxo_set'][self.current_key]["address"]=value
        elif action == 'utxo_stake_set':
            if 'utxo_stake_set' not in self.extracted_data:
                self.extracted_data['utxo_stake_set'] = {}
            if context_key=='address':
                if len(value)==114: # this is a full address pull the last 56 characters out for our stake key:
                    self.current_key = value[-56:]
                elif len(value)==58: # this is an enterprise address, ignore
                    self.current_key = value
                else:
                    pass
            elif context_key=='amount1':
                if value is not None:
                    if self.current_key not in self.extracted_data['utxo_stake_set']:
                        self.extracted_data['utxo_stake_set'][self.current_key]=0
                    self.extracted_data['utxo_stake_set'][self.current_key]+=value
            elif context_key=='amount2':
                if value is not None:
                    if self.current_key not in self.extracted_data['utxo_stake_set']:
                        self.extracted_data['utxo_stake_set'][self.current_key]=0
                    self.extracted_data['utxo_stake_set'][self.current_key]+=value
    
    def fill_buffer(self, f, chunk_size=4096):
        remaining = self.file_size - f.tell()
        #print(f"File position before fill: {f.tell()}")
        if remaining > 0:
            read_size = min(chunk_size, remaining)
            self.buffer = f.read(read_size)
            self.buffer_pos = 0
            #print(f"Filling buffer. Remaining: {remaining}, Read size: {read_size}") 


    def read_bytes(self, f, length=1):
        #print("before read", self.buffer_pos)
        bytes_collected = bytearray()
        while length > 0:
            if self.buffer_pos >= len(self.buffer):
                self.fill_buffer(f)
                if not self.buffer:  # Check if the buffer is still empty after attempting to fill
                    break
            bytes_to_read = min(length, len(self.buffer) - self.buffer_pos)
            bytes_collected.extend(self.buffer[self.buffer_pos:self.buffer_pos + bytes_to_read])
            self.last_byte = self.buffer[self.buffer_pos + bytes_to_read - 1:self.buffer_pos + bytes_to_read]
            self.buffer_pos += bytes_to_read
            length -= bytes_to_read
        #print("after read", self.buffer_pos)
        return bytes(bytes_collected)

    def seek_back(self, steps=1):
        #print("before seek", self.buffer_pos)
        if steps == 1 and self.last_byte is not None:
            if self.buffer_pos > 0:
                self.buffer_pos -= 1
            else:
                # Insert the last byte at the start of the buffer if at the buffer's beginning
                self.buffer = self.last_byte + self.buffer
                self.buffer_pos = 0
            #print("after seek", self.buffer_pos)
    
    def decode_item(self, f, hierarchy=[], top_level=True):
        if  self.terminate:
            return
        value = None
        
        read_byte = self.read_bytes(f,1)
        
        if not read_byte:
            return

        initial_byte = ord(read_byte)
        major_type = initial_byte >> 5
        length_or_value = initial_byte & 0x1F
        indefinite = False
        if major_type == 4 and length_or_value == 31:
            indefinite = True
        elif major_type == 5 and length_or_value == 31:
            indefinite = True
        else:
            if length_or_value > 23:
                if length_or_value == 24:
                    length_or_value = ord(self.read_bytes(f,1))
                elif length_or_value == 25:
                    if major_type == 7:
                        value = self.read_bytes(f,2)
                        length_or_value = struct.unpack('>e', value)[0]
                    else:
                        length_or_value = int.from_bytes(self.read_bytes(f,2), 'big')
                elif length_or_value == 26:
                    if major_type == 7:
                        value = self.read_bytes(f,4)
                        length_or_value = struct.unpack('>f', value)[0]
                    else:
                        length_or_value = int.from_bytes(self.read_bytes(f,4), 'big')
                elif length_or_value == 27:
                    if major_type == 7:
                        value = self.read_bytes(f,8)
                        length_or_value = struct.unpack('>d', value)[0]
                    else:
                        length_or_value = int.from_bytes(self.read_bytes(f,8), 'big')

        
        if major_type in [0, 1]:
            value = length_or_value
            
        elif major_type == 2:
            # if f.tell() + length_or_value > self.file_size:
            #     raise EOFError('Byte string extends beyond end of file:' + str(length_or_value) + ' bytes at position ' + str(f.tell()) + ' of ' + str(self.file_size))
            value = binascii.hexlify(self.read_bytes(f,length_or_value)).decode('utf-8')
            
        elif major_type == 4:
            if indefinite:
                i = 0
                while True:
                    byte = self.read_bytes(f,1)
                    if not byte or byte == b'\xff' or byte == b'0xf6':# and f.tell() == self.file_size:
                        break
                    else:
                        self.seek_back()
                        #self.read_bytes(f,-1)
                    self.decode_item(f, hierarchy + [i + 1], True)
                    i += 1
            else:
                for i in range(length_or_value):
                    self.decode_item(f, hierarchy + [i + 1], False)
        elif major_type == 5:
            if indefinite:
                i = 0
                while True:
                    byte = self.read_bytes(f,1)
                    #print("byte read: ", byte)
                    if not byte or byte == b'\xff':
                        break
                    else:
                        self.seek_back()
                        #self.read_bytes(f,-1)
                    #print(hierarchy)
                    self.decode_item(f, hierarchy + [i + 1] + [1], True)
                    self.decode_item(f, hierarchy + [i + 1] + [2], True)
                    i += 1
            else:
                for i in range(length_or_value):
                    self.decode_item(f, hierarchy + [i + 1] + [1], False)
                    self.decode_item(f, hierarchy + [i + 1] + [2], False)
        elif major_type == 6:
            self.decode_item(f, hierarchy + [1], False)
        elif major_type == 7:
            if length_or_value == 20 or length_or_value == 0:
                value = False
            elif length_or_value == 21 or length_or_value == 1:
                value = True
            elif length_or_value == 22 or length_or_value == 2:
                value = None
            
        elif major_type == 3:
            value = self.read_bytes(f,length_or_value).decode('utf-8')
           
        else:
            raise ValueError('Unknown major type: ' + str(major_type))
        
       
        hierarchy_len = len(hierarchy)
        # iterate over configs where completed=false
        for config in self.extraction_config:
            if 'completed' in config and config['completed']==True:
                continue
            config_path_len = len(config['path'])
            if hierarchy_len == config_path_len:
                if all(h == p or p == '*' for h, p in zip(hierarchy, config['path'])):
                    self.process_value(value, config, self.context)
                    break  
