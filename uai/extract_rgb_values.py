import cv2
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


def extract_single_channel_rgb_values(image_file, coordinates):
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

        # Calculate average R value and define G and B as 0
        average_r = roi_r.mean()
        average_g = average_b = 0.0

        print(f"{('UAP' if class_id == 1 else 'UAI')} Average RGB values for region ({x_min}, {y_min}) to ({x_max}, {y_max}):")
        print(f"Average RGB: (R: {average_r:.2f}, G: {average_g:.2f}, B: {average_b:.2f})")


if __name__ == "__main__":
    files_info = [
        ("/Users/ibrahimyucel/Desktop/uai/uai/inputfiles/04uai.jpg", "/Users/ibrahimyucel/Desktop/uai/uai/inputfiles/04uai.txt"),
        ("/Users/ibrahimyucel/Desktop/uai/uai/inputfiles/10192uai.jpg", "/Users/ibrahimyucel/Desktop/uai/uai/inputfiles/10192uai.txt")
    ]

    for image_file, coord_file in files_info:
        print(f"Processing {coord_file} with {image_file}...")

        coordinates = read_coordinates(coord_file)
        extract_single_channel_rgb_values(image_file, coordinates)
