docker-machine create LV
@FOR /f "tokens=*" %%i IN ('docker-machine env LV') DO @%%i