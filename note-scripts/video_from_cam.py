
"""
Simple script to collect data from the camera
"""

import cv2

import mediapipe as mp

# Load all the mediapipe drawing tools
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Generate hand processing toolset
mp_hands = mp.solutions.hands


if __name__=="__main__":
    cv2.namedWindow("preview")

    # Capture the video
    vc = cv2.VideoCapture(0) # This is the 0th position
    
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
        min_detection_confidence=0.5, min_tracking_confidence=0.5)
    hand_processor = mp_hands.Hands(model_complexity=1, min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    while vc.isOpened():
        is_success, frame = vc.read()

        if not is_success:
            print("Ignoring empty frame...")
            continue

        frame.flags.writeable = True
        # Convert the color space
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Process images
        face_mesh_results = face_mesh.process(image)
        hand_processor_results = hand_processor.process(image)

        if face_mesh_results.multi_face_landmarks:
            for face_landmarks in face_mesh_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image, landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())
        
        # Handle hand landmarks
        if hand_processor_results.multi_hand_landmarks:
            for hand_landmarks in hand_processor_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally
        cv2.imshow("mp face mesh", cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB))

        if cv2.waitKey(5) & 0xFF == 27:
            # exit on escape key
            break
    # --
    vc.release()
    cv2.destroyWindow("mp face mesh")
