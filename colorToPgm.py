import sys
import string
import cv2

def convert(inputfile, outputfile):
    #print outputfile
    img = cv2.imread(inputfile, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    #print "writing file %s " % outputfile
    #if (cv2.imwrite(outputfile, img)):
        #print "Success!"

def main(argv=None):
    if argv == None:
        argv = sys.argv

    inputfile = argv[1]
    outputfile = "temp.pgm"
    convert(inputfile, outputfile)


if __name__ == "__main__":
    main(sys.argv)
