import numpy as np
import os 
import sys
import matplotlib.pyplot as plt 

target = 2;
high = 1.17217; low = 1.16177; timz = 'Z';

def read_in (filename):
 x = []; 
 f = open(str(filename))
 a = f.read(); a = a.split('\n'); a.pop();
 for i in range(0, len(a)):
  temp=[];temp = a[i].split(' ');
  for l in range(0, len(temp)):
   temp[l] = (float(temp[l]))
  x.append(temp); 
 x = np.asarray(x) 
 return x 

def read_support_resistance():
 f = open('init_file.txt');
 a = f.read(); f.close();
 a = a.split('\n');
 h = float(a[0].split('=')[1]); l = float(a[1].split('=')[1]); 
 return h,l

def norm_data(data_in,size, end, skip, btest='t',h=0, l=0,):
  begin = end - (size*skip); global high; global low; 
  high, low = read_support_resistance();
  if (begin <0): print ("check sizes"); sys.exit();
  counter = begin; data = [];
  for i in range(0, size):
   counter = begin + (skip*i);#print (i, counter);
   data.append(data_in[counter]);
  data = np.asarray(data);  
  if (btest == 't'):
   h = np.max(data[:,1]); l = np.min(data[:,2]);
   high = h; low = l;   
  for i in range(0,len(data)):
   data[i][0] = (data[i][0]-low)/(high-low);
   data[i][1] = (data[i][1]-low)/(high-low);
   data[i][2] = (data[i][2]-low)/(high-low);
   data[i][3] = (data[i][3]-low)/(high-low);
  return data

def update_cnn(x_in, now_price):
  if (len(now_price) != 0):
   if (len(now_price) > 28): print ('Too many values to update, build dataset again or remake function'); sys.exit(0) 
   xtemp = list(x_in[0]);
   for z in range(0, len(now_price)):
    #print (now_price[z]);
    now_price[z][0] = float(now_price[z][0] - low)/(high - low); now_price[z][1] = float(now_price[z][1] - low)/(high - low);
    now_price[z][2] = float(now_price[z][2] - low)/(high - low); now_price[z][3] = float(now_price[z][3] - low)/(high - low);
    xtemp.pop(); xtemp.insert(0, now_price[z]);# print (now_price[z]);input("ok");
   x_in[0] = np.asarray(xtemp);return x_in; 
  else: x_in = []; return x_in;  

def update_lst (x_in, now_price):
  if (len(now_price) != 0):
   if (len(now_price) > 28): print ('Too many values to update, build dataset again or remake function'); sys.exit(0) 
   xtemp = (x_in[0][0]);#print (np.shape(now_price));sys.exit(0)
   for z in range(0, len(now_price)):
    now_price[z][0] = float(now_price[z][0] - low)/(high - low); now_price[z][1] = float(now_price[z][1] - low)/(high - low);
    now_price[z][2] = float(now_price[z][2] - low)/(high - low); now_price[z][3] = float(now_price[z][3] - low)/(high - low);
    xtemp = xtemp[:-4]; xtemp = np.insert(xtemp,[0,1,2,3],now_price[z]);
   x_in[0] = np.asarray(xtemp);return x_in; 
  else: x_in = []; return x_in;   

def update_x(x_in,ready_file = '/home/apn3/Desktop/Trading_Main/ready'):
  f = open(ready_file);  temp = []; global timz; 
  a = f.read(); f.close(); a = a.split('\n')
  print (a[0], a[-1])
  if (len(a) < 3): x_in = [];return x_in;
  print (a[1], timz); 
  if ((a[0] == 'ok') and (a[-1] =='now_read') and (a[1] != timz)): 
    #input('okk ok ')
    timz = a[1];  
    for i in range(2, len(a)):
      if (a[i]== 'now_read'): break
      b = a[i].split(' '); 
      b[0] = (float(b[0])-low)/(high-low); b[1] = (float(b[1])-low)/(high-low);
      b [2] = (float(b[2])- low)/(high-low); b[3] = (float(b[3])-low)/(high-low)
      temp.append(b)
  if (len(temp) > 0):
   if (len(temp) > 28): print ('Too many values to update, build dataset again or remake function'); sys.exit(0) 
   xtemp = list(x_in[0]);
   print (np.shape(temp), np.shape(x_in));#x_in = np.append(x_in, temp, axis=-1)
   for z in range(0, len(temp)):
    xtemp.pop(); xtemp.insert(0,temp[z]);
   print (np.shape(xtemp)); x_in[0] = np.asarray(xtemp)
  else: x_in = [];
  return x_in 


def return_x_y(x_in,btest='t'):
 stride = 28; 
 global target; 
 if (btest != 't'): target = 0;
 size = len(x_in)-(stride*stride) - target;
 x  = np.zeros ((size,28,28,4)); stride = 28; 
 if (btest == 't'):y = np.zeros((size));
 else: y = [];
 for i in range(0,size):
  init_counter =  i + (stride*stride);
  if (btest == 't'):
   y[i] = x_in[init_counter+target][3]; 
  #if (x_in[init_counter+1] > x_in[init_counter]):y[i] = 0
  #else: y[i] = 1;  
  for j in range(0, stride): 
   k_counter = stride*j;
   for k in range(0,stride):
    x[i][j][k][0] = x_in[init_counter - k_counter- k][0]; 
    x[i][j][k][1] = x_in[init_counter - k_counter- k][1];
    x[i][j][k][2] = x_in[init_counter - k_counter- k][2];
    x[i][j][k][3] = x_in[init_counter - k_counter- k][3];
 return x,y

def save_results(p,y_test, name ='2'):
 p = np.asarray(p); p.flatten();
 c= open('result' + str(name) + '.txt', 'w');
 for i in range(0,len(p)):
  p[i] = float(p[i]);
  c.write("%s %s" % (str(p[i][0]),str(y_test[i]))); c.write('\n')
 c.close();
 plt.plot(p, color='blue'), plt.plot(y_test, color='red'); 
 plt.show();
