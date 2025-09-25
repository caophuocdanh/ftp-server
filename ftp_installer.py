# -*- coding: utf-8 -*-
# File: installer.py (Phiên bản hoàn thiện với giao diện CLI nâng cao)
# QUAN TRỌNG: Hãy chắc chắn bạn lưu file này với định dạng mã hóa UTF-8

import os
import sys
import shutil
import subprocess
import ctypes
import time
import msvcrt  # Module để xử lý input không chặn trên Windows
import socket  # Module để lấy địa chỉ IP
from colorama import init, Fore, Style, Back

# --- CẤU HÌNH CHUNG ---
INSTALL_DIR = r"C:\windows\ftpserver"
SERVER_EXE_NAME = "ftpserver.exe"
# Tên quy tắc tường lửa hiện được quản lý trực tiếp trong hàm manage_firewall_rule

# --- CẤU HÌNH MÁY CHỦ FTP (Để hiển thị cho người dùng) ---
# Các giá trị này phải khớp với cấu hình trong ftp_server.py
FTP_DISPLAY_ROOT = r"C:\scan"
FTP_DISPLAY_USER = "scan"
FTP_DISPLAY_PASS = "123"

# --- BIỂU TƯỢNG (ICONS) CHO GIAO DIỆN ---
ICON_OK = f" {Back.GREEN}{Fore.WHITE} V {Style.RESET_ALL} "
ICON_ERROR = f" {Back.RED}{Fore.WHITE} X {Style.RESET_ALL} "
ICON_WARN = f" {Back.YELLOW}{Fore.BLACK} ! {Style.RESET_ALL} "
ICON_INFO = f" {Back.BLUE}{Fore.WHITE} * {Style.RESET_ALL} "
ICON_PROMPT = f"{Fore.YELLOW} ==> {Style.RESET_ALL}"

# --- CÁC HÀM TIỆN ÍCH ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_bundled_file_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

