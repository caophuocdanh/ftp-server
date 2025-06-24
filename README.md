# FTP Server Service

## 📋 Tổng quan

Dự án này là một FTP Server chạy dưới dạng Windows Service, được phát triển bằng Python. Server cung cấp khả năng truyền file qua giao thức FTP với tài khoản mặc định và thư mục gốc có thể cấu hình.

### ✨ Tính năng chính

- **Windows Service**: Chạy tự động khi khởi động hệ thống
- **FTP Server**: Hỗ trợ đầy đủ giao thức FTP (RFC 959)
- **Quản lý dễ dàng**: Installer/Uninstaller tự động
- **Logging**: Ghi log chi tiết vào file
- **Bảo mật**: Xác thực người dùng với username/password
- **Quyền truy cập**: Hỗ trợ đầy đủ các quyền FTP (read, write, execute, append, delete, rename, modify, list)

### 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────┐
│           FTP Client                │
└─────────────┬───────────────────────┘
              │ FTP Protocol (Port 21)
              ▼
┌─────────────────────────────────────┐
│        FTP Server Service           │
│  ┌─────────────────────────────┐    │
│  │    pyftpdlib Server         │    │
│  │  - DummyAuthorizer          │    │
│  │  - FTPHandler               │    │
│  │  - Threading Support       │    │
│  └─────────────────────────────┘    │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│       File System (C:\scan)        │
└─────────────────────────────────────┘
```

## 📁 Cấu trúc dự án

```
FTP Server/
├── ftp_server.py          # FTP Server chính - Windows Service
├── ftp_installer.py       # Trình cài đặt/gỡ cài đặt
├── ftp_server.ico         # Icon cho ứng dụng
├── build.cmd             # Script build PyInstaller
└── README.md             # Tài liệu này
```

## 💻 Yêu cầu hệ thống

### Hệ điều hành
- **Windows 7/8/10/11** (32-bit hoặc 64-bit)
- **Windows Server 2012/2016/2019/2022**

### Quyền hạn
- **Administrator privileges** (bắt buộc để cài đặt Windows Service)

### Phần cứng tối thiểu
- **RAM**: 512 MB trở lên
- **Ổ cứng**: 100 MB dung lượng trống
- **Network**: Card mạng hỗ trợ TCP/IP

### Port yêu cầu
- **Port 21**: FTP Control Connection (TCP)
- **Port 20**: FTP Data Connection (TCP) - mode active
- **Passive ports**: Dải port động cho passive mode

## 📦 Thư viện và Dependencies

### Thư viện Python chính

| Thư viện | Phiên bản | Mục đích |
|----------|-----------|----------|
| `pyftpdlib` | Latest | FTP server implementation |
| `pywin32` | Latest | Windows Service integration |
| `PyInstaller` | Latest | Đóng gói thành executable |

### Modules Windows API
```python
import servicemanager    # Quản lý Windows Service
import win32service     # Windows Service API
import win32serviceutil # Utilities cho Service
import win32event       # Event handling
```

### Standard Libraries
```python
import os              # File system operations
import sys             # System-specific parameters
import logging         # Logging functionality
import threading       # Multi-threading support
import shutil          # High-level file operations
import subprocess      # Process management
import ctypes          # Windows API calls
```

## 🚀 Cài đặt

### Cách 1: Sử dụng Installer (Khuyến nghị)

1. **Tải về file executable**:
   - `ftpinstaller.exe` (từ thư mục `dist/`)

2. **Chạy installer với quyền Administrator**:
   ```cmd
   # Chuột phải -> "Run as administrator"
   ftpinstaller.exe
   ```

3. **Chọn tùy chọn cài đặt**:
   ```
   Ban muon lam gi?
    1. Cai dat (Install)
    2. Go cai dat (Uninstall)
   Chon (1/2): 1
   ```

### Cách 2: Cài đặt từ source code

1. **Cài đặt Python dependencies**:
   ```powershell
   pip install pyftpdlib pywin32
   ```

2. **Cài đặt service thủ công**:
   ```powershell
   python ftp_server.py --startup auto install
   python ftp_server.py start
   ```

## 🔧 Cấu hình

### Cấu hình mặc định

| Tham số | Giá trị | Mô tả |
|---------|---------|--------|
| **Service Name** | `ftpserver` | Tên service trong Windows |
| **Display Name** | `FTP Server` | Tên hiển thị |
| **FTP Port** | `21` | Port FTP control |
| **FTP Root** | `C:\scan` | Thư mục gốc FTP |
| **Log Directory** | `C:\scan` | Thư mục chứa log |
| **Username** | `scan` | Tài khoản FTP |
| **Password** | `123` | Mật khẩu FTP |

### Tùy chỉnh cấu hình

Để thay đổi cấu hình, chỉnh sửa file `ftp_server.py`:

```python
# --- Cấu hình ---
SERVICE_NAME = "ftpserver"
SERVICE_DISPLAY_NAME = "FTP Server"
LOG_DIR = r"C:\scan"
FTP_ROOT = r"C:\scan"

