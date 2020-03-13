from datetime import datetime as dt
import requests
import csv


class DataTransformation:

    @classmethod
    def push_data_to_csv(cls, file_path, fields, data, duration):
        """
        :param file_path: the path where csv file will be created
        :param fields: csv headers
        :param data: response data from henry hubs opendata
        :param duration: the duration of data either(daily, monthly or yearly)
        :return:
        """
        my_dict = {}
        date_format = ""
        if duration == "daily":
            date_format = "%Y%m%d"
        elif duration == "monthly":
            date_format = "%Y%m"
        else:
            date_format = "%Y"
        # create and write into a new csv file
        with open(file_path, 'w', newline='') as write_obj:
            dict_writer = csv.DictWriter(write_obj, fieldnames=fields)
            dict_writer.writeheader()
            for value in data:
                # convert first item to date_format and update the dictionary
                date_value = dt.strptime(value[0], date_format).date()
                my_dict['date'] = date_value
                my_dict['price'] = value[1]
                dict_writer.writerow(my_dict)

    @classmethod
    def transform_daily_data_to_csv(cls, api_url, file_path, fields, duration='daily'):
        """
        :param api_url: opendata Url to make request to api
        :param file_path: path to create new csv file
        :param fields: csv headers for first row
        :param duration:  subsequent time for data
        :return: string, indicating new daily data csv file created
        """
        res = requests.get(api_url)
        data = res.json().get('series')[0].get('data')
        cls.push_data_to_csv(file_path, fields, data, duration)

        return 'successfully created Henry-Hub daily gas price list csv'

    @classmethod
    def transform_monthly_data_to_csv(cls, api_url, file_path, fields, duration='monthly'):
        """
       :param api_url: opendata Url to make request to api
        :param file_path: path to create new csv file
        :param fields: csv headers for first row
        :param duration:  subsequent time for data
        :return: string, indicating new monthly data csv file created
        """
        response = requests.get(api_url)
        data = response.json().get('series')[0].get('data')
        cls.push_data_to_csv(file_path, fields, data, duration)

        return 'successfully created Henry-Hub monthly gas price list csv'

    @classmethod
    def transform_yearly_data_to_csv(cls, api_url, file_path, fields, duration="yearly"):
        """
       :param api_url: opendata Url to make request to api
        :param file_path: path to create new csv file
        :param fields: csv headers for first row
        :param duration:  subsequent time for data
        :return: string, indicating new annually data csv file created
        """
        response = requests.get(api_url)
        data = response.json().get('series')[0].get('data')
        cls.push_data_to_csv(file_path, fields, data, duration)
        return 'successfully created Henry-Hub yearly gas price list csv'


if __name__ == '__main__':
    daily_data_url = "https://api.eia.gov/series/?api_key=d099e48793bf5a0f1a58a4f13b1a21b5&series_id=NG.RNGWHHD.D"
    monthly_data_url = "https://api.eia.gov/series/?api_key=d099e48793bf5a0f1a58a4f13b1a21b5&series_id=NG.RNGWHHD.M"
    yearly_data_url = "https://api.eia.gov/series/?api_key=d099e48793bf5a0f1a58a4f13b1a21b5&series_id=NG.RNGWHHD.A"
    daily_csv_file_name = '../data/Henry-Daily-gas-price.csv'
    monthly_csv_file_name = '../data/Henry-Monthly-gas-price.csv'
    yearly_csv_file_name = '../data/Henry-Yearly-gas-price.csv'

    field_names = ["date", "price"]

    print(DataTransformation.transform_daily_data_to_csv(daily_data_url, daily_csv_file_name, field_names))
    print(DataTransformation.transform_monthly_data_to_csv(monthly_data_url, monthly_csv_file_name, field_names))
    print(DataTransformation.transform_yearly_data_to_csv(yearly_data_url, yearly_csv_file_name, field_names))
