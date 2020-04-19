#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SAPAMS.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

'''
Information that demonstrates your understanding of the limitations of finite data representations in the computer

There are several datatypes available by default in python, which each have their specific use cases.

byte
----
Explanation
  A byte is 8 bits, or 1s and 0s (binary), and bytes can be combined to create more complex data types. 1 byte can hold 256 values since 2^8 = 256, and these values can be
  from anywhere between 0 to 255. 
Pros
  Very fundemental in nature, which allows them to be understood at the computer hardware level; can be put in series to store a variety of information types. 
Limitations
  Limit of 255 possible states; not very good at storing more complex data. Also difficult for humans to understand at first glance, which is why we use other data types to
  store our data rather than leave everything as bytecodes.  

str
---
Explanation
  Strings are sequences of characters; this can include letters of alphabets, numbers, and special characters. For example, a person's name, which is alphabetical in nature,
  would most likely be stored in a string.
Pros
  Can be used to represent practically anything; generally easy for humans to read and understand. There are widely-accepted standards for strings, such as UTF-8, which make
  using and displaying strings easy across platforms.
Limitations
  Mathematical operations cannot be done on numbers that are stored in strings, since it is being stored as a character and not a quantity.

int
---
Explanation
  An integer is a positive or negative whole number. For example, -50, -2, 0, 1, 100, and 123456789 are all valid integers.
Pros
  Integers can be used in mathematical calculations, since they represent a quantity and not just characters like strings do.
Limitations
  Integers cannot hold decimal values, which makes precise mathematical calculations difficult/impossible.

float
-----
Explanation
  A float, or floating point number, is a real number. It is similar to an integer, but functions in a slightly different way that makes use of scientific notation.
Pros
  Decimal values can be stored in floating point numbers; very efficient and effective for performing computations with extremely large and small values
Limitations
  Sometimes results in floating point rounding errors, which occur because floating point arithmetic revolves around significant digits and does not understand recurring
  digits. For example, the computer will add 1/3 + 1/3 + 1/3 to be 0.3333 + 0.3333 + 0.3333 = 0.9999 rather than 1 as a human would, since it runs out of digits and 
  doesn't understand math the same way a human does. These miniscule errors result in floating point numbers being difficult to work with in simpler scenarios, like
  dealing with money. Essentially, you don't need to tell someone that they have $220.45000000001 in their bank account, you would prefer to just tell them that
  they have $220.45, but floating point mathematics gives programmers these errors that we have to handle appropriately.

Researched from the YouTube channel 'Computerphile': https://www.youtube.com/watch?v=PZRI1IfStY0

object
------
Explanation
  An object is a special data type that can be created by a programmer to fulfill a specific task. An object can contain attributes, which are essentially
  variables of the other types outlined in this explanation (str, int, float, bool, etc) as well as methods. 
Pros
  Allow for great flexibility with data; allows data encapsulation; makes handling large quantities of pattern-following data easier to work with.
Limitations
  Difficult to learn in certain languages, lots of references to "self" or "this" can make programs hard to understand, require extensive documentation,
  poor implementation can result in computational costs increasing.

boolean
-------
Explanation
  Boolean variables have two possible states; True and False. True can be understood as "1" or "closed circuit" at the computer level. False can
  be understood as "0" or "open circuit" at the computer level. Booleans allow programmers to compare data and perform tasks if certain conditions
  are met.
Benefits
  Conditional statements have booleans at their core, and are a critical aspect to computer programming. They allow logic processing to occur on computers.
Limitations
  Having only two states means that booleans cannot easily be used to store more complex data types.
'''