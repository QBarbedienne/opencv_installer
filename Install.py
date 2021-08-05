from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os
import enum
import GPUtil
import shutil
import subprocess

class GPUEnum(enum.Enum):
    Nvidia_10XX = 1
    Nvidia_20XX = 2
    Nvidia_30XX = 3
    Invalid = -1

class GetGPU():
    def __init__(self):
        gpus = GPUtil.getGPUs()
        if not gpus:
            self.GPU = GPUEnum.Invalid
            self.GPUName = ""
        for gpu in gpus:
            self.GPUName = gpu.name
            if('TX 10' in gpu.name):
                self.GPU = GPUEnum.Nvidia_10XX
                break
            elif('TX 20' in gpu.name):
                self.GPU = GPUEnum.Nvidia_20XX
                break
            elif('TX 30' in gpu.name):
                self.GPU = GPUEnum.Nvidia_30XX
                break
            else:
                self.GPU = GPUEnum.Invalid
    
    def is10XX(self):
        return self.GPU == GPUEnum.Nvidia_10XX

    def is20XX(self):
        return self.GPU == GPUEnum.Nvidia_20XX

    def is30XX(self):
        return self.GPU == GPUEnum.Nvidia_30XX

    def isValid(self):
        return (self.is10XX() | self.is20XX() | self.is30XX())

    def getGPU(self):
        if self.GPUName == "":
            return "Pas de GPU Nvidia détecté"
        else:
            return self.GPUName

GPU = GetGPU()
version = '10.1' if not GPU.is30XX() else '11.3'

class FolderBrowser(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.dirpath = ''
        
        self.label = QLabel()

        self.label.setText('Ouvrir le dossier Cuda ' + version)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.label)
        
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedWidth(180)
        
        layout.addWidget(self.lineEdit)
        
        self.button = QPushButton('Rechercher')
        self.button.clicked.connect(self.getFile)
        layout.addWidget(self.button)
        layout.addStretch()

    def getFile(self):      
        self.dirpath = QFileDialog.getExistingDirectory(self, caption='Choisir dossier', directory=QDir.currentPath())
        self.lineEdit.setText(self.dirpath)

    def getPath(self):
        return self.dirpath

class MagicWizard(QWizard):
    def __init__(self, parent=None):
        super(MagicWizard, self).__init__(parent)
        self.addPage(Page1(self))
        self.addPage(Page2(self))
        self.addPage(Page3(self))
        self.addPage(Page4(self))
        self.addPage(Page5(self))
        self.setWindowTitle("Installation Cuda et build OpenCV")
        self.resize(640,480)

class Page1(QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.ShowNext = False
        self.text = QLabel()
        self.text.setText("Installation de Cuda")
        self.CudaImage = QLabel()
        pixmap = QPixmap('img\Cuda.png')
        self.CudaImage.setPixmap(pixmap)
        self.CudaImage.setAlignment(Qt.AlignCenter)
        self.GPUtext = QLabel()
        self.GPUtext.setText("Carte graphique détecté : " + GPU.getGPU())
        self.installButton = QPushButton()
        self.installButton.setEnabled(GPU.isValid())
        self.installButton.setText("Lancer l'installation")
        self.installButton.clicked.connect(self.InstallCuda)
        self.installButton.clicked.connect(self.completeChanged)
        if not GPU.isValid():
            self.installButton.setEnabled(False)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.CudaImage)
        layout.addWidget(self.GPUtext)
        layout.addWidget(self.installButton)
        self.setLayout(layout)

    def isComplete(self):
        return self.ShowNext

    def InstallCuda(self):
        cwd = os.getcwd()
        if GPU.is10XX() | GPU.is20XX():
            pathCuda = os.path.join(cwd, "cuda_10.1.105_win10_network.exe")
        elif GPU.is30XX():
            pathCuda = os.path.join(cwd, "cuda_11.3.0_win10_network.exe")
        else:
            return
        os.startfile(pathCuda)
        self.ShowNext = True

    def nextId(self):
        if GPU.is10XX() | GPU.is20XX():
            return 1
        elif GPU.is30XX():
            return 3
        else:
            return 0

