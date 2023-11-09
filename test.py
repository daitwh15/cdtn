import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap

class ObjectListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Objects List with Image and Text')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        list_widget = QListWidget()

        objects = [
            {'name': 'Object 1', 'image_path': 'https://www.google.com/search?q=anh&sca_esv=580810206&rlz=1C1KNTJ_enVN1012VN1012&tbm=isch&sxsrf=AM9HkKmFvFQmFBlf_oniDZDYPGl2qJz9SQ:1699526248317&source=lnms&sa=X&ved=2ahUKEwidv8TS3LaCAxUZk1YBHXuRBDgQ_AUoAXoECAMQAw&biw=1536&bih=715&dpr=1.25#imgrc=r1QLeemu7J6gHM'},
            {'name': 'Object 2', 'image_path': 'path_to_image2.png'},
            {'name': 'Object 3', 'image_path': 'path_to_image3.png'},
            # Add more objects as needed
        ]

        for obj in objects:
            list_item = QListWidgetItem()
            # list_item.setSizeHint(200, 60)  # Set the size for each item in the list

            h_layout = QHBoxLayout()

            image_label = QLabel()
            pixmap = QPixmap(obj['image_path'])
            pixmap = pixmap.scaledToWidth(50)  # Set the image width
            image_label.setPixmap(pixmap)

            text_label = QLabel(obj['name'])

            h_layout.addWidget(image_label)
            h_layout.addWidget(text_label)

            widget = QWidget()
            widget.setLayout(h_layout)

            list_widget.addItem(list_item)
            list_widget.setItemWidget(list_item, widget)

        layout.addWidget(list_widget)
        self.setLayout(layout)
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = ObjectListWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
