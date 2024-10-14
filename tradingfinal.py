from __future__ import print_function
import sys
import tkinter
import onlystream2 as osx
import stream_trade2 as st
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import ttk
from tkinter import *
import numpy as np
import tkinter.messagebox
import copy
from tkinter.ttk import *
import matplotlib.pyplot as plt
import mpl_finance as fnc
import subprocess
import notify2
#from helper import read_support_resistance as rsr
from matplotlib.widgets import Cursor
import time
#hs,lr = rsr();
hs=1.23;
lr=1.06;

	#reading file with 4 column values
def read_in (filename):
 x = []; 
 f = open(str(filename))
 a = f.read();
 a = a.split('\n'); 
 a.pop();
 for i in range(0, len(a)):
  temp=[];temp = a[i].split(' ');
  for l in range(0, len(temp)):
   temp[l] = (float(temp[l]))
  x.append(temp); 
 x = np.asarray(x) 
 return x 

#reading file with 1 column values
def read_preds(filename):
 x = []; 
 f = open(str(filename));
 a = f.read(); 
 a = a.split('\n');
 a.pop();
 for i in range(0, len(a)):
  a[i] = (float(a[i])*(hs-lr)) + lr;
 print (np.shape(a));	
 return a


 	#Global variable declaration 
global bidtext,asktext,tradesltext,tradetptext,buytptext,selltptext,buysltext,sellsltext
global bidline,askline,buyslline,buytpline,selltpline,sellslline,tradetpline,tradeslline;
global bid,div; div=None; bid=None;
global r,b,g,c2,l2,s1,ct2,tradelinetp,tradelinesl
global cntred,cntblue,cntgreen,cnt,buyviewcnt,sellviewcnt,cntcnn2,cntlstm2,cntsig,cntctrnn2,tradecnt,tradeviewcnt
cntgreen=0;cntblue=0;cntred=0;cnt=0;buyviewcnt=0;sellviewcnt=0;cntcnn2=0;cntlstm2=0;cntsig=0;cntctrnn2=0;tradecnt=0;tradeviewcnt=0
global skip; skip = 0; 
global exit_flag; exit_flag = False;
global draw_state;draw_state = 0;
global plist; plist = []

def oddEven(num):
 
  mod = num % 2
  if mod > 0:
    return 1
  else:
    return 0

def _quit():
    root.quit()     # stops mainloop
    root.destroy()
#update button currently updates the bid and ask lines and the sl,tp,price fields
def update():
  global bidline,askline,cnt,bidtext,asktext
  
  ask,bid=st.get_current_price()
  #setting the ask and bid value it's confusing
 # buysl.set(ask);buytp.set(bid);buytsl.set(bid);buyprice.set(ask);
 # sellsl.set(bid);selltp.set(ask);selltsl.set(ask);sellprice.set(bid);
  buysl.set(ask);buytp.set(ask);buytsl.set(bid);buyprice.set(ask);
  sellsl.set(bid);selltp.set(bid);selltsl.set(ask);sellprice.set(bid);
  plist =[]
  plist.append(ax.get_xbound())
  plist.append(ax.get_ybound())
  if cnt==0:
    bidline=plt.hlines(bid, 0, 15000, colors='k', linestyles='dotted')
    askline=plt.hlines(ask, 0, 15000, colors='k', linestyles='dotted')
    asktext=ax.text(1.0,ask,ask, va='center', ha="left", transform=ax.get_yaxis_transform())
    bidtext=ax.text(1.0,bid,bid, va='center', ha="left", transform=ax.get_yaxis_transform())
   #   x=plt.text(5000, float(bid), 'bid')
    cnt=1
  else:
    bidline.remove()
    askline.remove()
    bidtext.remove()
    asktext.remove()
    asktext=ax.text(1.0,ask,ask, va='center', ha="left", transform=ax.get_yaxis_transform())
    bidtext=ax.text(1.0,bid,bid, va='center', ha="left", transform=ax.get_yaxis_transform())
    #x=plt.text(5000, float(bid), 'bid')
    # plt.text(5000, float(ask), 'ask')
    bidline=plt.hlines(bid, 0, 15000, colors='k', linestyles='dotted')
    askline=plt.hlines(ask, 0, 15000, colors='k', linestyles='dotted')
  ax.set_xbound(plist[0][0],plist[0][1])
  ax.set_ybound(plist[1][0],plist[1][1])
  plist = []
  
  #toplevel = Toplevel()
  #label1 = Label(toplevel, text="ABOUT_TEXT")
  #label1.pack()
  fig.canvas.draw()