class Page2(QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.ShowNext = False
        self.text = QLabel()
        self.text.setText("Installation de Cuda update 1")
        self.CudaImage = QLabel()
        pixmap = QPixmap('img\Cuda.png')
        self.CudaImage.setPixmap(pixmap)
        self.CudaImage.setAlignment(Qt.AlignCenter)
        self.installButton = QPushButton()
        self.installButton.setText("Lancer l'installation")
        self.installButton.clicked.connect(self.InstallCudaUpdate1)
        self.installButton.clicked.connect(self.completeChanged)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.CudaImage)
        layout.addWidget(self.installButton)
        self.setLayout(layout)

    def isComplete(self):
        return self.ShowNext

    def InstallCudaUpdate1(self):
        cwd = os.getcwd()
        pathCuda = os.path.join(cwd, "cuda_10.1.168_win10_network.exe")
        os.startfile(pathCuda)
        self.ShowNext = True

class Page3(QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        self.ShowNext = False
        self.text = QLabel()
        self.text.setText("Installation de Cuda update 2")
        self.CudaImage = QLabel()
        pixmap = QPixmap('img\Cuda.png')
        self.CudaImage.setPixmap(pixmap)
        self.CudaImage.setAlignment(Qt.AlignCenter)
        self.installButton = QPushButton()
        self.installButton.setText("Lancer l'installation")
        self.installButton.clicked.connect(self.InstallCudaUpdate2)
        self.installButton.clicked.connect(self.completeChanged)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.CudaImage)
        layout.addWidget(self.installButton)
        self.setLayout(layout)

    def isComplete(self):
        return self.ShowNext

    def InstallCudaUpdate2(self):
        cwd = os.getcwd()
        pathCuda = os.path.join(cwd, "cuda_10.1.243_win10_network.exe")
        os.startfile(pathCuda)
        self.ShowNext = True

class Page4(QWizardPage):
    def __init__(self, parent=None):
        super(Page4, self).__init__(parent)
        self.ShowNext = False
        self.text = QLabel()
        self.text.setText("Installation de cuDNN")
        self.CudNNImage = QLabel()
        pixmap = QPixmap('img\cuDNN.png')
        self.CudNNImage.setPixmap(pixmap)
        self.CudNNImage.setAlignment(Qt.AlignCenter)
        self.search = FolderBrowser()
        self.exemple = QLabel()
        self.exemple.setText(R"Exemple : C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v" + version)
        self.installButton = QPushButton()
        self.installButton.setText("Lancer l'installation")
        self.installButton.clicked.connect(self.InstallCuDNN)
        self.installButton.clicked.connect(self.completeChanged)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.CudNNImage)
        layout.addWidget(self.search)
        layout.addWidget(self.exemple)
        layout.addWidget(self.installButton)
        self.setLayout(layout)

    def isComplete(self):
        return self.ShowNext

    def isPathValid(self):
        return True
    
    def InstallCuDNN(self):
        if self.search.getPath() == '':
            return
        if GPU.is10XX() | GPU.is20XX():         
            source_dir = os.path.join(os.getcwd() ,"cudnn-10.1-windows10-x64-v7.6.5.32\cuda")
        elif GPU.is30XX():
            source_dir = os.path.join(os.getcwd() ,"cudnn-11.3-windows-x64-v8.2.0.53\cuda")
        for root, directories, files in os.walk(source_dir):
            for name in directories:
                relPath = os.path.relpath(root, start=source_dir)
                path = os.path.join(self.search.getPath(), relPath, name)
                if not os.path.isdir(path):
                    os.mkdir(path)
            for name in files:
                if not ".txt" in name:
                    relPath = os.path.relpath(root, start=source_dir)
                    src = os.path.join(root, name)
                    dst = os.path.join(self.search.getPath(), relPath, name)
                    if os.path.isfile(dst):
                        os.chmod(dst, 0o777)
                        os.remove(dst)
                    shutil.copy(src, dst)
        print('done')
        self.ShowNext = True

