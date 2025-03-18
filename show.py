import cv2
import time

def main(image_path):
    while True:
        # Reload the image
        image = cv2.imread(image_path)
        
        if image is None:
            print("Error loading image")
            break
        
        # Display the image
        image = cv2.resize(image ,(650,900))
        cv2.imshow('Image', image)
        cv2.resizeWindow('Image', 650, 900)  # Set window size to 900x600
        # Wait for 1 second
        key = cv2.waitKey(1000)  # 1000 milliseconds = 1 second
        
        # Check if the user pressed 'q' to exit
        if key == ord('q'):
            break

    # Clean up and close the window
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Provide the path to your image file
    image_path = 'maps_annotated.png'
    main(image_path)
