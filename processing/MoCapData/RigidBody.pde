class RigidBody
{
  PVector position;
  Quaternion rotation;
  
  RigidBody(PVector p, Quaternion r)
  {
    position = p;
    rotation = r;
  }
}