class Page5(QWizardPage):
    def __init__(self, parent=None):
        super(Page5, self).__init__(parent)
        self.ShowNext = False
        self.text = QLabel()
        self.text.setText("Build d'OpenCV")
        self.OpenCVImage = QLabel()
        pixmap = QPixmap('img\OpenCV.png')
        self.OpenCVImage.setPixmap(pixmap)
        self.OpenCVImage.setAlignment(Qt.AlignCenter)
        self.textEdit = QTextEdit()
        self.textEdit.setEnabled(False)
        self.buildButton = QPushButton()
        self.buildButton.setText("Lancer le build")
        self.buildButton.clicked.connect(self.BuildOpenCV)
        self.buildButton.clicked.connect(self.BuildDone)
        self.compileButton = QPushButton()
        self.compileButton.setText("Compiler")
        self.compileButton.setEnabled(False)
        self.compileButton.clicked.connect(self.CompileOpenCV)
        self.compileButton.clicked.connect(self.completeChanged)
        HLayout = QHBoxLayout()
        HLayout.addWidget(self.buildButton)
        HLayout.addWidget(self.compileButton)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.OpenCVImage)
        layout.addWidget(self.textEdit)
        layout.addLayout(HLayout)
        self.setLayout(layout)

    def isComplete(self):
        return self.ShowNext

    def BuildOpenCV(self):
        CMakePath = "./cmake-3.21.0-windows-x86_64/bin"
        OpenPath = "./opencv-4.4.0"
        buildDir = './OpenCVBuild'
        if not os.path.isdir(buildDir):
            os.mkdir(buildDir)
        self.param = []
        self.NewParam(os.path.join(CMakePath, "cmake.exe"))
        self.NewParam('-S', OpenPath )
        self.NewParam('-B', buildDir )
        self.NewParam('-G', 'Visual Studio 16 2019')

        self.NewParam('-D', 'WITH_CUDA=ON')
        self.NewParam('-D', 'WITH_OPENGL=ON')
        if GPU.is10XX() | GPU.is20XX():
            self.NewParam('-D', 'CUDA_ARCH_BIN=6.0;6.1;7.0;7.5')
        elif GPU.is30XX():
            self.NewParam('-D', 'CUDA_ARCH_BIN=8.0;8.6')
        self.NewParam('-D', 'CUDA_FAST_MATH=ON')
        self.NewParam('-D', 'OPENCV_DNN_CUDA=ON')
        self.NewParam('-D', 'ENABLE_FAST_MATH=ON')
        self.NewParam('-D', 'BUILD_opencv_rgbd=OFF')

        process = subprocess.run(self.param)
        True

    def NewParam(self, par, value = ''):
        self.param.append(par)
        if not value == '':
            self.param.append(value)

    def BuildDone(self):
        self.compileButton.setEnabled(True)

    def CompileOpenCV(self):
        OpenPath = "./opencv-4.4.0"
        CMakePath = "./cmake-3.21.0-windows-x86_64/bin"
        buildDir = './OpenCVBuild'
        if not os.path.isdir(os.path.join(OpenPath, buildDir)):
            os.mkdir(os.path.join(OpenPath, buildDir))
        self.param = []
        self.NewParam(os.path.join(CMakePath, "cmake.exe"))
        self.NewParam('--build', buildDir )
        self.NewParam('--config', 'Release')
        self.NewParam('--target', 'install')

        process = subprocess.run(self.param)
        self.ShowNext = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wizard = MagicWizard()
    wizard.show()
    sys.exit(app.exec_())