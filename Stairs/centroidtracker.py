# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import os
import numpy as np
import colorama
import termcolor2
import datetime
from openpyxl import Workbook
import csv
from createfile import append_list_as_row,main
from screenshot import captura
import time
from Alerts import alerta


colorama.init()


class CentroidTracker():
	def __init__(self, maxDisappeared=20):

		# initialize the next unique object ID along with two ordered
		# dictionaries used to keep track of mapping a given object
		# ID to its centroid and number of consecutive frames it has
		# been marked as "disappeared", respectively
		self.nextObjectID = 0
		self.objects = OrderedDict()
		self.disappeared = OrderedDict()
		self.diccionarioInicial=dict()

		#Starting Time on the Screen
		self.start_time=datetime.datetime.now()

		# store the number of maximum consecutive frames a given
		# object is allowed to be marked as "disappeared" until we
		# need to deregister the object from tracking
		self.maxDisappeared = maxDisappeared
		

	def register(self, centroid,class_ids,frame):
    
		#Loop over the class (if exist more than one class at the same time)
		for clase in class_ids[0:len(class_ids)]:

			# when registering an object we use the next available objectID to store the centroid
			self.objects[self.nextObjectID] = centroid
			self.disappeared[self.nextObjectID] = 0
			self.nextObjectID += 1

			# Starting time when an object appear in the screen
			self.start_time=datetime.datetime.now()
			self.start_time=time.strftime("%H:%M:%S")

			# Create an empty list to contain to values: Starting Time and 
			# Action in the screen
			lista=[]
			 
			# Now, we are going to put the variable in a dict(), when you
			# can store the list with a key
			for i in range(0,1):

				#Create first slot in the list with the Starting time 
				lista.append(self.start_time)

				if clase==4:
					falla='Ninguna'
				else:
					if clase==0:
						falla='Bajando con Laptop'
					if clase==1:
						falla='Sosteniendo Vaso'
					if clase==2:
						falla='Hablando por Celular'
					if clase==3:
						falla='Usando Celular'

				#Create the second slot in the list with the Action
				lista.append(falla)

				#Take a screenshot of the action in the screen and store it.
				captura(frame,falla)

			#Add to the dictionary the objectID and the list with above two values
			self.diccionarioInicial.update({self.nextObjectID-1:lista})

		
	# Delete an objectID and calculate time in screen
	def deregister(self, objectID,class_ids):

		# to deregister an object ID we delete the object ID from
		# both of our respective dictionaries

		#Delete object in the screen
		del self.objects[objectID]
		del self.disappeared[objectID]

		# Read the dictionary to search what is the starting time to
		# calculate the elapsed time of the object.
		for k in self.diccionarioInicial.keys():

			if k==objectID:
				# Split the starting time to take the seconds
				inicial=int((str(self.diccionarioInicial[k][0])).split(':')[2])
				
				# Calculate the time of the deregister 
				final=datetime.datetime.now()
				final=int(time.strftime("%S"))

				# Delay
				resp=final-inicial-2
				if(resp<0):
					resp=resp+60

				# Validate the time to see if the element its correct in the 
				# screen or if its a false positive
				if (resp<2):
					pass
				else:
					#Create an alert
					print(" ")
					final=time.strftime("%H:%M")
					final2=datetime.datetime.now()
					final2=int(time.strftime("%S"))-2
					print (termcolor2.colored("ID: "+str(objectID), 'green'))
					print(" Hora Inicial       : {}".format((self.diccionarioInicial[k][0])))
					print(" Hora final         : {}:{}".format(final,final2))
					print(" Falta              : {}".format(self.diccionarioInicial[k][1]))
					print(" Total transcurrido : {} {}".format(resp,'Segundos'))
					screen="infraccion_{}{}{}.jpg".format((str(self.diccionarioInicial[k][0])).split(':')[0],
								(str(self.diccionarioInicial[k][0])).split(':')[1],
								(str(self.diccionarioInicial[k][0])).split(':')[2])
					main(self.diccionarioInicial[k][1],resp,screen)


	#Update a New ObjectID
	def update(self, rects,class_id,frame):
		
		# When the screen its empy
		#
		# check to see if the list of input bounding box rectangles is empty
		if len(rects) == 0:

			#Loop Because its empty
			# loop over any existing tracked objects and mark them
			# as disappeared

			for objectID in list(self.disappeared.keys()):

				#Time in screen without bounding box
				self.disappeared[objectID] += 1

				# if we have reached a maximum number of consecutive
				# frames where a given object has been marked as
				# missing, deregister it	
				
				if self.disappeared[objectID] > self.maxDisappeared:
					self.deregister(objectID,class_id) #Disappear the id tracker

					# It activate when there is only one ID on Screen

			# return early as there are no centroids or tracking info
			# to update
			return self.objects
		
		


		# initialize an array of input centroids for the current frame
		inputCentroids = np.zeros((len(rects), 2), dtype="int")

		# loop over the bounding box rectangles
		for (i, (startX, startY, endX, endY)) in enumerate(rects):
			# use the bounding box coordinates to derive the centroid
			cX = int((startX + endX) )
			cY = int((startY + endY) )
			inputCentroids[i] = (cX, cY)



		# The first element that appear in the screen
		#
		# if we are currently not tracking any objects take the input 
		# centroids and register each of them

		if len(self.objects) == 0:
			for i in range(0, len(inputCentroids)):
				self.register(inputCentroids[i],class_id,frame)
		

		
		# Already exists an object
		# otherwise, are currently tracking objects so we need to
		# try to match the input centroids to existing object centroids

		else:
			# Execute de code while there's something in the screen

			# grab the set of object IDs and corresponding centroids
			objectIDs = list(self.objects.keys())
			objectCentroids = list(self.objects.values())

			# compute the distance between each pair of object
			# centroids and input centroids, respectively -- our
			# goal will be to match an input centroid to an existing
			# object centroid
			D = dist.cdist(np.array(objectCentroids), inputCentroids)

			# in order to perform this matching we must 
			# (1) find the smallest value in each row and then 
			# (2) sort the row indexes based on their minimum values so that the row
			# with the smallest value as at the *front* of the index list
			rows = D.min(axis=1).argsort()

			# next, we perform a similar process on the columns by
			# finding the smallest value in each column and then
			# sorting using the previously computed row index list
			cols = D.argmin(axis=1)[rows]

			# in order to determine if we need to update, register,
			# or deregister an object we need to keep track of which
			# of the rows and column indexes we have already examined
			usedRows = set()
			usedCols = set()

			# loop over the combination of the (row, column) index tuples
			for (row, col) in zip(rows, cols):
				# if we have already examined either the row or
				# column value before, ignore it val

				if row in usedRows or col in usedCols:
					continue

				# otherwise, grab the object ID for the current row,
				# set its new centroid, and reset the disappeared
				# counter
				objectID = objectIDs[row]
				self.objects[objectID] = inputCentroids[col]
				self.disappeared[objectID] = 0

				# indicate that we have examined each of the row and
				# column indexes, respectively
				usedRows.add(row)
				usedCols.add(col)

			# compute both the row and column index we have NOT yet
			# examined
			unusedRows = set(range(0, D.shape[0])).difference(usedRows)
			unusedCols = set(range(0, D.shape[1])).difference(usedCols)

			# in the event that the number of object centroids is
			# equal or greater than the number of input centroids
			# we need to check and see if some of these objects have
			# potentially disappeared
			if D.shape[0] >= D.shape[1]:

				# loop over the unused row indexes
				for row in unusedRows:
					# grab the object ID for the corresponding row
					# index and increment the disappeared counter
					objectID = objectIDs[row]
					self.disappeared[objectID] +=1

					# check to see if the number of consecutive
					# frames the object has been marked "disappeared"
					# for warrants deregistering the object
					if self.disappeared[objectID] > self.maxDisappeared:
						self.deregister(objectID,class_id)
						
						# Activate when there's more than one ID in the screen
			
			# otherwise, if the number of input centroids is greater
			# than the number of existing object centroids we need to
			# register each new input centroid as a trackable object
			else:
				for col in unusedCols:
					#More than two
					self.register(inputCentroids[col],class_id,frame)

		# return the set of trackable objects
		return self.objects 