import cProfile
from server import calculate_distortion_score
import sys

if __name__ == "__main__":
    inputValue = "calculate_distortion_score('" + sys.argv[1] + "')"
    cProfile.run(inputValue)


