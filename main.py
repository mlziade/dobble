import math
import time
import itertools
import progressbar
from random import randint, sample
from cardnode import CardNode

## CONTANTS ##

DESIRED_NUMBER_OF_IMAGES = 10
DEFAULT_NUMBER_OF_IMAGES = 24 # Never change
TOTAL_NUMBER_OF_CARDS_IN_SET = 7
NUMBER_OF_IMAGES_IN_CARD = 3

# This is used to optimize the code as to not need to generate prime numbers programatically up to 24 (the games original rules)
# If the TOTAL_NUMBER_OF_IMAGES constant is HIGHER than 24, it generates more primes
# If the TOTAL_NUMBER_OF_IMAGES constant is SMALLER than 24, it splices the array
PRIME_NUMBERS = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89]

## FUNCTIONS ##

# Uses the Sieve of Eratosthenes (https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)
def generate_primes_sieve_of_eratosthenes(target_num_of_primes: int) -> list[int]:
    list_of_primes: list[int] = []
    count_primes_generated = 0

    # A hashmap in wich each value is a nom-prime number, and the values are arrays of primes that divide the key
    dict_of_composite_integers: dict = {} 
    current_num = 2 # Starts at the first prime number

    while count_primes_generated < target_num_of_primes:
        if current_num not in dict_of_composite_integers: # Its a prime number
            list_of_primes.append(current_num)
            dict_of_composite_integers[pow(current_num, current_num)] = [current_num]
            count_primes_generated += 1
        else: # Process composites and mark their next multiples
            for prime in dict_of_composite_integers[current_num]:
                dict_of_composite_integers.setdefault(prime + current_num, []).append(prime)
            del dict_of_composite_integers[current_num]
        current_num += 1
    
    return list_of_primes

# Alters the prime numbers vector based on the constants values and alters if necessary
def analyze_prime_vector(total_num_of_images: int) -> None:
    global PRIME_NUMBERS
    if DESIRED_NUMBER_OF_IMAGES < DEFAULT_NUMBER_OF_IMAGES:
        PRIME_NUMBERS = PRIME_NUMBERS[:DESIRED_NUMBER_OF_IMAGES]
    elif DESIRED_NUMBER_OF_IMAGES > DEFAULT_NUMBER_OF_IMAGES:
        PRIME_NUMBERS = generate_primes_sieve_of_eratosthenes(total_num_of_images)

def transform_card_tuple_into_product_of_primes(cards: tuple[int] | list[int]) -> int:
    product = 1
    for index, column in enumerate(cards):
        if column == 1:
            product *= PRIME_NUMBERS[index]
    return product

def reverse_product_of_primes_into_card_tuple(product: int) -> list[int]:
    card = [0 for _ in range(DESIRED_NUMBER_OF_IMAGES)]
    for index, prime in enumerate(PRIME_NUMBERS):
        if product % prime == 0:
            card[index] = 1
            product = product / prime
    return card

# Generates a total of 2^n - 1 numbers, where n is the number of digits
def iterative_binary_generator(number_of_digits: int):
    for i in range(2**number_of_digits):  # Iterate through all numbers from 0 to 2^n - 1
        binary = []
        for bit in range(number_of_digits):
            binary.insert(0, (i >> bit) & 1)  # Extract each bit
        yield binary

def check_gcd(a: int, b: int) -> int:
    return math.gcd(a,b)

def generate_random_card_array(number_images: int, total_number_of_images: int) -> list[int]:
    if number_images > total_number_of_images:
        raise ValueError("number_images cannot exceed total_number_of_images.")

    card = [0] * total_number_of_images

    ones_positions = sample(range(total_number_of_images), number_images)

    for pos in ones_positions:
        card[pos] = 1

    return card

# Recursive method that goes through all CardNodes, and for each:
# 1. Checks if the current_node path accepts the new card
#   1.1. If it accepts:
#       1.1.1 Calls yourself on children
#       1.1.2 Adds new card to node
#   1.2. If not:
#       1.2.1 Returns
def check_new_card_against_card_nodes(current_node: CardNode, path: list[int], new_card: CardNode, level: int):
    if new_card.value == current_node.value:
        return
    
    new_path = path + [current_node.value]

    # Use map to calculate the GCD of each card with current_card, and transform it into list
    gcds = map(lambda card: check_gcd(card, new_card.value), new_path)
    gcd_list = list(gcds)
    # print('List of gcds: [' + ', '.join(map(str, gcd_list)) + ']')
    # If at least one of the gcds is not a prime, than that card dosnt fit in the current set
    if set(gcd_list).issubset(PRIME_NUMBERS):
        if len(current_node.children) > 0:
            for child in current_node.children:
                check_new_card_against_card_nodes(child, new_path, new_card, level + 1)
        current_node.add_card(new_card)
        current_node.children[-1].update_level(level)
    else:
        return

def main():
    start = time.time()

    # widgets = [
    #     ' [', 
    #     progressbar.widgets.Timer(format='elapsed time: %(elapsed)s'), 
    #     '] ', 
    #     progressbar.widgets.Bar('*'), 
    #     ' (', 
    #     progressbar.widgets.ETA(), 
    #     ') ',
    # ]
    # max_value = pow(2, DESIRED_NUMBER_OF_IMAGES) - 1  # Assuming this is a valid number of iterations
    # bar = progressbar.ProgressBar(widgets=widgets, max_value=max_value).start()

    analyze_prime_vector(DESIRED_NUMBER_OF_IMAGES)
    print('Prime Numbers: ' + str(PRIME_NUMBERS))    

    # Initiates the Binary Tree of Cards, where each path to a leaf is a different set of cards
    root = None

    # Give root a random card
    root = CardNode(
        value = transform_card_tuple_into_product_of_primes(
            generate_random_card_array(
                NUMBER_OF_IMAGES_IN_CARD, DESIRED_NUMBER_OF_IMAGES
            )
        )
    )
    root.update_level(0)

    count = 0
    for binary_number in iterative_binary_generator(DESIRED_NUMBER_OF_IMAGES):
        # If it has a different number of 1's, its a invalid card
        if binary_number.count(1) != NUMBER_OF_IMAGES_IN_CARD:
            count += 1
            continue

        current_card: CardNode = CardNode(
            value = transform_card_tuple_into_product_of_primes(binary_number)
        )

        check_new_card_against_card_nodes(
            current_node = root,
            path = list(),
            new_card = current_card,
            level = 0,
        )

        print('Count: ' + str(count) + ' ---- ' + 'Binary Number: ' + str(binary_number))
        print('Current Card: ' + str(current_card.value))
        count += 1
        # bar.update(count)
        # print(root.get_paths_sizes())
        # print(root.get_paths_to_leaves())
        # input("Press Enter to continue...")
    
    end = time.time()
    elapsed_time = end - start
    print('Program Time: ' + str(elapsed_time))
    # bar.finish()

if __name__ == "__main__":
    main()