# Trong hàm run() của FTPServerThread
authorizer.add_user("scan", "123", FTP_ROOT, perm='elradfmw')
address = ("0.0.0.0", 21)
```

### Quyền FTP (perm parameter)

| Ký tự | Quyền | Mô tả |
|--------|-------|--------|
| `e` | Change directory | Chuyển thư mục |
| `l` | List files | Liệt kê file |
| `r` | Read files | Đọc file |
| `a` | Append to files | Ghi thêm vào file |
| `d` | Delete files | Xóa file |
| `f` | Rename files | Đổi tên file |
| `m` | Create directory | Tạo thư mục |
| `w` | Write files | Ghi file |

## 🎯 Build và Deploy

### Build executable với PyInstaller

1. **Chạy build script**:
   ```powershell
   .\build.cmd
   ```

2. **Output files**:
   ```
   dist/
   ├── ftpserver.exe      # FTP Server executable
   └── ftpinstaller.exe   # Installer executable
   ```

### Build command chi tiết

```batch
# Build FTP Server
pyinstaller --onefile --icon=ftp_server.ico --hidden-import win32timezone --name ftpserver ftp_server.py

# Build Installer (bao gồm ftpserver.exe)
pyinstaller --onefile --icon=ftp_server.ico --name ftpinstaller ftp_installer.py --add-binary "dist\ftpserver.exe;."
```

### PyInstaller Options

| Option | Mô tả |
|--------|--------|
| `--onefile` | Tạo một file executable duy nhất |
| `--icon` | Đặt icon cho executable |
| `--hidden-import` | Import module ẩn |
| `--name` | Tên file output |
| `--add-binary` | Thêm file binary vào package |

## 📋 Sử dụng

### Quản lý Service

```powershell
# Cài đặt service
python ftp_server.py install

# Khởi động service
python ftp_server.py start

# Dừng service
python ftp_server.py stop

# Gỡ cài đặt service
python ftp_server.py remove

# Xem trạng thái
sc query ftpserver
```

### Kết nối FTP

#### Sử dụng FTP Client
```bash
ftp <server_ip>
# Username: scan
# Password: 123
```

#### Sử dụng File Explorer (Windows)
```
ftp://<server_ip>
# hoặc
ftp://scan:123@<server_ip>
```

#### Sử dụng PowerShell
```powershell
# Upload file
$webclient = New-Object System.Net.WebClient
$webclient.Credentials = New-Object System.Net.NetworkCredential("scan", "123")
$webclient.UploadFile("ftp://<server_ip>/filename.txt", "C:\local\file.txt")
```

## 📊 Monitoring và Logging

### Log Files

| File | Đường dẫn | Mô tả |
|------|-----------|--------|
| Service Log | `C:\scan\ftp_service.log` | Log của FTP service |
| Windows Event Log | Event Viewer | Log của Windows Service Manager |

### Log Format

```
2025-06-24 10:30:15,123 - INFO - FTP server thread starting...
2025-06-24 10:30:15,456 - INFO - Created FTP root directory: C:\scan
2025-06-24 10:30:15,789 - INFO - FTP server listening on 0.0.0.0:21
```

### Kiểm tra trạng thái

```powershell
# Kiểm tra service status
Get-Service ftpserver

# Kiểm tra port listening
netstat -an | findstr :21

