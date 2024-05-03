# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is spectrometer implementation for wavelength mesuring device

### How do I get set up? ###

* pip install opsys-spectrometer

### Unit Testing

* python -m unittest -v

### Reference Links

* Installation Software: 'R:\Lidar\Dima\Software\AvaspecX64Dll_9.14.0.0.Setup_64bit.exe'
* MSL-Equipment documenetation: https://msl-equipment.readthedocs.io/en/latest/index.html

### Specifications

* For developers, use the following commands to install local venv:
```
python -m venv .env

.env\Scripts\activate.bat

python -m pip install --upgrade pip

pip install pip_system_certs

pip install -r requirements.txt
```

### Pyinstaller

* Directories containing DLLs should be imported by pyinstaller during executable generation.
* The following functionality should be added inside pyinstaller spec file:
```
def get_dirs(root_folder, hint):
    target_dirs = []
    for root, dirs, files in os.walk(root_folder):
        for dir in dirs:
            if '.env' in os.path.join(root, dir) and hint in dir:
                target_dirs.append(os.path.join(root, dir))
    return target_dirs

root_folder_path = os.getcwd()
dirs = get_dirs(root_folder_path, 'opsys_spectrometer')
datas_dirs = [(f'{_dir}\*', './opsys_spectrometer/') for _dir in dirs]
```
* ```datas_dirs``` should be added at ```datas``` variable:
```
pathex=[],
binaries=binaries_file,
datas=datas_dirs,
```

### Usage Example
```
from opsys_spectrometer.spectrometer_controller import SpectrometerController

spectrometer = SpectrometerController()

spectrometer.connect()
print(spectrometer.get_lambda())
spectrometer.disconnect()
```