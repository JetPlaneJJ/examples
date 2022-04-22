b'--- object_detector_test.py\t(original)'
b'+++ object_detector_test.py\t(refactored)'
b'@@ -11,20 +11,24 @@'
b' # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'
b' # See the License for the specific language governing permissions and'
b' # limitations under the License.'
b'-"""Unit test of object detection using ObjectDetector wrapper."""'
b'+u"""Unit test of object detection using ObjectDetector wrapper."""'
b' '
b'+from __future__ import division'
b'+from __future__ import with_statement'
b'+from __future__ import absolute_import'
b' import csv'
b' import unittest'
b' '
b' import cv2'
b' import object_detector as od'
b'+from io import open'
b' '
b"-_MODEL_FILE = 'efficientdet_lite0.tflite'"
b"-_GROUND_TRUTH_FILE = 'test_data/table_results.csv'"
b"-_IMAGE_FILE = 'test_data/table.jpg'"
b"+_MODEL_FILE = u'efficientdet_lite0.tflite'"
b"+_GROUND_TRUTH_FILE = u'test_data/table_results.csv'"
b"+_IMAGE_FILE = u'test_data/table.jpg'"
b' _BBOX_IOU_THRESHOLD = 0.9'
b"-_ALLOW_LIST = ['knife', 'cup']"
b"-_DENY_LIST = ['book']"
b"+_ALLOW_LIST = [u'knife', u'cup']"
b"+_DENY_LIST = [u'book']"
b' _SCORE_THRESHOLD = 0.3'
b' _MAX_RESULTS = 3'
b' '
b'@@ -32,13 +36,13 @@'
b' class ObjectDetectorTest(unittest.TestCase):'
b' '
b'   def setUp(self):'
b'-    """Initialize the shared variables."""'
b'-    super().setUp()'
b'+    u"""Initialize the shared variables."""'
b'+    super(ObjectDetectorTest, self).setUp()'
b'     self._load_ground_truth()'
b'     self.image = cv2.imread(_IMAGE_FILE)'
b' '
b'   def test_default_option(self):'
b'-    """Check if the default option works correctly."""'
b'+    u"""Check if the default option works correctly."""'
b'     detector = od.ObjectDetector(_MODEL_FILE)'
b'     result = detector.detect(self.image)'
b' '
b'@@ -58,10 +62,10 @@'
b'           break'
b' '
b'       # If no matching detection found, fail the test.'
b"-      self.assertTrue(is_gt_found, '{0} not found.'.format(gt_detection))"
b"+      self.assertTrue(is_gt_found, u'{0} not found.'.format(gt_detection))"
b' '
b'   def test_allow_list(self):'
b'-    """Test the label_allow_list option."""'
b'+    u"""Test the label_allow_list option."""'
b'     option = od.ObjectDetectorOptions(label_allow_list=_ALLOW_LIST)'
b'     detector = od.ObjectDetector(_MODEL_FILE, options=option)'
b'     result = detector.detect(self.image)'
b'@@ -70,10 +74,10 @@'
b'       label = detection.categories[0].label'
b'       self.assertIn('
b'           label, _ALLOW_LIST,'
b'-          \'Label "{0}" found but not in label allow list\'.format(label))'
b'+          u\'Label "{0}" found but not in label allow list\'.format(label))'
b' '
b'   def test_deny_list(self):'
b'-    """Test the label_deny_list option."""'
b'+    u"""Test the label_deny_list option."""'
b'     option = od.ObjectDetectorOptions(label_deny_list=_DENY_LIST)'
b'     detector = od.ObjectDetector(_MODEL_FILE, options=option)'
b'     result = detector.detect(self.image)'
b'@@ -81,10 +85,10 @@'
b'     for detection in result:'
b'       label = detection.categories[0].label'
b'       self.assertNotIn(label, _DENY_LIST,'
b'-                       \'Label "{0}" found but in deny list.\'.format(label))'
b'+                       u\'Label "{0}" found but in deny list.\'.format(label))'
b' '
b'   def test_score_threshold_option(self):'
b'-    """Test the score_threshold option."""'
b'+    u"""Test the score_threshold option."""'
b'     option = od.ObjectDetectorOptions(score_threshold=_SCORE_THRESHOLD)'
b'     detector = od.ObjectDetector(_MODEL_FILE, options=option)'
b'     result = detector.detect(self.image)'
b'@@ -93,41 +97,41 @@'
b'       score = detection.categories[0].score'
b'       self.assertGreaterEqual('
b'           score, _SCORE_THRESHOLD,'
b"-          'Detection with score lower than threshold found. {0}'.format("
b"+          u'Detection with score lower than threshold found. {0}'.format("
b'               detection))'
b' '
b'   def test_max_resultsss_option(self):'
b'-    """Test the max_results option."""'
b'+    u"""Test the max_results option."""'
b'     option = od.ObjectDetectorOptions(max_results=_MAX_RESULTS)'
b'     detector = od.ObjectDetector(_MODEL_FILE, options=option)'
b'     result = detector.detect(self.image)'
b' '
b'     self.assertLessEqual('
b"-        len(result), _MAX_RESULTS, 'Too many results returned.')"
b"+        len(result), _MAX_RESULTS, u'Too many results returned.')"
b' '
b'   def _load_ground_truth(self):'
b'-    """Load ground truth detection result from a CSV file."""'
b'+    u"""Load ground truth detection result from a CSV file."""'
b'     self._ground_truth_detections = []'
b'     with open(_GROUND_TRUTH_FILE) as f:'
b'       reader = csv.DictReader(f)'
b'       for row in reader:'
b'         category = od.Category('
b"-            label=row['label'],"
b"+            label=row[u'label'],"
b"             # As we don't care about the category index, we'll just set it to 0."
b'             index=0,'
b"-            score=float(row['score']))"
b"+            score=float(row[u'score']))"
b'         bounding_box = od.Rect('
b"-            left=float(row['left']),"
b"-            top=float(row['top']),"
b"-            right=float(row['right']),"
b"-            bottom=float(row['bottom']),"
b"+            left=float(row[u'left']),"
b"+            top=float(row[u'top']),"
b"+            right=float(row[u'right']),"
b"+            bottom=float(row[u'bottom']),"
b'         )'
b'         detection = od.Detection('
b'             bounding_box=bounding_box, categories=[category])'
b'         self._ground_truth_detections.append(detection)'
b' '
b'-  def _iou(self, rect1: od.Rect, rect2: od.Rect):'
b'-    """Calculate the Intersection over Union ratio of 2 given rectangles."""'
b'+  def _iou(self, rect1, rect2):'
b'+    u"""Calculate the Intersection over Union ratio of 2 given rectangles."""'
b'     # Determine the the intersection rectangle'
b'     x_min = max(rect1.left, rect2.left)'
b'     y_min = max(rect1.top, rect2.top)'
b'@@ -151,25 +155,25 @@'
b' # pylint: disable=g-unreachable-test-method'
b' '
b'   def _create_groud_truth_csv(self, output_file=_GROUND_TRUTH_FILE):'
b'-    """A util function to recreate the ground truth result."""'
b'+    u"""A util function to recreate the ground truth result."""'
b'     detector = od.ObjectDetector(_MODEL_FILE)'
b'     result = detector.detect(self.image)'
b"-    with open(output_file, 'w') as f:"
b"-      header = ['label', 'left', 'top', 'right', 'bottom', 'score']"
b"+    with open(output_file, u'w') as f:"
b"+      header = [u'label', u'left', u'top', u'right', u'bottom', u'score']"
b'       writer = csv.DictWriter(f, fieldnames=header)'
b'       writer.writeheader()'
b'       for d in result:'
b'         writer.writerow({'
b"-            'label': d.categories[0].label,"
b"-            'left': d.bounding_box.left,"
b"-            'top': d.bounding_box.top,"
b"-            'right': d.bounding_box.right,"
b"-            'bottom': d.bounding_box.bottom,"
b"-            'score': d.categories[0].score,"
b"+            u'label': d.categories[0].label,"
b"+            u'left': d.bounding_box.left,"
b"+            u'top': d.bounding_box.top,"
b"+            u'right': d.bounding_box.right,"
b"+            u'bottom': d.bounding_box.bottom,"
b"+            u'score': d.categories[0].score,"
b'         })'
b' '
b' '
b' # pylint: enable=g-unreachable-test-method'
b' '
b"-if __name__ == '__main__':"
b"+if __name__ == u'__main__':"
b'   unittest.main()'
