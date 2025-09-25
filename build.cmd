rmdir /s /q dist,build
del /f ftpinstaller.spec,ftpserver.spec
pip install -r requirements.txt
pyinstaller --onefile --icon=ftp_server.ico --hidden-import win32timezone --name ftpserver ftp_server.py
pyinstaller --onefile --icon=ftp_server.ico --name ftpinstaller ftp_installer.py --add-binary "dist\ftpserver.exe;."
