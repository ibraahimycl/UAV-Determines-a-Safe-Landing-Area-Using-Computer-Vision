import numpy as np
import cv2
import sys
import os
np.set_printoptions(threshold=sys.maxsize,linewidth=sys.maxsize)

def check_coordinate_intersection(etiketler, image_width=1920, image_height=1080):
    """Check if UAP/UAI coordinates intersect with other objects
    
    Returns:
        tuple: (has_intersection, is_uap, coordinates, landing_suitable)
        - has_intersection: True if UAP/UAI intersects with other objects
        - is_uap: True if UAP (class_id=1), False if UAI (class_id=0)
        - coordinates: [x1, x2, y1, y2] if intersection found, None otherwise
        - landing_suitable: True if landing area is suitable (no intersections)
    """
    class_box = {}
    flag = 0
    
    # First find UAP (class_id=1) and UAI (class_id=0) coordinates
    for key, value in etiketler.items():
        class_id = int(value[0])
        if class_id in [0, 1]:  # UAP or UAI
            left, top, right, bottom = value[1], value[2], value[3], value[4]
            x1 = int(left * image_width - (right * image_width) / 2)
            x2 = int(left * image_width + (right * image_width) / 2)
            y1 = int(top * image_height - (bottom * image_height) / 2)
            y2 = int(top * image_height + (bottom * image_height) / 2)
            
            if class_id == 1:  # UAP
                class_box['uap'] = [x1, x2, y1, y2]
                flag = 1
            elif class_id == 0:  # UAI
                class_box['uai'] = [x1, x2, y1, y2]
                flag = 1
    
    if flag == 0:
        return False, None, None, False
    
    # Check if UAP/UAI intersects with other objects (class_id not 0 or 1)
    for key, value in etiketler.items():
        class_id = int(value[0])
        if class_id in [0, 1]:  # Skip UAP and UAI
            continue
            
        left, top, right, bottom = value[1], value[2], value[3], value[4]
        x1 = int(left * image_width - (right * image_width) / 2)
        x2 = int(left * image_width + (right * image_width) / 2)
        y1 = int(top * image_height - (bottom * image_height) / 2)
        y2 = int(top * image_height + (bottom * image_height) / 2)
        
        # Check intersection with UAP
        if 'uap' in class_box:
            uap_coords = class_box['uap']
            if ((x1 >= uap_coords[0] and x2 <= uap_coords[1]) and 
                (y1 >= uap_coords[2] and y2 <= uap_coords[3])) or (
                ((uap_coords[0] <= x1 <= uap_coords[1]) or 
                 (uap_coords[0] <= x2 <= uap_coords[1])) and 
                ((uap_coords[2] <= y1 <= uap_coords[3]) or 
                 (uap_coords[2] <= y2 <= uap_coords[3]))):
                return True, True, uap_coords, False  # UAP with intersection - landing not suitable
        
        # Check intersection with UAI
        if 'uai' in class_box:
            uai_coords = class_box['uai']
            if ((x1 >= uai_coords[0] and x2 <= uai_coords[1]) and 
                (y1 >= uai_coords[2] and y2 <= uai_coords[3])) or (
                ((uai_coords[0] <= x1 <= uai_coords[1]) or 
                 (uai_coords[0] <= x2 <= uai_coords[1])) and 
                ((uai_coords[2] <= y1 <= uai_coords[3]) or 
                 (uai_coords[2] <= y2 <= uai_coords[3]))):
                return True, False, uai_coords, False  # UAI with intersection - landing not suitable
    
    # If we get here, we found UAP/UAI but no intersections - landing is suitable
    if 'uap' in class_box:
        return False, True, class_box['uap'], True  # UAP without intersection
    if 'uai' in class_box:
        return False, False, class_box['uai'], True  # UAI without intersection
    
    return False, None, None, False

