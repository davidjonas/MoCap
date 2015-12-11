using UnityEngine;
using System.Collections;

public class MoCapRigidBodiesCloner : MonoBehaviour {

	public GameObject rigidBodyObject;

	private MoCapOscInterface mocap; // store local instance


	// Use this for initialization
	void Start () {
		if (rigidBodyObject == null) {
			Debug.LogWarning ("rigidBodyObject not specified");
			return;
		}

		mocap = MoCapOscInterface.instance;

		// create objects for every rigid body that's already known in the system
		foreach (MoCapRigidBody current in mocap.rigidbodies) {
			createFollower(current);
		}

		// register a callback that creates new objects for every new rigid body
		// that is introduced to the system at a later time
		MoCapOscInterface.OnNewRigidBody += onNewRigidBody;
	}

	// Update is called once per frame
	void Update () {
	
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
