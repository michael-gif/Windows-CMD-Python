import os
import sys
import subprocess

from tkinter import *

def set_cursor_barrier(pos):
    global cursor_barrier
    cursor_barrier = pos

def prevent_mandatory_text_deletion(event):
    global text
    pos = output.index(INSERT)
    pos = pos.split('.')
    pos = [int(a) for a in pos]
    ignore = [33, 34, 35, 36, 37, 38, 39, 40]
    # ignore the arrow keys etc
    if event.keycode not in ignore:
        # prevent backspace from end of mandatory text
        if event.keycode == 8 and pos == cursor_barrier:
            return "break"
        # prevent any other keys from doing stuff
        elif pos[0] < cursor_barrier[0]:
            return "break"
        elif pos[0] == cursor_barrier[0] and pos[1] < cursor_barrier[1]:
            return "break"

def process_command(event):
    # prevent the enter key from working in the mandatory text
    pos = [int(a) for a in output.index(INSERT).split('.')]
    if pos[0] < cursor_barrier[0]:
        return "break"
    elif pos[0] == cursor_barrier[0] and pos[1] < cursor_barrier[1]:
        return "break"
    # process the command
    command = output.get('.'.join([str(a) for a in cursor_barrier]),END).strip('\n')
    parts = command.split(' ')
    keyword = parts[0]
    args = parts[1:]
    result = ''
    if keyword == 'exit':
        root.destroy()
        sys.exit()
    elif keyword == 'color':
        if len(args) > 0:
            color = None
            if args[0] == 'white':
                color = 'gray82'
            else:
                color = args[0]
            try:
                output.config(fg=color)
            except:
                result = f"NullError: color '{color}' does not exist"
    else:
        result = subprocess.run([command], capture_output=True, shell=True).stdout.decode('utf-8')
        if result == '':
            result = f"'{keyword}' is not recognized as an internal or external command, operable program or batch file."
    # output to the terminal
    output.insert(END, f'\n{result}\n\ninjection_bot >')
    output.delete('end-1c', 'end')
    output.see(END)
    # set the cursor_barrier to the end of the mandatory text
    set_cursor_barrier([int(a) for a in output.index(INSERT).split('.')])
    # prevent the enter key from creating a new line
    if event.keycode == 13:
        return "break"

root = Tk()
root.title('bing 2 electric boogaloo')
root.config(bg='black')
root.geometry('977x481')
root.iconbitmap('./resources/icon.ico')
root.resizable(False, False)

cursor_barrier = [4, 15]

output = Text(root, bg='black', fg='gray82', insertbackground='white')
output.place(x=0, y=0, width=977, height=481)
output.focus()
output.insert(END, 'Microhard Vindows [Version 420.69]\n(c) 2019 Microhard Corporation. All rights not reserved.\n\ninjection_bot >')
output.bind('<Key>',prevent_mandatory_text_deletion, add='+')
output.bind('<Return>', process_command, add='+')

root.mainloop()