def get_coordinates(txt_path, image_width=1920, image_height=1080):
    """Get coordinates from model detection or determine if image processing is needed
    
    Returns:
        tuple: (use_model, is_uap, coordinates, landing_suitable)
        - use_model: True if model detection should be used, False for image processing
        - is_uap: True if UAP (class_id=1), False if UAI (class_id=0)
        - coordinates: [x1, x2, y1, y2] if model detection, None if image processing
        - landing_suitable: True if landing area is suitable (no intersections)
    """
    try:
        with open(txt_path, "r") as file:
            content = file.readlines()
            if not content:
                raise ValueError(f"Empty coordinate file: {txt_path}")
            
            # Read all lines and store in dictionary
            etiketler = {}
            for i, line in enumerate(content):
                bilgi = line.strip().split()
                if len(bilgi) >= 5:
                    etiketler[i] = [float(x) for x in bilgi]
            
            # Check for intersections
            has_intersection, is_uap, coords, landing_suitable = check_coordinate_intersection(etiketler, image_width, image_height)
            
            if coords is None:
                raise ValueError(f"No UAP (class_id=1) or UAI (class_id=0) coordinates found in {txt_path}")
            
            # If there's an intersection, use model detection
            # If no intersection, use image processing (return None for coordinates)
            return has_intersection, is_uap, coords if has_intersection else None, landing_suitable
            
    except Exception as e:
        raise ValueError(f"Error reading coordinates from {txt_path}: {str(e)}")

def process_image(img_path, coord_txt_path, uap_threshold=127):
    """Process image using either model detection or image processing
    
    Args:
        img_path: Path to the image file
        coord_txt_path: Path to the coordinate text file
        uap_threshold: Threshold value for UAP images (default: 127)
    """
    # Read and validate image
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not read image at {img_path}")
    
    # Get image dimensions
    height, width = img.shape[:2]
    
    # Get coordinates and determine processing method
    use_model, is_uap, coords, landing_suitable = get_coordinates(coord_txt_path, width, height)
    
    if use_model:
        # Use model detection coordinates
        x_min, x_max, y_min, y_max = coords
        print(f"Using model detection for {'UAP' if is_uap else 'UAI'} (intersection found)")
        print(f"Landing area is {'NOT ' if not landing_suitable else ''}suitable")
    else:
        # Use image processing coordinates
        if not is_uap:  # UAI
            x_min, x_max, y_min, y_max = 744, 896, 470, 620  # UAI default
            print("Using image processing for UAI (no intersection)")
        else:  # UAP
            x_min, x_max, y_min, y_max = 775, 925, 500, 644  # UAP default
            print("Using image processing for UAP (no intersection)")
        print("Landing area is suitable (no objects detected in area)")
    
    if not is_uap:  # UAI
        # UAI processing - use red channel
        b, g, r = cv2.split(img)
        processed_img = r
        # UAI thresholding (fixed at 140)
        kordinata_gore = processed_img[y_min:y_max, x_min:x_max]
        kordinata_gore[kordinata_gore < 140] = 0
        kordinata_gore[kordinata_gore >= 140] = 255
    else:  # UAP
        # UAP processing - use grayscale
        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # UAP thresholding (adjustable)
        kordinata_gore = processed_img[y_min:y_max, x_min:x_max]
        _, kordinata_gore = cv2.threshold(kordinata_gore, uap_threshold, 255, cv2.THRESH_BINARY)
    
    return kordinata_gore, (x_min, x_max, y_min, y_max), is_uap, use_model, landing_suitable

def analyze_image(blackandwhite):
    top_index_list = []
    for i in range(0, blackandwhite.shape[1]):
        row_i = 0
        for out_value in blackandwhite[:,i]:
            total_in_values = 0
            if out_value == 255:
                for in_value in blackandwhite[row_i:row_i+5,i]:
                    if in_value==255:
                        total_in_values+=1

            if total_in_values > 4:
                top_index_list.append([row_i, i])
                break

            row_i+=1

    down_index_list = []
    for i in range(0, blackandwhite.shape[1]):
        row_i = blackandwhite.shape[0] - 1
        for out_value in blackandwhite[::-1, i]:
            total_in_values = 0
            if out_value == 255:
                for in_value in blackandwhite[row_i-5:row_i, i]:
                    if in_value == 255:
                        total_in_values += 1

            if total_in_values > 4:
                down_index_list.append([row_i, i])
                break

            row_i -= 1

    zipped_indexes = zip(top_index_list, down_index_list)

    total_white = 0
    total_black = 0
    total_pixels = 0
    for top, down in zipped_indexes:
        for value in blackandwhite[top[0]:down[0],top[1]]:
            if value == 255:
                total_white += 1
            if value == 0:
                total_black += 1
            total_pixels += 1

    return {
        "total_pixels": total_pixels,
        "total_white": total_white,
        "total_black": total_black,
        "black_ratio": total_black/total_pixels if total_pixels > 0 else 0
    }

