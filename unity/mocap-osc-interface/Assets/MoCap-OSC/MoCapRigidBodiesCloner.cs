using UnityEngine;
using System.Collections;

public class MoCapRigidBodiesCloner : MonoBehaviour {

	public GameObject rigidBodyObject;

	// We use a local instance instead of referencing the singleton instance everywhere,
	// this way, if there's ever need for multiple mocap instances, there's less refactoring to be done 
	private MoCapOscInterface mocapInstance; 
	
	// Use this for initialization
	void Start () {
		// start with uninitialized state
		mocapInstance = null;

		// we'll need a rigidBodyObject to initialize
		if (rigidBodyObject == null) {
			Debug.LogWarning ("rigidBodyObject not specified");
			// abort
			return;
		}

		// ok let's get ready
		Setup ();
	}

	// Update is called once per frame
	void Update () {
		// run Setup as soon as we get a rigidBodyObject
		if (mocapInstance == null && rigidBodyObject != null) {
			Setup ();
		}
	}

	private void Setup(){
		// we'll keep a local reference to the mocap osc interface
		mocapInstance = MoCapOscInterface.instance;

		// create objects for every rigid body that's already in the system
		foreach (MoCapRigidBody current in mocapInstance.rigidbodies) {
			createFollower(current);
		}

		// register an event callback handler that creates new objects for
		// every new rigid body that is introduced to the system at a later time
		MoCapOscInterface.OnNewRigidBody += onNewRigidBody;
	}

	void onNewRigidBody(MoCapRigidBody newBody){
		createFollower(newBody);
	}

	private void createFollower(MoCapRigidBody rigidbody){
		// create object
		GameObject obj = (GameObject)Instantiate (rigidBodyObject);
		// make it follow the specified rigidbody (always adopt its position and rotation)
		rigidbody.addFollower (obj);
		// make the new object a child of our main object (this)
		obj.transform.SetParent (this.transform);
	}
}
