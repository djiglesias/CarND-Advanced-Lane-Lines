import sys
import cv2





print(sys.argv)


if __name__ = "__main__":
	
	if len(sys.argv) != 2:
		print("Incorrect number of input arguments: Pass file name as an arguement.")
		sys.exit(1)

	


	image = cv2.imread(sys.argv[1])



def process_image(img):
	pass

def process_video(img):
	pass