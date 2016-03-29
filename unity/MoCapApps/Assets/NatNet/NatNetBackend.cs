using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using SimpleJSON;
using System;


[Serializable]
public class NatNetRigidbody
{
	public int id;
	public string name;
	public Vector3 position;
	public Quaternion rotation;
	
	public NatNetRigidbody(int i, Vector3 p, Quaternion r)
	{
		id = i;
		name = "unnamed";
		position = p;
		rotation = r;
	}

	public NatNetRigidbody(int i, Vector3 p, Quaternion r, string n)
	{
		id = i;
		name = n;
		position = p;
		rotation = r;
	}
	
	public void Update(Vector3 p, Quaternion r)
	{
		position = p;
		rotation = r;
	}
}

[Serializable]
class PositionUpdate
{
	public NatNetRigidbody rigidbody;
	public Vector3 position;
	public Quaternion rotation;
	public float frameTime;

	public PositionUpdate(NatNetRigidbody rb, Vector3 p, Quaternion r)
	{
		rigidbody = rb;
		position = p;
		rotation = r;
		frameTime = Time.time;
	}
}


[RequireComponent (typeof (UDPPacketIO), typeof (Osc))]
public class NatNetBackend : MonoBehaviour {

	public static NatNetBackend natnet;
	public List<NatNetRigidbody> rigidbodies;
	public string remoteIp = "127.0.0.1";
	public int sendToPort = 0;
	public int listenerPort = 8080;
	public int MaximumMessagesPerFrame = 100;

	private Osc oscHandler;
	private List<OscMessage> oscQueue;
	private int MaximumQueueSize = 1000;

	public delegate void NatNetAction(NatNetRigidbody rb);
	public static event NatNetAction onNatNetUpdate;

	~NatNetBackend()
	{
		if (oscHandler != null)
		{
			oscHandler.Cancel();
		}
		
		// speed up finalization by manually calling garbage collect.
		oscHandler = null;
		System.GC.Collect();
	}

	void OnDisable()
	{
		// close OSC UDP socket
		Debug.Log("closing OSC UDP socket in OnDisable");
		oscHandler.Cancel();
		oscHandler = null;
	}

	void Awake()
	{
		if(natnet == null)
		{
			natnet = this;
			DontDestroyOnLoad(gameObject);
		}
		else
		{
			Destroy(gameObject);
		}

		rigidbodies = new List<NatNetRigidbody>();
		oscQueue = new List<OscMessage>();
	}

	void Start()
	{
		UDPPacketIO udp = GetComponent<UDPPacketIO>();
		udp.init(remoteIp, sendToPort, listenerPort);
		
		oscHandler = GetComponent<Osc>();
		oscHandler.init(udp);
		
		oscHandler.SetAddressHandler("/rigidbody", Receive);
	}

	//Dealing with the messages on update to keep everything on the main thread.
	void Update()
	{
		OscMessage m;

		// process all osc message in the message queue
		for (int i=0; i<MaximumMessagesPerFrame; i++)
		{
			if (oscQueue.Count > 0) {
				// pop oldest message
				m = oscQueue [0];
				oscQueue.RemoveAt(0);
				if(m != null){
					processMessage(m);
				}
			}
			else
			{
				break;
			}
		}
	}

	public void processMessage(OscMessage m)
	{
		if(m.Address == "/rigidbody")
		{
			var rb = SimpleJSON.JSON.Parse(m.Values[0].ToString());
			Vector3 position = new Vector3(float.Parse(rb["position"][0]), float.Parse(rb["position"][1]),float.Parse(rb["position"][2]));
			Quaternion rotation = new Quaternion(float.Parse(rb["orientation"][0]),float.Parse(rb["orientation"][1]),float.Parse(rb["orientation"][2]),float.Parse(rb["orientation"][3]));
			int id = int.Parse(rb["id"]);
			bool found = false;
			
			foreach(NatNetRigidbody current in rigidbodies)
			{
				if(current.id == id)
				{
					current.Update(position, rotation);
					onNatNetUpdate(current);
					found = true;
					break;
				}
			}
			
			if (!found)
			{
				NatNetRigidbody r = new NatNetRigidbody(id, position, rotation);
				rigidbodies.Add(r);
				onNatNetUpdate(r);
			}
		}
	}

	public NatNetRigidbody getNatNetRigidBody(int id)
	{
		foreach(NatNetRigidbody r in rigidbodies)
		{	
			if (r.id == id)
			{
				return r;
			}
		}

		return null;
	}

	public void Receive(OscMessage m)
	{
		if (oscQueue.Count < MaximumQueueSize)
		{
			oscQueue.Add(m);
		}
	}
}



