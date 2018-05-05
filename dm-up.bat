docker-machine create LV
@FOR /f "tokens=*" %%i IN ('docker-machine env LV') DO @%%i
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm "LV" natpf1 "django,tcp,,8080,,8080"