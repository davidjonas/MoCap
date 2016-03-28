#include "Rigidbody.h"

Rigidbody::Rigidbody(ofPoint p, ofQuaternion r)
{
  position = p;
  rotation = r;
}

Rigidbody::Rigidbody()
{
}

void Rigidbody::set(ofPoint p, ofQuaternion r)
{
  position = p;
  rotation = r;
}
