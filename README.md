# FTP Server Service

## 📋 Giới thiệu

**FTP Server Service** là một ứng dụng Windows Service đơn giản để chia sẻ file qua giao thức FTP. Server tự động khởi động cùng Windows và cung cấp truy cập FTP với thư mục gốc tại `C:\scan`.

### ✨ Tính năng

- ✅ **Windows Service**: Chạy tự động khi khởi động máy
- ✅ **FTP Server**: Hỗ trợ đầy đủ giao thức FTP 
- ✅ **Installer đơn giản**: Cài đặt/gỡ cài đặt với 1 click
- ✅ **Firewall tự động**: Tự động mở port 21
- ✅ **Logging**: Ghi log chi tiết hoạt động
- ✅ **Không cần Python**: Đóng gói sẵn executable

## 📁 Cấu trúc dự án

```
FTP Server/
├── ftp_server.py          # FTP Server service (114 dòng)
├── ftp_installer.py       # Installer với UI đầy màu (208 dòng)  
├── ftp_server.ico         # Icon Windows
└── build.cmd             # Script build tự động
```

## 💻 Yêu cầu hệ thống

| Yêu cầu | Chi tiết |
|---------|----------|
| **OS** | Windows 7/8/10/11, Windows Server 2012+ |
| **Quyền** | Administrator (bắt buộc cho cài đặt) |
| **RAM** | 512 MB+ |
| **Disk** | 100 MB trống |
| **Network** | Port 21 (FTP), Port 20 (Active mode) |

## 🚀 Cài đặt

### Cách 1: Sử dụng Installer (Khuyến nghị)

1. **Tải file `ftpinstaller.exe`**

2. **Chạy với quyền Administrator**:
   ```cmd
   # Chuột phải -> "Run as administrator"  
   ftpinstaller.exe
   ```

3. **Chọn tùy chọn**:
   ```
   Bạn muốn làm gì?
    1. Cài đặt hoặc Cập nhật
    2. Gỡ cài đặt  
   ==> Chọn (1/2): 1
   ```

4. **Kết quả**:
   ```
   ✓ CÀI ĐẶT HOÀN TẤT!
   | FTP_DIR  = C:\scan     |
   | FTP_AUTH = scan|123    |  
   | FTP_IP   = 192.168.1.x |
   ```

### Cách 2: Manual (cho Developer)

```powershell
# Cài dependencies
pip install pyftpdlib pywin32 colorama

# Cài service
python ftp_server.py --startup auto install
python ftp_server.py start
```

## 🔧 Cấu hình

### Thông tin mặc định

| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| **Service Name** | `ftpserver` | Tên trong Windows Services |
| **FTP Port** | `21` | Port kết nối FTP |
| **FTP Root** | `C:\scan` | Thư mục gốc |
| **Username** | `scan` | Tài khoản đăng nhập |
| **Password** | `123` | Mật khẩu |
| **Log File** | `C:\scan\ftp_service.log` | File log |
| **Install Path** | `C:\windows\ftpserver` | Thư mục cài đặt |

### Quyền FTP

- **Đọc file** (r): Download file
- **Ghi file** (w): Upload file  
- **Liệt kê** (l): Xem danh sách file
- **Tạo thư mục** (m): Tạo folder mới
- **Xóa** (d): Xóa file/folder
- **Đổi tên** (f): Rename file/folder

## 📋 Sử dụng

### Quản lý Service

```powershell
# Khởi động/dừng service
net start ftpserver
net stop ftpserver

# Kiểm tra trạng thái
sc query ftpserver

# Hoặc mở Services Console
services.msc
```

### Kết nối FTP

#### Windows File Explorer
```
# Mở File Explorer, gõ vào address bar:
ftp://192.168.1.100
# Username: scan
# Password: 123
```

#### FTP Command Line
```bash
ftp 192.168.1.100
# Username: scan  
# Password: 123

# Commands:
ls           # List files
cd folder    # Change directory
get file.txt # Download
put file.txt # Upload
quit         # Exit
```

#### Third-party FTP Clients
- **FileZilla**: Client FTP miễn phí
- **WinSCP**: Windows file transfer
- **Total Commander**: File manager có FTP

---
**Phiên bản**: 1.0
**Cập nhật**: 25/06/2025
