#include "ofApp.h"

//--------------------------------------------------------------
void ofApp::setup(){
  //Setting up the communications port to receive the OSC messages. Change in ofApp.h
  receive.setup(PORT);

  //Just setting up the size and look of the boxes. Not important.
  ofBackground(20);
  box.set( 10 );
  ofSetSmoothLighting(true);
  pointLight.setDiffuseColor( ofFloatColor(.85, .85, .55) );
  pointLight.setSpecularColor( ofFloatColor(1.f, 1.f, 1.f));

  pointLight2.setDiffuseColor( ofFloatColor( 238.f/255.f, 57.f/255.f, 135.f/255.f ));
  pointLight2.setSpecularColor(ofFloatColor(.8f, .8f, .9f));

  pointLight3.setDiffuseColor( ofFloatColor(19.f/255.f,94.f/255.f,77.f/255.f) );
  pointLight3.setSpecularColor( ofFloatColor(18.f/255.f,150.f/255.f,135.f/255.f) );
  material.setShininess( 120 );
  material.setSpecularColor(ofColor(255, 255, 255, 255));

  ofPoint camPos;
  ofQuaternion camRotation;
  camRotation.makeRotate(-20, 1, 0, 0);;
  camPos.set(100, 200, 200);
  camera.setPosition(camPos);
  camera.setGlobalOrientation(camRotation);
}

//--------------------------------------------------------------
void ofApp::update(){
  handleMoCapMessages();

  //After handling the MoCap messages you can use the variable rigidboies that stores all the
  //rigidboies. It is a map of type std::map<int, Rigidbody>.
  //Each Rigidbody has public position (ofPoint) and rotation (ofQuaternion)
}

//--------------------------------------------------------------
void ofApp::draw(){

  //Setting up lights and stuff not important.
  ofEnableDepthTest();
  ofEnableLighting();
  pointLight.enable();
  pointLight2.enable();
  pointLight3.enable();

  camera.begin();

  //This is an easy way to iterate through all the rigidbodies
  for (auto const& rb : rigidbodies)
  {
    Rigidbody current = rb.second;

    //cout << "Rigidbody " << current.position << endl;

    //Drawing a box in the position and rotation of the current rigid body
    box.setPosition(current.position);
    box.setGlobalOrientation(current.rotation);

    box.draw();
  }

  camera.end();
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){

}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){

}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){

}

//--------------------------------------------------------------
void ofApp::handleMoCapMessages()
{
  while (receive.hasWaitingMessages()) {
    ofxOscMessage m;
    receive.getNextMessage(m);

    if(m.getAddress() == "/rigidbody")
    {
      std::string message = m.getArgAsString(0);
      ofxJSONElement result;
      if(result.parse(message))
      {
        int id = result["id"].asInt();
        ofPoint position;
        position.set(result["position"][0].asFloat() * 100,result["position"][1].asFloat() * 100,result["position"][2].asFloat() * 100);
        ofQuaternion rotation;
        rotation.set(result["orientation"][0].asFloat(),result["orientation"][1].asFloat(),result["orientation"][2].asFloat(), result["orientation"][3].asFloat());
        //delete rigidbodies[id]

        rigidbodies[id].set(position, rotation);
      }
    }
  }
}
