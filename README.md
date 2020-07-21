# LabelMe-Image-Annotation-Tools
Useful tools for creating image annotations through LabelMe

## Installation

- Make sure you have Anaconda, pip, and LabelMe installed for python 3.7.
- Run the code below to copy the code and enter it:
```
git clone https://github.com/WafflesAreFriends/LabelMe-Image-Annotation-Tools.git
cd LabelMe-Image-Annotation-Tools
```
- Activate the environment with LabelMe already installed then run the following code to install dependencies.
```
pip install piexif
conda install opencv
```

## Usage

Before usage, move the folder with images and LabelMe annotations into the project directory. Please have all the images in the direct subdirectory of the folder. This does not support nested folders yet.

### Quick use
Run the the following code in the same directory replacing 'FOLDERNAME' with the name of your folder. This can be done easily by typing the start of the folder name and then hitting tab.
```
sh run_sequence.sh FOLDERNAME
```

This will run the required scripts which will rename the images and json files, create a coco format annotation json file inside the target folder, and append EXIF data to the images according to the labels attached to it.
