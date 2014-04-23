from __future__ import division

import sys
import csv
import numpy as np
from operator import attrgetter
from scipy.optimize import minimize


class Scored_Image():
    def __init__(self, name, radial, focal_length, fov, camera_angle, overall, auto_name, auto_rad, auto_focal, auto_FOV):
        self.name = name
        self.radial = float(radial)
        self.focal_length = float(focal_length)
        self.fov = float(fov)
        self.camera_angle = float(camera_angle)
        self.overall = float(overall)
        self.auto_name = auto_name
        self.auto_rad = float(auto_rad)
        self.auto_focal = float(auto_focal)
        self.auto_FOV = float(auto_FOV)

    def __repr__(self):
        return '%s: \n  radial_score: %f \n  focal_len_score: %f \n  FOV_score: %f \n  camera_angle_score: %s \n  overall_score: %f \n Manual: %s: \n  radial_score: %f \n  focal_len_score: %f \n  FOV_score: %f' \
            % (self.name, self.radial, self.focal_length,
               self.fov, self.camera_angle, self.overall, self.auto_name, self.auto_rad, self.auto_focal, self.auto_FOV)


# global vars
num_headers = 2  # number of header lines in the csv with manual scores
curr_images = None


def process_scored_images(manual_csv_file, auto_csv_file):
    """
    Process a csv file with manually scored values for images and return a list of
    Manually_Scored_Image classes as representations for the images
    """
    with open(manual_csv_file, 'rb') as manual_f:
        with open(auto_csv_file, 'rb') as auto_f:

            manual_reader = csv.reader(manual_f)
            auto_reader = csv.reader(auto_f)
            images = []

            # for i, row in enumerate(manual_reader):
            #     if i < num_headers:
            #         continue

            for row1, row2 in zip(manual_reader, auto_reader):
                if row1[0].lower() != row2[0].split('\\')[-1].lower():
                    print "names don't align! ", row1[0], row2[0].split('\\')[-1]
                    return

                # ORDER: name | radial distortion | focal length | FOV / panoramic | angle of camera | overall distortion
                row = row1 + row2
                image = Scored_Image(*row)
                images.append(image)

    return images


def weigh_manual_distortion(image, weight):
    """
    Weigh image's manual distortion scores based on the values in weight
    """
    return (image.radial * weight[0] +
            image.focal_length * weight[1] +
            image.fov * weight[2] +
            image.camera_angle * weight[3])


def weigh_auto_distortion(image, weight):
    """
    Weigh image's manual distortion scores based on the values in weight
    """
    return (image.auto_rad * weight[0] +
            image.auto_focal * weight[1] +
            image.auto_FOV * weight[2])


def least_sq_distance(weight):
    """
    Calculate the sq distance of the curr_image's manual distortion scores weighted
    with weight and the computed distortion score for the image stored in
    curr_computed_score
    """

    total_distance = 0
    for i, image in enumerate(curr_images):
        manual_score = weigh_manual_distortion(image, weight)
        auto_score = weigh_auto_distortion(image, weight)

        sq_dist = (manual_score - auto_score) ** 2
        print manual_score, auto_score, sq_dist

        total_distance += sq_dist
    return total_distance


def normalize_images(images):
    max_auto_rad = float(0)
    max_auto_focal = float(0)
    max_auto_fov = float(0)

    max_auto_rad = max(images, key=attrgetter('auto_rad')).auto_rad
    max_auto_focal = max(images, key=attrgetter('auto_focal')).auto_focal
    max_auto_fov = max(images, key=attrgetter('auto_FOV')).auto_FOV

    for image in images:
        image.auto_rad = image.auto_rad * 10.0 / max_auto_rad
        image.auto_focal = image.auto_focal * 10.0 / max_auto_focal
        image.auto_FOV = image.auto_FOV * 10.0 / max_auto_fov

    return images


def try_weights(images):
    """
    computed_score: the computed score outputted by our program
    """
    global curr_images
    global curr_computed_scores
    curr_images = images

    # next 3 are for automatic: radial distortion | focal length | FOV | angle of camera (only for manual)
    initial_weights = np.array([.1, .1, .1, .1])
    res = minimize(least_sq_distance, initial_weights)
    print res
    return res.x


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: python score_images.py <manually_scored_images>.csv <auto_scored_images>.csv"

    else:
        images = process_scored_images(sys.argv[1], sys.argv[2])

        images = normalize_images(images)

        for image in images:
            print image
            print "--------------------"

        # try to get optimal weights of manual scores
        optimal_weights = try_weights(images)  # 20 = dummy computed score

        print "optimal weighting: "
        print "Manual: "
        print "\t radial: ", optimal_weights[0]
        print "\t focal length: ", optimal_weights[1]
        print "\t FOV: ", optimal_weights[2]
        print "\t camera angle: ", optimal_weights[3]
        print "------------------\nAuto:"
        print "\t radial: ", optimal_weights[0]
        print "\t focal length: ", optimal_weights[1]
        print "\t FOV: ", optimal_weights[2]
