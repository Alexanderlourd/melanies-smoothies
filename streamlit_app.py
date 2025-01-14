# Import python packages
import streamlit
from snowflake.snowpark.functions import col

# Write directly to the app
streamlit.title(":cup_with_straw: Customise Your Smoothie! :cup_with_straw:")
streamlit.write(
    """Choose the fruits you want in your custom Smoothie! 
    """)

name_on_order = streamlit.text_input("Name on Smoothie:")
streamlit.write("The name of your Smoothie will be:", name_on_order)

cnx = streamlit.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = streamlit.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)
if ingredients_list:

    ingredient_string = ''
    for fruit_chosen in ingredients_list:
        ingredient_string += fruit_chosen + ' '
    
    streamlit.write(ingredient_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values 
                    ('""" + ingredient_string + """','""" + name_on_order + """')"""

    time_to_insert = streamlit.button('Submit Order')
    streamlit.write(my_insert_stmt)
    # streamlit.stop()
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        streamlit.success("""Your Smoothie is ordered, '""" + name_on_order + """'!""", icon = "\u2611")
