using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using SimpleJSON;

public class MoCapRigidBody
{
	public int id;
	public Vector3 position;
	public Quaternion rotation;
	public GameObject gameObject;
	
	public delegate void UpdateHandler(MoCapRigidBody Rigidbody);
	public static event UpdateHandler OnUpdate;
	
	private List<GameObject> followerGameObjects;
	
	public MoCapRigidBody(int i, Vector3 p, Quaternion r)
	{
		id = i;
		position = p;
		rotation = r;
		gameObject = null;
		
		followerGameObjects = new List<GameObject> ();
	}
	
	public void AttachObject(GameObject go)
	{
		gameObject = go;
	}
	
	public void Update(Vector3 p, Quaternion r)
	{
		position = p;
		rotation = r;
		
		if (gameObject) {
			gameObject.transform.position = p;
			gameObject.transform.rotation = r;
		}
		
		foreach(GameObject o in followerGameObjects){
			o.transform.localPosition = p;
			o.transform.localRotation = r;
		}
		
		// trigger clalback event so users can hook into it
		//OnUpdate (this);
	}
	
	// convenience mehtod; every follower game object automatically
	// updates when this rigid body updates
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
	public static MoCapOscInterface instance;
	private Osc oscHandler;
	public string remoteIp;
	public int sendToPort;
	public int listenerPort;
	public GameObject prefab;
	private static List<OscMessage> oscMessageQueue;
	public List<MoCapRigidBody> rigidbodies;
	
	// events
	public delegate void NewRigidBodyHandler(MoCapRigidBody rigidbody);
	public static event NewRigidBodyHandler OnNewRigidBody;
	
	~MoCapOscInterface()
	{
		if (oscHandler != null)
		{
			oscHandler.Cancel();
		}
		
		// speed up finalization
		oscHandler = null;
		System.GC.Collect();
	}
	
	void Start()
	{
		UDPPacketIO udp = new UDPPacketIO (); //GetComponent<UDPPacketIO>();
		udp.init(remoteIp, sendToPort, listenerPort);
		
		oscHandler = new Osc (); //GetComponent<Osc>();
		oscHandler.init(udp);
		
		// oscHandler.SetAddressHandler("/rigidbody", onRigidBody);
		oscHandler.SetAllMessageHandler (onOscMessage);
	}
	
	void Update()
	{
		OscMessage m;
		int max = 100;
		int cnt = 0;
		
		// process all osc message in the message queue
		while (oscMessageQueue.Count > 0) {
			// pop oldest message
			m = oscMessageQueue [0];
			oscMessageQueue.RemoveAt(0);
			if(m != null){
				processOscMessage(m);
			}

			cnt++;
			if(cnt > max) break;
		}
	}
	
	void processOscMessage(OscMessage m){
		if (m.Address == "/rigidbody") {
			var rb = SimpleJSON.JSON.Parse (m.Values [0].ToString ());
			Vector3 position = new Vector3 (float.Parse (rb ["position"] [0]), float.Parse (rb ["position"] [1]), float.Parse (rb ["position"] [2]));
			Quaternion rotation = new Quaternion (float.Parse (rb ["orientation"] [0]), float.Parse (rb ["orientation"] [1]), float.Parse (rb ["orientation"] [2]), float.Parse (rb ["orientation"] [3]));
			int id = int.Parse (rb ["id"]);
			bool found = false;
			
			foreach (MoCapRigidBody current in rigidbodies) {
				if (current.id == id) {
					current.Update (position, rotation);
					found = true;
					break;
				}
			}
			
			if (!found) {
				MoCapRigidBody newBody = new MoCapRigidBody (id, position, rotation);
				rigidbodies.Add (newBody);
				if(prefab != null){
					newBody.AttachObject(Instantiate(prefab) as GameObject);
				}
				OnNewRigidBody(newBody);
			}
		}
	}
	
	void Awake()
	{
		if(instance == null)
		{
			instance = this;
		}
		else
		{
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
	
	private void onOscMessage(OscMessage m){
		// put all osc messages in a queue which is processed in the update function;
		// this function is called in a separate thread, it's safer better to process all messages in the main thread
		oscMessageQueue.Add (m);
	}
}
