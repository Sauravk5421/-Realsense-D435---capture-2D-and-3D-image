import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QObject, pyqtSignal
from Interface_Design import Ui_MainWindow

import os
import time
import datetime as dt
import numpy as np
import threading as th
import pyrealsense2 as rs
import cv2

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.dis_update.connect(self.camera_view)
        self.Button_colorphoto.clicked.connect(self.Button_colorphoto_clicked)
        self.thread_camera = None
        self.takePhotos = False
    dis_update = pyqtSignal(QPixmap)

    def Button_colorphoto_clicked(self):
        self.takePhotos = True

    def open_camera(self):
        self.thread_camera = th.Thread(target=self.Open_Realsense)
        self.thread_camera.start()
        print("Camera Opened")

    def camera_view(self, c):
        self.label_show.setPixmap(c)
        self.label_show.setScaledContents(True)

    def Open_Realsense(self):
        pc = rs.pointcloud()
        points = rs.points()
        # print(points)

        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        profile = pipeline.start(config)
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        #print("Depth Scale is: ", depth_scale)
        clipping_distance_in_meters = 0.40  # 1 meter
        clipping_distance = clipping_distance_in_meters / depth_scale

        colorizer = rs.colorizer()
        # Streaming loop
        try:
            while True:
                frames = pipeline.wait_for_frames()
                colorized = colorizer.process(frames)
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()

                if not depth_frame or not color_frame:
                    continue
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                grey_color = 153
                depth_image_3d = np.dstack((depth_image, depth_image, depth_image))  # depth image is 1 channel, color is 3 channels
                bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color,
                                      color_image)


                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
                images = np.hstack((color_image[0:720, 320:960], depth_colormap[0:720, 320:960]))

                if (self.takePhotos == True):
                    now_time = dt.datetime.now().strftime('%F_%H%M%S')
                    path_ok1 = os.path.exists('.\Color Image')
                    path_ok2 = os.path.exists('.\Depth Image')
                    path_ok3 = os.path.exists('.\PC Image')
                    if (path_ok1 == False):
                        os.mkdir('.\Color Image')
                    if (os.path.isdir('.\Color Image')):
                        color_full_path = os.path.join('./Color Image', now_time + '_color.png')
                        cv2.imencode('.png', color_image)[1].tofile(color_full_path)
                        print("Color Photo Taken")
                    if (path_ok2 == False):
                        os.mkdir('.\Depth Image')
                    if (os.path.isdir('.\Depth Image')):
                        depth_full_path = os.path.join('./Depth Image', now_time + '_depth.png')
                        cv2.imencode('.png', depth_colormap)[1].tofile(depth_full_path)
                        print("Depth Photo Taken")
                    if (path_ok3 == False):
                        os.mkdir('.\PC Image')
                    if (os.path.isdir('.\PC Image')):
                        # print("rhh",rs)
                        ply = rs.save_to_ply(r'.\PC Image\PC_' + now_time + '.ply')
                        print("Saving point cloud please wait.....")
                        ply.set_option(rs.save_to_ply.option_ply_binary, False)
                        ply.set_option(rs.save_to_ply.option_ply_normals, True)
                        ply.process(colorized)
                        print("3D Point Cloud Photo Taken")
                    self.takePhotos = False
#show images
                qimage = QImage(images, 1280, 720, QImage.Format_BGR888)
                pixmap = QPixmap.fromImage(qimage)
                self.dis_update.emit(pixmap)
                time.sleep(0)
        finally:
            pipeline.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    real_cam = MainWindow()
    real_cam.show()
    real_cam.open_camera()
    sys.exit(app.exec_())
