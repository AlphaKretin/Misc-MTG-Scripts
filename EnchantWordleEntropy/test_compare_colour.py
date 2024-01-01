def compare_colour(guess,answer):
    guess_col = set(guess["color_identity"])
    ans_col = set(answer["color_identity"])
    if guess_col == ans_col:
        return -1 # arbitrary value indicating exact match, otherwise count number of shared colours
    return len(guess_col & ans_col)

guess = {"color_identity": ["W", "B"]}
answer = {"color_identity": []}
print(compare_colour(guess,answer))