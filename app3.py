import os
import urllib.parse 
from flask import Flask, jsonify,request,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
import pytz
import time
import redis
import pickle


import pyodbc
app = Flask(__name__, template_folder='template')
server = 's6618.database.windows.net'
database = 'db6618'
username = 'sxv6618'
password = 'Shravs@23!'
driver= '{ODBC Driver 18 for SQL Server}' # You may need to change this depending on your system

conn_str = f"""DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};
              UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;
              Connection Timeout=30;"""
r = redis.StrictRedis(host='SXV6618.redis.cache.windows.net',
        port=6380, db=0, password='KPYmLQXBFdUarTkusWc8xxdFidBSWmA5nAzCaBcJfCU=', ssl=True)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
@app.route('/')
def users():
    
    return render_template('index.html')
@app.route('/r0', methods=['POST'])
def r0():
  
   no_of_queries=int(request.form['no_of_queries'])
   total_time=0
   for i in range (no_of_queries):
      t1=time.time()
      
      query= f"SELECT * FROM all_month where mag<=6"
      cursor.execute(query).fetchall()
      t2=time.time()
      t=t2-t1
      
      total_time+=t
   avg_time=total_time/no_of_queries
   x0= "average time to excute no cache and no restriction "+ str(no_of_queries)+" Queries is :"+str(avg_time)
   return render_template('r0.html',x0=x0)
@app.route('/r1', methods=['POST'])
def r1():
   magni = float(request.form['magni'])
   no_of_queries=int(request.form['no_of_queries'])
   total_time=0
   for i in range (no_of_queries):
      t1=time.time()
      
      query= f"SELECT * FROM all_month where mag>{magni}"
      cursor.execute(query).fetchall()
      t2=time.time()
      t=t2-t1
      
      total_time+=t
   avg_time=total_time/no_of_queries
   x= "average time to excute no cache and with restriction"+ str(no_of_queries)+" Queries is :"+str(avg_time)
   return render_template('r1.html',x=x)
@app.route('/r_cache', methods=['POST'])
def r_cache():
   
   no_of_queries=int(request.form['no_of_queries'])
   total_time=0
   for i in range (no_of_queries):
      t1=time.time()
      
      
      query= f"SELECT *  FROM all_month where mag<=6"
      cache_query(query)
      t2=time.time()
      
      t=t2-t1
      
      total_time+=t
   avg_time=total_time/no_of_queries
   x1= "average time to excute cache and no restriction "+ str(no_of_queries)+"  Queries is :"+str(avg_time)
   return render_template('r_cache.html',x1=x1)
@app.route('/r_cache1', methods=['POST'])
def r_cache1():
   magni = float(request.form['magni'])
   no_of_queries=int(request.form['no_of_queries'])
   total_time=0
   for i in range (no_of_queries):
      t1=time.time()
   
      
      query= f"SELECT *  FROM all_month where mag<=6"
      cache_query(query)
      t2=time.time()
      
      t=t2-t1
      
      total_time+=t
   avg_time=total_time/no_of_queries
   x01= "average time to excute cache and with restriction"+ str(no_of_queries)+" Queries is :"+str(avg_time)
   return render_template('r_cache1.html',x01=x01)
def cache_query(Query):
   #we are checking where the query is cached or not
   Check_cached=r.get(Query)
   #print(Check_cached)
   #this will return none or value for the key
   if Check_cached is not None:
      
      return Check_cached
   else:
      print("not cached")
      cacheTheQuery=  cursor.execute(Query).fetchall()
      
      data_str = pickle.dumps(cacheTheQuery)
      r.set(Query,data_str )
      return(data_str)
      
if __name__ == '__main__':
    app.run(debug=True)

 




