import cv2
from numba import jit, cuda
from centroidtracker import CentroidTracker
import argparse
import numpy as np
import time

starting_time = time.time() #Initial Time

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)



# Parsing Arguments
ap = argparse.ArgumentParser()
ap.add_argument('-c', '--config', help = 'path to yolo config file', default='custom/yolov3-tiny.cfg')
ap.add_argument('-w', '--weights', help = 'path to yolo pre-trained weights', default='custom/yolov3-tiny_last.weights')
ap.add_argument('-cl', '--classes', help = 'path to text file containing class names',default='custom/objects.names')
args = ap.parse_args()


# Load names classes
classes = None
with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]





# Get names of output layers, output for YOLOv3 is ['yolo_16', 'yolo_23']
def getOutputsNames(net):
    layersNames = net.getLayerNames()
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]




# Draw a rectangle surrounding the object with his class and percentage
def draw_pred(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])
    label = ('%.2f' % confidence) #Regular Expression to take the first to digits
    label=(float(label))*100

    if classes:
        assert(class_id < len(classes))
        label = '%s: %s %s' % (classes[class_id], label,'%')
    
    if classes[class_id]=='Person':
        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), (0,0,255), 3)
        cv2.putText(img, label, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    else:
        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), (0,255,0), 3)
        cv2.putText(img, label, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)

# Define a window to show the cam stream on it
window_title= "Aquiles Detector"   
cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)




#Generate color for each class randomly
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# Define network from configuration file and load the weights from the given weights file
net = cv2.dnn.readNet(args.weights,args.config)
print("[INFO] setting preferable backend and target to CUDA...")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)



# Define video capture for default cam
cap = cv2.VideoCapture(0)
frame_id=0


# @jit(target ="cuda")
while cv2.waitKey(1) < 0:
    
    
    hasframe, image = cap.read()
    frame_id += 1
    # image=cv2.resize(image, (620, 480)) 
    if W is None or H is None:
        (H, W) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 1.0/255.0, (416,416), [0,0,0], True, crop=False)
    Width = image.shape[1]
    Height = image.shape[0]
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    
    

    # In case of tiny YOLOv3 we have 2 output(outs) from 2 different scales [3 bounding box per each scale]
    # For normal normal YOLOv3 we have 3 output(outs) from 3 different scales [3 bounding box per each scale]
    
    # For tiny YOLOv3, the first output will be 507x6 = 13x13x18
    # 18=3*(4+1+1) 4 boundingbox offsets, 1 objectness prediction, and 1 class score.
    # and the second output will be = 2028x6=26x26x18 (18=3*6) 


    for out in outs: 
        for detection in out:
            
        #each detection  has the form like this [center_x center_y width height obj_score class_1_score class_2_score ..]
            scores = detection[5:]  #classes scores starts from index 5
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
                # print(class_id)   Send number of Class
        
    objects = ct.update(boxes,class_ids)
    # apply  non-maximum suppression algorithm on the bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for (objectID, centroid) in objects.items():
		# draw both the ID of the object and the centroid of the
		# object on the output frame

        # for clase in class_ids[0:len(class_ids)]:
        #     if clase==0:
        #         text = "Ok: {}".format(objectID)
        #     else:
        #         text = "Falla: {}".format(objectID)
                
        text = "Falla: {}".format(objectID)
        cv2.putText(image, text, (centroid[0]+10,centroid[1]+10),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0) , 2)
        cv2.circle(image,(centroid[0],centroid[1]),4, (0, 255, 0), -1)

        

       

    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_pred(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
   
    # Put efficiency information.
    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.putText(image, "FPS: " + str(round(fps, 2)), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    t, _ = net.getPerfProfile()
    labels = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    cv2.putText(image, labels, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    cv2.imshow(window_title, image)
    
