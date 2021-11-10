import data_base


data = data_base.Bot_Data()

field_names = ["opisanie", "vidy"]

name_table = "TGP"

data.create_table(name_table, field_names)

text1 = ["blablabla", "bleblebleble"]

data.insert_into(name_table, text1)

papa = data.select_all(name_table)

print(papa)