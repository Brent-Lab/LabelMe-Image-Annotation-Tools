import cv2
import imutils
import numpy as np
from U2Net import inference as u2
import tools

OUTPUT_FOLDER = '.U2Net/output/'
MODEL_NAME = 'u2net.pth'


def display_picture(img):
    cv2.imshow("Window", img)
    cv2.waitKey(0)


def get_mask_from_inference(img, pred_tensor):
    # Get numpy array from Tensor in single channel format
    pred_np = pred_tensor.squeeze().cpu().data.numpy()
    pred_np = cv2.resize(pred_np, (img.shape[1], img.shape[0]))

    # Change to correct format
    pred_np = pred_np * 255
    pred_np = pred_np.astype(np.uint8)
    pred_np[pred_np < 30] = 0
    return pred_np


def get_contours_of_largest_object(mask):
    thresh = cv2.threshold(mask, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    return max(cnts, key=cv2.contourArea)


def get_points_from_contour(c):
    points = []
    for index, point in enumerate(c):  # Every 5 points
        if index % 10 == 0:
            points.append(point[0].tolist())
    return points


def main():
    image_folder = './images/'

    inferences = u2.get_inference_from_images(MODEL_NAME, image_folder)
    for inference in inferences:
        img_dir, pred_tensor = inference
        img = cv2.imread(img_dir)

        pred_np = get_mask_from_inference(img, pred_tensor)

        c = get_contours_of_largest_object(pred_np)
        points = get_points_from_contour(c)

        cv2.drawContours(img, [c], -1, (255, 255, 255), 1)

        # json_path = tools.create_empty_labelme_json(img_dir)
        # annotation = tools.LabelMeAnnotation(json_path)
        # annotation.add_label("apple", points)
        # annotation.write_to_src()

        display_picture(img)
        display_picture(pred_np)


if __name__ == "__main__":
    main()