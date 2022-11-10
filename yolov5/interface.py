# -*- coding: utf-8 -*-

import os
import PySimpleGUI as sg
import threading

from detect import run
from statistik_detected_plancton_with_focus import get_statistiks

class check():
    def __init__(self, val):
        self.val = val

def long_operation_thread(window, pathFrom, pathTo, nosave, save_crop, unique, xcept, isactive, toExit, complete):
    for i in os.listdir(pathFrom):
        if toExit.val:
            complete.val = True
            break
        texti = 'Сканирование директории: ' + i
        window.write_event_value('-UPDATE-', texti)
        if not os.path.isfile(pathFrom+'/'+i): 
            #nosave сохранять ли размеченные фотографии
            run(source = pathFrom+'/'+str(i), project = pathTo, name = str(i), nosave=not(nosave), save_crop = save_crop)
            
    if unique:
        get_statistiks(pathTo, xcept)
        print('Отчёты находится в папке:', pathTo)
    isactive.val = True
    window.write_event_value('-THREAD-', '** DONE **')  # put a message into queue for GUI

    

def the_gui():
    toExit = check(False)
    isactive = check(True)
    complete = check(True)
    
    layout = [
        [sg.Text('Директория со снимками'), sg.InputText(), sg.FolderBrowse()],
        [sg.Text('Директория сохранения'), sg.InputText(), sg.FolderBrowse()],
        [sg.Checkbox('Сохранить размеченные изображения'), 
         sg.Checkbox('Сохранить вырезанные объекты')],
        [sg.Checkbox('Подготовить итоговые отчёты с уникальными объектами')],
        [sg.Checkbox('Добавить результаты Xception')],
        [sg.Output(size=(88, 20))],
        [sg.Button('Do Long Task', bind_return_key=True), sg.Button('Exit')]
    ]
    
    window = sg.Window('Multithreaded Window', layout)

    while True:
        event, values = window.read()
        if toExit.val:
            if complete.val:
                break
        else:
            if event in (sg.WIN_CLOSED, 'Exit'):
                toExit.val = True
                if complete.val:
                    break
                print('Досканирование папки и последующее завершение')
                
            elif event.startswith('Do'): 
                if isactive.val:
                    complete.val = False
                    print('Сканирование изображений: ', values[0])
                    threading.Thread(target=long_operation_thread, args=(window,values[0],values[1],values[2],values[3], values[4],values[5], isactive, toExit, complete), daemon=True).start()
                    isactive.val = False
                else:
                    print('Сканирование выполняется, ожидайте')
                
            elif event == '-UPDATE-':
                print(values[event])
            elif event == '-THREAD-':
                print(': ', values[event])

    window.close()

if __name__ == '__main__':
    the_gui()
    print('Выход из программы')


