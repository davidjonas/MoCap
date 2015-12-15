using UnityEngine;
using System.Collections;

public class BoneAnimationScript : MonoBehaviour {


	public Transform leftFootObj;
	public Transform rightFootObj;
	public Transform leftHandObj;
	public Transform rightHandObj;
	
	private Animator animator;

	void Start() {
		animator = GetComponent<Animator>();
	}

	void OnAnimatorIK(int layerIndex) {
		animator.SetIKPositionWeight(AvatarIKGoal.LeftFoot, 1.0f);
		animator.SetIKRotationWeight(AvatarIKGoal.LeftFoot, 1.0f);
		animator.SetIKPosition(AvatarIKGoal.LeftFoot, leftFootObj.position);
		animator.SetIKRotation(AvatarIKGoal.LeftFoot, leftFootObj.rotation);

		animator.SetIKPositionWeight(AvatarIKGoal.RightFoot, 1.0f);
		animator.SetIKRotationWeight(AvatarIKGoal.RightFoot, 1.0f);
		animator.SetIKPosition(AvatarIKGoal.RightFoot, rightFootObj.position);
		animator.SetIKRotation(AvatarIKGoal.RightFoot, rightFootObj.rotation);

		animator.SetIKPositionWeight(AvatarIKGoal.RightHand, 1.0f);
		animator.SetIKRotationWeight(AvatarIKGoal.RightHand, 1.0f);
		animator.SetIKPosition(AvatarIKGoal.RightHand, rightHandObj.position);
		animator.SetIKRotation(AvatarIKGoal.RightHand, rightHandObj.rotation);

		animator.SetIKPositionWeight(AvatarIKGoal.LeftHand, 1.0f);
		animator.SetIKRotationWeight(AvatarIKGoal.LeftHand, 1.0f);
		animator.SetIKPosition(AvatarIKGoal.LeftHand, leftHandObj.position);
		animator.SetIKRotation(AvatarIKGoal.LeftHand, leftHandObj.rotation);
	}
}
