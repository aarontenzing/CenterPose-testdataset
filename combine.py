import os
import json
import cv2

def copy_image(filename, idx):
    image = cv2.imread(filename) # read image
    cv2.imwrite(f"test/{idx}.jpg", image) # save image in test directory

def find_image(filepath, filename):

    # read json file in directory
    with open(filepath, 'r') as f:
        data = json.load(f)

    idx = filename.split('.')[0] # remove extension
    return data[int(idx)] # return annotation
        
def write_image(data):

    with open('test/anno.json', 'w') as file:
        json.dump(data, file, indent=2) # dict to array (json)

def normalize_dimensions(dimensions):
    dimensions[0] /= dimensions[1]
    dimensions[2] /= dimensions[1]
    dimensions[1] = 1
    return dimensions

def main(): 
    img_id = 0
    directories = []

    # get all directories
    # Get the current working directory
    current_directory = os.getcwd()

    # List directories excluding 'test' and sort numerically
    directories = [d for d in os.listdir(current_directory) 
                if os.path.isdir(os.path.join(current_directory, d)) 
                and d.isdigit()]
    directories = sorted(directories, key=lambda x: int(x))
    
    json_data = []

    for dir in directories:
        print("Current directory: \n", dir)
        images = os.listdir(dir)
        images = sorted(images, key=lambda x: float('inf') if x == 'annotations.json' else int(x.split('.')[0])) # list of images   
        print("Images in dir: \n", images)
        
        for img in images:
            if img.split('.')[-1] == 'jpg':
                path = dir + "/annotations.json"
                copy_image(dir + '/' + img, img_id)
                img_data = find_image(path, img) # get annotation
                dimensions = normalize_dimensions(img_data["dimensions"])
    
                data = {
                    "image" : img_id,
                    "whd" : dimensions,
                    "projection" : img_data["projection"],
                    "world" : img_data["world"]
                }
                json_data.append(data)
                img_id += 1 # increment image id
    
    write_image(json_data)
    print("Done!")

if __name__ == '__main__':
    main()
