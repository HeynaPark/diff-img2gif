import os
import cv2
import math
from PIL import Image

points = []


def click_and_calculate_distance(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

        # When two points are selected, calculate the distance and display it
        if len(points) == 2:
            distance = math.sqrt(
                (points[1][0] - points[0][0])**2 + (points[1][1] - points[0][1])**2)
            print(f"Pixel distance: {distance:.2f}")
            points = []  # Reset the points list for next selection


def save_difference_image(current_image, next_image, output_path):
    difference_image = cv2.absdiff(current_image, next_image)
    cv2.imwrite(output_path, difference_image)


def show_images(image_files):
    current_index = 0
    total_images = len(image_files)

    while True:
        image_file = image_files[current_index]
        image_name = os.path.basename(image_file)

        print(f"({current_index + 1}/{total_images}) {image_name}")

        image = cv2.imread(image_file)
        scale_percent = 50
        image = cv2.resize(image, None, fx=scale_percent/100,
                           fy=scale_percent/100, interpolation=cv2.INTER_AREA)
        cv2.imshow("Image", image)

        key = cv2.waitKey(0)

        if key == ord('d'):  # 방향키 왼쪽
            current_index = (current_index - 1) % total_images
            print('left')
        elif key == ord('f'):  # 방향키 오른쪽
            current_index = (current_index + 1) % total_images
            print('right')
        elif key == ord('w'):  # 'w' 키 누를 때
            if current_index + 1 < total_images:
                next_image = cv2.imread(image_files[current_index + 1])
                next_image = cv2.resize(next_image, None, fx=scale_percent/100,
                                        fy=scale_percent/100, interpolation=cv2.INTER_AREA)
                output_path = f"diff_{image_name}_to_{os.path.basename(image_files[current_index + 1])}.png"
                save_difference_image(image, next_image, output_path)
                print(f"Difference image saved as {output_path}")
        elif key == 27:  # ESC 키
            break

    cv2.destroyAllWindows()


def show_and_calc_distance(image_files):

    current_index = 0
    total_images = len(image_files)
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Image", click_and_calculate_distance)

    while True:
        image_file = image_files[current_index]
        image_name = os.path.basename(image_file)

        print(f"({current_index + 1}/{total_images}) {image_name}")

        image = cv2.imread(image_file)
        scale_percent = 50
        image = cv2.resize(image, None, fx=scale_percent/100,
                           fy=scale_percent/100, interpolation=cv2.INTER_AREA)
        cv2.imshow("Image", image)

        key = cv2.waitKey(0)

        if key == ord('d'):  # 방향키 왼쪽
            current_index = (current_index - 1) % total_images
            print('left')
        elif key == ord('f'):  # 방향키 오른쪽
            current_index = (current_index + 1) % total_images
            print('right')
        elif key == 27:  # ESC 키
            break

    cv2.destroyAllWindows()


def conver_gif(img_list):
    images = [Image.open(filename) for filename in img_list]

    first_image = images[0]
    output_path = 'output.gif'

    first_image.save(output_path, save_all=True,
                     append_images=images[1:], optimize=False, duration=200, loop=0)

    print('gif making done.')


if __name__ == "__main__":

    mode = 'toGIF'

    if mode == 'RAW':
        image_folder = "D:/Project/4dgolfer/data/right"

        image_files = [os.path.join(image_folder, file) for file in os.listdir(
            image_folder) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(image_files)

        if len(image_files) == 0:
            print("폴더에 이미지 파일이 없습니다.")
        else:
            show_images(image_files)

    elif mode == 'DIFF':
        diff_folder = 'output/right'
        diff_files = [os.path.join(diff_folder, file) for file in os.listdir(
            diff_folder) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if len(diff_files) == 0:
            print("폴더에 이미지 파일이 없습니다.")
        else:
            show_and_calc_distance(diff_files)

    elif mode == 'toGIF':
        diff_folder = 'output/center'
        diff_files = [os.path.join(diff_folder, file) for file in os.listdir(
            diff_folder) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

        conver_gif(diff_files)

    else:
        print('wrong input')
