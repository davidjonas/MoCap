using UnityEngine;
using System.Collections;

public class Poser : MonoBehaviour {

	public KeyCode cloneKey=KeyCode.C;
	public KeyCode deleteKey=KeyCode.D;
	public Vector3 offset=new Vector3(-2, 0, 0);
	public float cloneDelay=0.5f;
	public int maxClones=10;

	private float tLastClone=0.0f;
	private int cloneCount=0;
	
	// Use this for initialization
	void Start () {

	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown (cloneKey)) {
			makeClone();
		}

		if (Input.GetKeyDown (deleteKey)) {
			removeClone ();
		}

		if (cloneDelay > 0.0f && Time.time - tLastClone > cloneDelay) {
			makeClone ();
		}

	}

	void makeClone(){
		// make sure we've got a container GameObject
		GameObject container = GameObject.Find ("clones");
		if (container == null) {
			container = new GameObject ();
			container.name = "clones";
		}

		// find our mocap body
		GameObject body = GameObject.Find ("MocapBody");

		// create clone object
		GameObject newClone = new GameObject ();
		// clone all child objects (rigid bodies)
		foreach (Transform child in body.transform) {
			GameObject clone = (GameObject)Instantiate (child.gameObject);
			clone.transform.parent = newClone.transform;
		}

		// give a semi-usable name
		cloneCount++;
		newClone.name = "clone" + System.Convert.ToString (cloneCount);
		// make new clone body child of our container
		newClone.transform.parent = container.transform;
		newClone.transform.position = body.transform.position;

		// offset position of all clones (also newly created clone)
		foreach (Transform child in container.transform) {
			child.localPosition = child.transform.localPosition + offset;
		}

		if (maxClones > 0){
			for (int i=container.transform.childCount; i>maxClones; i--) {
				removeClone ();
			}
		}

		tLastClone = Time.time;
	}

	void removeClone(){
		GameObject container = GameObject.Find ("clones");
		if (container == null)
			return;

		if (container.transform.childCount > 0) {
			GameObject go = container.transform.GetChild (0).gameObject;
			go.transform.parent = null;
			Destroy (go);
		}
	}
}
