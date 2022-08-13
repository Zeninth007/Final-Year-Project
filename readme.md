# Photography Assistant
*this readme is a work in progress*
This software was done by CHAI JAY JAY for final year project. 

The main objective of this project was to help professional photographer in sorting of their images based on several criteria

Criteria includes
1. Sharpness of the image 
2. Contrasts levels

## Functions
Photography assistant primarily has 2 functions 

1. Analyze images based on contrasts and sharpness of images (the threshold are set by users)
2. Sort images based on timeline set by users

## Contrasts and Sharpness Analysis Criteria

* Contrasts
	contrast of the images are first converted into grayscale then proceeds to calculate *Standard deviation of the pixels* to output the the contrast level in integer format

* Sharpness
	sharpness of the images are measure by first converting to grayscale followed by calculatioin of the average gradient magnitude into integer format


## Processes

### Contrasts and Sharpness analysis process

1. User import the folder which contain the Jpeg images 
2. User will select the images which users would like to analyze
3. User will then input the threshold value into the prompt menu
4. System will process the images and sort into 4 different folder within the folder selected by users 

### Date Sorting process

1. User import the folder which contain the Jpeg images 
2. User will select the images which users would like to analyze
3. User will then input the date into the prompt menu
4. The system will then sort the images into 2 folders which are before and after the input date


