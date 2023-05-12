
import random


# Load a large text
with open("milton-paradise.txt", 'r') as input_text:
    body = input_text.read().split()


# Create a transition matrix: find all possible next words for a given word by order in the script
transition_matrix = {}
for i in range(len(body)-1):
    if body[i] not in transition_matrix:
        transition_matrix[body[i]] = [body[i+1]]
    else:
        transition_matrix[body[i]].append(body[i+1])


# Special case for the last word in the input text
# Whatever word was last has the possibility of ending the while loop generating text at the end of the script
if body[-1] not in transition_matrix:
    transition_matrix[body[-1]] = None
else:
    transition_matrix[body[-1]].append(None)


# Create a dictionary which changes (duplicate) values from the transition matrix into weighted values
# Used to collapse duplicate values in the transition matrix, and to simultaneously iterate the transition matrix with at the end of the script
tm_weights = {}
for word, lst in transition_matrix.items():

    #print(word, lst)

    # If there is only one possible next word, add a single weight and continue
    if len(lst) == 1:
        tm_weights[word] = [1]
        continue

    # If all next possible words are the same, collapse to a single weight, add a weight and continue
    if all(lst[0] == lst[i] for i in range(len(lst))):
        transition_matrix[word] = [lst[0]]
        tm_weights[word] = [1]
        continue

    # For all possible next words, add weights based on occurrence
    _occurrences = {}
    for i in range(len(lst)):
        if lst[i] not in _occurrences:
            _occurrences[lst[i]] = 1
        else:
            _occurrences[lst[i]] += 1

    # Collapse (duplicate) words in transition_matrix[word] through _occurrences
    transition_matrix[word] = [w for w in _occurrences.keys()]

    # Make a list of words through _occurrences
    _weights = []
    for weight in _occurrences.values():
        _weights.append(weight)

    # Add corresponding weights to tm_weights[word]
    tm_weights[word] = _weights


# Now the transition_matrix holds only words, and tm_weights contains the weights for each word


# Get the first word out of the transition_matrix regardless
current_state = None
for word in transition_matrix.keys():
    current_state = word
    break

# While the random walks haven't encountered the possibility of ending the script, keep churning new words
while current_state is not None:
    print(current_state)

    # If only one possible next word, then immediately take the next word
    if len(tm_weights[current_state]) == 1:
        current_state = transition_matrix[current_state][0]
        continue

    # Get a random word from the transition matrix, weighted.
    # k = 1 (default)
    current_state = random.choices(
        transition_matrix[current_state],
        weights=tm_weights[current_state],
        k = 1
    )

    current_state = current_state[0]