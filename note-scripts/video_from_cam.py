
"""
Simple script to collect data from the camera
"""

import cv2


if __name__=="__main__":
    cv2.namedWindow("preview")

    # Capture the video
    vc = cv2.VideoCapture(0) # This is the 0th position

    if vc.isOpened():  # This reads the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        cv2.imshow("preview", frame)

        # Update the video stream
        rval, frame = vc.read()

        key = cv2.waitKey(20)
        if key == 27:
            # Exit on ESC key
            break
    
    vc.release()
    cv2.destroyWindow("preview")
