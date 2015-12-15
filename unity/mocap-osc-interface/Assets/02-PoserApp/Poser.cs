using UnityEngine;
using System.Collections;

public class Poser : MonoBehaviour {

	public GameObject body;
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

		// auto-clone if clone delay is not zero
		if (cloneDelay > 0.0f && Time.time - tLastClone > cloneDelay) {
			makeClone ();
		}
	}

	void makeClone(){
		// we'll need a body object to clone from, abort if its missing
		if (body == null) {
			Debug.LogWarning ("no body GameObject specified");
			return;
		}

		// find clones container object, create it if it's not there
		GameObject container = GameObject.Find ("clones");
		if (container == null) {
			container = new GameObject ();
			container.name = "clones";
		}

		// create clone object
		GameObject newClone = new GameObject ();
		// clone all child objects (the rigid bodies)
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

		// auto-remove oldest clone if we've exceded the max. number of clones
		if (maxClones > 0){
			for (int i=container.transform.childCount; i>maxClones; i--) {
				removeClone ();
			}
		}

		// keep track of the time when the last clone was added;
		// necessary to determine when we can make the next auto-clone
		tLastClone = Time.time;
	}

	void removeClone(){
		// find container, if it's not there, abort
		GameObject container = GameObject.Find ("clones");
		if (container == null)
			return;

		// simply remove the first (oldest) child/clone in the container
		if (container.transform.childCount > 0) {
			GameObject go = container.transform.GetChild (0).gameObject;
			go.transform.parent = null; // it seems like Destroy keeps them in memory somehow, so also orphan the object
			Destroy (go);
		}
	}
}
