#%%
from nutrical import Ingredient, Recipe

apple = Ingredient("apple", portion='160g', calories=80, protein=.5, fiber=1)
banana = Ingredient("banana", portion='80g', calories=70, protein=1, fiber=1.6)
peanut = Ingredient("peanut", portion='20g', calories=110, protein=5.7, fat=20, fiber=1.8)

# Programmatic construction
data = {'name': 'hi', 'portion': '150g', 'dollar': 20, 'Soluble Fiber': 1}
Ingredient(**data)

# Nutrition info of 2 apples
2 * apple

# Change of basis
apple.to(portion='130g')  # a smaller apple

# how much apple to eat to reach 3g of fibers?
apple.to(fiber=3)         


#%%
# Create recipe from ingredients
recipe = Recipe("Fruit Cake", [
    2   * apple,    # 2 apple
    1   * banana,   # 1 banana
    1.5 * peanut    # 1.5 servings of peanut butter
])
recipe
#%%
# Export nutrition values
recipe.export_csv("FruitCake.csv")  
# %%
Food(portion=100, 蛋白質=5)
# %%
from foop import Food, Recipe
d = { 'a b': 1}

# %%