#buyView shows the preview of the tp,sl values lines
def buyView():
  global buytpline,buyslline,buyviewcnt,selltpline,sellslline,sellviewcnt,buytptext,buysltext
  plist =[]
  plist.append(ax.get_xbound())
  plist.append(ax.get_ybound())
  x=tp.get();y=stop_loss.get()
  if sellviewcnt==1:
    sellslline.remove()
    selltpline.remove()
    sellsltext.remove()
    selltptext.remove()
    sellviewcnt=0
  if buyviewcnt==0:
    x=tp.get();y=stop_loss.get()
    buytpline=plt.hlines(float(x), 0, 15000, colors='Red', linestyles='dotted')
    buyslline=plt.hlines(float(y), 0, 15000, colors='Red', linestyles='dotted')
    buytptext=ax.text(1.0,float(x),str(x), va='center', ha="left", transform=ax.get_yaxis_transform())
    buysltext=ax.text(1.0,float(y),str(y), va='center', ha="left", transform=ax.get_yaxis_transform())
    buyviewcnt=1
   
  else:
    buytpline.remove()
    buyslline.remove()
    buysltext.remove()
    buytptext.remove()
    buytptext=ax.text(1.0,float(x),str(x), va='center', ha="left", transform=ax.get_yaxis_transform())
    buysltext=ax.text(1.0,float(y),str(y), va='center', ha="left", transform=ax.get_yaxis_transform())
    buytpline=plt.hlines(float(x), 0, 15000, colors='Red', linestyles='dotted')
    buyslline=plt.hlines(float(y), 0, 15000, colors='Red', linestyles='dotted')
  ax.set_xbound(plist[0][0],plist[0][1])
  ax.set_ybound(plist[1][0],plist[1][1])
  plist = []  
  fig.canvas.draw()

def sellView():
  global selltpline,sellslline,sellviewcnt,buytpline,buyslline,buyviewcnt,sellsltext,selltptext
  plist =[]
  plist.append(ax.get_xbound())
  plist.append(ax.get_ybound())
  x=stp.get();y=sellstop_loss.get()
  if buyviewcnt==1:
    buyslline.remove()
    buytpline.remove()
    buytptext.remove()
    buysltext.remove()
    buyviewcnt=0
  if sellviewcnt==0:
    selltpline=plt.hlines(float(x), 0, 15000, colors='Red', linestyles='dotted',label='take Profit')
    sellslline=plt.hlines(float(y), 0, 15000, colors='Red', linestyles='dotted',label='stop loss')
    selltptext=ax.text(1.0,float(x),str(x), va='center', ha="left", transform=ax.get_yaxis_transform())
    sellsltext=ax.text(1.0,float(y),str(y), va='center', ha="left", transform=ax.get_yaxis_transform())
    sellviewcnt=1
    
  else:
    selltpline.remove()
    sellslline.remove()
    selltptext.remove()
    sellsltext.remove()
    selltptext=ax.text(1.0,float(x),str(x), va='center', ha="left", transform=ax.get_yaxis_transform())
    sellsltext=ax.text(1.0,float(y),str(y), va='center', ha="left", transform=ax.get_yaxis_transform())
    selltpline=plt.hlines(float(x), 0, 15000, colors='Red', linestyles='dotted',label='take Profit')
    sellslline=plt.hlines(float(y), 0, 15000, colors='Red', linestyles='dotted',label='stop loss')
  #plt.text(5000, float(x), 'take Profit',transform=ax.get_yaxis_transform())
 # plt.text(5000, float(y), 'stop loss')
  ax.set_xbound(plist[0][0],plist[0][1])
  ax.set_ybound(plist[1][0],plist[1][1])
  plist = []  
  fig.canvas.draw()

#method to draw the horizontal lines
def draw():
  global div,bid
  if div == None:
    div=fig.canvas.mpl_connect('button_press_event', horizontal_line)
    bid=fig.canvas.mpl_disconnect(bid)
    
  else:
    div=fig.canvas.mpl_disconnect(div)
 
#method to draw 2pnt lines or vertical lines
def draw_button():
  global bid,div
  if bid == None:
    bid=fig.canvas.mpl_connect('button_press_event', draw_lines)
    div=fig.canvas.mpl_disconnect(div)
  else:
    bid=fig.canvas.mpl_disconnect(bid)
