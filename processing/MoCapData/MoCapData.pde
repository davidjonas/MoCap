import java.util.Map;

//Creating the mocap object
MoCapConnection mocap;

void setup() {
  size(800,600, P3D);
  
  //Initiating communication on port 8080
  mocap = new MoCapConnection(this, 8080);
}


void draw() {
  
  //Just some camera positioning, fancy light setup and a floor for our 3D environment. Not necessary.
  background(200);
  camera(0,500,500, 0,0,0, 0,-1,0);
  directionalLight(51, 102, 126, -1, -1, 0);
  ambientLight(102, 102, 102);
  noStroke();
  fill(0);
  box(1000, 1, 1000);
  fill(255);
  
  //This code goes through all the rigid bodies
  HashMap<Integer,RigidBody> rb = mocap.getAllRigidBodies();
  
  for (Map.Entry me : rb.entrySet()) {
    RigidBody current = (RigidBody) me.getValue();
    
    //From here on you can do whatever you want with the "current" rigid body:
    //You can use current.position and current.rotation if you want to access the PVector and Quaternion values.
    //Be ware that quaternions are hard to understand and use.
    
    //rigidBodyBegin takes care of positioning your matrix to match the current rigid body.
    //In between rigidBodyBegin() and rigidBodyEnd() you can draw anything you like around the point 0,0 and it will be drawn
    //on the position and rotation of the current rigidBody.
    //Notice that in this example I am just drawing a box of 20 pixels size on the 0,0 point.
    mocap.rigidBodyBegin(current);
    box(20);
    mocap.rigidBodyEnd();
  }
  
}

/* 
incoming osc message are forwarded to the mocap object.
THIS FUNCTION IS NECESSARY. PLEASE KEEP IT UNCHANGED.
*/
void oscEvent(OscMessage theOscMessage) {
    mocap.handleMessage(theOscMessage);
}