# Dobble

## Objective

Create a set of cards that contains a number of images. Each card can have only one image in common with any other card of the set

## Definitions & Equations

1. Number of Symbols per Card (**n**)

This is the number of unique symbols present on each card. It is an adjustable parameter but must be consistent across all cards.

2. Number of Cards (**m**)

This refers to how many cards are in the deck. The number of cards is determined by the number of symbols per card and is calculated using a combinatorial design.

3. Total Number of Symbols (**S**)

This is the total number of unique symbols available for use in the deck. It is typically set at the beginning, and the deck configuration must ensure that the total number of symbols used does not exceed this value.

4. Equations

    - Number of Cards (m):

        $m = n^2 - n + 1$

        where *n* is the number of symbols per card.

    - Total Symbols Used:

        $n \times m$

        Ensure this is less than or equal to the total available symbols SS.

    - Constraint:

        $n \times m \leq S$


## Algorithm

To generate a valid set of cards, we treat each card as a row in a matrix, where each column represents a symbol. The matrix values are either 1 or 0. If a matrix entry is 1, it means the corresponding symbol is present on the card; if it’s 0, the symbol is absent.

Out of the universe of possible combinations of cards (for example, all combinations of 7 images out of 24 possible symbols), there are multiple sets that can be generated with the constraint that every pair of cards shares exactly one symbol in common.

However, as the number of symbols and cards increases, storing all possible combinations in a matrix becomes memory-intensive. To optimize memory usage, we can represent each symbol as a prime number, and then each card can be stored as the product of primes corresponding to the symbols present on that card. This approach reduces memory consumption significantly, though it may come at the cost of additional processing time, as checking for common symbols requires division operations rather than simple lookups in the matrix.

Here’s an example of how this works:

| Product | 2 | 3 | 5 | 7 | 11 | 13 | 17 |
|---------|---|---|---|---|----|----|----|
| 6       | 1 | 1 | 0 | 0 | 0  | 0  | 0  |
| 15      | 0 | 1 | 1 | 0 | 0  | 0  | 0  |
| 21      | 0 | 0 | 1 | 1 | 0  | 0  | 0  |

In this table:
- The card with a product of 6 corresponds to symbols 2 and 3.
- The card with a product of 15 corresponds to symbols 3 and 5.
- The card with a product of 21 corresponds to symbols 5 and 7.

To explore different valid sets of cards, we use a tree structure. Each node represents a card, and each card has an array of child nodes representing other cards. The path from the root to any node represents a set of cards. For example, one path might correspond to the set of cards [6, 15, 21].

This approach enables us to efficiently manage the complexity of generating and storing multiple sets of cards while maintaining the constraints of the game.

## Credits

- To my good friend [Carlos](https://www.linkedin.com/in/carloshdc/) for helping/inspiring me to this approach

- This project was based on the [Dobble](https://www.dobblegame.com/en/homepage/) game and a desire to understand how to programaticaly create any set that follow the rules stated above