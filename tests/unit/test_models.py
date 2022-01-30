# from dmLibrary.database.models import Customer

# def test_new_customer():
#     """
#     GIVEN a User model
#     WHEN a new User is created
#     THEN check the email, hashed_password, and role fields are defined correctly
#     """
#     data = {
#         "name":"testName testLastName",
#         "mobile":"0881231234",
#         "email":"testOne@gmail.com"
#     }
#     customer = Customer(**data)
#     assert customer.name == data["name"]
#     assert customer.mobile == data["mobile"]
#     assert customer.email == data["email"]