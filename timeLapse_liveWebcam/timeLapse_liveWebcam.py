from ctypes import windll
import os
import urllib
import time
import datetime
import shutil
#from win32con import *
#from PixarImagePlugin import Image

DEBUG = 1;

webcamImage = "liveCapture.jpg";
updateTime = 10 * 60; #Num of seconds to update

webLinks = [ "http://www.nps.gov/webcams-crla/camerasinnott.jpg", "http://www.nps.gov/webcams-crla/camera0.jpg",
           "http://www.nps.gov/webcams-crla/cameraHQ.jpg" ];

saveImgDir = "timeLapseImages"

SPI_SETDESKWALLPAPER = 20;
SPIF_UPDATEINIFILE = 1;
SPIF_SENDWININICHANGE = 2;

def getCurrentTime():
    now = datetime.datetime.now();
    dateNtime = str(now.day)+str(now.month)+str(now.year)+"_"+str(now.hour)+str(now.minute)+str(now.second)
    return dateNtime;

def setWallPaper(pathToImg):
    """ Given a path to a jpg, set it as the wallpaper """
    result = windll.user32.SystemParametersInfoA( SPI_SETDESKWALLPAPER, 0,
                                                 pathToImg,
                                                 SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE );
                                                                                                  
    if not result:
        raise Exception("Unable to set Wallpaper.")
    
    
#===============================================================================
# def convertToBMP(pathToImage):
#     """ Given a path to an image, convert it to bmp format and set it as the wallpaper"""
# 
#     bmpImage = Image.open(pathToImage)
#     newPath = os.getcwd()
#     newPath = os.path.join(newPath, 'pywallpaper.bmp')
#     bmpImage.save(newPath, "BMP")
#     setWallPaper( newPath )
#===============================================================================

def fetchLiveCameraImage( webPath ):
    urllib.urlretrieve( webPath, webcamImage );

def cycleThruImages():
    
    lenList = len( webLinks );
    timePerLink = updateTime/ lenList;
    
    while(1):
        linkNum = 0;
        
        for link in webLinks:
            if DEBUG: print "Fetching new image..."
            
            fetchLiveCameraImage( link );
            setWallPaper( webcamImage );    
                        
            if DEBUG: #To create TimeLapse video; save images
                dateNtime = getCurrentTime();
                shutil.copy2( webcamImage, os.path.join(saveImgDir, "link"+str(linkNum)+"_IMG_"+dateNtime+".jpg") );
                
                print "Waiting for "+str(timePerLink)+" seconds...";
                
            linkNum += 1;
            
            time.sleep( timePerLink );
    
if __name__ == "__main__":
    
    webcamImage = os.path.join( os.getcwd(), webcamImage );
    saveImgDir = os.path.join( os.getcwd(), saveImgDir );
    
    if not os.path.exists( saveImgDir ):
        os.makedirs( saveImgDir );
    
    cycleThruImages();
        