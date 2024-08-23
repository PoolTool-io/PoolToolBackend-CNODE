extraction_config_91babbage = [ # node 9.1 babbage era mark snapshot, blocks and epoch parameters
      
  
        # Configurations for capturing key-value pairs for complex structures like pool blocks and snapshot values
        {"path": [2 ,'*',1], "key": "pool_blocks", "action": "capture_simple_map", "context_key": "capturing_pool_blocks"},
        {"path": [2 ,'*',2], "key": "pool_blocks", "action": "capture_simple_map", "context_key": "capturing_pool_blocks"},

          # # Basic value extraction
        {"path": [4, 1, 1], "key": "treasury", "action": "store"},
        {"path": [4, 1, 2], "key": "reserves", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 1], "key": "txFeeFixed", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 2], "key": "txFeePerByte", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 3], "key": "maxBlockSize", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 4], "key": "maxTxSize", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 5], "key": "maxBhSize", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 6], "key": "stakeAddressDeposit", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 7], "key": "stakePoolDeposit", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 8], "key": "maxEpoch", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 9], "key": "optimalPoolCount", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 10, 1, 1], "key": "influence", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 10, 1, 2], "key": "influence_divisor", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 11, 1, 1], "key": "monetaryExpandRate", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 11, 1, 2], "key": "monetaryExpandRate_divisor", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 12, 1, 1], "key": "treasuryGrowthRate", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 12, 1, 2], "key": "treasuryGrowthRate_divisor", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 13], "key": "protocolMajor", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 14], "key": "protocolMinor", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 15], "key": "minPoolCost", "action": "store"},
        {"path": [4, 2, 2, 4, 3, 16], "key": "", "action": "mark_completed"},

        {"path": [4, 3, 1, 1, '*',1,1], "key": "snapshot_values", "action": "capture_snapshot_value", "context_key": "vk"},
        {"path": [4, 3, 1, 1, '*',1,2], "key": "snapshot_values", "action": "capture_snapshot_value", "context_key": "stake_key"},
        {"path": [4, 3, 1, 1, '*',2], "key": "snapshot_values", "action": "capture_snapshot_value", "context_key": "value"},  

        {"path": [4, 3, 1, 2, '*', 1,1], "key": "snapshot_delegations", "action": "capture_snapshot_delegation", "context_key": "dk"},
        {"path": [4, 3, 1, 2, '*', 1,2], "key": "snapshot_delegations", "action": "capture_snapshot_delegation", "context_key": "stake_key"},
        {"path": [4, 3, 1, 2, '*', 2], "key": "snapshot_delegations", "action": "capture_snapshot_delegation", "context_key": "pool_id"},
        {"path": [4, 3, 1, 3], "key": "", "action": "mark_completed"},

        {"path": [4, 3, 1, 3, '*', 1], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "pool_id"},
        {"path": [4, 3, 1, 3, '*', 2,1], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "pool_id_again"},
        {"path": [4, 3, 1, 3, '*', 2,2], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "unknownvalue"},
        {"path": [4, 3, 1, 3, '*', 2,3], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "pledge"},
        {"path": [4, 3, 1, 3, '*', 2,4], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "cost"},
        {"path": [4, 3, 1, 3, '*', 2,5,1,1], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "margin_num"},
        {"path": [4, 3, 1, 3, '*', 2,5,1,2], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "margin_den"},
        {"path": [4, 3, 1, 3, '*', 2,6], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "reward_address"},
        {"path": [4, 3, 1, 3, '*', 2,7,'*'], "key": "snapshot_poolparams", "type": "objectinarray","action": "capture_pool_params_map", "context_key": "owner_addresss"},
        {"path": [4, 3, 1, 3, '*', 2,8,'*',1 ], "key": "snapshot_poolparams", "type": "objectinarray","action": "capture_pool_params_map", "context_key": "relay_address_valency"},
        {"path": [4, 3, 1, 3, '*', 2,8,'*',2 ], "key": "snapshot_poolparams", "type": "objectinarray", "action": "capture_pool_params_map", "context_key": "relay_address_port"},
        {"path": [4, 3, 1, 3, '*', 2,8,'*',3 ], "key": "snapshot_poolparams", "type": "objectinarray", "action": "capture_pool_params_map", "context_key": "relay_address"},
        {"path": [4, 3, 1, 3, '*', 2,9 ], "key": "snapshot_poolparams", "action": "end_capture_pool_params_map", "context_key": ""},
        {"path": [4, 3, 2], "key": "", "action": "mark_completed"},
        {"path": [4, 3, 4], "key": "epoch_fees", "action": "store"},
        {"path": [4, 4, 2], "key": "reward_pot", "action": "store"},
        {"path": [4, 4, 3], "key": "", "action": "terminate"},
        ]