#method used when draw_button is clicked
def draw_lines(event):
  global draw_state; global plist; 
  draw_state = 1;
  mlist =[]
  mlist.append(ax.get_xbound())
  mlist.append(ax.get_ybound()) 
  plist.append([event.xdata,event.ydata]);
  if (draw_state == 1): 
    ax.scatter(event.xdata,event.ydata,c='b')
  if (len(plist) == 2):
    ax.arrow(plist[0][0],plist[0][1], plist[1][0]-plist[0][0],plist[1][1]-plist[0][1], width = 0.000001);
    plist=[]

  ax.set_xbound(mlist[0][0],mlist[0][1])
  ax.set_ybound(mlist[1][0],mlist[1][1])
  mlist = []  
  fig.canvas.draw()
#method called when draw button is pressed
def horizontal_line(event):
  global plist,bid
  mlist =[]
  mlist.append(ax.get_xbound())
  mlist.append(ax.get_ybound()) 
  plist=[]
  #ax.scatter(event.xdata,event.ydata,c='b')
  plt.hlines(event.ydata, 0, 15000, colors='k', linestyles='solid')
  ax.set_xbound(mlist[0][0],mlist[0][1])
  ax.set_ybound(mlist[1][0],mlist[1][1])
  mlist = []
  fig.canvas.draw()
def trade_view():
  global tradecnt,tradetpline,tradeslline,tradeviewcnt,tradetptext,tradesltext
  plist =[];
  plist.append(ax.get_xbound());
  plist.append(ax.get_ybound());
  if tradecnt==0:
    tradecnt=1
    vtrade.config(relief='sunken')
  else:
    tradecnt=0
    vtrade.config(relief='raised')
    if tradeviewcnt==1:
      tradetpline.remove()
      tradeslline.remove()
      tradesltext.remove()
      tradetptext.remove()
      tradeviewcnt=0
      ax.set_xbound(plist[0][0],plist[0][1]);
      ax.set_ybound(plist[1][0],plist[1][1])
      plist = [];
      fig.canvas.draw()
def trade_line():
  global tradelinetp,tradelinesl
  global tradetpline,tradeviewcnt,tradeslline,tradesltext,tradetptext
  tp=tradelinetp;sl=tradelinesl
  plist =[]
  plist.append(ax.get_xbound())
  plist.append(ax.get_ybound())
  if tradecnt==1:
    if tradeviewcnt==0:
      tradetpline=plt.hlines(float(tp), 0, 15000, colors='#224D17', linestyles='dotted',label='take Profit')
      tradeslline=plt.hlines(float(sl), 0, 15000, colors='magenta', linestyles='dotted',label='stop loss')
      tradetptext=ax.text(1.0,float(tp),str(tp), va='center', ha="left", transform=ax.get_yaxis_transform())
      tradesltext=ax.text(1.0,float(sl),str(sl), va='center', ha="left", transform=ax.get_yaxis_transform())
      tradeviewcnt=1
    else:
      tradetpline.remove()
      tradeslline.remove()
      tradesltext.remove()
      tradetptext.remove()
      tradetptext=ax.text(1.0,float(tp),str(tp), va='center', ha="left", transform=ax.get_yaxis_transform())
      tradesltext=ax.text(1.0,float(sl),str(sl), va='center', ha="left", transform=ax.get_yaxis_transform())
      tradetpline=plt.hlines(float(tp), 0, 15000, colors='#224D17', linestyles='dotted',label='take Profit')
      tradeslline=plt.hlines(float(sl), 0, 15000, colors='magenta', linestyles='dotted',label='stop loss')

  #ax.text(5000, float(x), 'take Profit',transform=ax.get_yaxis_transform())
 # plt.text(5000, float(y), 'stop loss')
  ax.set_xbound(plist[0][0],plist[0][1])
  ax.set_ybound(plist[1][0],plist[1][1])
  plist = []  
  fig.canvas.draw()

#just clears every thing and plot the candles and predictons
def clear_button():
  global r,b,g,s1,c2,l2,ct2,sellviewcnt,buyviewcnt,cnt,tradeviewcnt

  plist =[];
  plist.append(ax.get_xbound());
  plist.append(ax.get_ybound());
  ax.clear(); 
  draw_state = 0; 
  fnc.candlestick2_ohlc(ax,o,h,l,c,width=0.7,colorup='g', colordown='r');
  if(r!=0):
    r,=ax.plot(ctrnnpreds1,'y');
  if(b!=0):
    b,=ax.plot(cnnpreds,'b');
  if(g!=0):
    g,=ax.plot(lstmpreds,'g');
  if(s1!=0):
    s1,=ax.plot(lstmpreds,'r');
  if(c2!=0):
    c2,=ax.plot(cnnpreds,'violet');
  if(l2!=0):
    l2,=ax.plot(lstmpreds,'orange');
  if(ct2!=0):
    ct2,=ax.plot(ctrnnpreds1,'purple');
  if buyviewcnt==1:
    buyviewcnt=0
    buyView()
  if sellviewcnt==1:
    sellviewcnt=1
    sellView()
  if tradeviewcnt==1:
    tradeviewcnt=0
    trade_line()
  if cnt==1:
    cnt=0

  ax.set_xbound(plist[0][0],plist[0][1]);
  ax.set_ybound(plist[1][0],plist[1][1])
  plist = [];

  fig.canvas.draw()
