import pandas as pd
import re


def readCSV(path):
    recipes_df = pd.read_csv(path)

    recipe_cols = ['RecipeId', 'Name', 'CookTime', 'PrepTime', 'TotalTime', 'Description', 'Images',
                   'RecipeCategory', 'Keywords', 'RecipeIngredientQuantities', 'RecipeIngredientParts',
                   'AggregatedRating', 'Calories', 'RecipeServings', 'RecipeYield', 'RecipeInstructions']

    rp_df = recipes_df[recipe_cols]

    recipe_col_subset = ['RecipeId', 'Name', 'CookTime', 'PrepTime', 'TotalTime', 'Description', 'Images',
                         'RecipeCategory', 'Keywords', 'RecipeIngredientQuantities', 'RecipeIngredientParts',
                         'AggregatedRating', 'Calories', 'RecipeInstructions']

    rp_df = rp_df.dropna(subset=recipe_col_subset)
    rp_df = rp_df[rp_df.Images != 'character(0)']
    modify_col_list = ['Images', 'Keywords', 'RecipeIngredientQuantities', 'RecipeIngredientParts',
                       'RecipeInstructions']
    rp_df = rp_df.apply(lambda x: map_for_series(x) if x.name in modify_col_list else x)

    return rp_df


def map_str_to_list(string):
    #pattern = re.compile(r'\"(.+)\"')
    pattern = re.compile(r'\"([^"]+)\"')
    return pattern.findall(string)


def map_for_series(series: pd.Series):
    return series.apply(lambda i: map_str_to_list(i))