extraction_config_91conway = [ # node 9.1 conway era
        # # Basic value extraction
        {"path": [4, 1, 1], "key": "treasury", "action": "store"},
        {"path": [4, 1, 2], "key": "reserves", "action": "store"},
        {"path": [4, 3, 4], "key": "epoch_fees", "action": "store"},
        {"path": [5, 1, 2, 5, 2], "key": "reward_pot", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 1], "key": "txFeeFixed", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 2], "key": "txFeePerByte", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 3], "key": "maxBlockSize", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 4], "key": "maxTxSize", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 5], "key": "maxBhSize", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 6], "key": "stakeAddressDeposit", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 7], "key": "stakePoolDeposit", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 8], "key": "maxEpoch", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 9], "key": "optimalPoolCount", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 10, 1, 1], "key": "influence", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 10, 1, 2], "key": "influence_divisor", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 11, 1, 1], "key": "monetaryExpandRate", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 11, 1, 2], "key": "monetaryExpandRate_divisor", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 12, 1, 1], "key": "treasuryGrowthRate", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 12, 1, 2], "key": "treasuryGrowthRate_divisor", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 13, 1], "key": "protocolMajor", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 13, 2], "key": "protocolMinor", "action": "store"},
        {"path": [4, 2, 2, 4, 4, 14], "key": "minPoolCost", "action": "store"},

  
        # Configurations for capturing key-value pairs for complex structures like pool blocks and snapshot values
        {"path": [2 ,'*',1], "key": "pool_blocks", "action": "capture_simple_map", "context_key": "capturing_pool_blocks"},
        {"path": [2 ,'*',2], "key": "pool_blocks", "action": "capture_simple_map", "context_key": "capturing_pool_blocks"},
        {"path": [3], "key": "pool_blocks", "action": "end_capture_map", "context_key": "capturing_pool_blocks"},
        {"path": [4, 3, 1, 1, '*', 1, 2 ], "key": "snapshot_values", "action": "capture_simple_map", "context_key": "capturing_mark_snapshot_values"},
        {"path": [4, 3, 1, 1, '*', 2 ], "key": "snapshot_values", "action": "capture_simple_map", "context_key": "capturing_mark_snapshot_values"},
        {"path": [4, 3, 1, 2], "key": "snapshot_values", "action": "end_capture_map", "context_key": "capturing_mark_snapshot_values"},
        {"path": [4, 3, 1, 2, '*', 1,2], "key": "snapshot_delegations", "action": "capture_simple_map", "context_key": "capturing_mark_snapshot_delegations"},
        {"path": [4, 3, 1, 2, '*', 2], "key": "snapshot_delegations", "action": "capture_simple_map", "context_key": "capturing_mark_snapshot_delegations"},
        {"path": [4, 3, 1, 3], "key": "snapshot_delegations", "action": "end_capture_map", "context_key": "capturing_mark_snapshot_delegations"},
        {"path": [4, 3, 1, 3, '*', 1], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": ""},
        {"path": [4, 3, 1, 3, '*', 2,1], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "reward_address_maybe"},
        {"path": [4, 3, 1, 3, '*', 2,2], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "unknownvalue"},
        {"path": [4, 3, 1, 3, '*', 2,3], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "pledge"},
        {"path": [4, 3, 1, 3, '*', 2,4], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "cost"},
        {"path": [4, 3, 1, 3, '*', 2,5,1,1], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "margin_num"},
        {"path": [4, 3, 1, 3, '*', 2,5,1,2], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "margin_den"},
        {"path": [4, 3, 1, 3, '*', 2,6], "key": "snapshot_poolparams", "action": "capture_pool_params_map", "context_key": "reward_address_maybe2"},
        {"path": [4, 3, 1, 3, '*', 2,7,'*',1], "key": "snapshot_poolparams", "type": "objectinarray","action": "capture_pool_params_map", "context_key": "owner_addresss"},
        {"path": [4, 3, 1, 3, '*', 2,8,'*',1 ], "key": "snapshot_poolparams", "type": "objectinarray","action": "capture_pool_params_map", "context_key": "relay_address_valency"},
        {"path": [4, 3, 1, 3, '*', 2,8,'*',2 ], "key": "snapshot_poolparams", "type": "objectinarray", "action": "capture_pool_params_map", "context_key": "relay_address_port"},
        {"path": [4, 3, 1, 3, '*', 2,8,'*',3 ], "key": "snapshot_poolparams", "type": "objectinarray", "action": "capture_pool_params_map", "context_key": "relay_address"},
        {"path": [4, 3, 1, 3, '*', 2,9 ], "key": "snapshot_poolparams", "action": "end_capture_pool_params_map", "context_key": ""},
        ]
