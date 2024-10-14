import sys
import signal
import copy
import numpy as np
import argparse
import json
import datetime
from dateutil.parser import parse
import pytz
from oandapyV20 import API
from oandapyV20.exceptions import V20Error, StreamTerminated
from oandapyV20.endpoints.pricing import PricingStream, PricingInfo
from exampleauth import exampleAuth
from requests.exceptions import ConnectionError
from oandapyV20.exceptions import V20Error
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.accounts as accounts
from oandapyV20.contrib.requests import (
    MarketOrderRequest,
    LimitOrderRequest,
    TakeProfitDetails,
    StopLossDetails,
    TrailingStopLossDetails
)


def init(prefix):
 global accountID; global access_token; global api; global inz; global FILESTORE; global interrupted;
 accountID, access_token = exampleAuth()
 api = API(access_token = access_token, environment="practice"); 
 inz={"instruments": "EUR_USD"}
 FILESTORE = 'price_log/eurusd_'+str(prefix)+'.txt';interrupted = 'False';


#bid =sell and ask = buy
def get_current_price():
 r = PricingStream(accountID=accountID,params=inz) 
 x = api.request(r)
 print(r.response)
 for i in range(0, 10):
  x= next(r.response);
  if (x['type'] == 'PRICE'):
   ask =float(x['asks'][0]['price'])
   bid =float(x['bids'][0]['price'])
   print (bid,ask); break
  else: print ('cant get price') 
 return ask,bid     

def buy_market_order(num=9, sl=9, tk=10,tsl=9,res=10000, inst='EUR_USD'):
  ask,bid = get_current_price()
  EUR_USD_STOP_LOSS = sl
  EUR_USD_TAKE_PROFIT = tk
  EUR_USD_TRAILING_STOP_LOSS=tsl
  if (EUR_USD_STOP_LOSS)!= None:
    stopLossOnFill=StopLossDetails(price=EUR_USD_STOP_LOSS).data
  else:
    stopLossOnFill=None
  if (EUR_USD_TAKE_PROFIT) != None:
    takeProfitOnFill=TakeProfitDetails(price=EUR_USD_TAKE_PROFIT).data
  else:
    takeProfitOnFill=None
  if (EUR_USD_TRAILING_STOP_LOSS) != None:
    trailingStopLossOnFill=TakeProfitDetails(price=EUR_USD_TRAILING_STOP_LOSS).data
    print(trailingStopLossOnFill)
  else:
    trailingStopLossOnFill=None
  mktOrder = MarketOrderRequest(
    instrument=inst,
    units=num,
    takeProfitOnFill=takeProfitOnFill,
    stopLossOnFill=stopLossOnFill,
    trailingStopLossOnFill = trailingStopLossOnFill)


  print("Market Order specs: \n{}".format(json.dumps(mktOrder.data, indent=4)))
# create the OrderCreate request
  r = orders.OrderCreate(accountID, data=mktOrder.data)
  try:
    # create the OrderCreate request
    rv = api.request(r)
  except V20Error as err:
    print(r.status_code, err)
  else:
    print(json.dumps(rv, indent=2))
    if 'orderFillTransaction' in rv.keys() and 'orderCancelTransaction' not in rv.keys():
      return 1



def place_market_order(name='sell', num=9, sl=9, tk=10,res=10000, inst='EUR_USD'):
 ask,bid = get_current_price(); 
 if (name=='buy'):
  EUR_USD_STOP_LOSS = ask-(1/res)*sl
  EUR_USD_TAKE_PROFIT = ask+(1/res)*tk
 if (name=='sell'):
  EUR_USD_STOP_LOSS = bid+(1/res)*sl
  EUR_USD_TAKE_PROFIT = bid-(1/res)*tk
  num=0-num
 print (EUR_USD_TAKE_PROFIT, EUR_USD_STOP_LOSS); #sys.exit(0); 
# The orderspecs
# The orderspecs
 mktOrder = MarketOrderRequest(
    instrument=inst,
    units=num,
    takeProfitOnFill=TakeProfitDetails(price=EUR_USD_TAKE_PROFIT).data,
    stopLossOnFill=StopLossDetails(price=EUR_USD_STOP_LOSS).data)

 print("Market Order specs: \n{}".format(json.dumps(mktOrder.data, indent=4)))

# create the OrderCreate request
 r = orders.OrderCreate(accountID, data=mktOrder.data)

 try:
    # create the OrderCreate request
    rv = api.request(r)
 except V20Error as err:
    print(r.status_code, err)
 else:
    print(json.dumps(rv, indent=2))
