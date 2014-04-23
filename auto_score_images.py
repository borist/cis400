import sys
import glob
import cv2
import os
import csv
import focal_length
import radial_distortion


def compute_scores(image_path, comp_rad=True, comp_focal=True, comp_FOV=True):
    f, FOV, rad = float(-1), float(-1), float(-1)

    if comp_rad:
        # computer radial distortion score
        rad = float(radial_distortion.main(image_path))

    if comp_focal:
        # computer focal length
        (v0, o, h) = focal_length.compute_pp(image_path)
        f = float(focal_length.compute_focal_length(v0, o, h))

    if comp_FOV:
        # computer FOV
        img = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
        h, w = img.shape[:2]
        FOV = float(focal_length.compute_fov(w, h, f))

    return [rad, f, FOV]


if __name__ == "__main__":
    print "usage: python auto_score_images.py <dir of images> <output file name>"
    image_dir = sys.argv[1]
    if len(sys.argv) == 2:
        fname = 'auto_scores.csv'

    else:
        fname = sys.argv[2]

    comp_rad = True
    comp_focal = False
    comp_FOV = False

    if os.path.isdir(image_dir):
        images = glob.glob(image_dir+"/*")

        # write to file
        with open(fname, 'wb') as f:
            writer = csv.writer(f)

            for image in images:
                print "running file ", image
                scores = compute_scores(image, comp_rad, comp_focal, comp_FOV)
                print "scores: ", scores
                # write scores
                writer.writerow([image] + scores)

    else:
        print "running file ", image_dir

        scores = compute_scores(image_dir, comp_rad, comp_focal, comp_FOV)
        print "scores: ", scores

        # write to file
        with open(fname, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow([image_dir] + scores)

    print "output in: ", fname
