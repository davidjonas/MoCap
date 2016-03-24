using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class NatNetRigidBodySpawner : MonoBehaviour {

	public GameObject prefab;
	public Dictionary<int, GameObject> objects;

	void Awake()
	{
		objects = new Dictionary<int, GameObject>();
	}

	// Use this for initialization
	void Start () {
		NatNetBackend.onNatNetUpdate += natNetUpdateHandler;
	}
	
	// Update is called once per frame
	void Update () {

	}

	void natNetUpdateHandler(NatNetRigidbody rb)
	{
		if(objects.ContainsKey(rb.id))
		{
			objects[rb.id].transform.position = rb.position;
			objects[rb.id].transform.rotation = rb.rotation;
		}
		else
		{
			objects.Add(rb.id, Instantiate(prefab, rb.position, rb.rotation) as GameObject);
		}
	}
}
