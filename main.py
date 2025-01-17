import cv2
import mediapipe as mp
from exercises import pushups, lateral_raises, planks

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Define exercise type (use these functions in main)
def main():
    exercise = input("Enter exercise (pushups, lateral_raises, planks): ").lower()

    if exercise == "pushups":
        pushups.start(pose, mp_drawing, cap)
    elif exercise == "lateral_raises":
        lateral_raises.start(pose, mp_drawing, cap)
    elif exercise == "planks":
        planks.start(pose, mp_drawing, cap)
    else:
        print("Invalid exercise!")

if __name__ == "__main__":
    main()

    # Release resources and close windows after execution
    cap.release()
    cv2.destroyAllWindows()
