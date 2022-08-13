from PyQt5 import QtGui, QtCore, QtWidgets
from datetime import datetime
import numpy as np
import cv2
import sys
import os
import main_ui, progress_bar_ui, filter_feature_ui, filter_age_ui


class MainWindow(QtWidgets.QMainWindow, main_ui.Ui_MainWindow):
    def __init__(self):
        # Obligatory main setup
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)

        # Variables initialization
        self.file_paths = []
        self.sharpness = 0
        self.contrast = 0
        self.dt = datetime.now()

        # Widget-related initialization
        self.feature_pbar_dialog = ProgressBarDialog(window_title='Scan Feature')
        self.age_pbar_dialog = ProgressBarDialog(window_title='Scan Age')
        self.filter_feature_dialog = None
        self.filter_age_dialog = None
        self.model = None

        # Widget configurations
        self.feature_pbar_dialog.hide()
        self.age_pbar_dialog.hide()
        self.selectDirBtn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.selectDirBtn.setIcon(QtGui.QIcon('icons/select_folder.png'))
        self.selectDirBtn.setIconSize(QtCore.QSize(36, 36))
        self.scanFeatureBtn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.scanFeatureBtn.setIcon(QtGui.QIcon('icons/features.png'))
        self.scanFeatureBtn.setIconSize(QtCore.QSize(36, 36))
        self.scanAgeBtn.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.scanAgeBtn.setIcon(QtGui.QIcon('icons/calendar.png'))
        self.scanAgeBtn.setIconSize(QtCore.QSize(36, 36))

        # Button function assignments
        self.selectDirBtn.clicked.connect(self.select_directory)
        self.scanFeatureBtn.clicked.connect(self.start_feature_scan)
        self.scanAgeBtn.clicked.connect(self.start_age_scan)

        # Show main window
        self.show()

    def select_directory(self):
        # Open Window's directory selector
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')

        # Display the tree-view
        if dir_path:
            self.display_treeview(dir_path)

    def display_treeview(self, path):
        # Create the model to be applied to the tree-view (think of it as a structure format I guess)
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(path)

        # Get the index of the path to be displayed on the tree-view
        path_index = self.model.index(path)

        # Set the model of the tree-view and update the root index
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(path_index)

    def get_image_paths(self):
        # Empty the file path list
        self.file_paths.clear()

        # Get the tree-view indexes of the selected images
        indexes = self.treeView.selectedIndexes()

        # Get the file path for each of the indexes and append to the file path list
        for index in indexes:
            file_path = self.model.filePath(index)
            if file_path not in self.file_paths:
                self.file_paths.append(self.model.filePath(index))

    def get_feature_inputs(self):
        # Prompt the dialog box
        sharpness, _ = QtWidgets.QInputDialog.getDouble(self, 'Set Filter Value', 'Sharpness: ', value=self.sharpness)
        contrast, _ = QtWidgets.QInputDialog.getDouble(self, 'Set Filter Value', 'Contrast: ', value=self.contrast)

        # Assign the sharpness and contrast value
        self.sharpness = sharpness
        self.contrast = contrast

    def update_feature_pbar_progress(self, current_index):
        self.feature_pbar_dialog.progressBar.setValue(int(current_index/len(self.file_paths)*100))

    def update_age_pbar_progress(self, current_index):
        self.age_pbar_dialog.progressBar.setValue(int(current_index/len(self.file_paths)*100))

    def start_feature_scan(self):
        # Get the selected images' paths from the tree-view
        self.get_image_paths()

        # Get the user input for sharpness and contrast
        confirmed = FilterFeatureDialog(parent=self).exec_()

        # If the user clicks "confirm"
        if confirmed:
            if self.file_paths:
                # Display the progress bar dialog
                self.feature_pbar_dialog.show()

                # Create the separate folders to sort the images
                folder_names = [
                    f'sharpness_LT_{self.sharpness}contrast_LT_{self.contrast}',
                    f'sharpness_MT_{self.sharpness}contrast_MT_{self.contrast}',
                    f'sharpness_LT_{self.sharpness}contrast_MT_{self.contrast}',
                    f'sharpness_MT_{self.sharpness}contrast_LT_{self.contrast}'
                ]
                if not os.path.exists(folder_names[0]):
                    os.mkdir(folder_names[0])
                if not os.path.exists(folder_names[1]):
                    os.mkdir(folder_names[1])
                if not os.path.exists(folder_names[2]):
                    os.mkdir(folder_names[2])
                if not os.path.exists(folder_names[3]):
                    os.mkdir(folder_names[3])

                # Go through every image
                for i, file_path in enumerate(self.file_paths):
                    # Skip if is a folder
                    if os.path.isdir(file_path):
                        continue

                    # Get the file name
                    file_name = file_path.split('/')[-1]

                    # Open the image and convert it to gray-scale
                    image = cv2.imread(file_path)
                    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    # Calculate the image's sharpness
                    sharpness = self.get_image_sharpness(image_gray)

                    # Calculate the image's contrast
                    contrast = self.get_image_contrast(image_gray)

                    # Sort the images
                    if sharpness < self.sharpness and contrast < self.contrast:
                        cv2.imwrite(f'{folder_names[0]}\\{file_name}', image)
                    elif sharpness > self.sharpness and contrast > self.contrast:
                        cv2.imwrite(f'{folder_names[1]}\\{file_name}', image)
                    elif sharpness < self.sharpness and contrast > self.contrast:
                        cv2.imwrite(f'{folder_names[2]}\\{file_name}', image)
                    elif sharpness > self.sharpness and contrast < self.contrast:
                        cv2.imwrite(f'{folder_names[3]}\\{file_name}', image)

                    # Update the progress bar value
                    self.update_feature_pbar_progress(current_index=i)

                    # Call this method to update the GUI thus showing the flowing effect of the progress bar
                    QtWidgets.QApplication.processEvents()
            else:
                self.display_nfs_message()

            # Hide and reset the progress bar
            self.feature_pbar_dialog.hide()
            self.feature_pbar_dialog.progressBar.setValue(0)

            # Clear the selection
            self.treeView.clearSelection()

    def get_image_sharpness(self, image):
        # Convert the image object to a numpy array to perform calculations
        image_array = np.asarray(image, dtype=np.int32)

        # Calculate the image's sharpness
        gy, gx = np.gradient(image_array)
        g_norm = np.sqrt(gx ** 2 + gy ** 2)
        sharpness = np.average(g_norm)

        return sharpness

    def get_image_contrast(self, image):
        # Return image's contrast
        return image.std()

    def start_age_scan(self):
        # Get the selected images' paths from the tree-view
        self.get_image_paths()

        # Get user input for the datetime
        confirmed = FilterAgeDialog(parent=self).exec_()

        # If the user clicks "confirm"
        if confirmed:
            if self.file_paths:
                # Display the progress bar dialog
                self.age_pbar_dialog.show()

                # Create the separate folders to sort the images
                folder_names = [
                    f'before_{self.dt.strftime("%Y-%M-%d")}',
                    f'after_{self.dt.strftime("%Y-%M-%d")}',
                ]
                if not os.path.exists(folder_names[0]):
                    os.mkdir(folder_names[0])
                if not os.path.exists(folder_names[1]):
                    os.mkdir(folder_names[1])

                # Go through every image
                for i, file_path in enumerate(self.file_paths):
                    # Skip if is a folder
                    if os.path.isdir(file_path):
                        continue

                    # Get the file name
                    file_name = file_path.split('/')[-1]

                    # Open the image and convert it to gray-scale
                    image = cv2.imread(file_path)

                    # Get the image's last-modified date
                    timestamp = os.path.getmtime(file_path)
                    dt = datetime.fromtimestamp(timestamp)

                    # Sort the images
                    if dt < self.dt:
                        cv2.imwrite(f'{folder_names[0]}\\{file_name}', image)
                    elif dt > self.dt:
                        cv2.imwrite(f'{folder_names[1]}\\{file_name}', image)

                    # Update the progress bar value
                    self.update_age_pbar_progress(current_index=i)

                    # Call this method to update the GUI thus showing the flowing effect of the progress bar
                    QtWidgets.QApplication.processEvents()
            else:
                self.display_nfs_message()

            # Hide and reset the progress bar
            self.age_pbar_dialog.hide()
            self.age_pbar_dialog.progressBar.setValue(0)

            # Clear the selection
            self.treeView.clearSelection()

    def display_nfs_message(self):
        QtWidgets.QMessageBox.about(self, 'No Image Selected', 'You have not selected an image to be processed')


