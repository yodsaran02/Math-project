import cv2
import time
img = cv2.imread("./maps.png")

cv2.imshow("Window",img)

# Wait for the user to press a key
cv2.waitKey(0)
 
# Close all windows
cv2.destroyAllWindows()

number = [
	[1118,1428],
	[1106,1132],
	[942,1141],
	[942,899],
	[934,793],
	[928,477],
	[922,267],
	[416,206],
	[419,448],
	[422,747],
	[436,1009],
	[436,1184],
	[1213,505],
	[1233,891],
	[97,1540],
	[445,1494],
	[101,1018],
	[98,721],
	[88,481],
	[1237,1427]

]