#Successfully retrieving all the trade details of open trades.
#Also successfully placing in the trade bar.
def get_open_trades():
  global tradeID
  r = trades.OpenTrades(accountID)
  x=api.request(r)
  print(x)
  tp=None;sl=None;ts=None;currentUnits=0;instrument=0;price=0;tradeID=0;Type="";realizedpl="";unrealizedpl="";
  #number of elements in list/ trades placed
  tradenos=(len(x['trades']))
  print (tradenos)
  price_array = np.zeros((tradenos,10),dtype = 'object');
  #loop to retrieve all values of trade
  for counter in range (0,tradenos):
    print(counter)
    tp="";sl="";ts="";currentUnits=0;instrument=0;price=0;tradeID=0
    instrument=(x['trades'][counter]['instrument'])
    price=(x['trades'][counter]['price'])
    currentUnits=(x['trades'][counter]['currentUnits'])
    realizedpl=(x['trades'][counter]['realizedPL'])
    unrealizedpl=(x['trades'][counter]['unrealizedPL'])
    if int(currentUnits) < 0:
      Type="Short"
      currentUnits=abs(int(currentUnits))
    else:
      Type="Long"
    tradeID=(x['trades'][counter]['id'])
    if 'takeProfitOrder' in x['trades'][counter].keys():
      tp=(x['trades'][counter]['takeProfitOrder']['price'])
    if 'stopLossOrder' in x['trades'][counter].keys():
      sl=(x['trades'][counter]['stopLossOrder']['price'])
    if 'trailingStopLossOrder' in x['trades'][counter].keys():
      ts=(x['trades'][counter]['trailingStopLossOrder']['trailingStopValue'])
    price_array[counter][0] = tradeID;price_array[counter][1] = instrument; price_array[counter][2] = currentUnits; 
    price_array[counter][3] = Type; price_array[counter][4] = sl; price_array[counter][5] = tp;
    price_array[counter][6] = ts;  price_array[counter][7] = price;  price_array[counter][8] = realizedpl;
    price_array[counter][9] = unrealizedpl;
    print(tradeID,"  ",instrument ,"  ",currentUnits," ",tp,"  ",sl,"   ",ts," ",price)
  print (price_array);
  return price_array,tradenos
 #Currently not working 
 #I could not find any api methods like MarketOrderRequest() to change takeProfitOnFill and stopLossOnFill
 # into specified format required for crcdo
 
def get_account_summary():
  r = accounts.AccountSummary(accountID = accountID)
  x=api.request(r)
  print (x)
  balance= x['account']['balance']
  marginused=x['account']['marginUsed']
  unrealizedPL=x['account']['unrealizedPL']
  print(balance," ", marginused ," ", unrealizedPL)
  return balance,marginused,unrealizedPL


def change_trade(tradeID,tp,sl):
  tp=str(tp)
  sl=str(sl)
  data={"takeProfit": {"timeInForce": "GTC","price":tp},"stopLoss": {"timeInForce": "GTC","price":sl}}
  r = trades.TradeCRCDO(accountID=accountID,
                     tradeID=tradeID,
                       data=data)
  try:
    x=api.request(r)
  except V20Error as err:
    print(r.status_code, err)
  else:
    print (x)
    if 'takeProfitOrderCancelTransaction' in x.keys() and 'errorCode' not in x.keys():
      return 1 


#Successfully closes a open trade
def close_trade(tradeID):
  r=trades.TradeClose(accountID, tradeID, data=None)
  try:
    x=api.request(r)
  except V20Error as err:
    print(r.status_code, err)
  else:
    print (x)

def get_trade_details():
  td=trades.TradeDetails(accountID, tradeID)
  x=api.request(td)
  print(x)

def get_order_list():
  ra = orders.OrderList(accountID)
  x = api.request(ra);
  print (x);

def time_to_rcff(timestr):
  x = timestr.split(' ')
  y = x[1].split(':')
  seconds = y[2].split('-'); 
  seconds = str(round(float(seconds[0])));
  tim = str(y[0]) + ':' + str(y[1]) + ':'+ seconds;
  tim = str(tim)
  rcff = str(x[0]+'T'+tim);
  return rcff

def past_rcff_time(timestr, days=2, hours=0, mins=0):
  x = timestr.split('T'); dat = x[0]; tim = x[1];
  dat = dat.split('-'); tim = tim.split(':');
  year = (dat[0]); month = int(dat[1]); day = int(dat[2]) - days; 
  if (day < 1): day = 30; month = month -1;
  day = str(day); month = str(month)
  hour = int(tim[0]) - hours; 
  if (hour < 0): hour = 0;
  hour = str(hour)
  mint = int(tim[1]) - mins;
  if (mint < 0): mint = 0;
  mint = str(mint) 
  if (int(month) < 1):month = str(12); year = str(int(year)-1)
  final = str(year+'-'+month+'-'+day+'T'+hour+':'+mint+':00')
  return final;

