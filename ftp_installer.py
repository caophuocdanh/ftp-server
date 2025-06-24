# File: installer.py (Trình cài đặt và gỡ cài đặt mới)
import os
import sys
import shutil
import subprocess
import ctypes

# --- CẤU HÌNH ---
# Vị trí cài đặt cố định
INSTALL_DIR = r"C:\windows\ftpserver"
# Tên file dịch vụ sẽ được sao chép
SERVER_EXE_NAME = "ftpserver.exe"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_bundled_file_path(filename):
    """Lấy đường dẫn của file được PyInstaller đóng gói kèm."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

def install():
    print("--- Bat dau qua trinh cai dat ---")
    
    # 1. Tạo thư mục cài đặt cố định
    print(f"Tao thu muc: {INSTALL_DIR}")
    os.makedirs(INSTALL_DIR, exist_ok=True)

    # 2. Sao chép file server vào vị trí cố định
    source_server_path = get_bundled_file_path(SERVER_EXE_NAME)
    dest_server_path = os.path.join(INSTALL_DIR, SERVER_EXE_NAME)
    print(f"Sao chep file server toi: {dest_server_path}")
    shutil.copy2(source_server_path, dest_server_path)

    # 3. Gọi lệnh "install" của chính file server tại vị trí mới
    print("Dang ky dich vu Windows...")
    try:
        # Chạy lệnh: C:\FTPService\ftp_server.exe --startup auto install
        subprocess.run(
            [dest_server_path, '--startup', 'auto', 'install'],
            check=True, capture_output=True, text=True
        )
        print(" -> Dang ky dich vu thanh cong.")
        
        # 4. Khởi động dịch vụ
        print("Khoi dong dich vu...")
        subprocess.run([dest_server_path, 'start'], check=True, capture_output=True, text=True)
        print(" -> Dich vu da duoc khoi dong.")
        
        print("\n--- CAI DAT HOAN TAT! ---")

    except subprocess.CalledProcessError as e:
        print("\n--- LOI ---")
        print(f"Loi khi dang ky hoac khoi dong dich vu:\n{e.stderr}")
    except FileNotFoundError:
        print("\nLOI: Khong tim thay file server de dong goi. Ban da dong goi dung cach chua?")

def uninstall():
    print("--- Bat dau qua trinh go cai dat ---")
    dest_server_path = os.path.join(INSTALL_DIR, SERVER_EXE_NAME)

    if not os.path.exists(dest_server_path):
        print("Dich vu duong nhu chua duoc cai dat. Khong tim thay file.")
        return

    # 1. Dừng và xóa dịch vụ
    print("Dung va xoa dich vu...")
    try:
        subprocess.run([dest_server_path, 'stop'], capture_output=True)
        subprocess.run([dest_server_path, 'remove'], check=True, capture_output=True)
        print(" -> Da xoa dich vu.")
    except Exception:
        # Bỏ qua lỗi nếu dịch vụ không tồn tại
        print(" -> Dich vu khong ton tai hoac da duoc xoa.")

    # 2. Xóa thư mục cài đặt
    print(f"Xoa thu muc cai dat: {INSTALL_DIR}")
    try:
        shutil.rmtree(INSTALL_DIR)
        print(" -> Da xoa thu muc.")
    except Exception as e:
        print(f" -> Khong the xoa thu muc: {e}")

    print("\n--- GO CAI DAT HOAN TAT! ---")


def main():
    if not is_admin():
        print("LOI: Vui long chay voi quyen Administrator.")
        input("Nhan Enter de thoat.")
        return

    # Hỏi người dùng muốn làm gì
    print("Ban muon lam gi?")
    print(" 1. Cai dat (Install)")
    print(" 2. Go cai dat (Uninstall)")
    choice = input("Chon (1/2): ")

    if choice == '1':
        install()
    elif choice == '2':
        uninstall()
    else:
        print("Lua chon khong hop le.")
    
    input("\nNhan Enter de thoat.")

if __name__ == '__main__':
    main()