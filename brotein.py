import streamlit as st
import sys

us_pw = sys.argv[1]
db_ip = sys.argv[2]
port = sys.argv[3]

class saveInfo():
    def __init__(self, kind, row_info=0,show=False):
        '''
        Initialize the sqlite database

        input
        -----
        kind: str
            Information category: "bar" or "powder"
        row_info: dict
        show: bool
            Whether to show the specified table from db
        '''
        import sqlalchemy as sq
        import datetime as dt
        from pytz import timezone 
        import os

        # initialize engine
        #parent = os.path.dirname(os.getcwd()) # get parent of current directory
        engine = sq.create_engine(f'postgres://{us_pw}@{db_ip}:{port}')
        meta = sq.MetaData()
        tz = timezone('US/Eastern')

        if kind =='powder':
            self.db_table = "brotein_powder"
        elif kind == 'bar':
            self.db_table="brotein_snack"
        db_table = self.db_table
        self.kind = kind
        if (kind == "powder") & (show==False):
            # table format in db
            row_info['date_added'] = dt.datetime.now(tz)
            self.brotein = sq.Table(
               db_table, meta, 
               sq.Column('id', sq.Integer, primary_key = True), 
               sq.Column('brand', sq.String), 
               sq.Column('protein_per_100kc', sq.Float),
               sq.Column('price_per_20g', sq.Float),
               sq.Column('price',sq.Float),
               sq.Column('g_per_scoop',sq.Float),
               sq.Column('cal_per_scoop',sq.Float),
               sq.Column('servings_in_bag',sq.Float),
               sq.Column('date_added',sq.DateTime),
            )

        elif (kind == "bar") & (show==False):
            row_info['date_added'] = dt.datetime.now(tz)
            self.brotein = sq.Table(
                db_table, meta, 
                sq.Column('id', sq.Integer, primary_key = True), 
                sq.Column('brand', sq.String), 
                sq.Column('price_per_serving', sq.Float),
                sq.Column('protein_per_100kc',sq.Float),
                sq.Column('price_per_20g', sq.Float),
                sq.Column('servings',sq.Float),
                sq.Column('carbs',sq.Float),
                sq.Column('fats',sq.Float),
                sq.Column('protein',sq.Float),
                sq.Column('calories',sq.Float),
                sq.Column('price',sq.Float),
                sq.Column('date_added',sq.DateTime),
            )
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

    def show_table(self, sort_by = None, highlight_in = None):
        import pandas as pd
        df_og = pd.read_sql_table(self.db_table,self.engine,parse_dates='date_added')
        df_og = df_og.drop('id',axis=1)

        df = table_formatter(df_og,self.kind)

        if type(sort_by)==str:
            df = df.sort_values(sort_by)

#         if highlight_in != None:
#             if (self.kind == 'bar') & (highlight_in == 'Protein per 100 calories'):
#                 df['Protein per 100 calories'] = df['Protein per 100 calories'].astype(float)
#                 df = df.style.highlight_min(subset=highlight_in,color='#f7f123')
#             else:
#                 df = df.style.highlight_max(subset=highlight_in,color='#f7ff99')

        return df

def start(button=None):
    '''
    Main app. Creates the GUI and gathers basic info.
    '''
    if type(button)==str:
        pass
    st.title("Never get scammed by Big Bro again!")

    analysis = st.select_slider("",['Brotein Powder','Brotein Snack'])
    
    if analysis == 'Brotein Powder':

        ### Whey Layout ###
        st.write("## Let's compare wheys bro!")
        
        with st.beta_expander('Click me to calculate something', expanded=False):
            col_pro_name, col_pro_price = st.beta_columns(2)
            with col_pro_name:
                whey_brand = st.text_input(label='Brand name', key='brand_whey',)
            with col_pro_price:
                price = st.number_input(label='Price ($)*',step=10.0)    

            col_serv, col_cal, col_pro = st.beta_columns(3)
            with col_cal:
                cal_per_scoop = st.number_input(label='Calories per scoop*',step=10.0)
            with col_serv:
                servings = st.number_input(label='Scoops per bag*',step=10.0)
            with col_pro:
                protein_scoop_g = st.number_input(label='Protein per scoop (g)*',step=10.0)
            submit = st.button(label='Submit',key='submit_powder')

            try:
                bropow_dict = {
                    'brand':whey_brand,
                    'price':price,
                    'g_per_scoop':protein_scoop_g,
                    'servings_in_bag':servings,
                    'cal_per_scoop':cal_per_scoop
                }
                bro_dict,statement = brotein(bropow_dict,kind='powder')
                st.info(statement)
                if submit == True:
                    submit_info(row_info = bro_dict,kind='powder')
            except:
                st.warning('Not enough info to calculate')
                st.warning('NOTE: Some whey proteins have 2 scoops per serving of protein. Make sure to divide by two.')
        show = saveInfo(kind='powder',show=True)
        df_powder = show.show_table(sort_by='Price of 20g Protein',highlight_in='Price of 20g Protein')
        st.table(df_powder)

    else:
        ### Protein Snacks Comparison ###
        st.write("## Let's compare snacks bro!")
        with st.beta_expander('Click me to calculate something', expanded=False):
            ### Layout ###
            col_name, col_price,col_serv = st.beta_columns(3)
            with col_name:
                bar_brand = st.text_input(label = 'Brand name', key='brand_bar',)
            with col_price:
                bar_price = st.number_input(label='Price ($)*', min_value=0.0, step=10.0,)
            with col_serv:
                servings = st.number_input(label='Servings (bars/box)*',min_value=0.0,step=1.0,)        

            col_cal,col_fat,col_cho,col_aa = st.beta_columns(4)
            with col_cal:
                calories = st.number_input(label='Calories*',min_value=0.0,step=10.0)
            with col_fat:
                fat_g = st.number_input(label='Fats (g)',min_value=0.0,step=10.0,)
            with col_cho:
                cho_g = st.number_input(label='Carbohydrates (g)',min_value=0.0,step=10.0,)
            with col_aa:
                pro_g = st.number_input(label='Protein (g)*',min_value=0.0,step=10.0,)

            try:
                ### Calculate ###
                brobar_dict = {
                    'brand':bar_brand,
                    'price':bar_price,
                    'servings':servings,
                    'calories':calories,
                    'carbs':cho_g,
                    'fats':fat_g,
                    'protein':pro_g
                }
                bar_dict, statement = brotein(brobar_dict, kind='bar')
                st.info(statement)
                submit = st.button(label='Submit',key='submit_snack')
                if submit == True:
                    submit_info(row_info=bar_dict, kind='bar')          
            except:
                st.warning('Not enough info to calculate')
        ### Show Database ###
        show = saveInfo(kind='bar',show=True)
        df_bar = show.show_table(highlight_in='Protein per 100 calories')
        st.table(df_bar)
    st.warning('NOTE: At least 10g of protein per 100 calories recommended if cutting.')
    
