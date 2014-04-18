import sys
import csv


class Manually_Scored_Image():
    def __init__(self, name, radial, focal_length, fov, camera_angle, overall):
        self.name = name
        self.radial = int(radial)
        self.focal_length = int(focal_length)
        self.fov = int(fov)
        self.camera_angle = int(camera_angle)
        self.overall = int(overall)

    def __repr__(self):
        return '%s: \n  radial_score: %d \n  focal_len_score: %d \n  FOV_score: %d \n  camera_angle_score: %s \n  overall_score: %d \n-----------------' \
            % (self.name, self.radial, self.focal_length,
               self.fov, self.camera_angle, self.overall)


# global vars
num_headers = 2  # number of header lines in the csv with manual scores


def process_manually_scored_images(csv_file):
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "usage: python score_images.py <manually_scored_images>.csv"

    else:
        images = process_manually_scored_images(sys.argv[1])
        for image in images:
            print image
