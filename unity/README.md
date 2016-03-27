# MoCap Unity

To use MoCap in your Unity project, you need to have the python MoCap bridge running independently to forward the Motive MoCap data as OSC messages.

## Stream realtime data

Make sure the python MoCap Bridge is running and forwarding the NatNet data over OSC to:  

 * host: 127.0.0.1
 * port: 8080
 
See the [python README](https://github.com/davidjonas/MoCap/blob/master/python/README.md) for more instructions.

## A simple project that receives MoCap OSC data

 * Import all assets from the MoCap-OSC.unitypackage in the Unity folder into your project
 * Create and empty game object
 * Add the MoCapOscInterface script as component to the empty game object
   * The default MoCapOscInterface settings should work, but make sure the IP and port properties match with the Mocap Bridge configuration
   * If the python MoCap Bridge and unity are running on the same machine both _must_ use the 127.0.0.1 IP-address
 * Create a 3D game object asset to visualise the rigid bodies (we don't need it in the scene, just as an asset)
 * Point the MoCapOscInterface's 'Rigid Body Object' property to the 3D game object asset
 * Run the application; you should now see an instance of the 3D object for every rigid body

