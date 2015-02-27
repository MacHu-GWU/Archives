##encoding=UTF-8

from __future__ import print_function
from util.DATA import *
import util.constant

import sys
def research_use_hash_value_to_replace_lastname_state_pagenumber_combination():
    a = set()
    for lastname in util.constant.lastnamelist:
        for statename in util.constant.statenamelist:
            for i in range(1, 2):
                a.add("&&".join([lastname, statename, str(i)]))
    
    print(sys.getsizeof(a))
    safe_dump_pk(a, "a.p")
    print(len(a))
#     print(len(util.constant.lastnamelist) * len(util.constant.statenamelist))
    
research_use_hash_value_to_replace_lastname_state_pagenumber_combination()