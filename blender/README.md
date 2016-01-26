# MoCap Blender

To use MoCap in your blender project, copy all the contents of the blender/addons folder in this repository to the blender addons folder on your computer.

Location blender addons folder on a mac (for blender version 2.75):
`/Users/<username>/Library/Application Support/Blender/2.75/scripts/addons`

This will add the following python logic to your blender:


* MoCapSpawner addon
* MoCapOSC addon
* MoCapJSON addon
* mocap_bridge python package - required by all the MoCap* addons
* pythonosc package - extracted from the python-osc package, required by the MoCapOSC addon

Each of the addons has to be enabled File > User Preferences > Add-ons


### MoCapOSC blender addon

This addon receives and processes incoming OSC data (for example from an indepenedently running mocap_bridge python instance).

To use it;

* make sure the addon is enabled
* create an object in your scene
  * doesn't matter what kind of object, you'll probably want to use an 'empty' object
* enable MoCap OSC in the object panel
* configure MoCap OSC with a host (ip-address) and port for the incoming OSC data
* create a python game-logic controller for the object
* set the controller's script type (or mode) to 'module' (not 'script')
* set the controller's value to `MoCapOSC.update`
* hook the controller up to an 'Always sensor' with TRUE level triggering enabled


### MoCapJSON blender addon

This addon reads and processes mocap data from a local json file (which can be recorded using the mocap_bridge python package).

To use it;

* make sure the addon is enabled
* create an object in your scene
  * doesn't matter what kind of object, you'll probably want to use an 'empty' object
* enable MoCap JSON in the object panel
* configure MoCap JSON with a file path
* create a python game-logic controller for the object
* set the controller's script type (or mode) to 'module' (not 'script')
* set the controller's value to `MoCapJSON.update`
* hook the controller up to an 'Always sensor' with TRUE level triggering enabled


### MoCapSpawner blender addon

This will spawn an object for every rigid body (note you will still need on of the other addons to actually receive MoCap data).

To use it;

* make sure the addon is enabled
* create the template object that you want want to be spawned for every rigid body
	* you gotta make sure this object is on a layer that is inactive when you start the game engine, blender doesn't let you instantiate objects that are on a visible layer
* create an object that has either MoCapOSC or MoCapJSON enabled
  * all the spawned objects are created as a child of this object so their positions and orientations will be relative to this object's position and orientation
* enable MoCap Spawner in the object panel
* specify the name of the template object from step 2
* create a python game-logic controller for the object
* set the controller's script type (or mode) to 'module' (not 'script')
* set the controller's value to `MoCapSpawner.create`
* hook the controller up to an 'Always sensor' with both TRUE level triggering and FALSE level triggering disabled (no pulse mode)
* start the game engine (Game > Start Game Engine)




