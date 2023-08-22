import bitman
import forensictools
import cv2

# This is a VERY shitty watermarking method.

def main():
    img = cv2.imread("example.png")
    manipulator = bitman.NDArraySequenceManipulator()

    marker = forensictools.ForensicMark(
        "John Doe",
        "example@example.com",
        "Copyright",
        "blah blah"
    )
    print("Writing marker...")
    img = manipulator.write_max_sequence(marker.get_data(), img)
    cv2.imwrite("example_marked.png", img)
    print("Done")


if __name__ == "__main__":
    main()