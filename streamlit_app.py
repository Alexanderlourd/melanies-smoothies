# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie! 
    """)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name of your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)
if ingredients_list:

    ingredient_string = ''
    for fruit_chosen in ingredients_list:
        ingredient_string += fruit_chosen + ' '
    
    st.write(ingredient_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values 
                    ('""" + ingredient_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    st.write(my_insert_stmt)
    # st.stop()
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success("""Your Smoothie is ordered, '""" + name_on_order + """'!""", icon = "\u2611")
