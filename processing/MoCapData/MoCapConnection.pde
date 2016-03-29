import oscP5.*;
import netP5.*;


class MoCapConnection
{
  
  OscP5 oscP5;
  NetAddress myBroadcastLocation; 
  HashMap<Integer,RigidBody> rigidbodies = new HashMap<Integer, RigidBody>();
  
  MoCapConnection(PApplet context, int port)
  {
     oscP5 = new OscP5(context,port);
     rigidbodies = new HashMap<Integer,RigidBody>();
  }
  
  void handleMessage(OscMessage theOscMessage)
  {
    if(theOscMessage.addrPattern().equals("/rigidbody"))
    {
      try
      {
        JSONObject json = parseJSONObject(theOscMessage.get(0).stringValue());
        if (json == null) {
          println("JSONObject could not be parsed");
        } else {
            PVector position = new PVector(
              json.getJSONArray("position").getFloat(0)*100,
              json.getJSONArray("position").getFloat(1)*100,
              json.getJSONArray("position").getFloat(2)*100
            );
            
            Quaternion rotation = new Quaternion(
              json.getJSONArray("orientation").getFloat(0),
              json.getJSONArray("orientation").getFloat(1),
              json.getJSONArray("orientation").getFloat(2),
              json.getJSONArray("orientation").getFloat(3)
             );
            
            RigidBody rb = new RigidBody(position, rotation);
            
            rigidbodies.put(json.getInt("id"), rb);
        }
      } catch (Exception e)
      {
        println(e);
      }
    }
  }
  
  void rigidBodyBegin(RigidBody rb)
  {
    pushMatrix();
    PVector euler = rb.rotation.getEulerAngles();
    translate(rb.position.x, rb.position.y, rb.position.z);
    rotateY(euler.y);
    rotateX(euler.x);
    rotateZ(euler.z);
  }
  
  void rigidBodyEnd()
  {
    popMatrix();
  }
  
  HashMap<Integer,RigidBody> getAllRigidBodies()
  {
    return (HashMap<Integer,RigidBody>) rigidbodies.clone();
  }
  
  
}