def get_local_ip():
    """Lấy địa chỉ IP cục bộ của máy một cách đáng tin cậy."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Không cần phải kết nối được, chỉ cần thử để OS chọn IP phù hợp
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        # Nếu không có mạng, trả về địa chỉ loopback
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def prompt_with_timeout(seconds=5):
    print(f"{ICON_WARN} Nhấn phím bất kỳ để bỏ qua việc chờ...")
    for i in range(seconds * 10, 0, -1):
        countdown_text = f"Tự động tiếp tục sau {Style.BRIGHT}{i/10:.1f}{Style.NORMAL} giây... "
        sys.stdout.write(f"\r{Style.DIM}{countdown_text}{Style.RESET_ALL}")
        sys.stdout.flush()
        if msvcrt.kbhit():
            msvcrt.getch()
            sys.stdout.write("\r" + " " * (len(countdown_text) + 5) + "\r")
            print(f"{ICON_OK} Đã bỏ qua chờ, tiếp tục ngay lập tức.")
            return
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(countdown_text) + 5) + "\r")
    print(f"{ICON_OK} Hết thời gian chờ, tự động tiếp tục.")

def manage_firewall_rule(action):
    print(f"\n{Fore.CYAN}--- ĐĂNG KÝ TƯỜNG LỬA WINDOWS ---")
    base_rule_name = "FTP Server (Cổng 21)"
    protocols = ["TCP", "UDP"]

    for protocol in protocols:
        rule_name = f"{base_rule_name} ({protocol})"
        if action == "add":
            print(f"{ICON_INFO} Mở cổng 21 cho {protocol} (Rule: '{Style.BRIGHT}{rule_name}{Style.NORMAL}')")
            command = [
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name={rule_name}', 'dir=in', 'action=allow',
                f'protocol={protocol}', 'localport=21'
            ]
            
            for attempt in range(2): # Lặp lại tối đa 2 lần
                try:
                    result = subprocess.run(command, check=False, capture_output=True, text=True, encoding='utf-8')
                    
                    if result.returncode == 0:
                        print(f"{ICON_OK} Đã thêm quy tắc Firewall cho {protocol}.")
                        break # Thành công, thoát khỏi vòng lặp thử lại

                    output = f"{result.stdout}{result.stderr}".lower()
                    if 'already exists' in output or 'đã tồn tại' in output:
                        print(f"{ICON_WARN} Quy tắc Firewall cho {protocol} đã tồn tại.")
                        break # Thành công (đã tồn tại), thoát khỏi vòng lặp thử lại
                    
                    # Nếu đến đây, có nghĩa là đã thất bại.
                    if attempt == 0:
                        print(f"{ICON_WARN} Thêm quy tắc thất bại, thử lại sau 1 giây...")
                        time.sleep(1) # Đợi một giây trước khi thử lại
                    else:
                        # Đây là lần thử cuối cùng
                        print(f"{ICON_ERROR} Lỗi khi thêm quy tắc Firewall cho {protocol}:")
                        print(f"{Fore.RED}{result.stdout}{result.stderr}")

                except Exception as e:
                    if attempt == 0:
                        print(f"{ICON_WARN} Gặp lỗi, thử lại sau 1 giây... ({e})")
                        time.sleep(1)
                    else:
                        print(f"{ICON_ERROR} Lỗi ngoại lệ khi thêm quy tắc Firewall cho {protocol}: {e}")
        
        elif action == "remove":
            print(f"{ICON_INFO} Xóa quy tắc Firewall '{Style.BRIGHT}{rule_name}{Style.NORMAL}'")
            command = ['netsh', 'advfirewall', 'firewall', 'delete', 'rule', f'name={rule_name}']
            try:
                # Việc xóa một quy tắc không tồn tại không gây ra lỗi nghiêm trọng, vì vậy chúng ta chỉ cần chạy nó.
                subprocess.run(command, check=False, capture_output=True)
                print(f"{ICON_OK} Đã xử lý xóa quy tắc Firewall cho {protocol} (nếu tồn tại).")
            except Exception as e:
                print(f"{ICON_ERROR} Lỗi khi xóa quy tắc Firewall cho {protocol}: {e}")

# ===============================================================
# === HÀM INSTALL ĐÃ ĐƯỢC CẬP NHẬT ===
# ===============================================================
def install():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- BẮT ĐẦU QUÁ TRÌNH CÀI ĐẶT ---")
    
    print(f"{ICON_INFO} Tạo thư mục: {Style.BRIGHT}{INSTALL_DIR}{Style.NORMAL}")
    os.makedirs(INSTALL_DIR, exist_ok=True)

    source_server_path = get_bundled_file_path(SERVER_EXE_NAME)
    dest_server_path = os.path.join(INSTALL_DIR, SERVER_EXE_NAME)
    print(f"{ICON_INFO} Sao chép file dịch vụ tới: {Style.BRIGHT}{dest_server_path}{Style.NORMAL}")
    shutil.copy2(source_server_path, dest_server_path)

    manage_firewall_rule("add")

    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- BẮT ĐẦU ĐĂNG KÝ DỊCH VỤ WINDOWS ---")
    print(f"{ICON_INFO} Đăng ký Dịch vụ Windows...")
    try:
        subprocess.run(
            [dest_server_path, '--startup', 'auto', 'install'],
            check=True, capture_output=True, text=True, encoding='utf-8'
        )
        print(f"{ICON_OK} Đăng ký dịch vụ thành công.")
        
        print(f"{ICON_INFO} Khởi động dịch vụ...")
        subprocess.run([dest_server_path, 'start'], check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"{ICON_OK} Dịch vụ đã được khởi động.")
        
        # === PHẦN MỚI: HIỂN THỊ TÓM TẮT CẤU HÌNH ===
        print(f"\n{Fore.GREEN}{Style.BRIGHT}===> {ICON_OK} {Fore.GREEN}{Style.BRIGHT}CÀI ĐẶT HOÀN TẤT! {Fore.GREEN}{Style.BRIGHT}<===")
        local_ip = get_local_ip()
        print(f"{Fore.CYAN}{Style.BRIGHT}------------------------------------")
        print(f"{Fore.CYAN}{Style.BRIGHT}| {ICON_INFO} {'FTP_DIR':<10} = {FTP_DISPLAY_ROOT}{Fore.CYAN}{Style.BRIGHT}       |")
        print(f"{Fore.CYAN}{Style.BRIGHT}| {ICON_INFO} {'FTP_AUTH':<10} = {FTP_DISPLAY_USER}|{FTP_DISPLAY_PASS}{Fore.CYAN}{Style.BRIGHT}      |")
        print(f"{Fore.CYAN}{Style.BRIGHT}| {ICON_INFO} {'FTP_IP':<10} = {local_ip}{Fore.CYAN}{Style.BRIGHT} |")
        print(f"{Fore.CYAN}{Style.BRIGHT}------------------------------------")
        # =============================================

    except subprocess.CalledProcessError as e:
        print(f"\n{Back.RED}{Fore.WHITE}{Style.BRIGHT} ===> {ICON_ERROR} LỖI <=== ")
        print(f"{Fore.RED}Lỗi khi đăng ký hoặc khởi động dịch vụ:\n{e.stderr}")
    except FileNotFoundError:
        print(f"\n{ICON_ERROR} LỖI: Không tìm thấy file server để đóng gói. Bạn đã đóng gói đúng cách chưa?")


def uninstall():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- BẮT ĐẦU QUÁ TRÌNH GỠ CÀI ĐẶT ---")
    dest_server_path = os.path.join(INSTALL_DIR, SERVER_EXE_NAME)

    if not os.path.exists(dest_server_path):
        print(f"{ICON_WARN} Dịch vụ dường như chưa được cài đặt. Vẫn tiến hành dọn dẹp tường lửa...")
        manage_firewall_rule("remove")
        return

    print(f"{ICON_INFO} Dừng và xóa Dịch vụ...")
    try:
        subprocess.run([dest_server_path, 'stop'], capture_output=True)
        subprocess.run([dest_server_path, 'remove'], check=True, capture_output=True, encoding='utf-8')
        print(f"{ICON_OK} Đã xóa dịch vụ.")
    except Exception:
        print(f"{ICON_WARN} Dịch vụ không tồn tại hoặc đã được xóa trước đó.")

    manage_firewall_rule("remove")

    print(f"{ICON_INFO} Xóa thư mục cài đặt: {Style.BRIGHT}{INSTALL_DIR}{Style.NORMAL}")
    try:
        shutil.rmtree(INSTALL_DIR)
        print(f"{ICON_OK} Đã xóa thư mục.")
    except Exception as e:
        print(f"{ICON_ERROR} Không thể xóa thư mục: {e}")

    print(f"\n{Fore.GREEN}{Style.BRIGHT}===> {ICON_OK} {Fore.GREEN}{Style.BRIGHT}GỠ CÀI ĐẶT HOÀN TẤT! <===")


def main():
    init(autoreset=True)
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')

    if not is_admin():
        print(f"{ICON_ERROR}{Fore.RED}{Style.BRIGHT} LỖI: Vui lòng chạy với quyền Administrator.")
        input(f"{Style.DIM}Nhấn Enter để thoát.")
        return

    print(f"{Fore.YELLOW}{Style.BRIGHT}Bạn muốn làm gì?")
    print(f" {Fore.GREEN}{Style.BRIGHT}1. Cài đặt hoặc Cập nhật (Install / Update)")
    print(f" {Fore.GREEN}{Style.BRIGHT}2. Gỡ cài đặt (Uninstall)")
    choice = input(f"{ICON_PROMPT} Chọn (1/2): ")

    if choice == '1':
        dest_server_path = os.path.join(INSTALL_DIR, SERVER_EXE_NAME)
        if os.path.exists(dest_server_path):
            print(f"\n{ICON_WARN} {Fore.YELLOW}Đã phát hiện phiên bản cũ.")
            print(f"{Fore.YELLOW}Tiến hành gỡ bỏ phiên bản cũ để chuẩn bị cài đặt phiên bản mới.\n")
            prompt_with_timeout(seconds=5)
            uninstall() 
            print(f"\n{ICON_OK} Gỡ bỏ phiên bản cũ hoàn tất. Bắt đầu quá trình cài đặt mới...")
        
        install()

    elif choice == '2':
        dest_server_path = os.path.join(INSTALL_DIR, SERVER_EXE_NAME)
        if not os.path.exists(dest_server_path):
             print(f"\n{ICON_WARN} {Fore.YELLOW}Không tìm thấy dịch vụ nào để gỡ cài đặt.")
        else:
             uninstall()
    else:
        print(f"{ICON_ERROR} {Fore.RED}Lựa chọn không hợp lệ.")
    
    input(f"\n{Fore.GREEN}{Style.BRIGHT}Nhấn Enter để thoát.")

if __name__ == '__main__':
    main()
