from natnet_pipeline import NatNetPipeline
from default_readers import JSONNatNetReader
from default_writers import OSCNatNetWriter
import sys

pipeline = NatNetPipeline(JSONNatNetReader(sys.argv[1]), OSCNatNetWriter())
#pipeline = NatNetPipeline(JSONNatNetReader("data/sampleRecording3.json"), OSCNatNetWriter())

pipeline.start()

while True:
    try:
        pass
    except:
        pipeline.stop()
        break
