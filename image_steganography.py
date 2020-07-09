#Import the Libraries including cv2, numpy, types....

import cv2 
import numpy as np
import types
from termcolor import*
from google.colab.patches import cv2_imshow 

    #Function to convert secret message to binary form by checking its type
def Convert_secret_message_To_Binary(secret_message):
  if (type(secret_message) == str):     #If type of the secret message is string then do the following
    return ''.join([ format(ord(i), "08b") for i in secret_message ])
  elif (type(secret_message) == bytes or type(secret_message) == np.ndarray): #If type is in byte or in array then do the following
    return [ format(i, "08b") for i in secret_message ]
  elif (type(secret_message) == int or type(secret_message) == np.uint8): #If type is in int or uint8 then do the following
    return format(secret_message, "08b")
  else:                                             #else raise error of type
    raise TypeError("The input type entered by user is not supported.")

# Function to hide the secret message into the image
def hide_secret_Data(image, secret_message):
  # calculate the maximum bytes to encode
  number_of_bytes = image.shape[0] * image.shape[1] * 3 // 8
  print("  Maximum bytes to encode:   ", number_of_bytes)

  #Check if the number of bytes to encode is less than the maximum bytes in the image
  if (len(secret_message) > number_of_bytes):
      raise ValueError("Error has been found: insufficient bytes, need bigger image or less data to process!!")
  
  secret_message += "#####" # you can use any string as the delimeter

  data_index = 0
  
  # convert input data to binary format using Convert_secret_message_To_Binary() fucntion
  binary_secret_message = Convert_secret_message_To_Binary(secret_message)

  message_length = len(binary_secret_message) #Find the length of data that needs to be hidden
  for values in image:
      for pixels in values:
          # convert Red, Green, Blue  values to binary format
          red, green, blue = Convert_secret_message_To_Binary(pixels)
          # modify/Update the least significant bit (LSB) only if there is still data to store
          if (data_index < message_length):
              # hide the data into least significant bit(LSB) of red pixel
              pixels[0] = int(red[:-1] + binary_secret_message[data_index], 2)
              data_index += 1
          if (data_index < message_length):
              # hide the data into least significant bit(LSB) of green pixel
              pixels[1] = int(green[:-1] + binary_secret_message[data_index], 2)
              data_index += 1
          if (data_index < message_length):
              # hide the data into least significant bit(LSB) of  blue pixel
              pixels[2] = int(blue[:-1] + binary_secret_message[data_index], 2)
              data_index += 1
          # if data is encoded, just break out of the loop
          if (data_index >= message_length):
              break

  return image

#function to show the image in which the data to be hidden..
def show_Data_image(image):

  binary_data = ""  # a simple string
  for values in image:
      for pixels in values:
        # convert the red, green and blue values into the binary format
          red, green, blue = Convert_secret_message_To_Binary(pixels) 
          # extracting data from the least significant bit(LSB) of red pixel
          binary_data += red[-1] 
          # extracting data from the least significant bit(LSB) of green pixel
          binary_data += green[-1]
          # extracting data from the least significant bit(LSB) of blue pixel
          binary_data += blue[-1] 
  # split the message by 8-bits
  all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
  # convert from bits to characters
  decoded_data = ""
  for byte in all_bytes:
      decoded_data += chr(int(byte, 2))
      if decoded_data[-5:] == "#####": #check if we have reached the delimeter which is "#####"
          break
  #print(decoded_data)
  return decoded_data[:-5] #remove the delimeter to show the original hidden message

  # function to encode the secret message into the image..
def encode_secret_message_to_image(): 

  cprint("                                                              ***** Enter the image name (with its Extension)*****                                                     \n\n",'yellow')
  image_name = input() 
  image = cv2.imread(image_name) # Read the input image using OpenCV-Python.
  #It is a library of Python bindings designed to solve computer vision problems. 
  
  #details of the image
  print("The shape of the image is: ",image.shape) #check the shape of image to calculate the number of bytes in it
  print("\n\n")
  cprint(" ***** The original image is as shown below *****  \n\n\n",'blue')
  resized_image = cv2.resize(image, (1000, 500)) #resize the image as per your requirement
  cv2_imshow(resized_image) #display the image
  print("\n\n")
  
  cprint("                                                             ***** Enter the message to be encoded into the image *****                                                 \n\n",'yellow')
  data = input() 
  if (len(data) == 0): 
    raise ValueError('Data is empty')
  
  cprint("                                                            ***** Enter the name of new encoded image(with extension) ******                                              \n\n ",'yellow')
  filename=input()
  print("\n\n")
  encoded_image = hide_secret_Data(image, data) # call the hideData function to hide the secret message into the selected image
  cv2.imwrite(filename, encoded_image)

def decode_secret_message_from_image():
  # read the image that contains the hidden image
  cprint("                                                           ***** Enter the name of the steganographed image that you want to decode (with extension) *****                     \n\n",'yellow')
  image_name = input() 
  image = cv2.imread(image_name) #read the image using cv2.imread() 

  cprint("***** The Steganographed image is as shown below ****** \n\n ",'yellow')
  resized_image = cv2.resize(image, (1000, 500))  #resize the original image as per your requirement
  cv2_imshow(resized_image) #display the Steganographed image
    
  text = show_Data_image(image)
  return text

# Image Steganography         
def Steganography(): 
    print("\n\n")
    cprint("                                                                ***          IMAGE STEGANOGRAPHY          ***                                             \n\n ",'blue')
    cprint("                                                 1. Encode the data into Image                    2. Decode the data from Image                      \n\n\n",'green')
    cprint("                                                                  ***** Enter Your Input that You want *****                                                     \n\n  ",'yellow')
    a = input()
    userinput = int(a)
    if (userinput == 1):
      cprint("\n\n                                                                                Encoding.......                                        \n ",'blue')
      encode_secret_message_to_image() 
          
    elif (userinput == 2):
      cprint("\n\n                                                                                 Decoding.......                                         \n", 'blue') 

      print("\n\nDecoded message is : " + decode_secret_message_from_image()) 
    else: 
        raise Exception("Enter correct input") 
          
Steganography() #encode image
