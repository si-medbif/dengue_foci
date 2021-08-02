# import module
from foci_detection import *
from configparser import ConfigParser
import logging
from datetime import datetime

# =================== Load the configuration file ===================

parser = ConfigParser()
ini_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.ini')
parser.read(ini_path)

# configuration infomation
input_path = parser.get('Paths','input_image_folder')
output_path = parser.get('Paths','output_image_folder')
margin = parser.getint('Parameters','border_margin')
min_pixel = parser.getint('Parameters','min_foci_size')

# =================== timestamp ===================
dt_object = datetime.now()

# =================== loging file ===================

def my_custom_logger(logger_name, level=logging.INFO):
    """
    Method to return a custom logger with the given name and level
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    format_string = ('%(asctime)s, %(levelname)s, %(filename)s, %(message)s')
    log_format = logging.Formatter(format_string)
    # Creating and adding the console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    # Creating and adding the file handler
    file_handler = logging.FileHandler(logger_name, mode='a')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    return logger

# =================== make directory ====================

for plate in os.listdir(input_path):
  print(plate)
  # make new directory follow plate name
  plate_path = os.path.join(input_path,plate)
  plate_name = str(plate)+'_'+str(dt_object.year)+'-'+str(dt_object.month)+'-'+str(dt_object.day)+'_'+str(dt_object.hour)+'_'+str(dt_object.minute)+'_'+str(dt_object.second)
  plate_path_result = os.path.join(output_path,plate_name)

  info_file = os.path.join(plate_path_result,'foci_description')
  binary_box_path = os.path.join(plate_path_result,'binary_image')
  raw_box_path = os.path.join(plate_path_result,'raw_box')
  raw_number = os.path.join(plate_path_result,'raw_number')

  # try:
  os.mkdir(plate_path_result)
  os.mkdir(info_file)
  os.mkdir(binary_box_path)
  os.mkdir(raw_box_path)
  os.mkdir(raw_number)
  # except:
  #   print("error: can't make directory")

  # log information
  file_log_name = os.path.join(plate_path_result,'logfile.log')
  logger = my_custom_logger(file_log_name)

  # =================== setting ===========================

  imagesize = 500 # 500 pixels
  number_foci = list()
  radius = list()

  # =================== find radius  ======================

  print('find radius process...')
  for image in os.listdir(plate_path):
    print('find radius image > ', image)
    img_path = os.path.join(plate_path,image)
    img = cv2.imread(img_path, flags = cv2.IMREAD_GRAYSCALE)
    inner_border = border_detection(img, imagesize, 0) # set margin = 0
    if str(inner_border) == 'not circle detected':
      continue
    else:
      a,b,r = inner_border
      radius.append(r)

  med_r = radius_selector(radius)

  # =================== foci detection  ===================

  print('foci detection process...')
  for image in os.listdir(plate_path):
    try:
      # print('image > ', image)
      img_path = os.path.join(plate_path,image)
      img = cv2.imread(img_path, flags = cv2.IMREAD_GRAYSCALE)
      inner_border = border_detection(img, imagesize, margin) # user can set this margin
      img_crop = crop_inner_circle(img, imagesize, inner_border,med_r)
        
      # detection
      binary_img = binary_Threshold(img_crop,inner_border)
      box = foci_detection(binary_img, inner_border, min_pixel)

      # count number of Foci
      id = plate+'_'+image[:-4]
      number_foci.append([id,foci_count(box)])
      foci_info = num_pixels(box)
      img_csv = image[:-4]+".csv"
      foci_info.to_csv(os.path.join(info_file,img_csv))

      #image result
      result_binary_mask = foci_filter(binary_img,imagesize,box)
      result_raw_box = foci_draw_detected(img_crop,imagesize,box)
      result_raw_number = write_numberOfFoci(img_crop,imagesize,box)

      #save file
      os.chdir(binary_box_path)
      cv2.imwrite(image, result_binary_mask)
      os.chdir(raw_box_path)
      cv2.imwrite(image, result_raw_box)
      os.chdir(raw_number)
      cv2.imwrite(image, result_raw_number)

      # foci information log status
      logger.info('{}, {}, foci detected: success'.format(plate,image))

    except:
      logger.error('{}, {}, foci detected: success'.format(plate,image))
      

  foci_count_result = pd.DataFrame(number_foci, columns=["id", "foci count"])
  foci_count_result.to_csv(os.path.join(plate_path_result,'foci_count_result.csv'))
  print('find detection completed!')


