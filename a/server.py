import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon, QPixmap, QPainter
import socket
import threading


class ServerWindow(QMainWindow):
    def __init__(self):
        super(ServerWindow, self).__init__()
        self.setWindowTitle("服务器")
        self.setWindowIcon(QIcon("1.jpg"))
        self.resize(400, 300)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        self.pixmap = QPixmap('3.PNG')
        
        self.ip_line_edit = QLineEdit()
        self.ip_line_edit.setPlaceholderText("请输入IP")
        self.port_line_edit = QLineEdit()
        self.port_line_edit.setPlaceholderText("请输入端口号")
        self.send_text_edit = QTextEdit()
        self.send_text_edit.setFixedHeight(50)
        self.send_text_edit.setReadOnly(False)
        self.receive_text_edit = QTextEdit()
        self.receive_text_edit.setFixedHeight(200)
        self.receive_text_edit.setReadOnly(True)
        self.send_button = QPushButton("发送")
        self.accept_button=QPushButton("连接")
        
        layout = QVBoxLayout()
        layout.addWidget(self.receive_text_edit)
        layout.addWidget(self.send_text_edit)
        layout.addWidget(self.send_button)
        layout.addWidget(self.ip_line_edit)
        layout.addWidget(self.port_line_edit)
        layout.addWidget(self.accept_button)
        self.main_widget.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)
        self.accept_button.clicked.connect(self.connect_to_client)

        self.server_socket = None

    def closeEvent(self, event):
        self.client_socket.close()
        event.accept()

    @Slot()
    def send_message(self):
        if not self.client_socket:
            QMessageBox.warning(self, "警告", "请先连接服务器")
            return
        
        message = self.send_text_edit.toPlainText()
        self.client_socket.sendall(message.encode("utf-8"))
        self.receive_text_edit.append("已发送：" + message)
        self.send_text_edit.clear()
        
    @Slot()
    def connect_to_client(self):
        ip = self.ip_line_edit.text()
        port = int(self.port_line_edit.text())

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(1)

        self.client_socket, client_address = self.server_socket.accept()
        
        self.receive_text_edit.append("已连接客户机")

        threading.Thread(target=self.receive_message).start()
        

    def receive_message(self):
        while True:
            message = self.client_socket.recv(1024).decode("utf-8")
            self.receive_text_edit.append("客户机：" + message)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerWindow()
    window.show()
    sys.exit(app.exec_())
