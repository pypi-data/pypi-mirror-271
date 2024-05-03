
'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status_v1/status_loop_1.py
'''

#----
#
import vegan.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import vegan.besties.food_USDA.examples as USDA_examples	
import vegan.besties.food_USDA.nature_v2 as food_USDA_nature_v2
import vegan.mixes.insure.equality as equality
#
#
import json	
#
#----

	
def check_1 ():
	foods = [
		"branded/beet_juice_2412474.JSON",
		"branded/beet_juice_2642759.JSON",
		"branded/Gardein_f'sh_2663758.JSON",
		"branded/impossible_beef_2664238.JSON",
		"branded/vegan_pizza_2672996.JSON",	
		"branded/walnuts_1882785.JSON"
	]
	
	for food in foods:
		food_data = USDA_examples.retrieve (food)
		assertions_foundational.run (food_data)
		nature = food_USDA_nature_v2.create (food_data)
		
	
checks = {
	'check 1': check_1
}