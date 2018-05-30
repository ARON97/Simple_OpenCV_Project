# CAPTURE VIDEO WITH THE WEBCAM
import cv2, time, pandas
from datetime import datetime
# store the current frame of the video as soon as the video starts
first_frame = None

status_list = [None, None]
times = []
df = pandas.DataFrame(columns = ["Start","End"])
# reading the video
# the built-in cam will be index 0, the external cam will be 1 and the other 2
# if there is a video file you will pass in "movie.mp4" as the first parameter
video = cv2.VideoCapture(0)

# capture a video instead of a picture using a while loop, to capture picture remove while loop
while True:
	# frame object to capture the video in the cam
	check, frame = video.read() # check is a boolean

	status = 0
	# converting the frame to gray
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# apply gaussian blur to image to blur image
	# this removes noise and increases accuracy in difference calculation
	gray = cv2.GaussianBlur(gray, (21, 21), 0) # pass in the img and W and H and standard deviation(0)

	# check if the first frame is none
	if first_frame is None:
		# assign the first frame to the gray frame
		first_frame = gray
		continue # going to the beginning of the loop and continue with the second frame
	
	# compare the first frame(background) with the current frame
	delta_frame = cv2.absdiff(first_frame, gray)
	# Black and white image
	thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

	# smooth the thresh_frame
	thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
	
	# storing the CONTOURS in a tuple
	(_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	# FILTER CONTOUR, keeping the areas that are bigger then 1000p
	for contour in cnts:
		if cv2.contourArea(contour) < 10000:
			continue

		status = 1
		
		# if a contour is greater then 1000p. Draw a rect surrounding the contour to the current frame
		(x, y, w, h) = cv2.boundingRect(contour)
		# draw rect to current frame
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
	# append the current status of the list
	status_list.append(status)

	# Avoiding memory problems. Grabbing only the last two items of the status list
	status_list = status_list[-2:]

	# Recording the time when the status changes from 0 to 1(object entry)
	# check if the last items of the status list changes
	if status_list[-1] == 1 and status_list[-2] == 0:
		times.append(datetime.now())

	# Object exits. Status changes from 1 to 0
	if status_list[-1] == 0 and status_list[-2] == 1:
		times.append(datetime.now())
	# show the gray frame
	cv2.imshow("Gray Frame", gray)
	# show the delta frame
	cv2.imshow("Delta Frame", delta_frame)
	# show the threshold frame
	cv2.imshow("Threshold Frame", thresh_frame)
	cv2.imshow("Color Frame", frame)

	# closing the window when a button is pressed. The key is for the video here.
	key = cv2.waitKey(1)
	# print(gray)
	# # see the difference between the intensity of the corrosponding pixels 
	# print(delta_frame)

	# if q is pressed break the while loop
	if key == ord('q'):
		if status == 1:
			# add another item to the times list
			times.append(datetime.now())
		break

	# print out the status variable
	# print(status) # expected to see the status 0 or 1

# illustration of the status list
print(status_list)
print(times)

for i in range(0, len(times), 2):
	# updating the dataframe and pass in a dictionary
	df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index = True)

# write to data frame
df.to_csv("Times.csv")
# release the cam or video
video.release()
# close the window
cv2.destroyAllWindows