def Ctrnn1():
  global r,cntred
  cntred=cntred+1
  if(oddEven(cntred)):
    ax.lines.remove(r)
    line1.config(relief='sunken')
    r=0
    
  else:
    r,=ax.plot(ctrnnpreds1,'y');
    line1.config(relief='raised')

    #r=1
  fig.canvas.draw()
def Ctrnn2():
  global ct2,cntctrnn2
  cntctrnn2=cntctrnn2+1
  if(oddEven(cntctrnn2)):
    ax.lines.remove(ct2)
    line7.config(relief='sunken')
    ct2=0
  else:
    ct2,=ax.plot(ctrnnpreds1,'purple');
    line7.config(relief='raised')
    #r=1
  fig.canvas.draw()

def Cnn1():
  global b,cntblue
  cntblue=cntblue+1
  if(oddEven(cntblue)):
    ax.lines.remove(b)
    line2.config(relief='sunken')
    b=0
  else:
    b,=ax.plot(cnnpreds,'b');
    line2.config(relief='raised')
    
  fig.canvas.draw()
def Cnn2():
  global c2,cntcnn2
  cntcnn2=cntcnn2+1
  if(oddEven(cntcnn2)):
    ax.lines.remove(c2)
    line4.config(relief='sunken')
    c2=0
  else:
    c2,=ax.plot(cnnpreds,'violet');
    line4.config(relief='raised')
    
  fig.canvas.draw()

def lstm1():
  global g,cntgreen
  cntgreen=cntgreen+1
  if(oddEven(cntgreen)):
    ax.lines.remove(g)
    line3.config(relief='sunken')
    g=0
  else:
    g,=ax.plot(lstmpreds,'g');
    line3.config(relief='raised')
  fig.canvas.draw()
def lstm2():
  global l2,cntlstm2
  cntlstm2=cntlstm2+1
  if(oddEven(cntlstm2)):
    ax.lines.remove(l2)
    line5.config(relief='sunken')
    l2=0
  else:
    l2,=ax.plot(lstmpreds,'orange');
    line5.config(relief='raised')
  fig.canvas.draw()
def Sig():
  global s1,cntsig
  cntsig=cntsig+1
  if(oddEven(cntsig)):
    ax.lines.remove(s1)
    line6.config(relief='sunken')
    s1=0
  else:
    s1,=ax.plot(lstmpreds,'r');
    line6.config(relief='raised')
  fig.canvas.draw()
def getScript1(event):
  if tslbtn.get() ==1:
    stop_loss.configure(state=NORMAL)
    trailstop_loss.configure(state=DISABLED)
  if tslbtn.get() ==2:
    trailstop_loss.configure(state=NORMAL)
    stop_loss.configure(state=DISABLED)
def getScript(event):
  if slbtn.get() ==1:
    sellstop_loss.configure(state=NORMAL)
    selltrailstop_loss.configure(state=DISABLED)
  if slbtn.get() ==2:
    selltrailstop_loss.configure(state=NORMAL)
    sellstop_loss.configure(state=DISABLED)

def buyOrder():
  tk=tp.get();ordertype=buybtn.get();units=unit.get();sl=stop_loss.get();tsl=trailstop_loss.get();
  prices=price.get()
  if tslbtn.get() ==1:
    tsl=None
  elif tslbtn.get() ==2:
    sl=None
  else:
    notify2.init('app name')
    iconpath="/home/abhijeet/Desktop/final/2.png"
    n = notify2.Notification("Buy",
                         "Select sl or tsl",
                         icon=iconpath  # Icon name
                        )
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(1000)
    n.show()
  if ordertype==1:

    x=st.buy_market_order(units, sl,tk,tsl)
    if x==1:
      messagebox.showinfo('Yes', 'Order successfully placed')
    else:
      messagebox.showinfo('No', 'Order Not placed')
  if ordertype==2:
    print("Limit order yet to be completed")