extraction_config_91conway_autosaved_ledger = [ # node 9.1 conway era ledger save from node
        # {"path": [2,1,7,2,2,2,4,2,2,1,'*',1,1], "key": "utxo_set", "action": "capture_utxo_set","context_key": "input"},
        # {"path": [2,1,7,2,2,2,4,2,2,1,'*',1,2], "key": "utxo_set", "action": "capture_utxo_set","context_key": "index"},
        # {"path": [2,1,7,2,2,2,4,2,2,1,'*',2,1], "key": "utxo_set", "action": "capture_utxo_set","context_key": "address"},
        # {"path": [2,1,7,2,2,2,4,2,2,1,'*',2,2], "key": "utxo_set", "action": "capture_utxo_set","context_key": "amount"},
        {"path": [2,1,7,2,2,2,4,2,2,2], "key": "utxo_set", "action": "end_capture_utxo_set","context_key": ""},
        ]
extraction_config_91babbage_autosaved_ledger = [ # node 9.1 shelley era ledger save from node

        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',1], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "pool_id"},
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,1], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "pool_id_again"},
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,2], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "vrf"},
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,3], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "pledge"},
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,4], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "cost"},
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,5,1,1], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "margin_num"},
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,5,1,2], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "margin_den"},
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,6], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "reward_address"}, # with e1 at start
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,7,'*',1], "key": "live_poolparams", "type": "objectinarray","action": "capture_pool_params_map", "context_key": "owner_addresss"}, # with no e1
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,8,'*',1 ], "key": "live_poolparams", "type": "objectinarray","action": "capture_pool_params_map", "context_key": "relay_address_valency"},
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,8,'*',2 ], "key": "live_poolparams", "type": "objectinarray", "action": "capture_pool_params_map", "context_key": "relay_address_port"},
        {"path": [2,1,6,2,2,2,4,2,1,2,1,'*',2,8,'*',3 ], "key": "live_poolparams", "type": "objectinarray", "action": "capture_pool_params_map", "context_key": "relay_address"},
        {"path": [2,1,6,2,2,2,4,2,1,3,1,1,'*',1,2], "key": "delegations", "action": "capture_simple_delegation_map","context_key": "stake_key"},
        {"path": [2,1,6,2,2,2,4,2,1,3,1,1,'*',2,3,1],"key": "delegations", "action": "capture_simple_delegation_map","context_key": "pool_id"},
        {"path": [2,1,6,2,2,2,4,2,2,1,'*',2,1], "key": "utxo_set", "action": "utxo_stake_set","context_key": "address"},
        {"path": [2,1,6,2,2,2,4,2,2,1,'*',2,2], "key": "utxo_set", "action": "utxo_stake_set","context_key": "amount1"},
        {"path": [2,1,6,2,2,2,4,2,2,1,'*',2,2,1], "key": "utxo_set", "action": "utxo_stake_set","context_key": "amount2"}, # if the utxo has other policies then it will be an array in the first element.
        {"path": [2,1,6,2,2,2,5,1,2,3,'*',1,2], "key": "reward_accounts", "action": "capture_delegation_and_rewards_map","context_key": "stake_key"},
        {"path": [2,1,6,2,2,2,5,1,2,3,'*',2,1,2], "key": "reward_accounts", "action": "capture_delegation_and_rewards_map","context_key": "delegation"},
        {"path": [2,1,6,2,2,2,5,1,2,3,'*',2,1,3], "key": "reward_accounts", "action": "capture_delegation_and_rewards_map","context_key": "rewards"},
        
        ]