# Kiểm tra log
Get-Content "C:\scan\ftp_service.log" -Tail 50
```

## 🛠️ Troubleshooting

### Các lỗi thường gặp

#### 1. Service không khởi động được

**Triệu chứng**: Service start rồi stop ngay lập tức

**Giải pháp**:
```powershell
# Kiểm tra log
Get-Content "C:\scan\ftp_service.log"

# Kiểm tra Windows Event Log
Get-EventLog -LogName Application -Source "ftpserver" -Newest 10
```

#### 2. Port 21 đã được sử dụng

**Triệu chứng**: Error "Address already in use"

**Giải pháp**:
```powershell
# Kiểm tra process sử dụng port 21
netstat -ano | findstr :21

# Kill process nếu cần
taskkill /PID <process_id> /F
```

#### 3. Không thể connect từ client

**Kiểm tra**:
- Windows Firewall
- Network connectivity
- FTP client settings (Active/Passive mode)

**Giải pháp**:
```powershell
# Mở Windows Firewall cho FTP
New-NetFirewallRule -DisplayName "FTP Server" -Direction Inbound -Protocol TCP -LocalPort 21 -Action Allow
```

#### 4. Quyền truy cập thư mục

**Triệu chứng**: Permission denied khi truy cập file

**Giải pháp**:
- Đảm bảo service account có quyền đọc/ghi trên `C:\scan`
- Chạy service với account có đủ quyền

### Debug Mode

Để chạy debug mode không dùng service:

```python
# Thêm vào cuối ftp_server.py
if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'debug':
    server_thread = FTPServerThread()
    server_thread.run()  # Chạy trực tiếp, không dùng thread
```

## 🔒 Bảo mật

### Khuyến nghị bảo mật

1. **Thay đổi mật khẩu mặc định**:
   ```python
   authorizer.add_user("scan", "strong_password_here", FTP_ROOT, perm='elradfmw')
   ```

2. **Giới hạn quyền truy cập**:
   ```python
   # Chỉ cho phép đọc
   authorizer.add_user("readonly", "password", FTP_ROOT, perm='elr')
   ```

3. **Firewall Configuration**:
   - Chỉ mở port 21 cho các IP tin tưởng
   - Sử dụng VPN cho truy cập từ xa

4. **Monitoring**:
   - Theo dõi log thường xuyên
   - Cảnh báo khi có truy cập bất thường

### TLS/SSL Support (Tùy chọn)

Để thêm hỗ trợ FTPS (FTP over SSL):

```python
from pyftpdlib.handlers import TLS_FTPHandler

# Thay thế FTPHandler bằng TLS_FTPHandler
handler = TLS_FTPHandler
handler.certfile = 'path/to/certificate.pem'
handler.keyfile = 'path/to/private_key.pem'
```

## 📚 Tài liệu tham khảo

### External Documentation

- [pyftpdlib Documentation](https://pyftpdlib.readthedocs.io/)
- [Python Windows Service Tutorial](https://docs.python.org/3/library/winreg.html)
- [PyInstaller Manual](https://pyinstaller.readthedocs.io/)

### RFC Standards

- [RFC 959 - File Transfer Protocol](https://tools.ietf.org/html/rfc959)
- [RFC 2228 - FTP Security Extensions](https://tools.ietf.org/html/rfc2228)

## 🤝 Đóng góp

### Development Setup

1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest`
4. Build: `.\build.cmd`

### Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings for functions
- Include error handling

## 📝 License

Dự án này sử dụng MIT License. Xem file `LICENSE` để biết thêm chi tiết.

## 📞 Hỗ trợ

Nếu bạn gặp vấn đề hoặc có câu hỏi:

1. Kiểm tra phần Troubleshooting
2. Xem log files
3. Tạo issue trên repository
4. Liên hệ team phát triển

---

## 📋 Checklist cài đặt

- [ ] Đảm bảo chạy với quyền Administrator
- [ ] Kiểm tra Python dependencies đã cài đặt
- [ ] Xác nhận port 21 không bị chiếm dụng
- [ ] Cấu hình Windows Firewall
- [ ] Test kết nối FTP sau khi cài đặt
- [ ] Kiểm tra log files hoạt động bình thường
- [ ] Backup cấu hình nếu có thay đổi

**Phiên bản tài liệu**: 1.0  
**Cập nhật lần cuối**: 24/06/2025
