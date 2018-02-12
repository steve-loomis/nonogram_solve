# nonogram_solve

Solves nonograms, like the ones found at griddlers.net (among dozens of other places).

<p align="center"><img width=80% src="https://raw.githubusercontent.com/steve-loomis/nonogram_solve/master/Ex2.png"></p>

Here's a fairly simple example, with the inputs for the solver.

```shell
9x13x3
horiz
2g 2g
3g
5g
7g
7g
2r 3g 2r
1r 1g 2r 1g 2r 1g 1r
4r 1g 4r
2r 1g 1r 1g 1r 1g 2r
1g 3r 1g 3r 1g
4r 1g 4r
1r 1g 1r 1g 1r 1g 1r
2r 1g 2r
vert
3r 1g 1r
1g 2g 1r 1g 5r
1g 3g 3r 1g 2r 1g 1r
5g 7r
12g
5g 7r
1g 3g 3r 1g 2r 1g 1r
1g 2g 1r 1g 5r
3r 1g 1r
```

The inputs are fairly straightforward.  First, the dimensions of the puzzle.  That's 9 columns (or if you prefer, the rows are 9 squares long), 13 rows (i.e. columns 13 spaces tall), and 3 colors (there are only two colors shown in the row and column clues, but there's also a background color).

```shell
9x13x3
```

Then the row clues, starting with optional "horiz" and terminated by optional "vert".  Enter horiz and vert if it helps you keep track of where you are.  Don't enter them if you don't want to.

You have to pick a single character to represent the colors.  Here I went with g for the gray and r for the red.

```shell
horiz
2g 2g
3g
5g
7g
7g
2r 3g 2r
1r 1g 2r 1g 2r 1g 1r
4r 1g 4r
2r 1g 1r 1g 1r 1g 2r
1g 3r 1g 3r 1g
4r 1g 4r
1r 1g 1r 1g 1r 1g 1r
2r 1g 2r
```

Finally the column clues, with the same convention as the row clues.

```shell
vert
3r 1g 1r
1g 2g 1r 1g 5r
1g 3g 3r 1g 2r 1g 1r
5g 7r
12g
5g 7r
1g 3g 3r 1g 2r 1g 1r
1g 2g 1r 1g 5r
3r 1g 1r
```

Here's another simple example.

<p align="center"><img width=80% src="https://raw.githubusercontent.com/steve-loomis/nonogram_solve/master/Ex1.png"></p>

And the inputs for this one.

```shell
10x10x3
horiz
1b 1b 1b 1b
1b 1b 1b 1b
1b 2r 1b
4r 1b
1b 2r 2r 1b
1b 1r 1r 1b
1b 1b 4r 1b
1b 4r 1b
4r
1b 6r 1b
vert
1b 2b 1b
1b 1b 2b
1b 1r 1b 1r
7r
1b 2r 4r
1b 2r 4r
1b 7r
1r 1r
1b 2b
2b 1b 2b 1b
```

The solver uses a variety of solving techniques.  The simplest is to simply look at a row (or a column), find all the possible values for that row, and mark any squares which have the same value for all possibilities.

Slightly more advanced is to compare the intersection of each row and column against all possibile configurations for those clues and eliminate any color possibility which does not exist in both.  For example, the 3rd row might have no blue squares and the 5th column therefore can eliminate all possibilities in which the intersection with that row is blue.  In a similar case, perhaps that row has blue squares, but they cannot occur earlier than the 8th column.

These techniques yield partial information about the squares in a row (or column), which subsequently eliminate possible configurations in columns (or rows).

The solver attempts to use the techniques which are less computationally involved first, and presumably glean some information from those simpler techniques before moving on to more complicated ones.  Sometimes simple techniques can solve the entire puzzle.

As the puzzles get larger, they have potential to balloon a great deal for brute force approaches.  The total number of possible solutions for a row increases with the size of the row by factorials, and that gets hairy fast.  I'm percolating on ways to improve this by teaching the solver to ignore rows or columns entirely in the early iterations if they're going to result in massive brute force calculations.

Here's a couple more examples which are larger and require more iterations.  Depending on the speed of your rig, it might have to think a while about these.  Then again, you may have a much nicer computer than I do.

<p align="center"><img width=80% src="https://raw.githubusercontent.com/steve-loomis/nonogram_solve/master/Ex3.png"></p>

```shell
23x25x4
7k
1k 1b 3b 1b 1k
2k 2k
2k 4b 2k
2k 1b 3b 2k
1k 2b 1b 3b 2b 1k
1k 2b 5b 1r 3b 1k
1k 1k
15k
3k 1k 1k 3k
2k 1k 6b 1k 1k 1k 2k
1k 1k 1k 1k 1k 1k
1k 1k 6b 1k 1k 1k 1k
1k 1k 1k 1k 1k 1k
4k 4b 1k 1k 4k
1k 1k 1b 1b 1k 1k 1k 1k
1k 4k 1b 1b 3k 1k 1k
1k 1k 1k 1b 1b 1k 1k
1k 1k 1k 4b 1k 1k
1k 15k 1k
5k 5k
1k 1k 11k 1k 1k
1k 1k 1k 1k 1k 1k
1k 1k 1k 1k 1k 1k
5k 7k 5k
vert
3k
12k 1k
2k 1k 1k 1k
1k 1k 1k 1k
21k
2k 2b 1k 1k 2k
2k 2b 1k 1k 1k 1k
2k 1k 1b 1b 4k 1k
1k 1b 3b 1k 1b 1b 1k 1k 2k
1k 1b 1b 1k 1b 1b 5b 1k 2k 1k
1k 1b 1b 1b 1k 1b 1b 1b 1b 1k 1k 1k
1k 1b 4b 1k 1b 1b 1b 1b 1k 1k 1k
1k 1b 4b 1k 1b 1b 5b 1k 1k 1k
1k 2b 1r 1k 1k 2k 1k
1k 1b 9k 1k 1k 2k
2k 1b 1k 1k 1k 1k
2k 2b 9k 1k 1k
2k 2b 1k 2k
21k
1k 1k 1k 1k
2k 1k 1k 1k
12k 1k
3k
```

