import cv2
import mediapipe as mp
from utils.angles import calculate_angle

# Push-up rep counting logic
rep_count = 0
direction = 0  # 0 = down, 1 = up

def start(pose, mp_drawing, cap):
    global rep_count, direction
    print("Tracking Push-ups... Get ready!")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get key body parts: shoulders, elbows, wrists, etc.
            shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

            # Calculate the angle at the elbow
            angle = calculate_angle(shoulder, elbow, wrist)

            # Push-up rep counting logic
            if angle > 160:  # Arm is fully down
                direction = 0
            if angle < 90 and direction == 0:  # Arm is at peak (upward)
                direction = 1
            if angle > 160 and direction == 1:  # Arm back down
                direction = 0
                rep_count += 1  # Increment rep count
                print(f"Push-up Count: {rep_count}")

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.putText(frame, f'Reps: {rep_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Push-up Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
