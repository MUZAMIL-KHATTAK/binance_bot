import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QSystemTrayIcon, QComboBox, QMessageBox
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal
import requests

def whatsappMessage(msg,Ph_Number):
    # Ph_Number = Ph_Number
    instance_id='63F4EDD091777'
    access_token='a27e1f9ca2347bb766f332b8863ebe9f'
    url = f'https://mkt.eziline.com/api/send.php?number={Ph_Number}&type=text&message={msg}&instance_id={instance_id}&access_token={access_token}'
    # response = url
    
    try:
        response = requests.get(url)  # Adjust the HTTP method and request parameters as needed
        response.raise_for_status()  # Raise an exception if the API request was unsuccessful
        api_data = response.json()  # Extract the response data as JSON
        # Process the API response data
        print(api_data)

    except requests.exceptions.RequestException as e:
        # Handle any errors that occurred during the API request
        print('Error:', e)

class WorkerThread(QThread):
    update_progress = pyqtSignal(str)

    def __init__(self, selected_option, value,Ph_Number):
        super().__init__()
        self.selected_option = selected_option
        self.value = value
        self.check = True
        self.Ph_Num = Ph_Number

    def stop(self):
        self.check = False

    def run(self):
        options = Options()
        options.page_load_strategy = 'normal'
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-javascript")  # Disable JavaScript
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("start-minimized")  # open Browser in maximized mode
        options.add_argument("disable-infobars")  # disabling infobars
        options.add_argument("--disable-extensions")  # disabling extensions
        options.add_argument("--disable-gpu")  # applicable to windows os only
        options.add_argument("--remote-debugging-port=9222")  # use this port to debug
        options.add_argument("--disable-browser-side-navigation")  # Disable browser side navigation
        options.add_argument("--disable-features=VizDisplayCompositor")  # Disable

        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get(f"https://p2p.binance.com/en/trade/{self.selected_option}/USDT?fiat=USD")
        time.sleep(2)
        driver.back()
        filter_box = driver.find_element(By.CLASS_NAME, "css-5xw3l7")
        filter_box.click()
        time.sleep(2)
        filter_box = driver.find_element(By.CLASS_NAME, "css-1iztezc")
        filter_box.click()
        time.sleep(2)
        Refresh_2 = driver.find_element(By.CLASS_NAME, 'css-ybbx55')
        Refresh_2.click()
        Refresh_2.click()
        Refresh = driver.find_element(By.CLASS_NAME, 'css-10nf7hq')
        Refresh_button = driver.find_element(By.CLASS_NAME, 'css-s64j3f')
        Refresh_button.click()
        ten_sec = driver.find_element(By.XPATH,
                                      '//*[@id="__APP"]/div[2]/main/div[1]/div[3]/div[2]/div/div[6]/div/div[2]/div/div[2]')
        ten_sec.click()
        driver.implicitly_wait(10)
        count = 0
        while self.check:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            price = soup.find_all('div', class_='css-1m1f8hn')
            Ph_Numbr = self.Ph_Num
            for p in price:
                rates = p.text
                rates = float(rates)
                num = float(self.value)
                if rates < num:
                    count+=1
                    self.update_progress.emit('spotted')
                    notification_message = f"Your Rate was: {num} and the Spotted rate is {rates}"
                    whatsappMessage(notification_message,Ph_Numbr)
                if count == 10:
                    break                    
                else:
                    self.update_progress.emit('Price is high')
            # if count == 10:
            #     break

            time.sleep(8)
        driver.quit()
        
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Binance-App")
        self.setFixedSize(400, 150)
        self.label_Figure = QLabel(self)
        self.label_Figure.setText("Enter Rate here:")
        self.label_Figure.setStyleSheet("color: #112A46;")
        self.label_Figure.move(10, 15)
        self.input_Figure = QLineEdit(self)
        self.input_Figure.setStyleSheet("color: #112A46;")
        self.input_Figure.move(135, 10)
        self.input_Figure.resize(120, 30)

        self.label = QLabel(self)
        self.label.setText("Enter Phone Number:")
        self.label.setStyleSheet("color: #112A46;")
        self.label.move(10, 55)
        self.input = QLineEdit(self)
        self.input.setStyleSheet("color: #112A46;")
        self.input.setPlaceholderText("923123456789") 

        self.input.move(135, 50)
        self.input.resize(120, 30)

        self.label_dropdown = QLabel(self)
        self.label_dropdown.setText("Choose Your Bank:")
        self.label_dropdown.setStyleSheet("color: #112A46;")
        self.label_dropdown.move(10, 95)
        self.dropdown = QComboBox(self)
        self.dropdown.addItem("BankofAmerica")
        self.dropdown.addItem("Zelle")
        self.dropdown.move(135, 95)
        self.button = QPushButton("Check", self)
        self.button.setStyleSheet("color: #112A46;")
        self.button.move(330, 10)
        self.button.resize(60, 70)
        self.button.clicked.connect(self.start_check)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet("color: #112A46;")
        self.stop_button.move(260, 10)
        self.stop_button.resize(60, 70)
        self.stop_button.clicked.connect(self.stop_check)
        self.setStyleSheet("background-color: #F9EBEA;")
        self.setStyleSheet("border-color: #C39BD3;\n"
        "border-width: 5px;")
        self.worker_thread = None
        
    def start_check(self):
        text = self.input_Figure.text()
        Number = self.input.text()
        if not text or not Number:
            QMessageBox.warning(self, 'Error', 'Input is empty!')

        else:
            print(f"Submitted text: {text}")
            value = float(text)
            Ph_Number = Number
            selected_option = self.dropdown.currentText()
            print(f"Selected option: {selected_option}")

            if self.worker_thread is not None and self.worker_thread.isRunning():
                self.worker_thread.stop()

            self.worker_thread = WorkerThread(selected_option, value, Ph_Number)
            self.worker_thread.update_progress.connect(self.handle_progress)
            self.worker_thread.start()

    def stop_check(self):
        if self.worker_thread is not None and self.worker_thread.isRunning():
            self.worker_thread.stop()

    def handle_progress(self, message):
        print(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    icon = QIcon('icon.ico')
    window.setWindowIcon(QIcon(icon))
    tray_icon = QSystemTrayIcon(window)
    tray_icon.setIcon(QIcon(icon))
    
    tray_icon.showMessage("Title", "Message", icon)
    tray_icon.show()
    window.show()
    sys.exit(app.exec_())