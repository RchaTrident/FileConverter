import pandas as pd
import re
import json
from datetime import datetime


def convert_data(df):
    sheet_name = list(df.keys())[-1]
    last_tab = df[sheet_name]
    # print(last_tab)
    converted_data = []
    datapair = {}
    cleaned_json = None
    for index, row in last_tab.iterrows():

        empty_columns_count = sum(row.isnull())

        datapair = {}
        for key, value in row.items():
            
            # print(f"{key}: {value}")
            # print(value, "the value")
            if type(value) is datetime:
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            if key == " capital_movements " or key == " fp_redemptions " or key == " fp_crystalisations " or key == " management_fee " or key == " sys_calc_pf " and value == " -   ":
                value = 0
            datapair.update({key: value})
        # print(datapair, "datapair")       
        if datapair['comp_name'] != " -   ":  
        # if datapair['comp_name'] != "-":  
            converted_data.append(datapair)
    converted_data1 = []
    output_data = converted_data
    for i in output_data:
        cleaned_json = {key.strip(): value.strip() if isinstance(value, str) else value for key, value in i.items()}
        converted_data1.append(cleaned_json)
    return converted_data1





