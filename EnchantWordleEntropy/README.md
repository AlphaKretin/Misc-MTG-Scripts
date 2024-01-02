# Enchant Worldle Entropy
A script that calculates the entropy for each potential first guess in a game of [Enchant Worldle](https://enchantworldle.com/). Inspired by 3Blue1Brown's [Wordle video](https://www.youtube.com/watch?v=v68zYyaEmEA).

## filter.py
Filters a full card dump to only cards we expect to be legal answers in Enchant Worldle.

## patterns.py
The chunkiest script, precomputing the response patterns a game of Enchant Wordle would give for each combination of guess and answer. A not terribly efficient O(n^2) algorithm with n~=30000. Takes roughly 90 minutes to run on my machine.

## entropy.py
The main script, calculating the entropy for each card based on the information given by the precomputed response patterns. Should be adaptable to any input card pool that's a subet of the one given by filter.py, allowing for calculating the entropy of guesses in later stages of the game.

## sort.py
Takes the outputted list of entropies for each card and sorts them so you can easily find the "best" guess as determined by this metric.

## Test scripts
- test_compare_colour.py
- test_compare_mv.py
- test_get_types.py
- test_duplicate_cards.py
These are mostly basic tests of individual functions written to reimplement the logic of Enchant Worldle, so that I could be more sure things would work before committing to a long script run. The duplicate cards test was to make sure my edited filtering was in fact only returning one of each card name, using an example that had previously failed.