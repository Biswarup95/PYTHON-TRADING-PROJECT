import numpy as np
import matplotlib.pyplot as plt
import mpl_finance as fnc
from matplotlib.widgets import Cursor
import time
import math
import tkinter
from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


def annotation(filename):
	
	f = open(str(filename));
	a = f.read();
	a = a.split('\n');
	a.pop();

	price = []
	#Getting the closing price from the price file and storing in list: price[]
	for i in range(0, len(a)):
		temp = []
		temp = a[i].split(' ')
		price.append(float(temp[len(temp)-1]))

	
	file = open("price_annotation_file.txt", "w")
	

	for i in range(2000, len(price)):
		current_price = price[i]

		#The list of prices to be compared with compare_point
		time_frame = price[i-200:i]

		#The price point
		compare_point = price[i-201]
		buy_flag = 0
		sell_flag = 0
		neutral_flag = 0
		classification = ''
		for j in range(0, len(time_frame)):

			price_diff = time_frame[j] - compare_point
			price_diff_percent = float("{:.2f}".format((price_diff/compare_point)*100))
			
			#Buy point determination
			if price_diff_percent < 10:
				buy_flag = 1
			
			if (buy_flag == 0) and (price_diff_percent >= 30):
				classification = 'b'

			#Sell point determination
			if price_diff_percent > 10:
				sell_flag = 1
			
			if (sell_flag == 0) and (price_diff_percent <= 30):
				classification = 's'

		if (classification != 'b') or (classification != 's'):
			classification = 'n'

		file = open("price_annotation_file.txt","a")
		file.write(str(i)+" "+classification+"\n")
		
	file.close()
	print("price annotation file modified\n")

def read_in (filename):
 x = [];
 f = open(str(filename))
 a = f.read(); 
 a = a.split('\n'); 
 a.pop();

 for i in range(0, len(a)):
  temp = [];
  temp = a[i].split(' ');
  for l in range(0, len(temp)):
   temp[l] = (float(temp[l]))
  x.append(temp);
 x = np.asarray(x)
 return x

def _quit():
    root.quit()     # stops mainloop
    root.destroy()

def candle( ):
  global o,h,l,c
  plist =[];
  plist.append(ax.get_xbound());
  plist.append(ax.get_ybound());
  x = read_in(filename);
  
  
  o = x[:,0]; h =x[:,1]; l = x[:,2]; c = x[:,3];
  #fig, ax = plt.subplots()
  fnc.candlestick2_ohlc(ax,o,h,l,c,width=0.7,colorup='g', colordown='r');
  print("Candlesticks plotted");
 
  ax.set_xbound(plist[0][0],plist[0][1]);
  ax.set_ybound(plist[1][0],plist[1][1]);
  plist = [];
  fig.canvas.draw()




root = tkinter.Tk()
root.wm_title("JBS Trading")
fig,ax = plt.subplots()
frame = Frame(root)
frame.pack(side=TOP,fill=BOTH)

Topframe = Frame(root)
Topframe.pack( side = TOP, fill=BOTH)


filename = "eurusd_TEST.txt"
plt.subplots_adjust(left=0.06, bottom=0.08, right=0.96, top=0.97, wspace=0.20, hspace=None)
plt.ylim(0,100)
plt.xlim(-1000, 13000)
candle()
annotation(filename)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH ,expand=1)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


BottomFrame1=Frame(root)
BottomFrame1.pack( side = BOTTOM,fill=X )

button = tkinter.Button(master=BottomFrame1, text="Quit", command=_quit)
button.pack(side=tkinter.LEFT)


def my_mainloop():
    root.after(10000, my_mainloop)

root.after(1000, my_mainloop)
root.mainloop()