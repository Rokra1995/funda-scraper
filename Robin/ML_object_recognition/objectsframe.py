import numpy as np
import pandas as pd
import time
import cv2
import os

#The code for the objectdetection is taken by this tutorial:
#https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/

#In order to run this code three files are necessary:
# coco.names
# yolov3.cfg
# olov3.weights

#This files contain the Neural Network object detection model, respectivly named YOLO (You only look once), trained on the coco dataset.
#A ful list of what yolo can detect can be found here: https://github.com/pjreddie/darknet/blob/master/data/coco.names

#saving the args with the path to the image training data, the minimum confidence and the threshold in a dict for late use
args = {'yolo': 'yolo', 'confidence': 0.5, 'threshold': 0.3}
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])
# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

#the function that detects the objects and returns a list with the detected obejcts and a list with the probabilities.
def detect_objects(imagepath):
    # load our input image and grab its spatial dimensions
    image = cv2.imread(imagepath)
    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()
    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > args["confidence"]:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
        args["threshold"])
    objects_detected = []
    probability_calculated = []
    if len(idxs) > 0:
        for item in idxs.flatten():
            objects_detected.append(LABELS[classIDs[item]])
            probability_calculated.append(confidences[item])
    return objects_detected, probability_calculated

#read our house data with the stored imagepaths that belongs to one house
scraped_data = pd.read_csv('funda_2020_subset_onepic.csv')
final_dataframe = pd.DataFrame(columns=['house_id','image','objects','probabilities'])
#add the house id to be able to join the funda_2020 dataset with the image objects.
#The principle idea is to have one dataset with the funda houses and one dataset with the images, 
#the objects on each immage and the probability the that the neural network calculated to be that object.

scraped_data['house_id'] = 0

#loops over the scraped houses and extracts the imagepaths that belong to one house and runs the object
#recognition on all of the images of one house. and stores the altered housing dataset and the objects in 2
#seperate csv files.
for idx, img in scraped_data.iterrows():
    image_list = img.images.replace("[","").replace("]","").split("}, {")
    scraped_data.loc[idx,'house_id'] = idx
    for item in image_list:
        string = item
        Dict = dict((x.strip(), y.strip())  
                for x, y in (element.split(': ')  
                for element in string.split(', '))) 
        path = Dict["'path'"].replace("'","")
        try:
            obs, probs = detect_objects(path)
            image_name = path.split("/")[-1]
            image_names = []
            for i in range(len(obs)):
                image_names.append(image_name)
            data = {'house_id':idx,'image':image_names,'objects':obs, 'probabilities':probs}
            data_to_append = pd.DataFrame(data)
            final_dataframe = final_dataframe.append(data_to_append)
        except Exception as e:
            print(e)
final_dataframe.to_csv('image_recogniton.csv')
scraped_data.to_csv('funda_2020_subset_onepic_w_id.csv')
print(scraped_data)
print(final_dataframe)
