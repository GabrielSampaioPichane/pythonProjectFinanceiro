import PyInstaller.__main__

#Configurar o "APP"
'''
1 - Para transformar em execuavel, precisas conhecer a biblioteca Pyinstaller! 
2 - Caso queira apenas transformar sem conhecer a biblioteca, favor alterar o nome do arquivo
na qual queres transformar em .exe, nome esse que se encontra na primeira linha da função!
'''
#Codigo que transforma em executavel
PyInstaller.__main__.run([
    'veetor_test.py',
    '--onefile',
    '--windowed'
])
