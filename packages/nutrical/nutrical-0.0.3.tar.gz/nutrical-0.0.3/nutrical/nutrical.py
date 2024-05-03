'''API examples

>>> apple = Ingredient(protein=0.5, fat=9, calories=100, portion='100g', dollar=1.5)
>>> apple.to(portion='170g')  # Equivalent: 1.7 * apple
>>> apple.to(dollar=3)        # Equivalent: 3   * apple
>>> apple.to(protein=2)       # Equivalent: 4   * apple
'''

import csv
import json
from numbers import Number
from .utils import parse_portion, add_portion, add_dollar

class Recipe:

    def __init__(self, name=None, components=None):
        self.name = name
        self.components = components
    

    def __repr__(self):
        if self.name is not None:
            return f"Recipe ({self.name}):\n" + str(sum(self.components))
        return f"Recipe:\n" + str(sum(self.components))
    

    def export_csv(self, outfp):
        
        total = sum(self.components)
        cols = [ "name", "portion", "dollar", *total.nutrition ]
        
        rows = []
        for item in [ *self.components, total ]:
            item = { **item.__dict__, **item.__dict__['nutrition'] }
            row = []
            for k in cols:
                row.append( item.get(k, None) )
            rows.append(row)
        rows[-1][0] = "Total"

        with open(outfp, "w", encoding="UTF-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)



class Ingredient:
    def __init__(self, name=None, portion='100g', dollar=None, **kwargs):
        self.name = name
        self.dollar = dollar
        self.portion = parse_portion(portion)
        self.nutrition = {}
        
        for k, v in kwargs.items():
            self.nutrition[k.lower()] = v


    def to(self, **kwargs):
        '''Only the first kwarg is taken
        '''
        k, v = kwargs.popitem()
        k = k.lower()
        if k == 'dollar' and self.dollar is not None:
            fct = v / self.dollar
        elif k == 'portion' and self.portion is not None:
            fct = float(parse_portion(v) / self.portion)
        elif k in self.nutrition:
            fct = v / self.nutrition[k]
        else:
            raise Exception("Conversion unit not found!")

        return fct * self


    def __repr__(self):
        repr = {
            "portion": self.portion if self.portion is not None else "NA",
            "dollar": self.dollar if self.dollar is not None else "NA",
            **self.nutrition
        }
        repr2 = {}
        for k, v in repr.items():
            if not isinstance(v, str):
                v = round(v, 2)
            if k == "portion":
                v = str(v)
            repr2[k] = v
        s = json.dumps(repr2, indent=3, ensure_ascii=False)
        if self.name is not None:
            s = self.name + '\n' + s
        return s


    def __add__(self, item):
        args = {}
        portion = add_portion(self.portion, item.portion)
        dollar = add_dollar(self.dollar, item.dollar)
        for k in set( [*self.nutrition.keys(), *item.nutrition.keys()] ):
            args[k] = self.nutrition.get(k, 0) + item.nutrition.get(k, 0)
        
        return Ingredient(dollar=dollar, portion=portion, **args)


    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    

    def __mul__(self, fct: Number):
        if not isinstance(fct, Number): 
            raise Exception("Multiplication on numbers only!")
        
        args = {}
        try:
            portion = fct * self.portion
        except:
            portion = None
        try:
            dollar = fct * self.dollar
        except:
            dollar = None
        for k in self.nutrition.keys():
            args[k] = fct * self.nutrition[k]
        
        return Ingredient(name=self.name, dollar=dollar, portion=portion, **args)

    __rmul__ = __mul__

# %%
