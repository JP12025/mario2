# Mario 2

![double pyramid](https://cs50.harvard.edu/x/2024/psets/1/mario/more/pyramids.png)

# Le problème à résoudre

In “Super Mario Bros.” released in 1985, toward the beginning, Mario must hop over adjacent pyramids of blocks. In a file called `mario.py`, implement a program that recreates that pyramid, using `#` for bricks, as in the below:

```bash
$ python mario.py
Height: 8
       #  #
      ##  ##
     ###  ###
    ####  ####
   #####  #####
  ######  ######
 #######  #######
########  ########
```

First, prompt the user for an `int` for the pyramid’s actual height.
The height **must** be between 2 an 10.

```bash
$ python mario.py
Height: 4
   #  #
  ##  ##
 ###  ###
####  ####
```

Notice that width of the “gap” between adjacent pyramids is equal to the width of two hashes, irrespective of the pyramids’ heights.

> [!TIP]
> To transform `str` into `int`, simply use `int()`.

Re-prompt the user, again and again as needed, if their input is not correct.

```bash
$ python mario.py
Height: -3
Height: 15
Height: 3
  #  #
 ##  ##
###  ###
```

> [!TIP]
> To check that a string (`str`) contains only digits, you may use `isdigit()`. ([Doc str](https://docs.python.org/fr/3/library/stdtypes.html#str.isdigit))

# When to Do it

By Sunday, january 12, 2025 at 11:59 PM

# How to Test

- Test your script with command `./check [-v] mario.py`
- `-v` option gives the difference between what is expected and what your script prints

Don't forget it's important to test your program.
In fact, when you decide to test a program, you'll have to ask yourself questions about what your program does and what the special cases are.

What happens if the user input is :
* a negative number?
* 0 ?
* a positive number
* letters or words?
* nothing at all?

We tend to trust users' logic, but, when we write code, we have to imagine answers that don't follow any logic.

> "When you have eliminated the impossible, whatever remains, however improbable, must be the truth."
> Sherlock Holmes

# How to Submit

Once you're done with all tasks, submit all your python files on Moodle