def past_rcff_time2(timestr, counts=2, mode='d'):
  x = timestr.split('T'); dat = x[0]; tim = x[1];
  dat = dat.split('-'); tim = tim.split(':');
  year = (dat[0]); month = int(dat[1]); day = int(dat[2])
  hour = int(tim[0]); mint = int(tim[1]);
  if mode=='d':
   day = day - counts; 
   if (day < 1): day = 30; month = month -1;
   if (int(month) < 1):month = str(12); year = str(int(year)-1)
  if mode=='h':
   hour = hour - counts; 
   if (hour < 0): hour = 23; day = day -1;
   if ((day < 1 ) and (int(month)-1 == 2)): day = 28; month = month -1;
   if ((day < 1 ) and (int(month)-1 != 2)): day = 30; month = month -1;
   if (int(month) < 1):month = 12; year = str(int(year)-1)
  final = str(str(year)+'-'+str(month)+'-'+str(day)+'T'+str(hour)+':'+str(mint)+':00')
  return final


def build_base_dataset(instrument, counts=1000, starttime = 'UTC NOW'):
 rprice = []; len_count = 0; 
 time_now = time_to_rcff(str(datetime.datetime.now(tz=pytz.timezone('US/Eastern'))));
 while (1):
  prev_time = past_rcff_time2(time_now,8,'h'); 
  print (time_now);print (prev_time); #input("ok")
  r = instruments.InstrumentsCandles(instrument=instrument, params={"from":str(prev_time),"to":str(time_now),"granularity":"M2","includeFirst": "True"})
  x = api.request(r); rprice.append(x['candles']);
  len_count= len_count + len(x['candles']); print (len_count);#sys.exit(0)
  if (len_count > counts): break 
  else: time_now = copy.deepcopy(prev_time);
 print (rprice[0][-1]['complete']);
 if ((rprice[0][-1]['complete']) == False): 
  print (rprice[0][-1]['time']); time_stamp = rprice[0][-1]['time'];rprice[0].pop(); len_count = len_count -1;
 else: time_stamp = rprice[0][-1]['time']
 print (len_count) 
 price_array = np.zeros((len_count,4)); countz =0;
 for i in range(len(rprice)-1, -1,-1):
  for j in range(0, len(rprice[i])):
   price_array[countz][0] = rprice[i][j]['mid']['o']; price_array[countz][1] = rprice[i][j]['mid']['h']; 
   price_array[countz][2] = rprice[i][j]['mid']['l']; price_array[countz][3] = rprice[i][j]['mid']['c']; 
   countz = countz+1; 
 print (price_array); 
 return price_array,time_stamp

def update_dataset(prevz_time, instrument='USD_INR'): 
 timez_now = time_to_rcff(str(datetime.datetime.now(tz=pytz.timezone('US/Eastern'))));    
 time_now = timez_now.split('T');
 # min_temp = (time_now[1].split(':')); min_now = int(min_temp[1]); sec_now = (min_temp[2]).split('.'); sec_now = int(sec_now[0]);
 # time_now = prev_time.split('T');
 # min_temp = (time_now[1].split(':')); min_prev = int(min_temp[1]); sec_prev = (min_temp[2]).split('.'); sec_prev = int(sec_prev[0]);
 #print (min_now, sec_now, min_prev,sec_prev);
 time_stamp = []; print (prevz_time, timez_now); print ("ok");
 r = instruments.InstrumentsCandles(instrument=instrument, params={"from":str(prevz_time),"to":str(timez_now),"granularity":"M2","includeFirst":"True"})
 try:
  x = api.request(r); price = x['candles']; print (x); 
  new = np.zeros((len(price),4)); tf = np.zeros(len(price),dtype=bool);
  for i in range(0, len(price)): 
   new[i][0] = price[i]['mid']['o'];new[i][1] = price[i]['mid']['h']
   new[i][2] = price[i]['mid']['l'];new[i][3] = price[i]['mid']['c']; tf[i] = price[i]['complete']
   time_stamp.append(x['candles'][i]['time']); 
  return new, time_stamp,tf
 except: return [],[],[]


