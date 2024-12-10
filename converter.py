import pandas as pd
import re
import json
from datetime import datetime

def convert_bay_data(df):
    sheet_name = list(df.keys())[-1]
    last_tab = df[sheet_name]
    converted_data = []
    for index, row in last_tab.iterrows():
        empty_columns_count = sum(row.isnull())
        if empty_columns_count >= 4:
            continue  
        account_id = row['account_id']
        if account_id == 0:
            continue
        capital_movements = row["capital_movements"]
        capital_movements_float = float(capital_movements)
        if capital_movements_float < 1:
            capital_movements = '0'
        else:
            capital_movements = str(round(capital_movements_float, 6))
        description = row['description']
        valuation_date = row['valuation_date'].strftime("%Y-%m-%d %H:%M:%S")
        net_assets_bf = str(row['net_assets_bf']).replace(',', '')
        fp_crystalisations = str(row['fp_crystalisations']).replace('(', '').replace(')', '').replace(',', '')
        fp_redemptions = str(row['fp_redemptions']).replace('(', '').replace(')', '').replace(',', '')
        profit_allocation = str(row['profit_allocation']).replace(',', '')
        management_fee = str(row['management_fee']).replace(',', '')
        sys_calc_pf = str(row['sys_calc_pf']).replace(',', '')
        comp_name = row['comp_name']
        NAV = str(row['NAV']).replace(',', '')

        if isinstance(description, str):
            description = re.sub("'", "''", description)

        if isinstance(comp_name, str):
            comp_name = re.sub("'", "''", comp_name)

        datapair = {"account_id": account_id,
                    "description": description,
                    "valuation_date": valuation_date,
                    "net_assets_bf": net_assets_bf,
                    "capital_movements" : capital_movements,
                    "fp_crystalisations": fp_crystalisations,
                    "fp_redemptions": fp_redemptions,
                    "profit_allocation": profit_allocation,
                    "management_fee": management_fee,
                    "sys_calc_pf": sys_calc_pf,
                    "comp_name": comp_name,
                    "NAV": NAV
                }
        converted_data.append(datapair)
    converted_data1 = []
    output_data = converted_data
    for i in output_data:
        cleaned_json = {key.strip(): value.strip() if isinstance(value, str) else value for key, value in i.items()}
        converted_data1.append(cleaned_json)
    return converted_data1


