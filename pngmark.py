import argparse
import bitman
import forensictools
import cv2
import os

def main():
    parser = argparse.ArgumentParser(description="Extracts forensic marks from PNG images")

    parser.add_argument("image", help="Image to work on")
    parser.add_argument("-o", "--output", help="Output file, used when storing data or getting bitplanes", default="output.png")
    parser.add_argument("-b", "--bitplane", help="Bitplanes to extract, comma separated", type=str, default=None)
    parser.add_argument("-s", "--store", help="Path to file to store in image, ignored if not set", type=str, default=None)
    parser.add_argument("-r", "--retrieve", help="Should you extract data from the image", action="store_true")

    args = parser.parse_args()

    if not os.path.exists(args.image):
        print("FATAL: Image not found")
        return
    
    print("Loading image...")
    try:
        image = cv2.imread(args.image)
    except cv2.error:
        print("FATAL: Error reading image")
        return

    if args.bitplane is not None:
        # Parse bitplane string
        try:
            planes_to_extract = list(set([int(p) for p in args.bitplane.split(",")]))
        except ValueError:
            print("FATAL: Bitplanes must be integers (0-7)")
            return
        
        # Export each bitplane
        for plane in planes_to_extract:
            if plane < 0 or plane > 7:
                print("FATAL: Bitplanes must be integers (0-7)")
                return
            print(f"Extracting bitplane {plane}...")
            planeImg = forensictools.BitPlanes.get_bitplane(image, plane)

            base, ext = os.path.splitext(args.output)
            cv2.imwrite(f"{base}_plane{plane}{ext}", planeImg)
            print(f"Written to {base}_plane{plane}{ext}")
        print(f"Successfully extracted {len(planes_to_extract)} bitplanes")
        return

    if args.store is not None:
        if not os.path.exists(args.store):
            print("FATAL: File to store not found")
            return
        print("Loading file to store...")
        try:
            with open(args.store, "rb") as f:
                data = f.read()
        except IOError:
            print("FATAL: Error reading file to store")
            return
        print("Storing file...")
        manipulator = bitman.NDArraySequenceManipulator()
        try:
            image = manipulator.write_sequence(data, image)
        except Exception as e:
            print(f"FATAL: {e}")
            return
        print("Writing image...")
        try:
            cv2.imwrite(args.output, image)
        except cv2.error:
            print("FATAL: Error writing image")
            return
        print(f"Successfully stored file in {args.output}")
        return

    if args.retrieve:
        print("Retrieving data...")
        manipulator = bitman.NDArraySequenceManipulator()
        try:
            data = manipulator.read_sequence(image)
        except Exception as e:
            print(f"FATAL: {e}")
            return
        print("Writing data...")
        try:
            with open(args.output, "wb") as f:
                f.write(data)
        except IOError:
            print("FATAL: Error writing data")
            return
        print(f"Successfully retrieved data to {args.output}")
        
        return
    
if __name__ == "__main__":
    main()