def sellOrder():
  tk=stp.get();ordertype=sellbtn.get();units=sellunit.get();sl=sellstop_loss.get();tsl=selltrailstop_loss.get();
  prices=sprice.get()
  if slbtn.get() ==1:
    tsl=None
  elif slbtn.get() ==2:
    sl=None
  else:
    messagebox.showinfo('Sell', 'Select sl or tsl')

  if ordertype==1:
    units=0-float(units)
    x=st.buy_market_order(units, sl,tk,tsl)
    if x==1:
      messagebox.showinfo('Sell', 'Order successfully placed')
    else:
      messagebox.showinfo('Sell', 'Order Not placed')
  if ordertype==2:
    print("Limit order yet to be completed")
  else:
    print("ordertype not selected")
def close_Trade():
  tp=ctp.get();sl=csl.get();tradeid=ctradeId.get();
  st.close_trade(tradeid)

def edit_Trade():
  tp=ctp.get();sl=csl.get();tradeid=ctradeId.get();
  answer = messagebox.askokcancel("Question","Do you want to change trade ?")
  print(answer)
  if answer == True:
    x=st.change_trade(tradeid,tp,sl)
    print(x)
    if x== 1:
      messagebox.showinfo('CRCDO', 'Order Changed successfully')
    else:
      messagebox.showinfo('CRCDO', 'Order Not Changed')
  else:
    print("Change trade cancelled")

root = tkinter.Tk()
root.wm_title("JBS Trading")
fig,ax = plt.subplots()
frame = Frame(root)
frame.pack(side=TOP,fill=BOTH)

Topframe = Frame(root)
Topframe.pack( side = TOP, fill=BOTH)



