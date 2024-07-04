# Coin Detection Software

This python script employs a number of image processing techniques to count and outline flat coins in an image with varying levels of success based on the properties of the image.
I designed this program as an initial exploration of image processing techniques to identify objects in an image, therefore it is not perfect and can only handle more obvious cases without breaking down.

The program takes images such as...

![A picture of some coins lying flat on paper next to a complex block of text](https://github.com/Ben-G-Man/Coin-Detection-Algorithm/blob/main/Images/easy_case_6.png)

...And returns...

![The above coin picture with each coin marked by a red rectangle outlining their size](https://github.com/Ben-G-Man/Coin-Detection-Algorithm/blob/main/output_images/easy_case_6_with_bbox.png)
