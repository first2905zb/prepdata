import cv2
import numpy as np
import os

# ฟังก์ชันในการเพิ่มข้อมูล
def augment_image(image):
    augmented_images = []

    # การหมุน
    rotated_90 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    rotated_180 = cv2.rotate(image, cv2.ROTATE_180)
    rotated_270 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    augmented_images.extend([rotated_90, rotated_180, rotated_270])

    # การพลิก
    flipped_horizontal = cv2.flip(image, 1)
    flipped_vertical = cv2.flip(image, 0)

    augmented_images.extend([flipped_horizontal, flipped_vertical])

    # การปรับความสว่าง
    bright = cv2.convertScaleAbs(image, alpha=1.2, beta=30)  # ปรับความสว่าง
    dark = cv2.convertScaleAbs(image, alpha=0.8, beta=-30)  # ปรับให้มืดลง

    augmented_images.extend([bright, dark])

    # การครอบตัด
    height, width = image.shape[:2]
    crop = image[int(height/4):int(3*height/4), int(width/4):int(3*width/4)]
    augmented_images.append(crop)

    return augmented_images

# กำหนด path ของ folder ที่มีภาพต้นฉบับ
input_folder = 'cap/First/images'  # เปลี่ยนให้เป็น path ของ folder ของคุณ
output_folder = 'augmented_images'
os.makedirs(output_folder, exist_ok=True)

# เริ่มต้นหมายเลขไฟล์ที่ 201
file_counter = 10

# ลูปผ่านไฟล์ใน folder
for filename in os.listdir(input_folder):
    image_path = os.path.join(input_folder, filename)
    
    # ตรวจสอบว่าเป็นไฟล์รูปภาพ (กรณีนี้ตรวจนามสกุล jpg และ png)
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image = cv2.imread(image_path)
        parts = filename.split('_')
        if image is not None:
            augmented_images = augment_image(image)

            # บันทึกภาพที่เพิ่มข้อมูลโดยเริ่มจากไฟล์ที่ 201
            for augmented_image in augmented_images:
                output_path = os.path.join(output_folder, f'{file_counter}_{parts[1]}.jpg')
                cv2.imwrite(output_path, augmented_image)
                file_counter += 1
        else:
            print(f"ไม่สามารถโหลดภาพได้: {image_path}")
    else:
        print(f"ไฟล์นี้ไม่ใช่ภาพ: {filename}")
