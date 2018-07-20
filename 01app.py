import requests
import pusher
import json
from flask import Flask, render_template,jsonify,request
from snownlp import normal
from snownlp import seg
from snownlp.summary import textrank
from snownlp.sim import bm25
import math
import os
app=Flask(__name__)

pusher_client = pusher.Pusher(
  app_id='***',
  key='your_pusher_key',
  secret='***',
  cluster='ap1',
  ssl=True
)

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/message',methods =["POST"])
def message():
    #url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=***'
    url='http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=***'
    #city='Taipei'
    #r=requests.get(url.format(city)).json()
    try:
        doc2=[]
        with open('mybot.json', encoding='utf-8') as fh:
            data=json.load(fh)
        for i in range(5):
            doc2.append(data['List'][i]["question"])
        yee=bm25.BM25(doc2)
        yee.f
        yee.idf
        #username=request.form.get('username')
        username='機器人'
        message=request.form.get('message')
        #pusher_client.trigger('chat-channel', 'new-message', {'username':username,'message': message+message})
        if(message=='Hi'):
            pusher_client.trigger('chat-channel', 'new-message', {'username':username,'message': 'Hello'})
        if(message=='你好'):
            pusher_client.trigger('chat-channel', 'new-message', {'username':username,'message': '大家好'})
        if message.startswith('@'):
            message=message[1:]
            x=yee.simall(message)
            print(max(x))
            print('Answer:',end="")
            print(data['List'][x.index(max(x))]["answer"])
            youranswer=data['List'][x.index(max(x))]["answer"]
            pusher_client.trigger('chat-channel', 'new-message', {'username':username,'message':youranswer })
        if message.startswith('Weather'):
            message=message[8:]
            print(message)
            city=message
            r=requests.get(url.format(city)).json()
            #print(city,end ='')
            #print('現在的溫度是:', end ='')
            #print(r['main']['temp'],end='')
            #print('度')
            #print(r)
            #print( city+'現在的溫度是'+str(r['main']['temp'])+'度')
            print(json.dumps(r, indent=4))
            print('---------------------------')
            #print(r['list'][0]['dt_txt'])#小時預報
            yee1='時間:'+str(r['list'][3]['dt_txt'])+','+'氣溫:'+str(r['list'][3]['main']['temp'])+', 天氣狀況:'+str(r['list'][3]['weather'][0]['main'])+', '+str(r['list'][3]['weather'][0]['description'])
            print(yee1)
            yee2='時間:'+str(r['list'][4]['dt_txt'])+','+'氣溫:'+str(r['list'][4]['main']['temp'])+', 天氣狀況:'+str(r['list'][4]['weather'][0]['main'])+', '+str(r['list'][4]['weather'][0]['description'])
            print(yee2)
            pusher_client.trigger('chat-channel', 'new-message', {'username':username,'message':city+'的天氣預報:'})
            pusher_client.trigger('chat-channel', 'new-message', {'username':username,'message':yee1})
            pusher_client.trigger('chat-channel', 'new-message', {'username':username,'message':yee2})  
        print(username)
        print(message)
        
        return jsonify({'result':'success'})

    except:
        return jsonify({'result':'failure'})

if __name__=='__main__':
    app.run(debug=True)



