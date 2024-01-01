# Enchant Worldle Entropy
A script that calculates the entropy for each potential first guess in a game of [Enchant Worldle](https://enchantworldle.com/). Inspired by 3Blue1Brown's [Wordle video](https://www.youtube.com/watch?v=v68zYyaEmEA).

## filter.py
Filters a full card dump to only cards we expect to be legal answers in Enchant Worldle. Currently does not seem to do well enough at removing duplicate/non-first prints.

## entropy.py
The main script, generating response patterns for each guess against each possible answer, and using those to calculate the entropy for each card. A not terribly efficient O(n^2) algorithm with n~=30000. Takes roughly 90 minutes to run on my machine. In the future, I may want to seperate the pattern generation and the entropy calculation, so that we can keep a precomputed list of patterns and use them for more nuanced purposes.

## sort.py
Takes the outputted list of entropies for each card and sorts them so you can easily find the "best" guess as determined by this metric.

## Test scripts
- test_compare_colour.py
- test_compare_mv.py
- test_get_types.py
These are all basic tests of individual functions written to reimplement the logic of Enchant Worldle, so that I could be more sure things would work before committing to a long script run.