import sys
import cv2

def convert(inputfile, outputfile):
    #print outputfile
    img = cv2.imread(inputfile, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    width, height = img.shape[:2]
    img = cv2.resize(img, (0,0), fx=580/width, fy=580/height)
    #print "writing file %s " % outputfile
    cv2.imwrite(outputfile, img)
    #print "Success!"

def main(argv=None):
    if argv == None:
        argv = sys.argv

    inputfile = argv[1]
    outputfile = "temp.pgm"
    convert(inputfile, outputfile)


if __name__ == "__main__":
    main(sys.argv)
