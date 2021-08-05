echo off
echo Installation de Python, il faut ajouter Python au Path
python-3.9.6-amd64.exe

echo Ajout module Python
python -m pip install --upgrade pip
python -m pip install GPUtil
python -m pip install PyQt5
python -m pip install numpy

python Install.py
exit