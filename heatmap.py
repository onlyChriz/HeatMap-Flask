import datetime

from flask import render_template, request, Blueprint, current_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from map_funcs import Map_obj

from db_connection import db_connection
from db_con import db_con

from models.model import City, Coordinate



app = current_app
main = Blueprint('main', __name__)

#instanziate a db
database = db_connection(db_con())

engine = create_engine(database.connection_string)
Session = sessionmaker(bind=engine)
db_session = Session()

all_cities = db_session.query(City).order_by(City.city).all()
list_of_labels = ["3 dagar", "1 dag", "60 min", "30 min", "10 min"]

    

def get_time(time):
    #set the correct date to the query
    time_span = [3, 1, 1, 30, 10]
    current_time = datetime.datetime.utcnow()
              
    if time == 0:
        current_time -= datetime.timedelta(days=time_span[time])
    if time == 1:
        current_time -= datetime.timedelta(days=time_span[time])
    if time == 2:
        current_time -= datetime.timedelta(hours=time_span[time])
    if time == 3:
        current_time -= datetime.timedelta(minutes=time_span[time])
    if time == 4:
        current_time -= datetime.timedelta(minutes=time_span[time])
    return current_time


@main.route('/', methods=['GET', 'POST'])
def home():
    global all_cities
    map_o = Map_obj()

    coordinates = []
    
    #gets the value from dropdown
    selected_city = request.args.get('kommun') or request.form.get('kommun') or all_cities[0].city

    if request.method == 'GET':
        #Will be loaded the first time. A start of the browser is a GET!
        map_o.get_map()
        map_o.render_map()
        
        return render_template('index.html', map=map_o.map, Sverige='Sverige', time='', all_cities=all_cities,selected_time='0', label_value=list_of_labels[0], current_time='')
    
    if request.method == 'POST':
        
        if 'Hämta' in request.form: 
            #will be called when the user presses the submit/'Hämta' button       
            city = request.form['kommun']
            time = int(request.form.get('time'))
            current_time =get_time(time)

            #Gets the city from db
            choosen_city = db_session.query(City).filter_by(city=city).first()
            
            if choosen_city:
                #making an object of colleceted values from sql
                city_id = choosen_city.city_id
                coordinates = db_session.query(Coordinate).filter(
                    Coordinate.city_id == city_id,
                    Coordinate.datetime >= current_time
                ).all()
                       
                map_o.get_mask_layer(city)# Get the selected value from the dropdown
                map_o.get_map()
                list_coords = map_o.get_heatmap(coordinates, city) 
                map_o.render_map()
        
        return render_template('index.html', map=map_o.map, all_cities=all_cities, list_coords=list_coords,
                               selected=selected_city, Sverige=selected_city, selected_time=time, label_value=list_of_labels[time])
    else:
        
        return render_template('index.html', map=map_o.map, all_cities=all_cities,selected_time='0', label_value=list_of_labels[0])
    
@main.route('/norway', methods=['GET', 'POST'])
def norway():
    from datetime import datetime
    global all_cities
    database = db_connection(db_con())
    engine = create_engine(database.connection_string)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    map_o = Map_obj()
    
    coordinates = []
    if request.method == 'GET':
        map_o.get_norway_road()
        map_o.render_map() 

    
        return render_template('norway.html', map=map_o.map)
    
     #Implementera felmeddelande om det inte finns någon tid.
    if request.method == 'POST':        
            map_o.get_norway_road()

            from datetime import datetime


            date = '2023-11-17'

            start_time = request.form['from_time']
            end_time = request.form['to_time']

            start_datetime_str = f'{date} {start_time}'
            end_datetime_str = f'{date} {end_time}'
            
            start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M')
            end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M')



            coordinates = db_session.query(Coordinate).filter(Coordinate.datetime.between(start_datetime, end_datetime)).all()

            list_coords = map_o.get_heatmap(coordinates, "Väg 80")
            
        
            map_o.render_map()
            return render_template("norway.html", map=map_o.map, from_time=start_time, to_time=end_time)
         
@main.route('/customer/<city_id>', methods=['GET', 'POST'])
def customer(city_id):
    global all_cities
    map_o = Map_obj()
    coordinates = []
    
    selected_city = request.args.get('kommun') or request.form.get('kommun') or all_cities[0].city

    choosen_city = db_session.query(City).filter_by(city_id=city_id).first()
  
    if choosen_city is None:
        return render_template('error.html')   
            
    if request.method == 'GET':
        map_o.get_mask_layer(choosen_city.city)
        map_o.get_map()
        #map_o.add_layer_control(map)
        
        map_o.render_map()
        return render_template("customer.html", map=map_o.map, choosen_city=choosen_city, selected_time='0', label_value=list_of_labels[0])
    
    if request.method == 'POST':
            
        city = request.form['kommun']
        time = int(request.form.get('time'))
        current_time = get_time(time)
        
        map_o.get_mask_layer(city)# Get the selected value from the dropdown
        map_o.get_map()
        map_o.render_map()
            
        if choosen_city:
            city_id = choosen_city.city_id
            coordinates = db_session.query(Coordinate).filter(
                Coordinate.city_id == city_id,
                Coordinate.datetime >= current_time
            ).all()
            map_o.get_mask_layer(city)# Get the selected value from the dropdown
            map_o.get_map()
            list_coords = map_o.get_heatmap(coordinates, city) 
            map_o.render_map()    
            
        return render_template('customer.html', map=map_o.map, choosen_city=choosen_city, list_coords=list_coords,
                               selected=selected_city, selected_time=time, label_value=list_of_labels[time])
    
    else:
        map_o.get_map()
        map_o.render_map() 
        return render_template('customer.html', map=map_o, choosen_city=choosen_city,selected_time='0', label_value=list_of_labels[0])
     