class ProgressBarDialog(QtWidgets.QDialog, progress_bar_ui.Ui_Dialog):
    def __init__(self, window_title=''):
        # Obligatory main setup
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)

        # Set the title of the window
        self.setWindowTitle(window_title)

        # Prevent interaction on the parent window
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)

        # Show the dialog
        self.show()


class FilterFeatureDialog(QtWidgets.QDialog, filter_feature_ui.Ui_Dialog):
    def __init__(self, parent=None):
        # Obligatory main setup
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)

        # Set the title of the window
        self.setWindowTitle('Scan Feature')

        # Variables initialization
        self.parent = parent

        # Button function assignments
        self.cancelBtn.clicked.connect(self.reject)
        self.confirmBtn.clicked.connect(self.return_values_to_parent)

        # Widget configurations
        self.initialize_spinbox_value()

    def initialize_spinbox_value(self):
        # Initialize the values of the spinbox
        if self.parent:
            self.sharpnessSpinbox.setValue(self.parent.sharpness)
            self.contrastSpinbox.setValue(self.parent.contrast)

    def return_values_to_parent(self):
        # Return the datetime to the parent (MainWindow)
        if self.parent:
            # Get the sharpness and contrast from the spin-boxes
            sharpness = self.sharpnessSpinbox.value()
            contrast = self.contrastSpinbox.value()

            # Pass the values to the parent (MainWindow)
            self.parent.sharpness = sharpness
            self.parent.contrast = contrast

            # Close the dialog
            self.accept()


class FilterAgeDialog(QtWidgets.QDialog, filter_age_ui.Ui_Dialog):
    def __init__(self, parent=None):
        # Obligatory main setup
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)

        # Set the title of the window
        self.setWindowTitle('Scan Age')

        # Variables initialization
        self.parent = parent

        # Button function assignments
        self.cancelBtn.clicked.connect(self.reject)
        self.confirmBtn.clicked.connect(self.return_values_to_parent)

        # Widget configurations
        self.initialize_dateedit_value()

    def initialize_dateedit_value(self):
        # Initialize the values of the date-edit
        if self.parent:
            qdate = QtCore.QDate(self.parent.dt.year, self.parent.dt.month, self.parent.dt.day)
            qtime = QtCore.QTime(self.parent.dt.hour, self.parent.dt.minute, self.parent.dt.second)
            qdatetime = QtCore.QDateTime(qdate, qtime)
            self.dateTimeEdit.setDateTime(qdatetime)

    def return_values_to_parent(self):
        # Return the datetime to the parent (MainWindow)
        if self.parent:
            # Get the datetime object from the datetime edit widget
            dt = self.dateTimeEdit.dateTime().toPyDateTime()

            # Pass the datetime to the parent (MainWindow)
            self.parent.dt = dt

            # Close the dialog
            self.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
