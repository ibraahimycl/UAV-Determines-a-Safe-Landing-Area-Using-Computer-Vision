"""import cv2
import os


def read_coordinates(coord_file):
    with open(coord_file, 'r') as file:
        lines = file.readlines()
    coordinates = {}
    for i, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) >= 5:
            class_id = int(parts[0])
            coordinates[i] = [class_id] + [float(p) for p in parts[1:]]
    return coordinates


def process_image(image_file, coordinates):
    image = cv2.imread(image_file)
    if image is None:
        raise ValueError(f"Could not read image at {image_file}")

    height, width = image.shape[:2]

    for id, vals in coordinates.items():
        class_id = vals[0]
        left, top, right, bottom = vals[1:]  # Normalized coordinates

        x_min = int(left * width - (right * width) / 2)
        x_max = int(left * width + (right * width) / 2)
        y_min = int(top * height - (bottom * height) / 2)
        y_max = int(top * height + (bottom * height) / 2)

        # Extract ROI using red channel
        b, g, r = cv2.split(image)
        roi_r = r[y_min:y_max, x_min:x_max]

        # Extract ROI using grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        roi_gray = gray_image[y_min:y_max, x_min:x_max]

        # Show images
        cv2.imshow('Red Channel ROI', roi_r)
        cv2.imshow('Grayscale ROI', roi_gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    coord_file = "/Users/ibrahimyucel/Desktop/uai/uai/inputfiles/10192uai.txt"
    image_file = "/Users/ibrahimyucel/Desktop/uai/uai/inputfiles/10192uai.jpg"

    coordinates = read_coordinates(coord_file)
    process_image(image_file, coordinates)
"""




