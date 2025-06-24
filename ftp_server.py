# File: ftp_server.py (Phiên bản Dịch vụ Windows chính thống)
import os
import sys
import logging
import threading
import servicemanager  # Từ pywin32
import win32service  # Từ pywin32
import win32serviceutil  # Từ pywin32
import win32event  # Từ pywin32

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# --- Cấu hình ---
SERVICE_NAME = "ftpserver"
SERVICE_DISPLAY_NAME = "FTP Server"
LOG_DIR = r"C:\scan"
FTP_ROOT = r"C:\scan"
log_file = os.path.join(LOG_DIR, "ftp_service.log")

# Thiết lập logging cơ bản
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class FTPServerThread(threading.Thread):
    """Lớp chạy server FTP trong một luồng riêng biệt."""
    def __init__(self):
        super().__init__()
        self.server = None

    def run(self):
        logging.info("FTP server thread starting...")
        try:
            # Tạo thư mục gốc nếu chưa có
            if not os.path.exists(FTP_ROOT):
                os.makedirs(FTP_ROOT)
                logging.info(f"Created FTP root directory: {FTP_ROOT}")

            authorizer = DummyAuthorizer()
            authorizer.add_user("scan", "123", FTP_ROOT, perm='elradfmw')
            
            handler = FTPHandler
            handler.authorizer = authorizer
            handler.banner = "FTP Server Ready."
            
            address = ("0.0.0.0", 21)
            self.server = FTPServer(address, handler)
            
            logging.info(f"FTP server listening on {address[0]}:{address[1]}")
            self.server.serve_forever()
            logging.info("FTP server has stopped serving.")

        except Exception as e:
            logging.error(f"Error in FTP server thread: {e}", exc_info=True)

    def stop(self):
        logging.info("Stopping FTP server...")
        if self.server:
            self.server.close_all()
        logging.info("FTP server stopped.")

class MyFTPService(win32serviceutil.ServiceFramework):
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME
    _svc_description_ = "FTP server running as a Windows service."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.ftp_thread = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        logging.info("Stop signal received. Stopping service.")
        if self.ftp_thread:
            self.ftp_thread.stop()
        win32event.SetEvent(self.hWaitStop)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        logging.info("Service stopped.")

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        logging.info("Service is starting.")
        
        self.main()
        
        # Chờ tín hiệu dừng
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
        logging.info("Exit signal received from SvcStop.")

    def main(self):
        self.ftp_thread = FTPServerThread()
        self.ftp_thread.start()
        logging.info("FTP server thread has been started.")

if __name__ == '__main__':
    # Đoạn này cho phép chúng ta quản lý dịch vụ từ dòng lệnh
    # ví dụ: python ftp_server.py install
    #        python ftp_server.py start
    #        python ftp_server.py stop
    #        python ftp_server.py remove
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyFTPService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyFTPService)