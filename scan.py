import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

# Use zbar to detect and decode codes
def decode(img):
    decoded = pyzbar.decode(img)
    
    # Display text on screen with the type and data of the code
    codes = 0
    for obj in decoded:
        codes = codes + 1
        string = 'Type: ' + (obj.type) + ' Data: ' + str(obj.data)
        cv2.putText(img, string, (10,30 * codes),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0, 0), 2)
    print(len(decoded))

    return decoded
# Draw bounding box around detected code
def display(img, decoded):

    # Get the bounding points for the code
    for obj in decoded:
        points = obj.polygon
    
        # If the bounds do not resemble a rectangle, perform a convex hull
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        
        # Draw the bounding box around the code
        for j in range (0,n):
            cv2.line(img, hull[j], hull[(j+1) % n], (255, 0, 0), 3)

if __name__ == '__main__':
    # Begin video capture
    cap = cv2.VideoCapture(0)
    
    while(True):
        # Get each frame
        ret, frame = cap.read()
        # Gray scale for increased performance
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Find codes
        codes = decode(gray)
        
        # Display boundaries
        display(gray, codes)

        # Display frames 
        cv2.imshow('Feed', gray)

        # Close window when Q key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