def process_single_image(image_path, coord_path, uap_threshold=127):
    """Process a single image with its coordinates
    
    Args:
        image_path: Path to the image file
        coord_path: Path to the coordinate file
        uap_threshold: Threshold value for UAP images (default: 127)
    """
    # Read and validate image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    # Get image dimensions
    height, width = img.shape[:2]
    
    # Read coordinate file to determine if UAP or UAI
    try:
        with open(coord_path, "r") as file:
            content = file.readlines()
            if not content:
                raise ValueError(f"Empty coordinate file: {coord_path}")
            
            # Read first line to get class_id
            first_line = content[0].strip().split()
            if len(first_line) < 5:
                raise ValueError(f"Invalid coordinate format in {coord_path}")
            
            class_id = int(first_line[0])
            if class_id not in [0, 1]:
                raise ValueError(f"Invalid class_id {class_id} in {coord_path}. Must be 0 (UAI) or 1 (UAP)")
            
            is_uap = (class_id == 1)
            
            # Read all coordinates for intersection check
            etiketler = {}
            for i, line in enumerate(content):
                bilgi = line.strip().split()
                if len(bilgi) >= 5:
                    etiketler[i] = [float(x) for x in bilgi]
            
            # Check for intersections
            has_intersection, is_uap_check, coords, landing_suitable = check_coordinate_intersection(etiketler, width, height)
            
            if has_intersection:
                print(f"\n{'UAP' if is_uap else 'UAI'} Results (Model Detection):")
                print(f"Image: {image_path}")
                print(f"Coordinates: {coord_path}")
                print(f"Landing area is NOT suitable (objects detected in area)")
                return None
            
            # If no intersection, process the specific coordinates
            if coords is None:
                raise ValueError(f"No valid coordinates found in {coord_path}")
            
            x_min, x_max, y_min, y_max = coords
            
            # Process the image based on UAP/UAI
            if is_uap:
                # UAP processing - use grayscale
                processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                kordinata_gore = processed_img[y_min:y_max, x_min:x_max]
                _, kordinata_gore = cv2.threshold(kordinata_gore, uap_threshold, 255, cv2.THRESH_BINARY)
            else:
                # UAI processing - use red channel
                b, g, r = cv2.split(img)
                processed_img = r
                kordinata_gore = processed_img[y_min:y_max, x_min:x_max]
                kordinata_gore[kordinata_gore < 140] = 0
                kordinata_gore[kordinata_gore >= 140] = 255
            
            # Analyze the image
            results = analyze_image(kordinata_gore)
            
            # Determine landing suitability based on total black pixels
            landing_suitable = results['total_black'] <= 200
            
            # Print results
            print(f"\n{'UAP' if is_uap else 'UAI'} Results (Image Processing):")
            print(f"Image: {image_path}")
            print(f"Coordinates: {coord_path}")
            print(f"Coordinates used: ({x_min}, {x_max}, {y_min}, {y_max})")
            print(f"Total pixels: {results['total_pixels']}")
            print(f"Total white pixels: {results['total_white']}")
            print(f"Total black pixels: {results['total_black']}")
            print(f"Black pixel ratio: {results['black_ratio']:.2%}")
            print(f"Landing area is {'NOT ' if not landing_suitable else ''}suitable (black pixels {'>' if not landing_suitable else '<='} 200)")
            
            # Save processed image
            output_name = f"{'uap' if is_uap else 'uai'}_processed.jpg"
            cv2.imwrite(output_name, kordinata_gore)
            
            return results
            
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")

# Main processing
try:
    # Get image and coordinate paths from user input
    image_path = input("Enter image path: ").strip()
    coord_path = input("Enter coordinate file path: ").strip()
    
    # Verify files exist
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if not os.path.exists(coord_path):
        raise FileNotFoundError(f"Coordinate file not found: {coord_path}")
    
    # Process the image
    results = process_single_image(image_path, coord_path)
    
except FileNotFoundError as e:
    print(f"File Error: {str(e)}")
    sys.exit(1)
except ValueError as e:
    print(f"Error: {str(e)}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    sys.exit(1)

# Optional: Display image

# window_name = "Processed Image"
# cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
# cv2.imshow(window_name, processed_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

