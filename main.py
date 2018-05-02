# Python semestral work

import sys
sys.excepthook = sys.__excepthook__
import os
import numpy as np
from PIL import Image
# clear display
print('\033[2J', end='')

def loadInput():
    print('\033[2J')
    file = input('Zadejte jméno souboru:\n')
    while os.access(file, os.R_OK) == False:
        print('\033[2J', end='')
        print('Zadaný soubor nelze načíst, zadejte jiný:')
        file = input('Zadejte jméno souboru: ( nebo cestu k němu )\n')
    print('\033[2J', end='')
    fileData = np.array(Image.open(file))
    return file, fileData

def saveOutput(fileData, file, change):
    f = Image.fromarray(fileData, 'RGB')
    pre, po = file.split('.')
    f.save(pre + "_" + change + "." + po )

flag = 0
print('Program pro úpravu obrázku, zadej jméno souboru, ktery chceš upravit: ')
file, fileData = loadInput()
# file, fileData = 'test.png', np.array(Image.open('test.png'))

while True:
    fileData = np.array(Image.open(file))
    if flag == -1:
        print('Špatný výběr, volte znovu')
    else:
        print()

    # interface
    print('Aktuální soubor: \"' + file + '\"' )
    print('''Seznam možností (vyber číslo a stiskni enter):
          0. exit - vypne program
          1. nový soubor - nechá uživatele zadat nový soubor
          2. rotace do prava o 90 stupňů
          3. rotace do leva o 90 stupňů
          4. zrcadlení obrazu
          5. inverze obrazu
          6. převod do odstínu šedi
          7. zesvětlení
          8. ztmavení
          9. zvýraznění hran''')
    flag = input()

    # end program
    if flag == '0':
        print('\033[2J', end='')
        exit()
    # load new input
    elif flag == '1':
        file, fileData = loadInput()
    # rotate image to right
    elif flag == '2':
        w, h, s = fileData.shape
        data = np.zeros((h, w, 3), dtype=np.uint8)
        for i in range(h):
            for j in range(w):
                data[i][j] = fileData[-j][-i]
        saveOutput(data, file, "rotateRight")
    # rotate image to left
    elif flag == '3':
        w, h, s = fileData.shape
        data = np.zeros((h, w, 3), dtype=np.uint8)
        for i in range(h):
            for j in range(w):
                data[i][j] = fileData[j][i]
        saveOutput(data, file, "rotateLeft")
    # mirror the image
    elif flag == '4':
        w, h, s = fileData.shape
        data = np.zeros((w, h, 3), dtype=np.uint8)
        for i in range(h):
            data[:,i] = fileData[:,-i]
        saveOutput(data, file, "mirror")
    elif flag == '5':
        fileData[::] = 255 - fileData[::]
        saveOutput(fileData, file, "invert")
    # turn image to grayscale
    elif flag == '6':
        for i in range(len(fileData)):
            for j in range(len(fileData[0])):
                fileData[i][j] = np.dot(fileData[i][j], [0.299, 0.587, 0.114]).sum()
        saveOutput(fileData, file, "greyscale")
    # lighten image
    elif flag == '7':
        scale = 10
        while scale > 9 or scale < 0:
            scale = int(input('Zadej číslo 0-9 (čím větší tím bude světlejší obrázek): '))
        scale = (scale+1) * 0.08
        fileData[...] = fileData[...] + (255 - fileData[...]) * scale
        saveOutput(fileData, file, "lighter")
    # darken image
    elif flag == '8':
        scale = 10
        while scale > 9 or scale < 0:
            scale = int(input('Zadej číslo 0-9 (čím menší tím bude tmavší obrázek): '))
        scale = (scale+1) * 0.08
        fileData[...] = (fileData[...]) * scale
        saveOutput(fileData, file, "darker")
    # yellow edges of image
    elif flag == '9':
        fileData[-3:,:] = 255, 255, 5
        fileData[:3,:] = 255, 255, 5
        fileData[:,:3] = 255, 255, 5
        fileData[:,-3:] = 255, 255, 5
        saveOutput(fileData, file, "edge")
    # wrong input prompt user again
    else:
        flag = -1
    print('\033[2J', end='')
