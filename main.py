import math
import time
import itertools
from random import randint

## CONTANTS ##

DESIRED_NUMBER_OF_IMAGES = 24
DEFAULT_NUMBER_OF_IMAGES = 24
TOTAL_NUMBER_OF_CARDS_IN_SET = 52
NUMBER_OF_IMAGES_IN_CARD = 7

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
def analyze_prime_vector(total_num_of_images: int):
    global PRIME_NUMBERS
    if len(PRIME_NUMBERS) < DEFAULT_NUMBER_OF_IMAGES:
        PRIME_NUMBERS = PRIME_NUMBERS[:DESIRED_NUMBER_OF_IMAGES]
    elif len(PRIME_NUMBERS) > DEFAULT_NUMBER_OF_IMAGES:
        PRIME_NUMBERS = generate_primes_sieve_of_eratosthenes(total_num_of_images)

def transform_card_tuple_into_product_of_primes(card_tuple: tuple[int]) -> int:
    product = 1
    for index, column in enumerate(card_tuple):
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

def iterative_binary_generator(number_of_digits: int):
    for i in range(2**number_of_digits):  # Iterate through all numbers from 0 to 2^n - 1
        binary = []
        for bit in range(number_of_digits):
            binary.insert(0, (i >> bit) & 1)  # Extract each bit
        yield binary

def check_gcd(a: int, b: int) -> int:
    return math.gcd(a,b)

def print_cards_formatted(matrix: list[list[int]]):
     for row in matrix:
        print(" ".join(map(str, row)))

def main():
    start = time.time()
    # Creates a set of cards to have a 0(1) look-up cost
    set_of_cards: set[int] = set()

    count = 0
    for binary_number in iterative_binary_generator(DESIRED_NUMBER_OF_IMAGES):
        # If it has a different number of 1's, its a invalid card
        if binary_number.count(1) != NUMBER_OF_IMAGES_IN_CARD:
            continue

        current_card = transform_card_tuple_into_product_of_primes(binary_number)
        # If its the first card, add it
        if len(set_of_cards) == 0:
            set_of_cards.add(current_card)
        # If the set is full, break the loop
        elif len(set_of_cards) == TOTAL_NUMBER_OF_CARDS_IN_SET:
            break
        # Verify if the card can be added to the set
        else:            
            # Use map to calculate the GCD of each card with current_card, and transform it into list
            gcds = map(lambda card: check_gcd(card, current_card), set_of_cards)
            gcd_list = list(gcds)
            # print('List of gcds: [' + ', '.join(map(str, gcd_list)) + ']')
            # If at least one of the gcds is not a prime, than that card dosnt fit in the current set
            if set(gcd_list).issubset(PRIME_NUMBERS):
                set_of_cards.add(current_card)
        
        # print('Count: ' + str(count) + ' ---- ' + 'Binary Number: ' + str(binary_number))
        # print('Current Card: ' + str(current_card))
        count += 1
    
    final_cards_as_matrix = list(map(reverse_product_of_primes_into_card_tuple, set_of_cards))
    print('Final set of cards:')
    print_cards_formatted(final_cards_as_matrix)
    
    end = time.time()
    elapsed_time = end - start
    print('Program Time: ' + str(elapsed_time))

if __name__ == "__main__":
    main()