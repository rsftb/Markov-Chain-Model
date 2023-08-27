"""
Markov Chain Text Generator
Starts and ends with the first and last words of the given script respectively
Weighted probability selection
Lots of comments
"""

import random


# Load a large .txt file
with open("milton-paradise.txt", 'r') as input_text:
    body = input_text.read().split()


# Create a transition matrix: find all possible next words for a given word -
#                             - by order of the words in the body of text given
# Example:
# transition_matrix["Hello,"] = ["World!", "Foo", "Foo", "Jones"]
# transition_matrix["Foo"] = ["Bar", "Bar", "Baz"]
# transition_matrix["Bar"] = ["at", "Baz.", "was"]
# transition_matrix["Baz."] = [None, "Which"]
transition_matrix = {}
for i in range(len(body)-1):
    if body[i] not in transition_matrix:
        transition_matrix[body[i]] = [body[i+1]]
    else:
        transition_matrix[body[i]].append(body[i+1])


# Special case for the last word in the input text
# Whatever word was last has the possibility of ending the while loop -
# - generating text at the of of the script
if body[-1] not in transition_matrix:
    transition_matrix[body[-1]] = [None]
else:
    transition_matrix[body[-1]].append(None)


# Extra: for loop block below will refactor duplicates in transition_matrix by -
#        - collapsing them and adding a weights dictionary.
# Example:
# transition_matrix["Hello,"] = ["World!", "Foo", "Jones"]
#        tm_weights["Hello,"] = [1, 2, 1]
# transition_matrix["Foo"] = ["Bar", "Baz"]
#        tm_weights["Foo"] = [2, 1]
# transition_matrix["Bar"] = ["at", "Baz.", "was"]
#        tm_weights["Bar"] = [1, 1, 1]
# transition_matrix["Baz."] = [None, "Which"]
#        tm_weights["Baz."] = [1, 1]
tm_weights = {}
for word, lst in transition_matrix.items():

    #print(word, lst)

    # If all next possible words are the same, collapse to a single word, -
    # - add one weight and continue
    # Works for len(1) also
    if all(items == lst[0] for items in lst):
        transition_matrix[word] = [lst[0]]
        tm_weights[word] = [1]
        continue

    # For all possible next words, add weights based on occurrence
    occurrences = {}
    for i in range(len(lst)): #< Simplify
        if lst[i] not in occurrences:
            occurrences[lst[i]] = 1
        else: 
            occurrences[lst[i]] += 1

    # Collapse duplicate words in transition_matrix[word] through occurrences
    transition_matrix[word] = [w for w in occurrences.keys()]

    # Make a list of words through occurrences
    _weights = []
    for weight in occurrences.values():
        _weights.append(weight)

    # Add corresponding weights to tm_weights[word]
    tm_weights[word] = _weights


# Now the transition_matrix[word] holds a list of next possible words, and-
# -tm_weights contains the probability of any word being selected
# We can almost start generating words

# Get the first word out of the transition matrix as the current state
current_state = next(iter(transition_matrix))

# While the weighted random walks haven't encountered the possibility of -
# - ending the script, keep printing the current state
while current_state is not None:
    print(current_state)

    # If only one possible next word, then immediately take the next word
    if len(tm_weights[current_state]) == 1:
        current_state = transition_matrix[current_state][0]
        continue

    # Get a random word from the transition matrix using the weights
    # k = 1 (default value, returns k amount of choices in a list)
    current_state = random.choices(
        transition_matrix[current_state],
        weights=tm_weights[current_state],
        k = 1
    )

    current_state = current_state[0]
