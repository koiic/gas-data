from datetime import datetime as dt, timedelta
import requests
import csv

# load data from as a csv file



def push_daily_data_to_csv(file_path, fields, data):
    my_dict = {}
    with open(file_path, 'w', newline='') as write_obj:
        dict_writer = csv.DictWriter(write_obj, fieldnames=fields)
        dict_writer.writeheader()
        for value in data:
            # convert first item to date_format andcreate a dictionary
            date_value = dt.strptime(value[0], "%Y%m%d").date()
            my_dict['date'] = date_value
            my_dict['price'] = value[1]
            dict_writer.writerow(my_dict)


def push_monthly_data_to_csv(file_path, fields, data):
    my_dict = {}
    with open(file_path, 'w', newline='') as write_obj:
        dict_writer = csv.DictWriter(write_obj, fieldnames=fields)
        dict_writer.writeheader()
        for value in data:
            # convert first item to date_format andcreate a dictionary
            date_value = dt.strptime(value[0], "%Y%m").date()
            my_dict['date'] = date_value
            my_dict['price'] = value[1]
            dict_writer.writerow(my_dict)


def transform_daily_data_to_csv(api_url, file_path, fields):
    res = requests.get(api_url)
    data = res.json().get('series')[0].get('data')
    push_daily_data_to_csv(file_path, fields, data)

    return 'successfully created Henry-Hub daily gas price list csv'


def transform_monthly_data_to_csv(api_url, file_path, fields):
    response = requests.get(api_url)
    data = response.json().get('series')[0].get('data')
    push_monthly_data_to_csv(file_path, fields, data)

    return 'successfully created Henry-Hub monthly gas price list csv'



if __name__ == '__main__':
    daily_data_url = "https://api.eia.gov/series/?api_key=d099e48793bf5a0f1a58a4f13b1a21b5&series_id=NG.RNGWHHD.D"
    monthly_data_url = "https://api.eia.gov/series/?api_key=d099e48793bf5a0f1a58a4f13b1a21b5&series_id=NG.RNGWHHD.M"
    daily_csv_file_name = '/Users/ismailibrahim/Documents/work/datopian/gas-data/data/Henry-Daily.csv'
    monthly_csv_file_name = '/Users/ismailibrahim/Documents/work/datopian/gas-data/data/Henry-Monthly.csv'

    field_names = ["date", "price"]

    print(transform_daily_data_to_csv(daily_data_url, daily_csv_file_name, field_names))
    print(transform_monthly_data_to_csv(monthly_data_url, monthly_csv_file_name, field_names))
