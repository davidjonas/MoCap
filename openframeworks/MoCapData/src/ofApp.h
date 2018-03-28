#pragma once

#include "ofMain.h"
#include "ofxOsc.h"
#include "ofxJSON.h"
#include "Rigidbody.h"

#define PORT 8080

class ofApp : public ofBaseApp{

	public:
		void setup();
		void update();
		void draw();

		void keyPressed(int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void mouseEntered(int x, int y);
		void mouseExited(int x, int y);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);
		void handleMoCapMessages();

		ofxOscReceiver receive;
		map<int, Rigidbody> rigidbodies;

		//These are just for the current example. Not Important
		ofBoxPrimitive box;
		ofLight pointLight;
    ofLight pointLight2;
    ofLight pointLight3;
    ofMaterial material;
		ofCamera camera;
};
