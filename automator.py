import uiautomator2 as u2
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class AndroidTestAutomator:
    """Базовый класс для автоматизированного взаимодействия с Android-приложениями."""

    def __init__(self, device_address="127.0.0.1:5555"):
        self.device_address = device_address
        self.device = None

    def connect(self):
        try:
            self.device = u2.connect(self.device_address)
            logging.info(f"Подключение установлено: {self.device.info.get('productName', 'Unknown')}")
            return True
        except Exception as e:
            logging.error(f"Сбой подключения к эмулятору/устройству: {e}")
            return False

    def launch_application(self, package_name, timeout=15):
        if not self.device:
            logging.error("Устройство не инициализировано.")
            return False

        self.device.app_start(package_name)
        for _ in range(timeout):
            current_app = self.device.app_current().get('package')
            if current_app == package_name:
                logging.info(f"Процесс {package_name} успешно запущен.")
                return True
            time.sleep(1)

        logging.warning(f"Превышен таймаут запуска {package_name}.")
        return False

    def close_application(self, package_name):
        if self.device:
            self.device.app_stop(package_name)
            logging.info(f"Процесс {package_name} завершен.")