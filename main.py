import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

with open('myDataFile.tExt') as f:
    myDataList = f.read().splitlines()

while True:
    success, img = cap.read()

    # Decode QR codes in the frame
    decoded_objects = decode(img)

    for barcode in decoded_objects:
        myData = barcode.data.decode('utf-8')

        if myData in myDataList:
            myOutput = 'Authorized'
            myOutputColor = (0, 255, 0)  # Green color for "Authorized"
        else:
            myOutput = 'Un-Authorized'
            myOutputColor = (0, 0, 255)  # Red color for "Un-Authorized"

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myOutputColor, 2)  # Reduce thickness to 2
        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, myOutputColor, 2)

        # Display the decoded data below the frame
        cv2.putText(img, myData, (pts2[0], pts2[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    cv2.imshow('QR Code Detection', img)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' key to exit the loop
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
