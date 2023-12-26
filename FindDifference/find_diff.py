import os, time
import pyautogui
from PIL import ImageChops

# 원본 이미지
# 시작좌표 (1030, 64)

# 비교대상 이미지
# 시작 좌표 (1030, 761)

# 이미지 크기
# width 847
# height 678

width, height = 865, 693
x_pos = 1030

src = pyautogui.screenshot(region=(x_pos, 64, width, height))
src.save('src.jpg')

dest = pyautogui.screenshot(region=(x_pos, 761, width, height))
dest.save('dest.jpg')

diff = ImageChops.difference(src, dest)
diff.save('diff.jpg')

# 파일 생성 대기
while not os.path.exists('diff.jpg'):
    time.sleep(1)

import cv2
src_img = cv2.imread('src.jpg')
dest_img = cv2.imread('dest.jpg')
diff_img = cv2.imread('diff.jpg')

gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
gray = (gray > 25) * gray
contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

COLOR = (0, 200, 0)
for cnt in contours:
    if cv2.contourArea(cnt) > 100:
        x, y, width, height = cv2.boundingRect(cnt)
        cv2.rectangle(src_img, (x, y), (x + width, y + height), COLOR, 2)
        cv2.rectangle(dest_img, (x, y), (x + width, y + height), COLOR, 2)
        cv2.rectangle(diff_img, (x, y), (x + width, y + height), COLOR, 2)

cv2.imshow('src', src_img)
cv2.imshow('dest', dest_img)
cv2.imshow('diff', diff_img)

cv2.waitKey(0)
cv2.destroyAllWindows()