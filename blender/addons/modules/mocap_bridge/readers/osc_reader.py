from mocap_bridge.utils.color_terminal import ColorTerminal

loaded = False
try:
    # first try pyOSC implementation (works with python 2.7)
    from mocap_bridge.readers._osc_reader_pyosc import OscReader
    loaded = True
except ImportError:
    loaded = False

if not loaded:
    ColorTerminal().warn("Couldn't load pyOSC, trying python-osc implementation")
    # this should work for python 3.*
    try:
        from mocap_bridge.readers._osc_reader_pythonosc import OscReader
        loaded = True
    except ImportError:
        loaded = False

if not loaded:
    ColorTerminal().warn("Couldn't load python-osc implementation, can't load OscReader")
