import cv2

cap = cv2.VideoCapture('номер камеры или название')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ret, frame = cap.read()
cv2.imwrite('pick4a', frame)
cap.release()