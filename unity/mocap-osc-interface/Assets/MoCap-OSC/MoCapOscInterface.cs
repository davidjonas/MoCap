using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using SimpleJSON;

public class MoCapRigidBody
{
	// properties
	public int id;
	public Vector3 position;
	public Quaternion rotation;

	// utility (should maybe be refactored out of this class?
	private List<GameObject> followerGameObjects;
	
	// Constructor
	public MoCapRigidBody(int i, Vector3 p, Quaternion r)
	{
		id = i;
		position = p;
		rotation = r;
		followerGameObjects = new List<GameObject> ();
	}
	
	public void Update(Vector3 p, Quaternion r)
	{
		position = p;
		rotation = r;

		foreach(GameObject o in followerGameObjects){
			o.transform.localPosition = p;
			o.transform.localRotation = r;
		}
	}

	// the following functions make it easy for GameObjects to follow
	// rigid bodies (adopt position and rotation) 
	public void addFollower(GameObject obj){
		followerGameObjects.Add(obj);
	}

	public void removeFollower(GameObject obj){
		followerGameObjects.Remove (obj);
	}
}

// Simple OSC test communication script
[AddComponentMenu("Scripts/MoCapOscInterface")]
public class MoCapOscInterface : MonoBehaviour
{
	// this will (almost) always be a singleton class
	public static MoCapOscInterface instance;
	public string oscSenderIp;
	private int sendToPort=0; // not used, this class only receives data
	public int listenerPort;
	public GameObject rigidBodyObject;

	private Osc oscHandler;
	private static List<OscMessage> oscMessageQueue;
	private static int oscMaxMessagesPerFrame = 100; // the max. number of messages to process in one frame

	public List<MoCapRigidBody> rigidbodies; // this list will hold our intrnal representation of the mocap rigid bodies

	// events
	public delegate void NewRigidBodyHandler(MoCapRigidBody rigidbody);
	public static event NewRigidBodyHandler OnNewRigidBody;

	public delegate void UpdateRigidBodyHandler(MoCapRigidBody rigidbody);
	public static event UpdateRigidBodyHandler OnRigidBodyUpdate;


	// Destructor
	~MoCapOscInterface(){
		if (oscHandler != null){
			oscHandler.Cancel();
			oscHandler = null;
		}
		
		// speed up finalization
		System.GC.Collect();
	}

	void Awake()
	{
		// Singleton stuff
		if(instance == null){
			instance = this;
		} else {
			Debug.LogError("MoCapOscInterface is a singleton class; only one game object is allowed to have this component");
			Destroy (gameObject);
		}

		rigidbodies = new List<MoCapRigidBody>();
		oscMessageQueue = new List<OscMessage> ();
	}

	void OnDisable()
	{
		// close OSC UDP socket
		Debug.Log("closing OSC UDP socket in OnDisable");
		oscHandler.Cancel();
		oscHandler = null;
	}

	void Start()
	{
		// initialize udp and osc stuff (both necessary for OSC network communication)
		UDPPacketIO udp = new UDPPacketIO ();
		udp.init(oscSenderIp, sendToPort, listenerPort);

		oscHandler = new Osc ();
		oscHandler.init(udp);

		// oscHandler.SetAddressHandler("/rigidbody", onRigidBody);
		oscHandler.SetAllMessageHandler (onOscMessage);

		// the rigidBodyObject attribute shouldn't logically be part of this class, but is added as
		// a convenience property to quick and easily visualize the mocap rigid bodies by just specifieing
		// an object to visually represent the rigid bodies. We'll outsource all the logic to the
		// MoCapRigidBodiesCloner class whose tasks is exactly this.
		if (rigidBodyObject) {
			// create a GameObject to hold all the rigid bodies
			GameObject go = new GameObject();
			go.name = "GeneratedRigidBodies";
			// add the cloner component
			MoCapRigidBodiesCloner cloner = go.AddComponent<MoCapRigidBodiesCloner>();
			// give it the specified object and let it take care of the rest
			cloner.rigidBodyObject = rigidBodyObject;
		}
	}

	void Update()
	{
		OscMessage m;
		int messageCount = 0;
		
		// process all osc message in the message queue
		// we're using this queue mechanism instead of processing message
		// directly when they come in, because they come in through a handler function
		// in a separate thread which cause all kinds of issues
		while (oscMessageQueue.Count > 0) {
			// pop oldest (first) message
			m = oscMessageQueue [0];
			oscMessageQueue.RemoveAt(0);

			// process message
			if(m != null){
				processOscMessage(m);
			}

			// keep track of the number of message we've processed this frame
			messageCount++;
			// if we've processed he maximum amount; break out of the while loop
			if(messageCount > oscMaxMessagesPerFrame) break;
		}
	}

	void processOscMessage(OscMessage m){
		// process rigid body message
		if (m.Address == "/rigidbody") {
			// parse json data to object data
			var rb = SimpleJSON.JSON.Parse (m.Values [0].ToString ());
			Vector3 position = new Vector3 (float.Parse (rb ["position"] [0]), float.Parse (rb ["position"] [1]), float.Parse (rb ["position"] [2]));
			Quaternion rotation = new Quaternion (float.Parse (rb ["orientation"] [0]), float.Parse (rb ["orientation"] [1]), float.Parse (rb ["orientation"] [2]), float.Parse (rb ["orientation"] [3]));
			int id = int.Parse (rb ["id"]);

			// find in-memory represnetation of the given rigid body (match by id)
			foreach (MoCapRigidBody current in rigidbodies) {
				if (current.id == id) {
					current.Update (position, rotation); // update our in-memory representation of the rigid body
					// the line below is ERROR-ing, not sure why...
					// OnRigidBodyUpdate(current); // trigger any registered update handlers
					return; // we're done
				}
			}

			// if we reach this point, this means no existing rigid body instance could be found
			// let's create one
			MoCapRigidBody newBody = new MoCapRigidBody (id, position, rotation);
			rigidbodies.Add (newBody);
			OnNewRigidBody(newBody); // let everybody know we've got a new rigid body
		}
	}

	private void onOscMessage(OscMessage m){
		// put all osc messages in a queue which is processed in the update function;
		// this function is called in a separate thread, it's safer better to process all messages in the main thread
		oscMessageQueue.Add (m);
	}
}
