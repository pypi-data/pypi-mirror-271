
'''
	python3 status.proc.py besties/food_USDA/nature_v2/_status_v1/status_3.py
'''

from vegan.mixes.insure.override_print import override_print
import vegan.mixes.insure.equality as equality

import vegan.besties.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import vegan.besties.food_USDA.examples as USDA_examples
import vegan.besties.food_USDA.nature_v2 as food_USDA_nature_v2
from vegan.shows_v2.treasure.nature.land.grove._ops.seek_name_or_accepts import seek_name_or_accepts
from rich import print_json
	
def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	assertions_foundational.run (walnuts_1882785)
	nature = food_USDA_nature_v2.create (walnuts_1882785)
	equality.check (nature ["identity"]["FDC ID"], "1882785")
	
	print_json (data = nature ["essential nutrients"] ["measures"])
	
	energy = seek_name_or_accepts (
		grove = nature ["essential nutrients"] ["grove"],
		name_or_accepts = "energy",
		return_none_if_not_found = True
	)
	
	print_json (data = energy)
	
checks = {
	'check 1': check_1
}