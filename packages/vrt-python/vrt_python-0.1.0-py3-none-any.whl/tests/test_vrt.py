from image_diff.image_diff import ImageDifference
import os
import unittest

project_directory = os.getcwd()


class TestCalculator(unittest.TestCase):
    def test_ImageDifference(self):
        image = ImageDifference(expectation_path="testing_images/test_image_expected.png",
                                actual_path="testing_images/test_image_actual.png")
        screenshot = ImageDifference(expectation_path="testing_images/test_screenshot_expected.png",
                                     actual_path="testing_images/test_screenshot_actual.png")

        no_difference_image = ImageDifference(expectation_path="testing_images/test_image_expected.png",
                                              actual_path="testing_images/test_image_expected.png")
        no_difference_screenshot = ImageDifference(expectation_path="testing_images/test_screenshot_expected.png",
                                                   actual_path="testing_images/test_screenshot_expected.png")

        self.assertEqual(image.generate_difference_image(test=True), 0.01875)
        self.assertEqual(screenshot.generate_difference_image(test=True), 0.2416681483636677)
        self.assertEqual(no_difference_screenshot.generate_difference_image(test=True), 0)
        self.assertEqual(no_difference_image.generate_difference_image(test=True), 0)

        self.assertEqual(os.path.exists(f'{project_directory}/test_image_actual_difference.png'), True)
        self.assertEqual(os.path.exists(f'{project_directory}/test_image_expected_difference.png'), True)
        self.assertEqual(os.path.exists(f'{project_directory}/test_screenshot_actual_difference.png'), True)
        self.assertEqual(os.path.exists(f'{project_directory}/test_screenshot_expected_difference.png'), True)


if __name__ == '__main__':
    unittest.main()
