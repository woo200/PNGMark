import bitman
import forensictools
import cv2

def main():
    img = cv2.imread("example_marked.png")
    manipulator = bitman.NDArraySequenceManipulator()

    print("Reading image...")
    img_data = manipulator.read_sequence(img, False)
    print("Reading marker...")
    marker = forensictools.ForensicMark.get_mark(img_data)
    print(f"Found mark: {marker}")
    
if __name__ == "__main__":
    main()