# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os
import datetime


"""
Take the frame: Recieve the frame of the infraction.
Take de Fault - Identify whats the problem.
"""

def captura(frame,falta):

    ##Just the First Time

    if os.path.exists('evidencias/HablandoCelular'):
        pass
    else:
        os.mkdir('evidencias/HablandoCelular')
        os.mkdir('evidencias/CelularEnMano')
        os.mkdir('evidencias/CopaEnLaMano')
        os.mkdir('evidencias/Laptop')

    current_dt = datetime.datetime.now()
    name = '{}{}{}'.format(current_dt.hour,current_dt.minute,current_dt.second)
    # cv2.imshow('Infraccion',frame) #display the captured image

    if falta == 'Hablando por Celular':
        cv2.imwrite('evidencias/HablandoCelular/Infraccion_{}.jpg'.format(name),frame)
    elif falta == 'Usando Celular':
        cv2.imwrite('evidencias/CelularEnMano/Infraccion_{}.jpg'.format(name),frame)
    elif falta == 'Bajando con Laptop':
        cv2.imwrite('evidencias/Laptop/Infraccion_{}.jpg'.format(name),frame)
    elif falta == 'Sosteniendo Vaso':
        cv2.imwrite('evidencias/CopaEnLaMano/Infraccion_{}.jpg'.format(name),frame)

    return '/evidencias'
    cv2.destroyAllWindows()
        
        
