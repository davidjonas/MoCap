using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using SimpleJSON;

/*public class NatNetRigidbody
{
	public int id;
	public Vector3 position;
	public Quaternion rotation;
	public GameObject gameObject;

	public NatNetRigidbody(int i, Vector3 p, Quaternion r)
	{
		id = i;
		position = p;
		rotation = r;
		gameObject = null;
	}

	public void AttachObject(GameObject go)
	{
		gameObject = go;
	}

	public void Update(Vector3 p, Quaternion r)
	{
		position = p;
		rotation = r;
	}
}

// Simple OSC test communication script
[AddComponentMenu("Scripts/OSCTestSender")]
public class OSCTestSender : MonoBehaviour
{
	public static OSCTestSender instance;
    private Osc oscHandler;
    public string remoteIp;
    public int sendToPort;
    public int listenerPort;
	public GameObject prefab;
	public List<NatNetRigidbody> rigidbodies;

    ~OSCTestSender()
    {
        if (oscHandler != null)
        {
            oscHandler.Cancel();
        }

        // speed up finalization
        oscHandler = null;
        System.GC.Collect();
    }

    // Update is called every frame, if the MonoBehaviour is enabled.
    void Update()
    {
        //Debug.LogWarning("time = " + Time.time);

        //OscMessage oscM = Osc.StringToOscMessage("/1/push1");
        //oscHandler.Send(oscM);

		foreach(NatNetRigidbody current in rigidbodies)
		{
			if(current.gameObject == null)
			{
				current.AttachObject(Instantiate(prefab, current.position, current.rotation) as GameObject);
			}
			else
			{
				current.gameObject.transform.position = current.position;
				current.gameObject.transform.rotation = current.rotation;
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

		rigidbodies = new List<NatNetRigidbody>();
    }

    void OnDisable()
    {
        // close OSC UDP socket
        Debug.Log("closing OSC UDP socket in OnDisable");
        oscHandler.Cancel();
        oscHandler = null;
    }


    // Start is called just before any of the Update methods is called the first time.
    void Start()
    {

        UDPPacketIO udp = GetComponent<UDPPacketIO>();
        udp.init(remoteIp, sendToPort, listenerPort);

	    oscHandler = GetComponent<Osc>();
        oscHandler.init(udp);

        oscHandler.SetAddressHandler("/rigidbody", Receive);
    }

    public void Receive(OscMessage m)
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
				found = true;
				break;
			}
		}

		if (!found)
		{
			rigidbodies.Add(new NatNetRigidbody(id, position, rotation));
		}
    }
}*/
