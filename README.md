This is our project for the course CZ1003: Introduction to Computational Thinking at NTU

** Special module packages needed to be install
1) pygame
2) pandas
3) numpy
4) openpyxl
4) googlemaps (python 3)
5) base64

** Instruction

* All the materials needed for the program are divided into different parts (images, data,...)
Please put download all of them in the same folder in order to make sure the codes run well.
- The main program is run on project.py, other files must come along with the main file to ensure the inner
codes work well.

- Make sure that your computer is connected to internet to allow the google map api direction work. Otherwise,
if you click the "Show direction" button, errors will occur (api would not work)

- To use direction function, you also need to use Google Map API Key.

- About the SpellChecker, because its database is quite small, it only can suggest words which are reasonably similar
to the user input.

- Log in section:
	+ Username: a
	+ Password: a
  You can see an excel file named "Admin" which has the valid users, but all of the usernames and passwords are
encoded (to increase security) by base64 (just basic encoding strings to bits).
 Now you cannot have new accounts by creating accounts in the program, but you can encode username and password
separately and take them to the "Admin" excel file.

- The database is almost not true to the reality, especially for the price. It is used only for testing the program.
If you have the correct data, change it to our data format (in excel) and it would highly likely work.

- If you want to see the switching between pages in the menu, we recommend you to choose fast food -> McDonald's
to see how you can switch between 25 pages of dishes in the McDonald's menu.

- Most of the clicks the program is the left-click. The scroll bar appearing in the direction instruction can be
controlled with wheel on the mouse.

** Contact
If there are some errors or questions, please email our group at phatdat001@e.ntu.edu.sg


