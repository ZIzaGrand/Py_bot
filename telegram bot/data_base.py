import sqlite3


class Bot_Data:
	def __init__(self):
		self.conn = sqlite3.connect('test.db')
		self.cur = self.conn.cursor()


	def save_close(self):
		self.conn.commit()
		self.conn.close()


	def create_table(self, name_table, field_names):
		col = ''
		for i in field_names:
			col += f'{i} TEXT,'

		self.cur.execute(f"CREATE TABLE IF NOT EXISTS {name_table}({col[:-1]})")


	def insert_into (self, name_table, text1):
		self.cur.execute(f"INSERT INTO {name_table} VALUES ({text1});", (name_table, text1))

	def select_all(self, name_table):
		self.cur.execute(f"SELECT * FROM {name_table}", (name_table))
		self.all_results = self.cur.ferchall()
		return self.all_results
		self.save_close()