from natnet_pipeline import NatNetPipeline
from default_readers import *
from default_writers import OSCNatNetWriter
import sys

def t():
    rb = pipeline.reader.getAllRigidbodies()
    for r in rb:
        print rb[r].position

def s():
    sk = pipeline.reader.skeletons
    for skeleton in sk:
        print sk[skeleton].id

#pipeline = NatNetPipeline(JSONNatNetReader(sys.argv[1]), OSCNatNetWriter())
#pipeline = NatNetPipeline(LiveNatnetReader("0.0.0.0", "239.255.42.99", "1511"), OSCNatNetWriter(host="192.168.1.3",port=8080))
pipeline = NatNetPipeline(LiveNatnetReader("0.0.0.0", "239.255.42.99", "1511"), OSCNatNetWriter(port=8080))

pipeline.start()

#pipeline.reader.onUpdate += t

while True:
    try:
        pass
    except:
        pipeline.stop()
        break
