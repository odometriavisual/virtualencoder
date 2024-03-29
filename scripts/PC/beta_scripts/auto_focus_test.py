import time

import cv2
import matplotlib.pyplot as plt
import numpy as np

from virtualencoder.visualodometry.score_focus import score_teng

camera_id = 0  # Altere o id da câmera aqui
total_rec_time = 60  # seconds
max_fps = 30  # Define o FPS máximo desejado
camera_exposure = -6       # Defina exposição da câmera

score_history = [0]*255

def show_img(img):
    plt.clf()
    plt.imshow(img)
    plt.pause(0.01)  # Pause para atualizar o gráfico

# define a video capture object
print('Requesting access to camera. This may take a while...')

vid = cv2.VideoCapture(camera_id,cv2.CAP_MSMF)
print('Got access to camera!')

frame_num = 0  # para guardar o número de frames.
vid.set(cv2.CAP_PROP_AUTOFOCUS, 0)
counter = 0
vid.set(cv2.CAP_PROP_FOCUS, counter)
plt.show()
ax = plt.gca()
plt.axis('off')

print("Iniciando calculo de foco")

while True:
    try:
        ret, frame = vid.read()
        cv2_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        show_img(cv2_img)
        if counter < 255:
            focus_score = score_teng(cv2_img)
            score_history[counter] = focus_score
        elif counter == 255:
            print(f"Foco ideal detectado: {int(np.argmax(score_history))}")
        counter+=5
        if counter < 255:
            vid.set(cv2.CAP_PROP_FOCUS, counter)
        else:
            vid.set(cv2.CAP_PROP_FOCUS, int(np.argmax(score_history)))
    except KeyboardInterrupt:
        vid.release()
        exit()