extraction_config_91babbage_utxo_set = [ # node 9.1 babbage utxo set
           {"path": [4,2,1,2,1,'*',1], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "pool_id"},
        {"path": [4,2,1,2,1,'*',2,1], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "pool_id_again"},
        {"path": [4,2,1,2,1,'*',2,2], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "vrf"},
        {"path": [4,2,1,2,1,'*',2,3], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "pledge"},
        {"path": [4,2,1,2,1,'*',2,4], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "cost"},
        {"path": [4,2,1,2,1,'*',2,5,1,1], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "margin_num"},
        {"path": [4,2,1,2,1,'*',2,5,1,2], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "margin_den"},
        {"path": [4,2,1,2,1,'*',2,6], "key": "live_poolparams", "action": "capture_pool_params_map", "context_key": "reward_address"}, # with e1 at start
        {"path": [4,2,1,2,1,'*',2,7,'*',1], "key": "live_poolparams", "type": "objectinarray","action": "capture_pool_params_map", "context_key": "owner_addresss"}, # with no e1
        {"path": [4,2,1,2,1,'*',2,8,'*',1 ], "key": "live_poolparams", "type": "objectinarray","action": "capture_pool_params_map", "context_key": "relay_address_valency"},
        {"path": [4,2,1,2,1,'*',2,8,'*',2 ], "key": "live_poolparams", "type": "objectinarray", "action": "capture_pool_params_map", "context_key": "relay_address_port"},
        {"path": [4,2,1,2,1,'*',2,8,'*',3 ], "key": "live_poolparams", "type": "objectinarray", "action": "capture_pool_params_map", "context_key": "relay_address"},
       
        {"path": [4,2,2,1,'*',2,1], "key": "utxo_set", "action": "utxo_stake_set","context_key": "address"},
        {"path": [4,2,2,1,'*',2,2], "key": "utxo_set", "action": "utxo_stake_set","context_key": "amount1"},
        {"path": [4,2,2,1,'*',2,2,1], "key": "utxo_set", "action": "utxo_stake_set","context_key": "amount2"}, # if the utxo has other policies then it will be an array in the first element.
        {"path": [4,2,1,3,1,1,'*',1,2], "key": "reward_accounts", "action": "capture_delegation_and_rewards_map","context_key": "stake_key"},
        {"path": [4,2,1,3,1,1,'*',2,1,1,1], "key": "reward_accounts", "action": "capture_delegation_and_rewards_map","context_key": "rewards"},
        {"path": [4,2,1,3,1,1,'*',2,3,1], "key": "reward_accounts", "action": "capture_delegation_and_rewards_map","context_key": "delegation"},
]