import cv2
import mediapipe as mp
import random
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

score = 0
ball_x, ball_y = random.randint(100, 500), random.randint(100, 400)
start_time = time.time()
game_duration = 30  # Main selama 30 detik

while cap.isOpened():
    success, img = cap.read()
    if not success: break

    img = cv2.flip(img, 1)
    h, w, c = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # sisa waktu
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(game_duration - elapsed_time))

    if remaining_time > 0:
        # Gambar Bola 
        cv2.circle(img, (ball_x, ball_y), 20, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (ball_x, ball_y), 25, (0, 255, 0), 2) # Outer ring

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Titik 8 adalah ujung jari telunjuk
                index_tip = hand_landmarks.landmark[8]
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)

                # Jarak antara jari dan bola
                distance = ((ix - ball_x)**2 + (iy - ball_y)**2)**0.5
                if distance < 30:
                    score += 1
                    # Pindahkan bola ke lokasi acak baru
                    ball_x, ball_y = random.randint(50, w-50), random.randint(50, h-50)

                # Gambar titik di jari telunjuk
                cv2.circle(img, (ix, iy), 10, (255, 0, 0), cv2.FILLED)

        # Tampilkan Skor dan Waktu
        cv2.putText(img, f"SKOR: {score}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, f"WAKTU: {remaining_time}s", (w-200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        # Game Over Screen
        cv2.putText(img, "WAKTU HABIS!", (w//4, h//2), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)
        cv2.putText(img, f"SKOR AKHIR: {score}", (w//3, h//2 + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, "Tekan 'r' untuk main lagi", (w//3, h//2 + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.imshow("Energy Catch Game", img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('r'): # Reset Game
        score = 0
        start_time = time.time()

cap.release()
cv2.destroyAllWindows()