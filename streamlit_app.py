import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError
streamlit.title(" My Mom's New Healthy Diner ")
streamlit.header(' 🥣Breakfast Favorites ')
streamlit.text(' 🥗Omega 3 & strawberry Oatmeal ')
streamlit.text(' 🥑🍞Kale, Spinach and Rocket smoothie ')
streamlit.text(' 🐔Hard boiled free range egg ')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)
#stremlit.dataframe(fruits_selected)


#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/kiwi")
#streamlit.text(fruityvice_response)
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#streamlit.dataframe(fruityvice_normalized)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get Info!")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
    
#streamlit.stop()

streamlit.header("View Our Fruit List - Add your Favourites!")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_row)
#streamlit.text("SELECT * from fruit_load_list")
#streamlit.text(my_data_row)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('" jackfruit" + "papaya" + "guava" + "kiwi "')")
    return "Thanks for adding "+ new_fruit
  
fruit_add = streamlit.text_input('What fruit would you like to add ?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(fruit_add)
  streamlit.text(back_from_function)
  
#fruityvice_response1 = requests.get("https://fruityvice.com/api/fruit/"+ fruit_add)
#fruityvice_normalized1 = pandas.json_normalize(fruityvice_response1.json())
#streamlit.dataframe(fruityvice_normalized1)
