from config import *
import time
from pt_utils import *
from fb_utils import *
fb=fb_utils()

recent_block=fb.getKey(baseNetwork+"/recent_block")

if recent_block is None or 'block' not in recent_block:
    print("wtf, could not find last verified block.  exiting")
    time.sleep(30)
    exit()
cursortext = f"{recent_block['cslot']},{recent_block['hash']}"
command = f"/usr/local/bin/oura daemon --config /home/ubuntu/PoolToolBackend-CNODE/oura_daemon.toml --cursor {cursortext}"
print(command)
print("starting Oura")
te = runcli(command)
if te is not None:
    print(f"oura started successfully")
else:
    print(f"oura failed")

print("wait 30 seconds before allowing systemctl to restart")
time.sleep(30)
