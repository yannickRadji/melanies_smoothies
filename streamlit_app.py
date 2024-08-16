# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits for your Smoothie
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
st.dataframe(data=my_dataframe, use_container_width=True)

name = st.text_input("Name on Smoothie:")
st.write("the name on cup will be:", name)
option = st.multiselect(
    "What is your favorite fruits?",
    my_dataframe, max_selections = 5
)
if option:
    st.write("You selected:", option)
    st.text(option)
    ingredients_string=" ".join(option)
    for name in option:
        response = requests.get(f"https://www.fruityvice.com/api/fruit/{name}")
        if response.json().get("name"):
            st.subheader(name + "Nutrition Info")
            fv_df = st.dataframe(data=response.json(), use_container_width=True)

    my_insert_stmt = f" insert into smoothies.public.orders(ingredients, NAME_ON_ORDER) values ('{ingredients_string}','{name}')"

    exec_insert =  st.button('SUBMIT ORDER')
    
    st.write(my_insert_stmt)

    if exec_insert:

        sess_return = session.sql(my_insert_stmt).collect()
    
        st.success(f"what is return {sess_return}")
