import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pandas as pd

from PIL import Image, ImageTk
from matplotlib import pyplot as plt, patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_img():
    filetypes = [('Jpg Files', '*.jpg'),
                 ('PNG Files', '*.png')]
    filename = tk.filedialog.askopenfilename(filetypes=filetypes)
    img = Image.open(filename)
    img = img.resize((450, 300))
    img = ImageTk.PhotoImage(img)
    label = tk.Label(window)
    label.grid(row=5, column=0)
    label.image = img
    label['image'] = img
    img = Image.open(filename)

    img = img.quantize(colors=11, kmeans=10).convert('RGB')
    n_common = 11
    common_colors = sorted(img.getcolors(2 ** 24), reverse=True)[:n_common]
    # print(common_colors)

    colors_list = str(common_colors).replace('[', '').split('),')[0:-1]
    # print(colors_list)
    percent = [i.split(', (')[0].replace('(', '') for i in colors_list]
    # print(percent)
    rgb = ['(' + i.split(', (')[1] for i in colors_list]
    # print(rgb)
    hex = ['#%02x%02x%02x' % (int(i.split(", ")[0].replace("(", "")),
                              int(i.split(", ")[1]),
                              int(i.split(", ")[2].replace(")", ""))) for i in rgb]
    # print(hex)

    df = pd.DataFrame(zip(hex, percent), columns=['Color Code', 'Occurence'])
    fig, ax = plt.subplots(figsize=(150, 80), dpi=10)
    fig.set_facecolor('white')
    plt.savefig('bg.png')
    plt.close(fig)

    bg = plt.imread('bg.png')
    fig = plt.figure(figsize=(60, 60), dpi=10)
    ax = fig.add_subplot(1, 1, 1)
    chart_type = FigureCanvasTkAgg(fig, window)
    chart_type.get_tk_widget().grid(row=5, column=1)
    list_color = list(df['Color Code'])
    list_percent = [int(i) for i in list(df['Occurence'])]
    x_pos, y_pos, y_pos2 = 220, 15, 15
    for color in list_color:
        if list_color.index(color) <= 4:
            y_pos += 125
            rect = patches.Rectangle((x_pos, y_pos), 200, 80, facecolor=color)
            ax.add_patch(rect)
            ax.text(x=x_pos + 250, y=y_pos + 50, s=color, fontdict={'fontsize': 100})
        else:
            y_pos2 += 125
            rect = patches.Rectangle((x_pos + 700, y_pos2), 200, 80, facecolor=color)
            ax.add_artist(rect)
            ax.text(x=x_pos + 950, y=y_pos2 + 50, s=color, fontdict={'fontsize': 100})

    ax.axis('off')
    plt.imshow(bg)
    plt.tight_layout()


window = Tk()
window.title("Color Extractor")
window.config(pady=50, bg="white")
window.geometry("1300x645")

font = "Arial"
text_label = Label(text="Image Color Extract", width=75, font=(font, 20, "bold"), pady=10, fg="blue", bg="sky blue")
text_label.grid(row=1, column=0, columnspan=2)
photo_label = tk.Label(window, text='Upload Image', width=30, font=(font, 14), bg="white", fg="blue", pady=10)
photo_label.grid(row=3, column=0)
photo_button = tk.Button(window, text='Upload File', command=open_img, bg="white", fg="red", width=30, font=(font, 12))
photo_button.grid(row=3, column=1)
window.mainloop()
