from ShoppingList.Database_food import food
from Menu.Person import Person
from Menu.factors_calc_meal import factors
from Menu.Meal import Product, Meal, Menu
import pandas as pd
import copy
from Menu.utils import *

pd.set_option('display.width', 200)

# users inputs
username = input("Enter your username [max 20 alphanum. characters('.'/'_'/'-' are allowed, min. 2 letters): ")
username = check_username(username)
height = input("Enter your height in [cm]: ")
height = check_height(height)
weight = input("Enter your weight in [kg]: ")
weight = check_weight(weight)
age = input("Enter your age : ")
age = check_age(age)
sex = input("Enter your sex [M/F]: ")
sex = check_sex(sex)
print("\nDaily activities: ")
for i in range(1, len(factors) + 1):
	print("{} : {}".format(i, factors.loc[i, 'Activity']))
	
activity_index = input("Select number of your activity from list above: ")
activity_index = check_activity_index(activity_index, factors)
activity = factors.iloc[int(activity_index) - 1, 1]
person1 = Person(username, height, weight, age, sex, activity)
person1.show_info()

menu = Menu(person1.cmr, person1.daily_carbo, person1.daily_proteins, person1.daily_fats)

print("Possible set of meals per day: ")
for k, v in menu.possible_set_meals.items():
	print("{}. {}".format(k, v))

your_menu = input("Select set of meals from list above: ")
menu.quantity_of_meals = len(menu.possible_set_meals[int(your_menu)])

for i in range(menu.quantity_of_meals):
	meal = Meal(menu.possible_set_meals[int(your_menu)][i])
	menu.add_meal(meal)

categories = sorted(list(set(food.index.get_level_values(0))))

