from typing import TypeVar

T = TypeVar("T")


class Range[T]:

    def __init__(self, min_val: [T], max_val: [T]):
        self.min_val = min_val
        self.max_val = max_val


# ----- User
password_range = Range[int](8, 20)
name_range = Range[int](2, 50)
email_range = Range[int](4, 254)
first_name_range = Range[int](2, 20)
last_name_range = Range[int](2, 20)
phone_number_range = Range[int](8, 12)
user_title_range = Range[int](2, 5)
company_range = Range[int](3, 100)
country_range = Range[int](3, 100)
state_range = Range[int](3, 100)
city_range = Range[int](3, 100)
address1_range = Range[int](3, 100)
address2_range = Range[int](3, 100)
zip_code_range = Range[int](3, 100)

# ----- Review
review_message_range = Range[int](3, 2000)

# ----- Card
card_name = Range[int](3, 24)
card_number_range = Range[int](16, 19)
