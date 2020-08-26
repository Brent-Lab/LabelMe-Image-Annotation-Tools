# LabelMe-Image-Annotation-Tools
LabelMe Image Annotation Tools is an application meant to be paired with the LabelMe application to
easily process the annotations and images.

LabelMe: https://github.com/wkentaro/labelme

## Installation
- Make sure to have Anaconda installed with python version 3.7.
- Clone the repository
```
git clone https://github.com/WafflesAreFriends/LabelMe-Image-Annotation-Tools.git
```
### Easy installation
- Run the following in the command line from the main directory to setup the environment.
    - Note that doing this will automatically install LabelMe as well.
```
conda env create -f environment.yml
```
### Manual Installation
- Install LabelMe from the following link: https://github.com/wkentaro/labelme
- Install the following dependencies:
```
pip install piexif
```


## Usage
Activate the python environment with the needed dependencies installed.

Run the following code to turn on the application.
```
python annotation_tool
```