#variable declaration for differnt oreder fields
buybtn = IntVar();buytp=IntVar();buysl=IntVar();buytsl=IntVar();buyprice=IntVar();
sellbtn=IntVar();selltp=IntVar();sellsl=IntVar();selltsl=IntVar();sellprice=IntVar();slbtn=IntVar();tslbtn=IntVar()
csl=StringVar();ctp=StringVar();ctradeId=StringVar()
#buttons of buy order
updatebutton = Button(frame, text="Update",command= update).pack( side = LEFT)
Drawbutton = Button(frame, text="Draw",command=draw).pack( side = LEFT)
linebutton = Button(frame, text="Draw Line", command=draw_button).pack(side = LEFT)
clearbutton = Button(frame, text="Clear",command=clear_button).pack( side = LEFT)
buy= Button(frame, text="Buy",command=buyOrder).pack(side=LEFT)
lunit=Label(frame, text="Unit").pack(side=LEFT)
unit=Spinbox(frame,from_=1,to_=2000000, increment="1")
unit.pack(side=LEFT)
sl = Label(frame, text="sl").pack( side = LEFT)
stop_loss=Spinbox(frame,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f",textvariable=buysl)
stop_loss.pack(side=LEFT)
tsl = Label(frame, text="tsl")
tsl.pack( side = LEFT)
trailstop_loss=Spinbox(frame,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f",textvariable=buytsl)
trailstop_loss.pack(side=LEFT)
ltp = Label(frame, text="tp").pack( side = LEFT)
tp=Spinbox(frame,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f",textvariable=buytp)
tp.pack(side=LEFT)
lprice = Label(frame, text="price").pack( side = LEFT)
price=Spinbox(frame,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f", textvariable=buyprice)
price.pack(side=LEFT)
market_order=Radiobutton(frame, text="Market order",value=1,variable=buybtn)
market_order.pack(anchor= W)
limit_order=Radiobutton(frame, text="Limit order", value=2,variable=buybtn)
limit_order.pack(side = LEFT)
#summary= Button(frame, text="Summary",command=st.get_account_summary).pack(side=LEFT)
slradiobutton=Radiobutton(frame, text="Stop Loss",value=1,variable=tslbtn,command = lambda : getScript1(None))
slradiobutton.pack(anchor=W)
tslradiobutton=Radiobutton(frame, text="Trail Stop Loss", value=2,variable=tslbtn,command = lambda : getScript1(None))
tslradiobutton.pack(anchor = W)

#TOP FRAME,Buttons for sell order
auto=Button(Topframe, text="Auto").pack(side=LEFT)
lock=Button(Topframe, text="Lock").pack(side=LEFT)
viewsell=Button(Topframe, text="Sell View",command=sellView).pack(side=LEFT)
viewbuy=Button(Topframe, text="Buy View",command=buyView).pack(side=LEFT)
sell= Button(Topframe, text="Sell",command=sellOrder).pack(side=LEFT)
lunit=Label(Topframe, text="Unit").pack(side=LEFT)
sellunit=Spinbox(Topframe,from_=1,to_=2000000, increment="1")
sellunit.pack(side=LEFT)
sl = Label(Topframe, text="sl").pack( side = LEFT)
sellstop_loss=Spinbox(Topframe,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f",textvariable=sellsl)
sellstop_loss.pack(side=LEFT)
tsl = Label(Topframe, text="tsl")
tsl.pack( side = LEFT)
selltrailstop_loss=Spinbox(Topframe,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f",textvariable=selltsl)
selltrailstop_loss.pack(side=LEFT)
ltp = Label(Topframe, text="tp").pack( side = LEFT)
stp=Spinbox(Topframe,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f",textvariable=selltp)
stp.pack(side=LEFT)
lprice = Label(Topframe, text="price").pack( side = LEFT)
sprice=Spinbox(Topframe,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f", textvariable=sellprice)
sprice.pack(side=LEFT)
sellmarket_order=Radiobutton(Topframe, text="Market order",value=1,variable=sellbtn)
sellmarket_order.pack(anchor= W)
selllimit_order=Radiobutton(Topframe, text="Limit order", value=2,variable=sellbtn)
selllimit_order.pack(side = LEFT)
sellslradiobutton=Radiobutton(Topframe, text="Stop Loss",value=1,variable=slbtn,command = lambda : getScript(None))
sellslradiobutton.pack(anchor=W)
selltslradiobutton=Radiobutton(Topframe, text="Trail Stop Loss", value=2,variable=slbtn,command = lambda : getScript(None))
selltslradiobutton.pack(anchor = W)



#stop_loss.configure(state=DISABLED)
from scipy.signal import savgol_filter

ctrnnpreds1 = read_preds('5800.txt') #file path edited

#ctrnnpreds2 = read_preds ('/home/apn3/sim_lugustech/6200.txt')
cnnpreds = read_preds('cnn_8Dec'); 
lstmpreds = read_preds('lstm_8dec');
buff = [lr]*784;
cnnpreds = buff+cnnpreds; lstmpreds = buff + lstmpreds;
buff = [lr]*500;
ctrnnpreds1 = buff+ctrnnpreds1
lstmpreds = savgol_filter(lstmpreds, 11, 5);


print (len(cnnpreds), len(ctrnnpreds1));

filename = "price_log/eurusd_8_Dec.txt";
#filename = "eurusd_8_Dec.txt";
#Candle method is called every 2 mins when a complete candle is retrieved new candlestick is plotted
def candle( ):
  global o,h,l,c,r,b,g,s1,l2,c2,ct2
  plist =[];
  plist.append(ax.get_xbound());
  plist.append(ax.get_ybound());
#x = read_in(filename);
  x=osx.price_set
#print("Hii")
#print (np.shape(x)); 
  o = x[:,0]; h =x[:,1]; l = x[:,2]; c = x[:,3];
#fig, ax = plt.subplots()
  fnc.candlestick2_ohlc(ax,o,h,l,c,width=0.7,colorup='g', colordown='r');
  print("Candle updated");
  if(r!=0):
    ax.lines.remove(r)
    r,=ax.plot(ctrnnpreds1,'y');
  if(b!=0):
    ax.lines.remove(b)
    b,=ax.plot(cnnpreds,'b');
  if(g!=0):
    ax.lines.remove(g)
    g,=ax.plot(lstmpreds,'g');
  if(s1!=0):
    ax.lines.remove(s1)
    s1,=ax.plot(lstmpreds,'r');
  if(c2!=0):
    ax.lines.remove(c2)
    c2,=ax.plot(cnnpreds,'violet');
  if(l2!=0):
    ax.lines.remove(l2)
    l2,=ax.plot(lstmpreds,'orange');
  if(ct2!=0):
    ax.lines.remove(ct2)
    ct2,=ax.plot(ctrnnpreds1,'purple');
  ax.set_xbound(plist[0][0],plist[0][1]);
  ax.set_ybound(plist[1][0],plist[1][1])
  plist = [];
  fig.canvas.draw()


r,=ax.plot(ctrnnpreds1,'y');
b,=ax.plot(cnnpreds,'b'); 
g,=ax.plot(lstmpreds,'g');
s1,=ax.plot(lstmpreds,'r');
c2,=ax.plot(cnnpreds,'violet');
l2,=ax.plot(lstmpreds,'orange');
ct2,=ax.plot(ctrnnpreds1,'purple')

#plt.gca().yaxis.set_minor_formatter()
plt.xlim(0,100)
plt.ylim(0, 12000)
plt.subplots_adjust(left=0.06, bottom=0.08, right=0.96, top=0.97, wspace=0.20, hspace=None)


candle()

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH ,expand=1)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


BottomFrame1=Frame(root)
BottomFrame1.pack( side = BOTTOM,fill=X )
BottomFrame=Frame(root)
BottomFrame.pack( side = BOTTOM,fill=X )


line1 = tkinter.Button(master=BottomFrame1, text="Ctrnn1", command=Ctrnn1)
line1.pack(side=tkinter.RIGHT)
line7 = tkinter.Button(master=BottomFrame1, text="Ctrnn2", command=Ctrnn2)
line7.pack(side=tkinter.RIGHT)
line2 = tkinter.Button(master=BottomFrame1, text="Cnn1", command=Cnn1)
line2.pack(side=tkinter.RIGHT)
line4 = tkinter.Button(master=BottomFrame1, text="Cnn2", command=Cnn2)
line4.pack(side=tkinter.RIGHT)
line3 = tkinter.Button(master=BottomFrame1, text="lstm1", command=lstm1)
line3.pack(side=tkinter.RIGHT)
line5 = tkinter.Button(master=BottomFrame1, text="lstm2", command=lstm2)
line5.pack(side=tkinter.RIGHT)
line6 = tkinter.Button(master=BottomFrame1, text="Sig", command=Sig)
line6.pack(side=tkinter.RIGHT)  


tid=Label(BottomFrame1, text="TradeID").pack(side=LEFT)
tidbox=Spinbox(BottomFrame1,from_=1,to_=2000000, increment="1",textvariable=ctradeId)
tidbox.pack(side=LEFT)
ssl = Label(BottomFrame1, text="sl").pack( side = LEFT)
sloss=Spinbox(BottomFrame1,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f",textvariable=csl)
sloss.pack(side=LEFT)
ltp = Label(BottomFrame1, text="tp")
ltp.pack( side = LEFT)
tpbox=Spinbox(BottomFrame1,from_=1.00000,to_=2.00000, increment="0.0001",format="%.5f",textvariable=ctp)
tpbox.pack(side=LEFT)
tclose = tkinter.Button(master=BottomFrame1, text="Close", command=close_Trade)
tclose.pack(side=tkinter.LEFT)
tedit = tkinter.Button(master=BottomFrame1, text="Edit", command=edit_Trade)
tedit.pack(side=tkinter.LEFT)
vtrade = tkinter.Button(master=BottomFrame1, text="View Trade",command=trade_view)
vtrade.pack(side=tkinter.LEFT)
button = tkinter.Button(master=BottomFrame1, text="Quit", command=_quit)
button.pack(side=tkinter.LEFT)

# Treeview for the trade bar 
style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, rowheight=25,font=('Calibri', 11))
style.configure("mystyle.Treeview.Heading", font=('Calibri', 11,'bold'))
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'ns'})])
tree=ttk.Treeview(BottomFrame,height=3,style="mystyle.Treeview")
tree.tag_configure('odd', background='#E8E8E8')
tree.tag_configure('even', background='#DFDFDF')
tree.pack(side=LEFT,fill=X)
tree["columns"]=("zero","one","two","three","four","five","six","seven","eight","nine")
tree.column("#0", width=0, minwidth=0, stretch=NO)
tree.column("zero", width=150, minwidth=150, stretch=NO)
tree.column("one", width=150, minwidth=150, stretch=NO)
tree.column("two", width=150, minwidth=200, stretch=NO)
tree.column("three", width=150, minwidth=50, stretch=NO)
tree.column("four", width=150, minwidth=50, stretch=NO)
tree.column("five", width=150, minwidth=50, stretch=NO)
tree.column("six", width=150, minwidth=50, stretch=NO)
tree.column("seven", width=150, minwidth=50, stretch=NO)
tree.column("eight", width=150, minwidth=50, stretch=NO)
tree.column("nine", width=150, minwidth=50, stretch=YES)
tree.heading("#0",text="Ticket",anchor=E)
tree.heading("zero",text="TradeID",anchor=N)
tree.heading("one", text="Market",anchor=N)
tree.heading("two", text="units",anchor=N)
tree.heading("three", text="Type",anchor=N)
tree.heading("four", text="SL",anchor=N)
tree.heading("five", text="TP",anchor=N)
tree.heading("six", text="TS",anchor=N)
tree.heading("seven", text="Price",anchor=N)
tree.heading("eight", text="R P/L",anchor=N)
tree.heading("nine", text="UR P/L",anchor=N)
vsb = ttk.Scrollbar(BottomFrame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side=LEFT,fill=BOTH)
#tree.grid(row=0, column=0, sticky='nsew')
def trade_Update():
  val,tradenos=st.get_open_trades()
  for i in tree.get_children():
    tree.delete(i)
  for x in range(0,tradenos):
    tree.insert('', x, values=(val[x][0],val[x][1],val[x][2],val[x][3],val[x][4],val[x][5],val[x][6], val[x][7],val[x][8],val[x][9]),tags=("odd",))
  #tree.insert('', 1, values=("110","100","","120","130","140","150"),tags=("odd",))


def selectItem(a):
  global tradelinetp,tradelinesl
  curItem = tree.focus();
  
  x=tree.item(curItem)
  TradeID=x['values'][0];sl=x['values'][4];tp=x['values'][5]
  tradelinesl=sl;tradelinetp=tp;
  ctradeId.set(TradeID);csl.set(sl);ctp.set(tp)
  trade_line()
  print(TradeID,"",tp,"",sl)

tree.bind('<ButtonRelease-1>', selectItem)

style1 = ttk.Style()
style1.configure("mystyle.Treeview", highlightthickness=0, bd=0,rowheight=25,height=50, font=('Calibri', 11))
style1.configure("mystyle.Treeview.Heading", font=('Calibri', 11,'bold'))
style1.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
tree1=ttk.Treeview(BottomFrame,height=3,style="mystyle.Treeview")
tree1.tag_configure('odd', background='#E8E8E8')
tree1.tag_configure('even', background='#DFDFDF')
tree1.pack(side=RIGHT,fill=X)
tree1["columns"]=("zero","one")
tree1.column("#0", width=0, minwidth=0, stretch=NO)
tree1.column("zero", width=150, minwidth=150, stretch=NO)
tree1.column("one", width=150, minwidth=150)
tree1.heading("#0",text="Ticket",anchor=N)
tree1.heading("zero",text="Account",anchor=N)
tree1.heading("one", text="GBP",anchor=N)
balance,rpl,urpl=st.get_account_summary()
tree1.insert('', END, values=('Balance',balance))
tree1.insert('', 1, values=('Realized P/L',rpl))
tree1.insert('', 2, values=('Margin Used',urpl))

#tree.delete(m)
#tree.detach(n)
#tree.move(n,'',2)

def my_mainloop():
    print ("Hello World!");
    trade_Update()
    #Automatically updating the price only for marketorder(view purpose)
    if sellbtn.get() ==1 and buybtn.get() == 1 :
      ask,bid=st.get_current_price()
      buyprice.set(ask);sellprice.set(bid)
    elif buybtn.get() == 1:
      ask,bid=st.get_current_price()
      buyprice.set(ask);
    elif sellbtn.get() ==1:
      ask,bid=st.get_current_price();
      sellprice.set(bid)
    #st.signal.signal(st.signal.SIGINT, st.signal_handler); 
    x,t2,comp = st.update_dataset(osx.latest_ny_time, 'EUR_USD'); 
    flag, now_price,false_time = st.check_and_print(osx.latest_time, t2, x,comp)
    if (flag == 1): 
      osx.price_set = np.append(osx.price_set,now_price,axis=0);#we're just appending the last price//because currently the nets just spit 1 output. Most the time it'll be like 1 new price anyway
      osx.latest_time = false_time; osx.latest_ny_time = st.convert_time_stamp(osx.latest_time); print ("updated"); 
      osx.latest_price = copy.deepcopy(now_price);
      #cnn_output,cnn_base_set =dtest.pred(cnn_base_set, model1, now_price);
      now_price = copy.deepcopy(osx.latest_price);
      #lst_output, lst_base_set = ltest.pred(lst_base_set,model_lst, now_price)
      #ctrnn_output = read_ctrnn_data('/home/apn3/sim_lugustech/mpipredict.txt');
      #save_outputs(latest_price[-1],cnn_output,lst_output,ctrnn_output);
      #print (latest_price[-1],cnn_output, lst_output, ctrnn_output); 
      #input("press enter")
      candle()
    root.after(10000, my_mainloop)
root.after(1000, my_mainloop)
root.mainloop()
