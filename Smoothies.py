# Import python packages
import streamlit as st
import os
import requests  

from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in the Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name is", name_on_order)


#st.write("""You selected:""",option)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe,use_container_width=True)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients: ", my_dataframe)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string =''
    for ingredient in ingredients_list:
        ingredients_string+=ingredient +' '

    #st.write(ingredients_string)
    

    my_insert_stmt = """insert into SMOOTHIES.PUBLIC.ORDERS (ingredients,name_on_order) VALUES ('""" +  ingredients_string + """','"""+name_on_order+"""')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")


smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
