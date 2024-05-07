# Data transformation library
This project builds python library, containing data transformation functions. 
Library supposed to be used by data-scientists.

# Project Description
The Python data transformation package is designed to assist with common data 
transformation and manipulation tasks. Described data transformation package
provides three essential functions:
    - *Transpose Data*: "transpose2d" function allows user to swap rows and columns in a matrix
(list of lists of float values). It’s particularly useful when you need to reorganize data for further
analysis. For example:
```  
You have a matrix, which looks like:
    [[1.0, 2.0, 3.8],
     [4.0, 5.5, 6.4],
     [1.0, 2.0, 3.8], 
     [4.0, 5.5, 6.4]])
After applying "transpose2d" result matrix would look like:
    [[1.0, 4.0, 1.0, 4.0], 
     [2.0, 5.5, 2.0, 5.5], 
     [3.8, 6.4, 3.8, 6.4]]  
```

    - *Sliding Window*: "window1d" function creates a sliding window over a sequence of data (NumPy array).
Given a window size, shift and stride, it iterates through the data, providing overlapping subsets. 
For example:
```
You have an array: np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]
And you would like to get sliding windows of 4 elements each, containing every second element from the sequence
and shifting by 1 position each time.
After applying "window1d" function, received sliding windows would looke like:
    [[2 4 6 8]
        [3 5 7 9]]
```
    - *Convolutional Matrix*: "convolution2d" function performs matrix convolution. Convolution is commonly used
in image processing, signal analysis, and neural networks. In this package, it will be applied on 2D matrix 
(NumPy array) with possibility to define stride. Using this function, custom kernels could be applied on data:
```
You have a 2D matrix: 
        np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
You have a kernel matrix:
        np.array([[10, 20], [40, 50]])
And you decide that stride will be 2.
After applying "convolution2d" function, received convolutional matrix (sum of kernel multiplied by parts of the
input matrix) would look like:
    [[ 550.  790.]
     [1510. 1750.]]
```

# How to Install and Run the Project
Package could 
Installation instruction assumes that package user is using Windows OS and poetry, since it is a prerequisite in the
project we currently work.

    - 1. *Install Poetry*: Open PowerShell and execute the following command:
```
curl -sSL https://install.python-poetry.org | python3 -
```
    - 2. *Add Poetry to your %PATH% environment variable: This can be done by going to Settings -> "Edit the system 
environment variables" -> Environment Variables -> User Variable -> New and setting the Name as POETRY_HOME and the 
Value as the path to your Poetry installation.

    - 3. *Create a new project using poetry*: In your IDE tool open the terminal and run command to create new project:
```
poetry new my_project_name
```
    - 4. *Install data-transformation library*: Using the terminal, enter created project and run this command to install
data-transformation package:
poetry add data-transformation-marta-miseke1




pip install data-transformation-marta-miseke1

If you are working on a project that a user needs to install or run locally in a machine like a "POS", you should include the steps required to install your project and also the required dependencies if any.

Provide a step-by-step description of how to get the development environment set and running.

5. How to Use the Project
Provide instructions and examples so users/contributors can use the project. 
6. This will make it easy for them in case they encounter a problem – they will always have a place
7. to reference what is expected.

You can also make use of visual aids by including materials like screenshots to show examples of the running project and also the structure and design principles used in your project.

Also if your project will require authentication like passwords or usernames, this is a good section to include the credentials.



10. Include Tests
Go the extra mile and write tests for your application. Then provide code examples and how to run them.

This will help show that you are certain and confident that your project will work without any challenges, which will give other people confidence in it, too

Extra points
Here are a few extra points to note when you're writing your README:

Keep it up-to-date - It is a good practise to make sure your file is always up-to-date. In case there are changes make sure to update the file where necessary.
Pick a language - We all come from different zones and we all speak different languages. But this does not mean you need to translate your code into vernacular. Writing your README in English will work since English is a globally accepted language. You might want to use a translator tool here if your target audience isn't familiar with English.