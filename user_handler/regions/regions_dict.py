import json

file = open('user_handler/regions/regions.json', encoding='utf-8')
# file = open('./regions.json')


class RegionsData:
    data = json.load(file)

    def generate_region(self):
        region_list = []
        last_item = ''
        counter = 1
        for item in self.data:
            if item['region'] != last_item:
                region_list.append((counter, item['region']))
                counter += 1
            last_item = item['region']

        return region_list

    def generate_city(self):
        city_list = []
        counter = 1
        for item in self.data:
            city_list.append((counter, item['city']))
            counter += 1

        return city_list


DATA = RegionsData()
DATA_REGIONS = DATA.generate_region()
DATA_CITIES = DATA.generate_city()
# print(DATA_REGIONS)
