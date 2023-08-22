import cv2
import numpy as np
import bitman

def main():
    img = cv2.imread("example_marked.png")
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), np.uint8).flatten()

    manipulator = bitman.BitManipulator()

    for i, px in enumerate(img.flatten()):
        blank_image[i] = 255 if manipulator.LSB_is_set(px) else 0
    
    blank_image = blank_image.reshape(img.shape)
    cv2.imwrite("example_marked_lsb_plane.png", blank_image)

if __name__ == "__main__":
    main()