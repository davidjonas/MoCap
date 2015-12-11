using UnityEngine;
using System.Collections;

public class MoCapRigidBodiesCloner : MonoBehaviour {

	public GameObject prefab;

	private MoCapOscInterface mocap; // store local instance


	// Use this for initialization
	void Start () {
		mocap = MoCapOscInterface.instance;
		cloneCurrentRigidBodies ();
		MoCapOscInterface.OnNewRigidBody += onNewRigidBody;
	}
	
	// Update is called once per frame
	void Update () {
	
	}

	void cloneCurrentRigidBodies(){
		foreach (MoCapRigidBody current in mocap.rigidbodies) {
			createFollower(current);
		}
	}

	void onNewRigidBody(MoCapRigidBody newBody){
		createFollower(newBody);
	}

	private void createFollower(MoCapRigidBody rigidbody){
		GameObject obj = (GameObject)Instantiate (prefab);
		rigidbody.addFollower (obj);
		obj.transform.SetParent (this.transform);
	}
}
