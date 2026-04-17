# UsbFileChecker
Предназначен для копирования определенного файла с USB в локальную директорию.
Сверяет содержимое исходного файла и локальной копии по хэш-сумме.


## Установка:
- Скорировать usbfilechecker.pp в каталог манифестов сервера puppet `/etc/puppetlabs/code/environments/production/manifests/`
- Скопировать каталог ./usbfilechecker в каталог в модулей сервера puppet `/etc/puppetlabs/code/environments/production/modules/` 

- В фале манифеста usbfilechecker.pp установить значение переменной source_filename равное имени исходного файла, обычно это серийный номер устройства `SN.xls`
- По умолчанию файл копирутеся в каталог `/usr/share/usbfilechecker` 