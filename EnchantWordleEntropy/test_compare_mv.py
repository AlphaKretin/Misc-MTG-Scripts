def compare_mv(guess,answer):
    guess_mv = guess["cmc"]
    ans_mv = answer["cmc"]
    if guess_mv == ans_mv:
        return "g" # representing a green square
    if guess_mv > ans_mv:
        if guess_mv - ans_mv <= 2:
            return "yup" # yellow up arrow
        return "up"
    # else lesser
    if ans_mv - guess_mv <= 2:
        return "ydn"
    return "dn"

guess = {"cmc": 5}
answer = {"cmc": 2}
print(compare_mv(guess,answer))