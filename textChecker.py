from csv import reader
import webbrowser
import pytesseract
import io
import requests
from PIL import Image, ImageEnhance 
from IPython.display import display
import PIL.ImageOps 
import json
from urllib import parse, request


#get search term from user
searchTerm = input('enter search term\n')

#uses the search term entered by user, gets 5 gif urls from the JSON data and stores them in a List
def getGiphys (Term):
  url = "http://api.giphy.com/v1/gifs/search"
  params = parse.urlencode({
    "q": Term,
    "api_key": "api key here",
    "limit": "5"
  })

  urlList = []

  with request.urlopen("".join((url, "?", params))) as response:
    data = json.loads(response.read())

  #uncomment to see ALL json data
  #print(json.dumps(data, sort_keys=True, indent=4))
  
  urlList.append(data['data'][0]['images']['original']['url'])
  urlList.append(data['data'][1]['images']['original']['url'])
  urlList.append(data['data'][2]['images']['original']['url'])
  urlList.append(data['data'][3]['images']['original']['url'])
  urlList.append(data['data'][4]['images']['original']['url'])

  
  return(urlList)


#storing getGiphy function results in List
L = getGiphys(searchTerm)
L2 = []


#loop through list checking each frame of each gif in the list
#if text is found in frame, it is displayed along with the frame it was found on 
#if a gif makes it through the loops with no text found on any frame, it will be stored in L2 to be displayed later
length = len(L)
for i in range(length):
    url = requests.get(L[i])
    img = Image.open(io.BytesIO(url.content))
    textFound = False
    for frame in range(0,img.n_frames):
        img.seek(frame)

        #image enhancements to make it easier for OCR
        imgrgb = img.convert('RGB')
        imgrgb = PIL.ImageOps.invert(imgrgb)
        enhancer = ImageEnhance.Brightness(imgrgb)
        imgrgb = enhancer.enhance(10.8)
        enhancer = ImageEnhance.Contrast(imgrgb)
        imgrgb = enhancer.enhance(10.0)
        imgrgb = imgrgb.convert('L')
        text = pytesseract.image_to_string(imgrgb,config="-c tessedit_char_whitelist=01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

        #check frames for text
        if len(text) > 3:
            print("Frame: ", frame+1)
            print(text)
            print("======================\n")
            textFound = True
            break
    #add clean gifs to list    
    if textFound == False:
        L2.append(L[i])


#opens gifs that have no text
length2 = len(L2)
for j in range(length2):
  webbrowser.open(L2[j])


#shows all 5 gif URLs if you want to double check 
#print(L)
  

        
            
        
        

        