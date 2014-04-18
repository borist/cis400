import sys
import csv
import numpy as np
from scipy.optimize import minimize


class Manually_Scored_Image():
    def __init__(self, name, radial, focal_length, fov, camera_angle, overall):
        self.name = name
        self.radial = int(radial)
        self.focal_length = int(focal_length)
        self.fov = int(fov)
        self.camera_angle = int(camera_angle)
        self.overall = int(overall)

    def __repr__(self):
        return '%s: \n  radial_score: %d \n  focal_len_score: %d \n  FOV_score: %d \n  camera_angle_score: %s \n  overall_score: %d' \
            % (self.name, self.radial, self.focal_length,
               self.fov, self.camera_angle, self.overall)


# global vars
num_headers = 2  # number of header lines in the csv with manual scores
curr_images = None
curr_computed_scores = None


def process_manually_scored_images(csv_file):
    """
    Process a csv file with manually scored values for images and return a list of
    Manually_Scored_Image classes as representations for the images
    """
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        images = []

        for i, row in enumerate(reader):
            if i < num_headers:
                continue

            # ORDER: name | radial distortion | focal length | FOV / panoramic | angle of camera | overall distortion
            image = Manually_Scored_Image(*row)
            images.append(image)

    return images


def weigh_distortion(image, weight):
    """
    Weigh image's manual distortion scores based on the values in weight
    """
    return (image.radial * weight[0] +
            image.focal_length * weight[1] +
            image.fov * weight[2] +
            image.camera_angle * weight[3] +
            image.overall * weight[4])


def least_sq_distance(weight):
    """
    Calculate the sq distance of the curr_image's manual distortion scores weighted
    with weight and the computed distortion score for the image stored in
    curr_computed_score
    """
    total_distance = 0
    for i, image in enumerate(curr_images):
        manual_score = (weigh_distortion(image, weight) - curr_computed_scores[i]) ** 2
        total_distance += manual_score
    return total_distance


def try_weights(images, computed_scores):
    """
    computed_score: the computed score outputted by our program
    """
    global curr_images
    global curr_computed_scores
    curr_images = images
    curr_computed_scores = computed_scores

    # radial distortion | focal length | FOV / panoramic | angle of camera | overall distortion
    initial_weights = np.array([.1, .1, .1, .1, .1])
    res = minimize(least_sq_distance, initial_weights)
    return res.x


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: python score_images.py <manually_scored_images>.csv"

    else:
        images = process_manually_scored_images(sys.argv[1])

        for image in images:
            print image
            print "--------------------"

        # try to get optimal weights of manual scores
        computed_scores = [20]*len(images)  # 20 = dummy computed score
        optimal_weights = try_weights(images, computed_scores)  # 20 = dummy computed score
        print "optimal weighting: ", optimal_weights
