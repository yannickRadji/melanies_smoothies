# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from functools import reduce

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits for your Smoothie
    """
)

session = get_active_session()
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
    st.text(ingredients_string)

    my_insert_stmt = f" insert into smoothies.public.orders(ingredients, NAME_ON_ORDER) values ('{ingredients_string}','{name}')"

    exec_insert =  st.button('SUBMIT ORDER')
    
    st.write(my_insert_stmt)

    if exec_insert:

        sess_return = session.sql(my_insert_stmt).collect()
    
        st.success(f"what is return {sess_return}")
