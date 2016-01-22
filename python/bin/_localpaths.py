# Add project path to system's python path,
# so we can find and import the mocap_bridge package
import os, sys

thisdir = os.path.dirname(__file__)
projectdir = os.path.abspath(os.path.join(thisdir, '..'))
# packagedir = os.path.abspath(os.path.join(thisdir, '../mocap_bridge'))

if projectdir not in sys.path:
  sys.path.insert(0, projectdir)
