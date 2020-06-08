import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class GripPipeline:
    """
    An OpenCV pipeline generated by GRIP.
    """

    def __init__(self):
        """initializes all values to presets or None if need to be set
        """

        self.__find_blobs_min_area = 1.0
        self.__find_blobs_circularity = [0.0, 1.0]
        self.__find_blobs_dark_blobs = False

        self.find_blobs_output = None

    def process(self, source0):
        """
        Runs the pipeline and sets all outputs to new values.
        """
        # Step Find_Blobs0:
        self.__find_blobs_input = source0
        (self.find_blobs_output) = self.__find_blobs(self.__find_blobs_input, self.__find_blobs_min_area,
                                                     self.__find_blobs_circularity, self.__find_blobs_dark_blobs)

    @staticmethod
    def __find_blobs(input, min_area, circularity, dark_blobs):
        """Detects groups of pixels in an image.
        Args:
            input: A numpy.ndarray.
            min_area: The minimum blob size to be found.
            circularity: The min and max circularity as a list of two numbers.
            dark_blobs: A boolean. If true looks for black. Otherwise it looks for white.
        Returns:
            A list of KeyPoint.
        """
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = 1
        params.blobColor = (0 if dark_blobs else 255)
        params.minThreshold = 10
        params.maxThreshold = 220
        params.filterByArea = True
        params.minArea = min_area
        params.filterByCircularity = True
        params.minCircularity = circularity[0]
        params.maxCircularity = circularity[1]
        params.filterByConvexity = False
        params.filterByInertia = False
        detector = cv2.SimpleBlobDetector_create(params)
        return detector.detect(input)


def rgb_img_to_binary(img):
    return np.array(list(map(lambda row: [sum(color_vec) < 255 for color_vec in row], img)))


if __name__ == '__main__':
    img_path = 'D:\\Users\\yonat\\Desktop\\HUJI\\HUJI Homework\\Advanced Physics Lab A\\Water Heating - Experiment B\\Camera Pics\\8.6.2020\\main exp pics\\16-28-07.000-070.png'

    image = Image.open(img_path)

    fig, axs = plt.subplots(ncols=3, sharex=True, sharey=True)
    axs[0].imshow(~np.asarray(image), cmap='Greys')
    axs[0].set_title('Original image')

    # get blobs from the main pipeline
    pipeline = GripPipeline()
    pipeline.process(np.asarray(image))
    img_blobs_keypoints = pipeline.find_blobs_output
    blobs_only_img = cv2.drawKeypoints(np.zeros_like(image), img_blobs_keypoints, np.array([]), (0, 0, 255),
                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    axs[1].imshow(cv2.cvtColor(blobs_only_img, cv2.COLOR_BGR2RGB))
    axs[1].set_title('Blobs only, unfilled')

    # fill in the blobs and get the area of the bubbles
    filled_image = cv2.floodFill(blobs_only_img, None, (0, 0), 255)[1]

    axs[2].imshow(rgb_img_to_binary(filled_image), cmap='Greys')
    axs[2].set_title('Blobs only, filled')

    plt.show()