while True:
	menu.get_meals_names()
	chosen_meal = input("Select meal to compose (choose number above) or select [F] to Finish and print your Menu: ")
	if chosen_meal == "F":
		break
	selected_meal = menu.menu_list[int(chosen_meal) - 1]
	
	while True:
		if len(selected_meal) == 0:
			print("Completing {}".format(selected_meal.get_meal_name()))
			action = input("Select action [Add product: (A), Finish (F), Print personal parameters (P)]: ")
			if action == "F":
				break
			elif action == "P":
				person1.show_info()
			elif action == "A":
				for item in range(len(categories)):
					print("{}: {}".format(item + 1, categories[item]))
				category = int(input("Select categories [1-22], select [0] to undo: "))
				if category > len(categories):
					print("Wrong number!")
					continue
				elif category == 0:
					break
				print(food.loc[categories[category - 1]].loc[:, ["Product", 'Kcal', 'Carbo(g)', 'Protein(g)', 'Fats(g)']])
				index_number = int(input('Select number of product from list above [select "0" to undo]: '))
				if index_number == 0:
					continue
				elif index_number > len(food.loc[categories[category - 1]].loc[:, ["Product", 'Kcal', 'Carbo(g)', 'Protein(g)', 'Fats(g)']]):
					print("Wrong number!")
					continue
				product = Product(food.loc[(categories[category - 1], index_number), "Product"],
				                  food.loc[(categories[category - 1], index_number), "Price[PLN]"],
				                  {"Protein(g)": food.loc[(categories[category - 1], index_number), "Protein(g)"],
				                   "Fats(g)": food.loc[(categories[category - 1], index_number), "Fats(g)"],
				                   "Carbo(g)": food.loc[(categories[category - 1], index_number), "Carbo(g)"]},
				                  food.loc[(categories[category - 1], index_number), "Weight_pcs/pack[g]"],
				                  food.loc[(categories[category - 1], index_number), "Kcal"],
				                  food.loc[(categories[category - 1], index_number), "unit"])
				print("Weight of average piece/portion of {}: {}g.".format(product.name, product.weight))
				unit_type = input("Select unit type g [G] / psc. [P]: ")
				if unit_type == "G":
					quantity_in_grams = input("How many grams of product do you want to add: ")
					quantity = float(quantity_in_grams)
				elif unit_type == "P":
					quantity_in_pcs = input("How many pcs. of product do you want to add: ")
					quantity = float(quantity_in_pcs) * float(product.weight)
				# blockage in case of exceeding the daily limit - calories, nutrition
				temp_menu = copy.deepcopy(menu)
				temp_menu.menu_list[int(chosen_meal) - 1].add_product(product, quantity)
				if temp_menu.get_menu_calories() > person1.cmr:
					print("Your daily calorie limit is {}.".format(person1.cmr))
					print("Calorie content of your menu after adding the last product {} kcal.".format(
						temp_menu.get_menu_calories()))
					print("Reduce the number of calories!")
					temp_menu = None
					continue
				elif temp_menu.get_menu_proteins() > person1.daily_proteins:
					print("Your daily protein limit is {}.".format(person1.daily_proteins))
					print("Proteins content of your menu after adding the last product {} g.".format(
						temp_menu.get_menu_proteins()))
					print("Reduce the number of Proteins!")
					temp_menu = None
					continue
				elif temp_menu.get_menu_carbohydrates() > person1.daily_carbo:
					print("Your daily carbohydrates limit is {}.".format(person1.daily_carbo))
					print("Carbohydrates content of your menu after adding the last product {} g.".format(
						temp_menu.get_menu_carbohydrates()))
					print("Reduce the number of Carbohydrates!")
					temp_menu = None
					continue
				elif temp_menu.get_menu_fats() > person1.daily_fats:
					print("Your daily fats limit is {}.".format(person1.daily_fats))
					print("Fats content of your menu after adding the last product {} g.".format(temp_menu.get_menu_fats()))
					print("Reduce the number of Fats!")
					temp_menu = None
					continue
				else:
					selected_meal.add_product(product, quantity)
		
		if len(selected_meal) > 0:
			print("Completing {}".format(selected_meal.get_meal_name()))
			action = input("Select action [Add product: (A), Remove Product: (R), "
			               "Change quantity [g]: (Q), Finish (F), Print your personal parameters and menu (P)]: ")
			if action == "A":
				for item in range(len(categories)):
					print("{}: {}".format(item + 1, categories[item]))
				category = int(input("Select categories [1-22], select [0] to undo: "))
				if category > len(categories):
					print("Wrong number!")
					continue
				elif category == 0:
					break
				print(food.loc[categories[category - 1]].loc[:, ["Product", 'Kcal', 'Carbo(g)', 'Protein(g)', 'Fats(g)']])
				index_number = int(input('Select number of product from list above [select "0" to undo]: '))
				if index_number == 0:
					continue
				elif index_number > len(food.loc[categories[category - 1]].loc[:,
				                        ["Product", 'Kcal', 'Carbo(g)', 'Protein(g)', 'Fats(g)']]):
					print("Wrong number!")
					continue
				product = Product(food.loc[(categories[category - 1], index_number), "Product"],
				                  food.loc[(categories[category - 1], index_number), "Price[PLN]"],
				                  {"Protein(g)": food.loc[(categories[category - 1], index_number), "Protein(g)"],
				                   "Fats(g)": food.loc[(categories[category - 1], index_number), "Fats(g)"],
				                   "Carbo(g)": food.loc[(categories[category - 1], index_number), "Carbo(g)"]},
				                  food.loc[(categories[category - 1], index_number), "Weight_pcs/pack[g]"],
				                  food.loc[(categories[category - 1], index_number), "Kcal"],
				                  food.loc[(categories[category - 1], index_number), "unit"])
				print("Weight of average piece/portion of {}: {}.".format(product.name, product.weight))
				unit_type = input("Select unit type g [G] / psc. [P]: ")
				if unit_type == "G":
					quantity_in_grams = input("How many grams of product do you want to add: ")
					quantity = float(quantity_in_grams)
				elif unit_type == "P":
					quantity_in_pcs = input("How many pcs. of product do you want to add: ")
					quantity = float(quantity_in_pcs) * float(product.weight)
				
				# blockage in case of exceeding the daily limit - calories, nutrition
				temp_menu = copy.deepcopy(menu)
				temp_menu.menu_list[int(chosen_meal) - 1].add_product(product, quantity)
				if temp_menu.get_menu_calories() > person1.cmr:
					print("Your daily calorie limit is {}.".format(person1.cmr))
					print("Calorie content of your menu after adding the last product {} kcal.".format(
						temp_menu.get_menu_calories()))
					print("Reduce the number of calories!")
					temp_menu = None
					continue
				elif temp_menu.get_menu_proteins() > person1.daily_proteins:
					print("Your daily protein limit is {}.".format(person1.daily_proteins))
					print("Proteins content of your menu after adding the last product {} g.".format(
						temp_menu.get_menu_proteins()))
					print("Reduce the number of Proteins!")
					temp_menu = None
					continue
				elif temp_menu.get_menu_carbohydrates() > person1.daily_carbo:
					print("Your daily carbohydrates limit is {}.".format(person1.daily_carbo))
					print("Carbohydrates content of your menu after adding the last product {} g.".format(
						temp_menu.get_menu_carbohydrates()))
					print("Reduce the number of Carbohydrates!")
					temp_menu = None
					continue
				elif temp_menu.get_menu_fats() > person1.daily_fats:
					print("Your daily fats limit is {}.".format(person1.daily_fats))
					print("Fats content of your menu after adding the last product {} g.".format(
						temp_menu.get_menu_fats()))
					print("Reduce the number of Fats!")
					temp_menu = None
					continue
				else:
					selected_meal.add_product(product, quantity)
				
			elif action == "Q":
				while True:
					selected_meal.show_products_in_meal()
					number_product = int(input("Select position from Product List [select 0 to Undo]: "))
					if number_product == 0:
						break
					elif number_product > len(selected_meal):
						print("Wrong number!")
						continue
					change_quantity = input("Select: increase the number of grams of the product - [A], reduce the number of grams of the product [R], Finish [F]: ")
					if change_quantity == "R":
						print("Weight of average piece/portion of {}: {}g".format(product.name, product.weight))
						unit_type = input("Select unit type g [G] / psc. [P]: ")
						if unit_type == "G":
							quantity_in_grams = input("How many grams of product do you want to remove: ")
							quantity = float(quantity_in_grams)
						elif unit_type == "P":
							quantity_in_pcs = input("How many pcs. of product do you want to remove: ")
							quantity = float(quantity_in_pcs) * float(product.weight)
						if quantity > selected_meal.products_list[selected_meal[number_product - 1]]:
							print("Quantity of this product in your meal is less.Choose the correct quantity")
							continue
						selected_meal.remove_product(selected_meal[number_product - 1], quantity)
						if len(selected_meal) == 0:
							print("Meal is Empty!!")
							break
						change_next = input("Do you want to reduce the quantity of another product? [Y/N]:  ")
						if change_next == "Y":
							continue
						if change_next == "N":
							break
						else:
							print("Wrong command!")
							continue
					elif change_quantity == "A":
						print("Weight of average piece/portion of {}: {}g.".format(product.name, product.weight))
						unit_type = input("Select unit type g [G] / psc. [P]: ")
						if unit_type == "G":
							quantity_in_grams = input("How many grams of product do you want to add: ")
							quantity = float(quantity_in_grams)
						elif unit_type == "P":
							quantity_in_pcs = input("How many pcs. of product do you want to add: ")
							quantity = float(quantity_in_pcs) * float(product.weight)
						selected_meal.add_product(selected_meal[number_product - 1], quantity)
						change_next = input("Do you want to increase the quantity of another product? [Y/N]: ")
						if change_next == "Y":
							continue
						if change_next == "N":
							break
						else:
							print("Wrong command!")
							continue
					elif change_quantity == "F":
						break
						
				continue_adding = input("Do you want to continue completing your meal? [Y/N]: ")
				if continue_adding == "Y":
					continue
				elif continue_adding == "N":
					print("*" * 150)
					selected_meal.show_products_in_meal()
					print("*" * 150)
					break
				else:
					print("Wrong command!")
					continue
					
			elif action == "R":
				while True:
					selected_meal.show_products_in_meal()
					number_product = int(input("Select position from Product List [select 0 to Undo]: "))
					if number_product == 0:
						break
					elif number_product > len(selected_meal):
						print("Wrong number!")
						continue
					selected_meal.remove_item(selected_meal[number_product - 1])
					selected_meal.show_products_in_meal()
					if len(selected_meal) == 0:
						print("Meal is Empty!!")
						break
					remove_next = input("Do you want to remove next product: [Y/N]: ")
					if remove_next == "Y":
						continue
					elif remove_next == "N":
						break
					else:
						print("Wrong command!")
						continue
						
				continue_adding = input("Do you want to continue completing your meal? [Y/N]: ")
				if continue_adding == "Y":
					continue
				elif continue_adding == "N":
					print("*" * 150)
					selected_meal.show_products_in_meal()
					print("*" * 150)
					break
				else:
					print("Wrong command!")
					continue
					
			elif action == "P":
				person1.show_info()
				menu.get_menu_info()
	
			elif action == 'F':
				break
			
			else:
				print("Wrong command!")
				continue
		
			
menu.get_menu_info()

