import cv2
import time

def alerta(tipo_falta):

    if tipo_falta=='Hablando por Celular':
        url='screens/hablar-telefono.jpg'
    elif tipo_falta=='Usando Celular':
        url='screens/handphone.jpg'
    elif tipo_falta=='Bajando con Laptop':
        url='screens/laptop.jpg'
    elif tipo_falta=='Sosteniendo Vaso':
        url='screens/cup.jpg'
    elif tipo_falta=='Lo hiciste bien':
        url='screens/finish.jpg'


    cap = cv2.VideoCapture(url)
    capname = "Infracción"
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.namedWindow(capname, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(capname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(capname, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        else:
            time.sleep(2)
            cv2.destroyAllWindows()
            break