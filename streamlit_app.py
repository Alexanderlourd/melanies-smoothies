import streamlit as st
from snowflake.snowpark.functions import col

# Streamlit title and description
st.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for name on smoothie
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name of your Smoothie will be:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch available fruits
fruit_names = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
fruit_list = [row['FRUIT_NAME'] for row in fruit_names]

# Multiselect for ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_list, max_selections=5)

if ingredients_list:
    ingredient_string = ' '.join(ingredients_list)
    st.write("Your selected ingredients are:", ingredient_string)

    # Button to submit the order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.table("smoothies.public.orders").insert([ingredient_string, name_on_order]).collect()
        st.success(f"Your Smoothie is ordered, '{name_on_order}'!", icon="\u2611")