<p align="center"><img width=80% src="https://raw.githubusercontent.com/steve-loomis/nonogram_solve/master/Ex4.png"></p>

```shell
23x25x4
3k 3k
1k 1g 1k 1k 1g 1k
1k 1y 1k 1k 1y 1k
1k 1g 1k 1k 1g 1k
7k
1k 1y 1g 1y 1g 1y 1k
1k 1g 1y 1g 1y 1g 1k
9k
1k 1y 1k 1y 1k 1y 1k 1y 1k
1k 1y 1k 1y 1k 1y 1k 1y 1k
17k
1k 7g 1k 7g 1k
1k 2g 1k 1g 1k 2g 1k 2g 3k 2g 1k
1k 2g 1k 1g 1k 2g 1k 4g 1k 2g 1k
3k 1g 1k 1g 1k 1g 3k 1g 3k 1g 3k
1k 2g 1k 1g 1k 2g 1k 4g 1k 2g 1k
1k 2g 1k 1g 1k 2g 1k 2g 3k 2g 1k
3k 2g 1k 2g 3k 5g 3k
1k 7g 1k 7g 1k
17k
1k 1k 1k 1k 1k
5k 1k 5k 1k 5k
1k 3g 1k 1k 1k 3g 1k 1k 1k 3g 1k
1k 3g 1k 1k 3g 1k 1k 3g 1k
1k 1y 3k 1y 1k 1k 1y 3k 1y 1k 1k 1y 3k 1y 1k
vert
1k
3k 1y
1k 1k 1k 2g 1k
12k 2g 1k
1k 3g 1k 2g 1k 1g 1k 1k 2g 1k
1k 8g 1k 3k 1y
1k 1g 5k 2g 1k 1k
4k 6g 1k 1g 4k
8k 2y 1k 1g 5k 2g 1k 1k
1k 1g 1y 1g 1k 1y 1g 4k 8g 1k 3k 1y
5k 1g 1y 1k 2y 1k 3g 1k 2g 1k 1g 1k 1k 2g 1k
1k 1y 1g 15k 2g 1k
5k 1g 1y 1k 2y 1k 3g 1k 2g 1k 1g 1k 1k 2g 1k
1k 1g 1y 1g 1k 1y 1g 4k 8g 1k 3k 1y
8k 2y 1k 1g 1k 1g 1k 1g 1k 2g 1k 1k
4k 1g 1k 1g 1k 1g 1k 2g 4k
1k 1g 5k 2g 1k 1k
1k 8g 1k 3k 1y
1k 3g 1k 2g 1k 1g 1k 1k 2g 1k
12k 2g 1k
1k 1k 1k 2g 1k
3k 1y
1k
```


This one is a surprisingly difficult puzzle, a real tedious slog.  But tedium is why we automate.

<p align="center"><img width=80% src="https://raw.githubusercontent.com/steve-loomis/nonogram_solve/master/Ex5.png"></p>

```shell
25x15x3
1g 1g 6g 2g 3g
1g 1g 1g 1g 4g 1w
1g 1w 1g 1g 1g 2g 2g
1g 1g 1w 1g 4g
1g 2g 2w 2g 4g
1g 1g 2w 10g 3g
1w 1g 1g 1g 1w 1w 1g 2w 1g 2g 1w 1g
1w 1g 1w 1g 2w 5g 1g 1w 1g
1g 1g 1w 3g 1w 1g 1g 1w 1w 3g
1g 2g 1g 2g 1g 1g 1w 1g
3g 1w 1g 1g 3g 1w 2g 1g
1g 1w 2g 1w 1g 1g 4g 1g
1g 2g 1w 3g 1w 2g 1g 1w 2g 1w 1g
1w 1g 1g 1g 1g 1g 2g 1w 1g 2g
2g 4g 4g 2g 1w 1g
vert
3g 2w 1g 1g 1w 1g
1w 4g 2g
2g
6g 3g
4g 2w 3g 1g
1g 1w 1g 5g 2w 1g
1g 1g 2w 2g 3g
1g 2w 1g 2g
1g 1g 1w 1g 3w 4g
1g 2g 1w 2g 3w 1g
1g 1g 2g 1g 3g 1g
3g 3g 3g
1g 1w 1g
1g 1w 1g 2g
1g 2g 1g 1g 1g
1g 3g 1g 1g
1g 2g 1g 1w 1g
1g 2g 2g 2g
1g 2g 1w 2g 1w 1g
2g 2g 1w 3g 1w
1g 1w 1g 2g 1w 2g 1g
1g 1g 1g 1w 1w 2g 1w 1g
1g 1g 4g 1w 2g
1g 1g 2g
1g 2g
```

To try any of these puzzles on your own, simply type at the command line:

```shell
python nonogram_solve.py
```
and then enter the definitions above at the prompts.  Or find a new puzzle at the link above, and enter your own definition at the prompts.
