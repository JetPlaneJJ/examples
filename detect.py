b'--- detect.py\t(original)'
b'+++ detect.py\t(refactored)'
b'@@ -11,7 +11,9 @@'
b' # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'
b' # See the License for the specific language governing permissions and'
b' # limitations under the License.'
b'-"""Main script to run the object detection routine."""'
b'+u"""Main script to run the object detection routine."""'
b'+from __future__ import division'
b'+from __future__ import absolute_import'
b' import argparse'
b' import sys'
b' import time'
b'@@ -22,9 +24,9 @@'
b' import utils'
b' '
b' '
b'-def run(model: str, camera_id: int, width: int, height: int, num_threads: int,'
b'-        enable_edgetpu: bool) -> None:'
b'-  """Continuously run inference on images acquired from the camera.'
b'+def run(model, camera_id, width, height, num_threads,'
b'+        enable_edgetpu):'
b'+  u"""Continuously run inference on images acquired from the camera.'
b' '
b'   Args:'
b'     model: Name of the TFLite object detection model.'
b'@@ -41,7 +43,7 @@'
b' '
b'   # Start capturing video input from the camera'
b' #   cap = cv2.VideoCapture(camera_id)'
b"-  cap = cv2.VideoCapture('nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=(fraction)15/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink', cv2.CAP_GSTREAMER)"
b"+  cap = cv2.VideoCapture(u'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=(fraction)15/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink', cv2.CAP_GSTREAMER)"
b'   cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)'
b'   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)'
b' '
b'@@ -66,7 +68,7 @@'
b'     success, image = cap.read()'
b'     if not success:'
b'       sys.exit('
b"-          'ERROR: Unable to read from webcam. Please verify your webcam settings.'"
b"+          u'ERROR: Unable to read from webcam. Please verify your webcam settings.'"
b'       )'
b' '
b'     counter += 1'
b'@@ -85,7 +87,7 @@'
b'       start_time = time.time()'
b' '
b'     # Show the FPS'
b"-    fps_text = 'FPS = {:.1f}'.format(fps)"
b"+    fps_text = u'FPS = {:.1f}'.format(fps)"
b'     text_location = (left_margin, row_size)'
b'     cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,'
b'                 font_size, text_color, font_thickness)'
b'@@ -93,7 +95,7 @@'
b'     # Stop the program if the ESC key is pressed.'
b'     if cv2.waitKey(1) == 27:'
b'       break'
b"-    cv2.imshow('object_detector', image)"
b"+    cv2.imshow(u'object_detector', image)"
b' '
b'   cap.release()'
b'   cv2.destroyAllWindows()'
b'@@ -103,34 +105,34 @@'
b'   parser = argparse.ArgumentParser('
b'       formatter_class=argparse.ArgumentDefaultsHelpFormatter)'
b'   parser.add_argument('
b"-      '--model',"
b"-      help='Path of the object detection model.',"
b"+      u'--model',"
b"+      help=u'Path of the object detection model.',"
b'       required=False,'
b"-      default='efficientdet_lite0.tflite')"
b"+      default=u'efficientdet_lite0.tflite')"
b'   parser.add_argument('
b"-      '--cameraId', help='Id of camera.', required=False, type=int, default=0)"
b"+      u'--cameraId', help=u'Id of camera.', required=False, type=int, default=0)"
b'   parser.add_argument('
b"-      '--frameWidth',"
b"-      help='Width of frame to capture from camera.',"
b"+      u'--frameWidth',"
b"+      help=u'Width of frame to capture from camera.',"
b'       required=False,'
b'       type=int,'
b'       default=640)'
b'   parser.add_argument('
b"-      '--frameHeight',"
b"-      help='Height of frame to capture from camera.',"
b"+      u'--frameHeight',"
b"+      help=u'Height of frame to capture from camera.',"
b'       required=False,'
b'       type=int,'
b'       default=480)'
b'   parser.add_argument('
b"-      '--numThreads',"
b"-      help='Number of CPU threads to run the model.',"
b"+      u'--numThreads',"
b"+      help=u'Number of CPU threads to run the model.',"
b'       required=False,'
b'       type=int,'
b'       default=4)'
b'   parser.add_argument('
b"-      '--enableEdgeTPU',"
b"-      help='Whether to run the model on EdgeTPU.',"
b"-      action='store_true',"
b"+      u'--enableEdgeTPU',"
b"+      help=u'Whether to run the model on EdgeTPU.',"
b"+      action=u'store_true',"
b'       required=False,'
b'       default=False)'
b'   args = parser.parse_args()'
b'@@ -139,5 +141,5 @@'
b'       int(args.numThreads), bool(args.enableEdgeTPU))'
b' '
b' '
b"-if __name__ == '__main__':"
b"+if __name__ == u'__main__':"
b'   main()'
