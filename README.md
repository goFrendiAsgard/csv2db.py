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

| id  | code     | date          |
| :-- | :------: | ------------: |
| 1   | T001     | 2013-08-10    |
| 2   | T002     | 2013-08-20    |

The content of `item` will be:

| id  | code     | name          | price       |
| :-- | :------: | :-----------: | ----------: |
| 1   | I001     | Candy         | 5           |
| 2   | I002     | Chocolate     | 10          |
| 3   | I004     | Coke          | 7           |

The content of `transaction detail` will be:

| id  | id_transaction   | id_item     | qty     |
| :-- | :--------------: | :---------: | ------: |
| 1   | 1                | 1           | 4       |
| 2   | 1                | 2           | 5       |
| 3   | 2                | 3           | 1       |
| 4   | 2                | 1           | 1       |



Prerequisites
=============

* python 2.7
* sqlalchemy
* a functioning brain :)

How to use
==========

* If your file is in either `xls` or `ods` extension, you must convert them into `csv` (i.e: By using `File|Save As` menu).
  The `csv` file is still readable and editable by your office program. In addition, the csv can also be viewed as `text file`

* Here is the `csv` of the previous worksheet example:
    ```
    Transaction Code,Date,Item Code,Item Name,Price,Quantity
    T001,08/10/13,I001,Candy,$5.00,4
    ,,I002,Chocolate,$10.00,5
    T002,08/20/13,I003,Coke,$7.00,1
    ,,I001,Candy,$5.00,1
    ```

* Make a python script just as in `test.py`

* Run your python script