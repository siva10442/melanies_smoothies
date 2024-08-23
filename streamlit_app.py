# Import python packages 
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
#from snowflake.snowpark.context import get_active_session


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

Name_On_Order=st.text_input("Name on Smoothie:")
st.write('The name on your Smoothie will be:',Name_On_Order)


#session = get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
#st.dataframe(df)
#st.stop()
ingredients_list=st.multiselect("Choose up to 5 ingrediants", my_dataframe ,max_selections=5)
if ingredients_list:
    ingredients_string=''
    for fruits_chosen in ingredients_list:
        ingredients_string+= fruits_chosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruits_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruits_chosen,' is ', search_on, '.')
        st.subheader(fruits_chosen+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruits_chosen)
        #st.text(fruityvice_response.json())
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + ingredients_string + """','""" + Name_On_Order + """')"""
    time_to_insert=st.button("Submit Order")


    #st.write(my_insert_stmt)
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")

