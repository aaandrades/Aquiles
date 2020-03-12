import cv2
import time

def alerta(tipo_falta):
    url='AlertaCasco.jpg'
    cap = cv2.VideoCapture(url)
    capname = "Detector"
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