def check_and_print (prev_tim, now_tim_arr, now_price):
 for i in range(0 , len(now_tim_arr)):
  if (now_tim_arr[i] == prev_tim): now_price = np.delete(now_price, (i), axis=0); 
 print (now_price, prev_tim, now_tim_arr); #input('ok')
 if (len(now_price) != 0): 
  f = open(FILESTORE, 'a'); f2 = open('ready','w'); f2.write('ok\n'); f2.write(str(prev_tim)); f2.write('\n')
  for i in range (0, len(now_price)):
   f.write("%s %s %s %s" % (str(now_price[i][0]),str(now_price[i][1]),str(now_price[i][2]),str(now_price[i][3]))); f.write('\n');
   f2.write("%s %s %s %s" % (str(now_price[i][0]),str(now_price[i][1]),str(now_price[i][2]),str(now_price[i][3]))); f2.write('\n');
  f.close(); f2.write('now_read') ;f2.close();         
  return 1, now_price
 else: return 0, now_price 

def check_and_print (prev_tim, now_tim_arr, now_price, comp_arr):
 false_time = []; 
 for i in range(0 , len(comp_arr)):
  if (comp_arr[i] == False):  now_price = np.delete(now_price, (i), axis=0); false_time.append(now_tim_arr[i]);
 #print (false_time); input("ok") 
 if (len(now_price) != 0):  
  f = open(FILESTORE, 'a'); f2 = open('ready','w'); f2.write('ok\n'); f2.write(str(prev_tim)); f2.write('\n')
  for i in range (0, len(now_price)):
   f.write("%s %s %s %s" % (str(now_price[i][0]),str(now_price[i][1]),str(now_price[i][2]),str(now_price[i][3]))); f.write('\n');
   f2.write("%s %s %s %s" % (str(now_price[i][0]),str(now_price[i][1]),str(now_price[i][2]),str(now_price[i][3]))); f2.write('\n');
  f.close(); f2.write('now_read') ;f2.close();  
  if (len(false_time)== 0): false_time.append(now_tim_arr[-1]);       
  return 1, now_price,false_time[0]
 else: return 0, now_price,0


def signal_handler(signal, frame):
 print('You pressed Ctrl+C!'); global interrupted; interrupted = 'True';
 
def convert_time_stamp(t):
  t = parse(t);convtime = t.astimezone(pytz.timezone('US/Eastern'))
  convtime = str(convtime);
  convtime = convtime.split(' '); convtime = convtime[0]+'T'+(convtime[1].split('-')[0]);
  return convtime

def write_base_set_and_get_time(p,t):
 f = open(FILESTORE,'w'); 
 for i in range(0, len(p)):
  f.write("%s %s %s %s" % (str(p[i][0]),str(p[i][1]),str(p[i][2]),str(p[i][3]))); f.write('\n');
 f.close(); 
 latest_time = t; 
 latest_ny_time = convert_time_stamp(t); 
 return latest_ny_time, latest_time
# p,t = build_base_dataset('EUR_USD',3000); 
# f = open(FILESTORE,'w');
# for i in range(0, len(p)):
#  f.write("%s %s %s %s" % (str(p[i][0]),str(p[i][1]),str(p[i][2]),str(p[i][3]))); f.write('\n');
# f.close(); 
# latest_time = t; 
# latest_ny_time = convert_time_stamp(t); 

# while(1): 
#  signal.signal(signal.SIGINT, signal_handler); 
#  if (interrupted == 'True'): break;
#  x,t2 = update_dataset(latest_ny_time, 'EUR_USD'); 
#  if (check_and_print (latest_time, t2, x) == 1): 
#   latest_time = t2[-1]; latest_ny_time = convert_time_stamp(latest_time); print ("updated"); #input("press enter")
# time_now = str(datetime.utcnow());
# print(time_to_rcff(time_now));
# r = instruments.InstrumentsCandles(instrument="USD_INR", params={"from":"2018-06-01T03:43:00","to":"2018-06-04T03:48:00","granularity":"M1","alignmentTimezone":"UTC"})#params={"from": "2018-05-30T02:00:00.0","to": "2018-05-30T03:00:00.0","granularity": "M1"})
# #r = PricingStream(accountID=accountID,params=inz)                          
# x = api.request(r)
# print (x);
# price_array = [];
# for i in range(0, len(x['candles'])):
#  temp = [];
#  h = float(x['candles'][i]['mid']['h'])
#  l= float(x['candles'][i]['mid']['l'])
#  o = float(x['candles'][i]['mid']['o'])
#  c = float(x['candles'][i]['mid']['c'])
#  temp.append(o); temp.append(h); temp.append(l); temp.append(c)
#  price_array.append(temp);
# print (np.shape(price_array))
# price_array = np.asarray(price_array)
# print (price_array[:,3])
# sys.exit(0);

#place_market_order('sell',10, 100, 100,1000,'USD_INR')
#get_current_price();
#get_order_list();

#