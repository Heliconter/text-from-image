# text-from-image

## Используемые библиотеки  
Pillow 8.2.0 (https://pypi.org/project/Pillow/)  
Pytesseract 0.3.7 (https://pypi.org/project/pytesseract/)  
PyQt5 5.12.2 (https://pypi.org/project/PyQt5/)   
```
pip install pil  
pip install pytesseract  
pip install PyQt5
```
## Шаги по сборке под Windows
1. Установка Tesseract OCR
https://tesseract-ocr.github.io/tessdoc/Downloads.html
2. Установка необходимых python библиотек (PIL, pytesseract, PyQt5)  
3. Установка pyinstaller для сборки исполняемого файла .exe  
```
pip install pyinstaller
```
4. Запустить команду для сборки файла .exe в директории проекта  
```
pyinstaller -F src\main.py
```

## Шаги по сборке под Linux
1. Установка Tesseract OCR

    Archlinux/Manjaro: `sudo pacman -S tesseract tesseract-data-eng tesseract-data-rus`
  
2. Установка необходимых python библиотек (PIL, pytesseract, PyQt5)  
3. Установка pyinstaller для сборки исполняемого файла  
```
pip install pyinstaller
```
4. Запустить команду для сборки исполняемого файла в директории проекта  
```
pyinstaller -F src/main.py
```
