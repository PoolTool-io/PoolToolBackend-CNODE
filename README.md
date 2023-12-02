# PoolToolBackend
PoolTool Backend Processing Toolset (python)

## Overall architecture
Pooltool is currently operating across two different servers.
CNODE SERVER:  Has cardano node, ogmios and txpipe oura system.   The focus is on following the chain, parsing ledger state dumps, and sending all data to the database server for processing.
DATABASE SERVER:  Has a postgres database and all remaining processing for pooltool.  In addition, due to legacy code, we use a sqlite database with the telegram bot on this server.

## Databases
We use a postgres database on the DATABASE SERVER to maintain high speed data access.  In addition we use a firebase instance to maintain live data for the website and the pooltool mobile app.  Finally we store static information on aws s3 as much as possible to minimize cost and keep it out of the expensive postgres database system.

## CNODE SERVER:

### Primary Files
- oura-Configured with oura_daemon.toml - This Oura chain sync client will follow the node 6 blocks back from the tip.  This allows for rollbacks to not be processed by the system.  A rollback of over 6 blocks will cause problems for pooltool.
- oura-Configured with oura_justthetipe.toml - This Oura chain sync client follows the node at the bleeding edge.  This allows us to process new accounts or password recovery transactions expediously.
- cnode_epoch_processing.py - Monitors the state of the local cardano node and launches some processes when the epoch switches over.  Specifically:
  1) Query and decode ledger state for necessary data and send to the CNODE SERVER.
  2) update the price of ADA at the epoch boundary
- periodicProcessesCnodeServer.py - queries ogmios for the daedalus pool ranking every hour.

### Utility and Helper Files
- pt_utils.py - misc utility pooltool and crypto functions
- nomemdecoder_util.py - incrementally decode cbor ledger state without loading it into memory.  Designed and updated for each version of ledger state as new node versions (and thus ledger state) are released.
- fb_utils.py - misc utilty functions for interacting with the firebase database
- aws_utils.py - misc utility functions for interacting with AWS (mostly s3)
- autostart_oura.py - service executable that will monitor oura and restart if necessary with the correct cursor based on saved database processing markers
- outostart_oura_justthetip.py - service executable that will monitor oura and restart if necessary with the correct cursor based on saved database processing markers