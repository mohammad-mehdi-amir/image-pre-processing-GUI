import sys
import cv2
import numpy as np

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QComboBox, QSlider, QVBoxLayout, QHBoxLayout, QFileDialog,
    QMessageBox, QGroupBox
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap


class ImageProcessingGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.original_image = None
        self.processed_image = None

        self.setWindowTitle("Image Processing Project")
        self.setGeometry(100, 100, 1300, 700)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        top_layout = QHBoxLayout()

        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_image)

        self.save_button = QPushButton("Save Output")
        self.save_button.clicked.connect(self.save_image)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_image)
        
        self.use_output_button = QPushButton("Use Output as Input")
        self.use_output_button.clicked.connect(self.use_output_as_input)

        top_layout.addWidget(self.open_button)
        top_layout.addWidget(self.save_button)
        top_layout.addWidget(self.reset_button)
        top_layout.addWidget(self.use_output_button)
        main_layout.addLayout(top_layout)

        content_layout = QHBoxLayout()

        control_box = QGroupBox("Controls")
        control_layout = QVBoxLayout()
        control_box.setLayout(control_layout)

        self.operation_combo = QComboBox()
        self.operation_combo.addItems([
            "Gray Scale",
            "Salt and Pepper",
            "Brightness",
            "Gaussian Blur",
            "median",
            "mean",
            "Threshold",
            "Canny Edge",
            "laplacian",
            "sobel x",
            "sobel y",
            "sobel",
            "Sharpen",
            "High Boost",
            "Laplacian Sharpen",
            "Multiply Images",
            "Add Images",
            "Power Law Transformation",
            "Histogram Equalization",
        ])

        self.operation_combo.currentTextChanged.connect(self.change_operation)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(120)
        self.slider.valueChanged.connect(self.apply_processing)

        self.value_label = QLabel("Value: 120")

        control_layout.addWidget(QLabel("Select Operation:"))
        control_layout.addWidget(self.operation_combo)
        control_layout.addWidget(self.value_label)
        control_layout.addWidget(self.slider)
        control_layout.addStretch()

        content_layout.addWidget(control_box, 1)

        self.original_label = QLabel("Original Image")
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(450, 450)
        self.original_label.setStyleSheet("border: 1px solid black;")

        self.processed_label = QLabel("Processed Image")
        self.processed_label.setAlignment(Qt.AlignCenter)
        self.processed_label.setMinimumSize(450, 450)
        self.processed_label.setStyleSheet("border: 1px solid black;")

        content_layout.addWidget(self.original_label, 3)
        content_layout.addWidget(self.processed_label, 3)

        main_layout.addLayout(content_layout)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_name:
            self.original_image = cv2.imread(file_name)

            if self.original_image is None:
                QMessageBox.warning(self, "Error", "Image could not be loaded")
                return

            self.processed_image = self.original_image.copy()

            self.show_image(self.original_image, self.original_label)
            self.show_image(self.processed_image, self.processed_label)

    def save_image(self):
        if self.processed_image is None:
            QMessageBox.warning(self, "Error", "No processed image to save")
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "PNG Files (*.png);;JPG Files (*.jpg)"
        )

        if file_name:
            cv2.imwrite(file_name, self.processed_image)

    def reset_image(self):
        if self.original_image is None:
            return

        self.processed_image = self.original_image.copy()
        self.show_image(self.processed_image, self.processed_label)

    
    def use_output_as_input(self):
        if self.processed_image is None:
            QMessageBox.warning(self, "Error", "No output image exists")
            return

        self.original_image = self.processed_image.copy()

        self.show_image(self.original_image, self.original_label)

        self.processed_image = self.original_image.copy()
        self.show_image(self.processed_image, self.processed_label)
        
    def change_operation(self):
        operation = self.operation_combo.currentText()

        if operation == "Brightness":
            self.slider.setMinimum(-100)
            self.slider.setMaximum(100)
            self.slider.setValue(0)
            
        elif operation == "Salt and Pepper":
            self.slider.setMinimum(0)
            self.slider.setMaximum(100)
            self.slider.setValue(5)
        
        elif operation == "Gaussian Blur":
            self.slider.setMinimum(1)
            self.slider.setMaximum(31)
            self.slider.setValue(5)

        elif operation == "median":
            self.slider.setMinimum(3)
            self.slider.setMaximum(31)
            self.slider.setValue(5)
        
        elif operation == "mean":
            self.slider.setMinimum(1)
            self.slider.setMaximum(31)
            self.slider.setValue(5)
        
        elif operation == "Threshold":
            self.slider.setMinimum(0)
            self.slider.setMaximum(255)
            self.slider.setValue(120)

        elif operation == "Canny Edge":
            self.slider.setMinimum(0)
            self.slider.setMaximum(255)
            self.slider.setValue(100)
            
        elif operation == "laplacian":
            self.slider.setMinimum(1)
            self.slider.setMaximum(31)
            self.slider.setValue(3)

        elif operation == "sobel x":
            self.slider.setMinimum(1)
            self.slider.setMaximum(31)
            self.slider.setValue(3)
        
        elif operation == "sobel y":
            self.slider.setMinimum(1)
            self.slider.setMaximum(31)
            self.slider.setValue(3)
            
        elif operation == "sobel":
            self.slider.setMinimum(1)
            self.slider.setMaximum(31)
            self.slider.setValue(3)
        
        elif operation == "Sharpen":
            self.slider.setMinimum(1)
            self.slider.setMaximum(10)
            self.slider.setValue(1)
        
        elif operation == "High Boost":
            self.slider.setMinimum(10)
            self.slider.setMaximum(50)
            self.slider.setValue(15)
        
        elif operation == "Laplacian Sharpen":
            self.slider.setMinimum(1)
            self.slider.setMaximum(7)
            self.slider.setValue(3)
        
        elif operation == "Multiply Images":
            self.slider.setMinimum(0)
            self.slider.setMaximum(1)
            self.slider.setValue(0)
        
        elif operation == "Add Images":
            self.slider.setMinimum(0)
            self.slider.setMaximum(1)
            self.slider.setValue(0)
        
        elif operation == "Power Law Transformation":
            self.slider.setMinimum(1)
            self.slider.setMaximum(50)
            self.slider.setValue(10)
        
        elif operation == "Histogram Equalization":
            self.slider.setMinimum(0)
            self.slider.setMaximum(1)
            self.slider.setValue(0)
                
        
        else:
            self.slider.setMinimum(0)
            self.slider.setMaximum(1)
            self.slider.setValue(0)
        
        self.apply_processing()

    def apply_processing(self):
        if self.original_image is None:
            return

        operation = self.operation_combo.currentText()
        value = self.slider.value()

        if operation == "Power Law Transformation":
            self.value_label.setText(f"Gamma: {value / 10}")
        else:
            self.value_label.setText(f"Value: {value}")

        if operation == "Gray Scale":
            result = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

        elif operation == "Salt and Pepper":
            result = self.original_image.copy()

            noise_percent = value / 100

            height, width = result.shape[:2]

            number_of_pixels = int(noise_percent * height * width)

            salt_y = np.random.randint(0, height, number_of_pixels)

            salt_x = np.random.randint(0, width, number_of_pixels)

            result[salt_y, salt_x] = 255

            pepper_y = np.random.randint(0, height, number_of_pixels)

            pepper_x = np.random.randint(0, width, number_of_pixels)

            result[pepper_y, pepper_x] = 0
                
        elif operation == "Brightness":
            result = cv2.convertScaleAbs(self.original_image, alpha=1, beta=value)

        elif operation == "Gaussian Blur":
            if value % 2 == 0:
                value += 1

            result = cv2.GaussianBlur(
                self.original_image,
                (value, value),
                0
            )

        elif operation == "median":
            if value % 2 == 0:
                value += 1

            result = cv2.medianBlur(self.original_image, value)
            
            
        elif operation == "mean":
            if value % 2 == 0:
                value += 1

            result = cv2.blur(
                self.original_image,
                (value, value)
    )
            
        elif operation == "Threshold":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

            _, result = cv2.threshold(
                gray,
                value,
                255,
                cv2.THRESH_BINARY
            )

        elif operation == "Canny Edge":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

            result = cv2.Canny(
                gray,
                value,
                value * 2
            )

        elif operation == "laplacian":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

            result = cv2.Laplacian(
                gray,
                cv2.CV_64F,
                ksize=value
            )
            result = cv2.convertScaleAbs(result)
        elif operation == "sobel x":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)    
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=value)
            # sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=value)
            # result = cv2.magnitude(sobelx)
            result = cv2.convertScaleAbs(sobelx)
            
        elif operation == "sobel y":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)    
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=value)
            # sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=value)
            # result = cv2.magnitude(sobely)
            result = cv2.convertScaleAbs(sobely)
        
        elif operation == "sobel":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)    
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=value)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=value)
            result = cv2.magnitude(sobelx, sobely)
            result = cv2.convertScaleAbs(result)
            
        elif operation == "Sharpen":
            blurred = cv2.GaussianBlur(self.original_image, (5, 5), 0)

            mask = cv2.subtract(self.original_image, blurred)

            result = cv2.addWeighted(
                self.original_image,
                1 + (value / 10),
                blurred,
                -(value / 10),
                0)
        elif operation == "High Boost":
            A = value / 10

            blurred = cv2.GaussianBlur(self.original_image, (5, 5), 0)

            result = cv2.addWeighted(
                self.original_image,
                A,
                blurred,
                -(A - 1),
                0
            )
            
        
        elif operation == "Laplacian Sharpen":
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

            if value % 2 == 0:
                value += 1

            laplacian = cv2.Laplacian(
                gray,
                cv2.CV_64F,
                ksize=value
            )

            sharpened = gray - laplacian

            result = cv2.convertScaleAbs(sharpened)
        
        elif operation == "Multiply Images":
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Select Second Image",
                "",
                "Image Files (*.png *.jpg *.jpeg *.bmp)"
            )

            if not file_name:
                return

            second_image = cv2.imread(file_name)

            if second_image is None:
                QMessageBox.warning(self, "Error", "Second image could not be loaded")
                return

            height, width = self.original_image.shape[:2]

            if len(self.original_image.shape) == 2:
                second_image = cv2.cvtColor(second_image, cv2.COLOR_BGR2GRAY)

            second_image = cv2.resize(second_image, (width, height))

            result = cv2.multiply(self.original_image, second_image, scale=1 / 255)
        
        elif operation == "Add Images":
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Select Second Image",
                "",
                "Image Files (*.png *.jpg *.jpeg *.bmp)"
            )

            if not file_name:
                return

            second_image = cv2.imread(file_name)

            if second_image is None:
                QMessageBox.warning(self, "Error", "Second image could not be loaded")
                return

            height, width = self.original_image.shape[:2]

            if len(self.original_image.shape) == 2:
                second_image = cv2.cvtColor(second_image, cv2.COLOR_BGR2GRAY)

            second_image = cv2.resize(second_image, (width, height))

            result = cv2.add(self.original_image, second_image)

        elif operation == "Power Law Transformation":
            gamma = value / 10
            normalized_image = self.original_image.astype(np.float32) / 255.0
            result = np.power(normalized_image, gamma)
            result = (result * 255).astype(np.uint8)
        
        
        elif operation == "Histogram Equalization":
            if len(self.original_image.shape) == 2:
                result = cv2.equalizeHist(self.original_image)

            else:
                ycrcb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2YCrCb)

                ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])

            result = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        
        self.processed_image = result
        self.show_image(result, self.processed_label)
        
        

    def show_image(self, image, label):
        if len(image.shape) == 2:
            height, width = image.shape
            bytes_per_line = width

            q_image = QImage(
                image.data,
                width,
                height,
                bytes_per_line,
                QImage.Format_Grayscale8
            )

        else:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            height, width, channel = rgb_image.shape
            bytes_per_line = channel * width

            q_image = QImage(
                rgb_image.data,
                width,
                height,
                bytes_per_line,
                QImage.Format_RGB888
            )

        pixmap = QPixmap.fromImage(q_image)

        pixmap = pixmap.scaled(
            label.width(),
            label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        label.setPixmap(pixmap)


app = QApplication(sys.argv)

window = ImageProcessingGUI()
window.show()

sys.exit(app.exec())