def brotein(my_dict, kind):
    '''
    Calculates a standardized price of whey (per 20g protein)

    price: In dollars, for package
    protein_scoop_g: grams of protein per scoop
    servings: number of servings per package
    name_str: name of whey
    '''
    if my_dict['price'] == 0.0:
        raise 'Dev Zero'
    if kind == 'powder':
        st_cost = round((my_dict['price']/(my_dict['g_per_scoop'] * my_dict['servings_in_bag']))*20,2)
        protein_cal = round((my_dict['g_per_scoop']/my_dict['cal_per_scoop'])*100,2)

        my_dict['protein_per_100kc'] = protein_cal
        my_dict['price_per_20g'] = st_cost

        statement = f'''{my_dict['brand']} has {my_dict['protein_per_100kc']}g protein per 100 calories, and is ${my_dict['price_per_20g']} per 20g protein.'''

    elif kind == 'bar':
        bar_cost = round((my_dict['price']/my_dict['servings']),2)
        aa_cost = round((bar_cost/my_dict['protein'])*20,2)
        protein_cal = round((my_dict['protein']/my_dict['calories'])*100,2)
        my_dict['price_per_serving'] = bar_cost
        my_dict['price_per_20g'] = aa_cost
        my_dict['protein_per_100kc'] = protein_cal
        statement = f"{my_dict['brand']} is ${my_dict['price_per_serving']} per snack, ${my_dict['price_per_20g']} per 20g protein, and {my_dict['protein_per_100kc']}g of protein per 100 calories."
    return my_dict, statement

def table_formatter(dataframe,kind):
    '''
    pd.Dataframe.style keeps adding trailing zeros to all digits. This function formats all floats to str with only 2 digits (9.99)
    '''
    if kind == 'bar':
        dataframe[['carbs','fats','protein']] = dataframe[['carbs','fats','protein']].astype({
            'carbs':int,
            'fats':int,
            'protein':int})
        dataframe['carbfatpro'] = dataframe['carbs'].astype(str) + '/' + dataframe['fats'].astype(str) + '/' + dataframe['protein'].astype(str)
    df_type = dataframe.dtypes.reset_index()
    float_cols = []
    for i, row in df_type.iterrows():
        if (row[0] == float) & (row['index']!='carbfatpro'):
            float_cols.append(row['index'])
    dataframe[float_cols] = dataframe[float_cols].applymap('{:,.2f}'.format)
    
    if kind == 'powder':
        dataframe.columns = ['Brand','Protein per 100 calories','Price of 20g Protein',
                             'Price','Protein per Scoop','Calories per Scoop',
                             'Num of Servings','Date Added']
        dataframe = dataframe[['Brand','Calories per Scoop','Protein per Scoop',
                               'Protein per 100 calories','Price of 20g Protein',
                               'Price','Num of Servings']]
    elif kind == 'bar':
        dataframe.columns = ['Brand','Price per Snack','Protein per 100 calories',
                             'Price of 20g Protein','Num of Servings','Carbs','Fats',
                             'Protein','Calories','Price','Date Added', 'Carb/Fat/Pro']
        dataframe = dataframe[['Brand','Calories','Carb/Fat/Pro','Protein per 100 calories',
                               'Price per Snack','Price of 20g Protein','Price',
                               'Num of Servings']]
    return dataframe

def submit_info(row_info, kind):
    save = saveInfo(row_info=row_info,kind=kind)
    save.save_table()
    st.success('Saved in brotein database.')

def app():
    start(button='start')
    
app()