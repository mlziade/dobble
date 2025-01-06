# Double

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

Imagine a matrix in wich each value is either (1 or 0). Each row represents a card, and the columns represent images. If a column value on a row is 1, then that image is contained in the card.

Out of a universe of all combinations of cards (for example, all combination of 7 images out of 24 possibles) that are many sets of cards that we can generate that only have 1 image in common.

Depending on the total number of images and cards, this can start consuming a lot of memory. We can represent each image as a prime number, and more efficiantly store cards as products of primes. This might cost us more proccessing time (checking for division instead of looking up values on a matrix) but its a trade in the name of memory efficency.

Check the example below:

| Product | 2 | 3 | 5 | 7 | 11 | 13 | 17 |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | -----------
| 06 | 1 | 1 | 0 | 0 | 0 | 0 | 0
| 15 | 0 | 1 | 1 | 0 | 0 | 0 | 0
| 21 | 0 | 0 | 1 | 1 | 0 | 0 | 0

## Credits

- To my good friend [Carlos](https://www.linkedin.com/in/carloshdc/) for helping me design  this approach during a new year's travel after playing the game with the night before

- This project was based on the [Double](https://www.dobblegame.com/en/homepage/) game and a desire to understand how to programaticaly create any set that follow the rules stated above