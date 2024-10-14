import stream_trade2 as st
# import cnn_test as dtest
# import lst_test as ltest
import sys
import copy
import numpy as np
from helper import read_support_resistance as rsr
# ctrnn_tim = "Z";
if (len(sys.argv) != 2): print ("check input parameters"); #sys.exit(0);
prefix = str(sys.argv[1]); 

# def read_ctrnn_first(filename):
#   f = open(filename); a = f.read(); f.close(); a = a.split('\n'); a.pop(); predz = [];
#   for i in range(0, len(a)): predz.append(float(a[i]))
#   return predz

# def read_ctrnn_data(filename):
#   f = open(filename); global ctrnn_tim;
#   a = f.read(); a = a.split(' '); f.close();
#   if (len(a) > 1):
#    if (ctrnn_tim != str(a[0])): 
#     ctrnn_tim = str(a[0]);
#     return (float(a[1]))
#   return 999;

def save_outputs(latest_price,cnn_output, lst_output, ctrnn_output):
  f = open("output/result_"+str(sys.argv[1]) + ".txt", 'a');
  f.write("%s %s %s %s %s %s %s \n"%(str(latest_price[0]),str(latest_price[1]),str(latest_price[2]),str(latest_price[3]),str(cnn_output['pred_output_classes'][-1][-1]),str(lst_output['pred_output_classes'][-1][-1]), str(ctrnn_output))); 
  f.close();

st.init(prefix);
price_set,t = st.build_base_dataset('EUR_USD',5000); 

latest_ny_time, latest_time = st.write_base_set_and_get_time(price_set,t);
#lates_ny_time is basically the current time

h,l = rsr(); print (h,l); #sys.exit(0)
# ctrnn_init_preds = read_ctrnn_first("/home/apn3/sim_lugustech/mpi_first.txt"); print (ctrnn_init_preds);

# model1 = dtest.load("/home/apn3/CNN_TRADING/18sept_/1537265465");
# model_lst = ltest.load('/home/apn3/CNN_TRADING/lst_/1537272032');

# cnn_base_set, cnn_init_preds = dtest.init(sys.argv[1]); 
# lst_base_set, lst_init_preds = ltest.init(sys.argv[1]); 

