import os
import json
import cv2

def copy_image(filename, idx):
    image = cv2.imread(filename)
    cv2.imwrite(f"test/{idx}.jpg", image)

def find_image(filepath, filename):

    with open(filepath, 'r') as f:
        data = json.load(f)

    for idx in range(len(data)):
        if data[idx]['img_name'] == filename:
            return data[idx]
        
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

    for i in os.listdir():
        if os.path.isdir(i) and i != 'test':
            directories.append(i)

    directories = sorted(directories, key=lambda x: int(x.split('_')[0]))
    json_data = []

    for dir in directories:
        images = os.listdir(dir)
        images = sorted(images, key=lambda x: float('inf') if x == 'annotations.json' else int(x.split('.')[0])) # sort images
        print("Current directory: \n", dir)
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
