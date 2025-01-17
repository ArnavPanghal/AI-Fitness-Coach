import cv2
import mediapipe as mp
from utils.angles import calculate_angle

# Plank counting logic
time_in_plank = 0  # Track time in plank position
plank_started = False

def start(pose, mp_drawing, cap):
    global time_in_plank, plank_started
    print("Tracking Planks... Get ready!")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get key body parts: shoulders, hips, ankles
            shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]

            # Calculate angle between shoulder, hip, and ankle to detect plank position
            angle = calculate_angle(shoulder, hip, ankle)

            if angle < 180 and angle > 160:  # User is holding the plank position (straight body)
                if not plank_started:
                    plank_started = True  # Plank started
                    print("Plank started!")
            else:
                if plank_started:
                    plank_started = False  # Plank ended
                    print(f"Plank duration: {time_in_plank} seconds")
                    time_in_plank = 0

            if plank_started:
                time_in_plank += 1  # Increment plank time

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.putText(frame, f'Time: {time_in_plank}s', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Plank Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
