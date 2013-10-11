What is it?
===========

csv2db.py is a simple program to import data into any database platform (which is supported by sqlalchemy).

What is it for?
===============

__Short answer:__

To help you

__Long answer:__ 

You have make a complex and perfect database structure. You have also finish the program, so it should work just fine. Later, you find that your client already has a primitive-worksheet data storage which is consist of thousands rows (usually in xls extension). Simply import csv into database is impossible since a row in the worksheet is related to several tables.

Look for this `normal` worksheet: 

| Transaction code  | Date          | Item code     | Item name     | Price        | Quantity     |
| :---------------- | :-----------: | :-----------: | :-----------: | :----------: | -----------: |
| T001              | 08/10/2013    | I001          | Candy         | $5           | 4            |
|                   |               | I002          | Chocolate     | $10          | 5            |
| T002              | 08/20/2013    | I004          | Coke          | $7           | 1            |
|                   |               | I001          | Candy         | $5           | 1            |


Pretty normal, right?

Now, you want to import the worksheet into 3 tables, `transaction`, `transaction_detail`, and `item`
The content of `transaction` will be:

| id  | Transaction code    | Date          |
| :-- | :---------------- : | ------------: |
| 1   | T001                | `2013-08-10`  |
| 2   | T002                | `2013-08-20`  |

The content of `item` will be:

| id  | Item code     | Item name     | Price       |
| :-- | :-----------: | :-----------: | ----------: |
| 1   | I001          | Candy         | 5           |
| 2   | I002          | Chocolate     | 10          |
| 3   | I004          | Coke          | 7           |

The content of `transaction detail` will be:

| id  | id_transaction   | id_item     | Quantity     |
| :-- | :--------------: | :---------: | -----------: |
| 1   | 1                | 1           | 4            |
| 2   | 1                | 2           | 5            |
| 3   | 2                | 3           | 1            |
| 4   | 2                | 1           | 1            |



Prerequisites
=============

* python 2.7
* sqlalchemy
* a functioning brain :)

How to use
==========

Look at test.py