#ifndef _RIGIDBODY
#define _RIGIDBODY
#include "ofMain.h"

class Rigidbody{

	public:
    Rigidbody(ofPoint p, ofQuaternion r);
    Rigidbody();
    void set(ofPoint p, ofQuaternion r);

    ofPoint position;
    ofQuaternion rotation;
};
#endif
