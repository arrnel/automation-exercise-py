class Range:

    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val


password_range = Range(8, 20)
name_range = Range(2, 20)
first_name_range = Range(2, 20)
last_name_range = Range(2, 20)
phone_number_range = Range(8, 12)
user_title_range = Range(2, 5)
company_range = Range(3, 100)
country_range = Range(3, 100)
state_range = Range(3, 100)
city_range = Range(3, 100)
address1_range = Range(3, 100)
address2_range = Range(3, 100)
zip_code_range = Range(3, 100)
