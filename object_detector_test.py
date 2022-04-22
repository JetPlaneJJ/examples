# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
u"""Unit test of object detection using ObjectDetector wrapper."""

from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
import csv
import unittest

import cv2
import object_detector as od
from io import open

_MODEL_FILE = u'efficientdet_lite0.tflite'
_GROUND_TRUTH_FILE = u'test_data/table_results.csv'
_IMAGE_FILE = u'test_data/table.jpg'
_BBOX_IOU_THRESHOLD = 0.9
_ALLOW_LIST = [u'knife', u'cup']
_DENY_LIST = [u'book']
_SCORE_THRESHOLD = 0.3
_MAX_RESULTS = 3


class ObjectDetectorTest(unittest.TestCase):

  def setUp(self):
    u"""Initialize the shared variables."""
    super(ObjectDetectorTest, self).setUp()
    self._load_ground_truth()
    self.image = cv2.imread(_IMAGE_FILE)

  def test_default_option(self):
    u"""Check if the default option works correctly."""
    detector = od.ObjectDetector(_MODEL_FILE)
    result = detector.detect(self.image)

    # Check if all ground truth detection is found.
    for gt_detection in self._ground_truth_detections:
      is_gt_found = False
      for real_detection in result:
        is_label_match = real_detection.categories[
            0].label == gt_detection.categories[0].label
        is_bounding_box_match = self._iou(
            real_detection.bounding_box,
            gt_detection.bounding_box) > _BBOX_IOU_THRESHOLD

        # If a matching detection is found, stop the loop.
        if is_label_match and is_bounding_box_match:
          is_gt_found = True
          break

      # If no matching detection found, fail the test.
      self.assertTrue(is_gt_found, u'{0} not found.'.format(gt_detection))

  def test_allow_list(self):
    u"""Test the label_allow_list option."""
    option = od.ObjectDetectorOptions(label_allow_list=_ALLOW_LIST)
    detector = od.ObjectDetector(_MODEL_FILE, options=option)
    result = detector.detect(self.image)

    for detection in result:
      label = detection.categories[0].label
      self.assertIn(
          label, _ALLOW_LIST,
          u'Label "{0}" found but not in label allow list'.format(label))

  def test_deny_list(self):
    u"""Test the label_deny_list option."""
    option = od.ObjectDetectorOptions(label_deny_list=_DENY_LIST)
    detector = od.ObjectDetector(_MODEL_FILE, options=option)
    result = detector.detect(self.image)

    for detection in result:
      label = detection.categories[0].label
      self.assertNotIn(label, _DENY_LIST,
                       u'Label "{0}" found but in deny list.'.format(label))

  def test_score_threshold_option(self):
    u"""Test the score_threshold option."""
    option = od.ObjectDetectorOptions(score_threshold=_SCORE_THRESHOLD)
    detector = od.ObjectDetector(_MODEL_FILE, options=option)
    result = detector.detect(self.image)

    for detection in result:
      score = detection.categories[0].score
      self.assertGreaterEqual(
          score, _SCORE_THRESHOLD,
          u'Detection with score lower than threshold found. {0}'.format(
              detection))

  def test_max_resultsss_option(self):
    u"""Test the max_results option."""
    option = od.ObjectDetectorOptions(max_results=_MAX_RESULTS)
    detector = od.ObjectDetector(_MODEL_FILE, options=option)
    result = detector.detect(self.image)

    self.assertLessEqual(
        len(result), _MAX_RESULTS, u'Too many results returned.')

  def _load_ground_truth(self):
    u"""Load ground truth detection result from a CSV file."""
    self._ground_truth_detections = []
    with open(_GROUND_TRUTH_FILE) as f:
      reader = csv.DictReader(f)
      for row in reader:
        category = od.Category(
            label=row[u'label'],
            # As we don't care about the category index, we'll just set it to 0.
            index=0,
            score=float(row[u'score']))
        bounding_box = od.Rect(
            left=float(row[u'left']),
            top=float(row[u'top']),
            right=float(row[u'right']),
            bottom=float(row[u'bottom']),
        )
        detection = od.Detection(
            bounding_box=bounding_box, categories=[category])
        self._ground_truth_detections.append(detection)

  def _iou(self, rect1, rect2):
    u"""Calculate the Intersection over Union ratio of 2 given rectangles."""
    # Determine the the intersection rectangle
    x_min = max(rect1.left, rect2.left)
    y_min = max(rect1.top, rect2.top)
    x_max = min(rect1.right, rect2.right)
    y_max = min(rect1.bottom, rect2.bottom)

    # Compute the area of intersection rectangle
    inter_area = max(0.0, x_max - x_min) * max(0.0, y_max - y_min)

    # Compute the area of the each input rectangle
    rect1_area = (rect1.right - rect1.left) * (rect1.bottom - rect1.top)
    rect2_area = (rect2.right - rect2.left) * (rect2.bottom - rect2.top)

    # Compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the intersection area
    iou = inter_area / float(rect1_area + rect2_area - inter_area)

    return iou

# pylint: disable=g-unreachable-test-method

  def _create_groud_truth_csv(self, output_file=_GROUND_TRUTH_FILE):
    u"""A util function to recreate the ground truth result."""
    detector = od.ObjectDetector(_MODEL_FILE)
    result = detector.detect(self.image)
    with open(output_file, u'w') as f:
      header = [u'label', u'left', u'top', u'right', u'bottom', u'score']
      writer = csv.DictWriter(f, fieldnames=header)
      writer.writeheader()
      for d in result:
        writer.writerow({
            u'label': d.categories[0].label,
            u'left': d.bounding_box.left,
            u'top': d.bounding_box.top,
            u'right': d.bounding_box.right,
            u'bottom': d.bounding_box.bottom,
            u'score': d.categories[0].score,
        })


# pylint: enable=g-unreachable-test-method

if __name__ == u'__main__':
  unittest.main()
