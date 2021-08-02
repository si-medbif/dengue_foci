# Image segmentation for dengue virus foci detection in focus forming assay
<img src="https://github.com/si-medbif/dengue_foci/blob/8e39c289992df571dc877bbf3a45a8527c5a889f/workflow.png" style="max-width: 60%;" align="center" />

## About
A project aims to count numbers and measure areas of dengue foci in focus forming assay (FFA) image by computer vision technology `(OpenCV)`. The specificity of the developed foci detection program is 93.75%. The R-value of the correlation between the foci measured by program and human-measured is 0.993. However, the number measured by the program significantly less than the average human-measured is 2.4 foci.

Project information: [ https://github.com/si-medbif/dengue_foci/PDF/Project information.pdf](https://github.com/si-medbif/dengue_foci/blob/dffa6158f7201189d605cebe3bd88061e2beb717/PDF/Project%20information.pdf)
## User manual
Instructions for installation and usage can be followed by this link: [https://github.com/si-medbif/dengue_foci/PDF/Program guidebook demo version.pdf](https://github.com/si-medbif/dengue_foci/blob/8a031d0b03dee3857547c57965aeb27fe2aea0df/PDF/Program%20guidebook%20demo%20version.pdf)
    
## Requirements
1. You need install `Python >= 3.9.6`
2. Library requirement

        numpy == 1.21.0
        pandas == 1.3.0
        statistics == 1.0.3.5
        opencv-python == 4.5.3.56
        configparser == 5.0.2




## Installation
1. clone this project followed by Github CLI command: 

        gh repo clone si-medbif/dengue_foci
   or download project `zip` file
2. Open a command prompt or terminal for `CD` command to change the directory to project location.
3. Installation with pip allows the usage of the install command:

        pip install -r requirements.txt
   
## Step for work
1. create input folder and output folder
    
        Input                       # input folder
        │
        ├── Plate_1                 # Plate 1 folder
        │   ├── A1.jpg              # FFA image that would like to detect foci
        │   ├── A2.jpg
        │   ├── A3.jpg 
        │   └── ...
        ├── Plate_2                 # Plate 2 folder
        │   ├── A1.jpg              # FFA image that would like to detect foci
        │   ├── A2.jpg
        │   ├── A3.jpg 
        │   └── ...
        └── ...
        
        Outout                      # output folder
        │
        └── ...
2. set parameter in `config.ini`

        [Paths]
        input_image_folder = #location path of input folder that you create in step 1
        output_image_folder = #location path of output folder that you create in step 1

        [Parameters]
        ; default parameter: margin = 0 pixel
        border_margin = 0
        ; set min pixel area for foci detction: 9 pixels is default parameter
        min_foci_size = 9

4. run the `app_window.py` file
5. after the program running has finished

        Outout                            # output folder result
        │
        ├── Plate_1_year-month-day_hours_minutes_seconds
        │   │
        │   ├── binary_image              # binary_image folder
        │   │   ├── A1.jpg
        │   │   ├── A2.jpg
        │   │   └── ...
        │   │
        │   ├── foci_description          # foci_description folder
        │   │   ├── A1.csv
        │   │   ├── A2.csv
        │   │   └── ...
        │   │
        │   ├── raw_box                   # raw_box folder
        │   │   ├── A1.jpg
        │   │   ├── A2.jpg
        │   │   └── ...
        │   │
        │   ├── raw_number                # raw_number folder
        │   │   ├── A1.jpg
        │   │   ├── A2.jpg
        │   │   └── ...
        │   └── foci_count_result.csv
        │
        └── Plate_2_year-month-day_hours_minutes_seconds
        │   │
        │   └── ...
        └── ...
