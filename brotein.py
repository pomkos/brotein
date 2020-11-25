import streamlit as st

st.title("Let's Compare Proteins Bro")

class saveInfo():
    def __init__(self, row_info=0):
        '''
        Initialize the sqlite database
        
        input
        -----
        row_info: dict
        '''
        import sqlalchemy as sq
        import datetime as dt
        from pytz import timezone 

        # initialize engine
        engine = sq.create_engine('sqlite:///brotein.db')
        meta = sq.MetaData()
        # table format in db
        self.brotein = sq.Table(
           'brotein', meta, 
           sq.Column('id', sq.Integer, primary_key = True), 
           sq.Column('brand', sq.String), 
           sq.Column('cost_per_20g', sq.Float),
           sq.Column('price',sq.Float),
           sq.Column('g_per_scoop',sq.Float),
           sq.Column('servings_in_bag',sq.Float),
           sq.Column('date_added',sq.DateTime),
        )

        # format data into proper list of dictionaries
        tz = timezone('US/Eastern')
        row_info['date_added'] = dt.datetime.now(tz)
        self.row = row_info
        meta.create_all(engine) # not sure why its needed, but its in the tutorial so ... :shrug:
        self.engine = engine
        
    def save_table(self):
        '''
        Saves information to database
        '''
        import datetime as dt
        
        conn = self.engine.connect()
        result = conn.execute(self.brotein.insert(), self.row)
        
def brotein(price, protein_scoop_g, servings, name_str):
    '''
    Standardizes price of whey
    
    price: In dollars, for package
    protein_scoop_g: grams of protein per scoop
    servings: number of servings per package
    name_str: name of whey
    '''
    st_cost = round((price/(protein_scoop_g * servings))*20,2)
    bro_dict = {
        'brand':name_str,
        'cost_per_20g': st_cost,
        'price':price,
        'g_per_scoop':protein_scoop_g,
        'servings_in_bag':servings,
    }

    statement = f'''{bro_dict['brand']} is ${bro_dict['cost_per_20g']} per 20g protein. Saved in brotein database.'''   
    return bro_dict, statement

name_str = st.text_input(label='Brand name')

col_price, col_pro, col_serv = st.beta_columns(3)

with col_price:
    price = st.number_input(label='Price in dollars')
with col_pro:
    protein_scoop_g = st.number_input(label='Grams per scoop')
with col_serv:
    servings = st.number_input(label='Scoops per bag')

try:
    bro_dict,statement = brotein(name_str=name_str, price=price, protein_scoop_g=protein_scoop_g, servings=servings)
    statement
except:
    ''
submit = st.button(label='Submit')

if submit == True:
    save = saveInfo(row_info=bro_dict)
    save.save_table()

import pandas as pd
import sqlalchemy as sq
engine = sq.create_engine('sqlite:///brotein.db')
df = pd.read_sql_table('brotein',engine,parse_dates='date_added')
df = df.iloc[:,1:]
df = df.sort_values('cost_per_20g')
df
