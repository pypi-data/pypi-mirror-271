# Data transformation library
This project builds python library, containing data transformation functions. 
Library is supposed to be used by data-scientists.

# Project Description
The Python data transformation package is designed to assist with a common data 
transformation and manipulation tasks. Described data transformation package
provides three essential functions:
* **Transpose Data**: "transpose2d" function allows users to swap rows and columns in a matrix
(list of lists of float values). 
It’s particularly useful when you need to reorganize data for further analysis. 
For example:
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
* **Sliding Window**: "window1d" function creates a sliding window over a sequence of data (NumPy array).
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
* **Convolutional Matrix**: "convolution2d" function performs matrix convolution. 
Convolution is commonly used in image processing, signal analysis, and neural networks. In this package, 
it will be applied on 2D matrix(NumPy array) with possibility to define stride. 
Using this function, custom kernels could be applied on data. 
For example:
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
Project package is publised here: https://pypi.org/project/data-transformation-marta-miseke1/

Package is written using python 3.11 and it uses these packages with particular versions (allowing posibility 
to upgrade to the next minor version):
```
python = "~3.11"
numpy = "~1.26.4"
logging = "~0.4.9.6"
pytest = "~8.2.0"
```

# How to Install and Run the Project
Installation instruction assumes that package user is using Windows OS and poetry, since it is a prerequisite in the
project we currently work.
* **Install Poetry**: Open PowerShell and execute the following command:
```
curl -sSL https://install.python-poetry.org | python3 -
```
* **Create a new project using poetry**: In your IDE tool open the terminal and run command to create new project:
```
poetry new my_project_name
```
* **Install data-transformation library**: Using the terminal, enter created project and run this command to install
data-transformation package:
```
poetry add data-transformation-marta-miseke1
```

# How to Run Tests
Project contains 5 unit tests. To make sure that all features work correctly, tests could be run using command:
```
poetry run pytest
```

# How to Use the Package
To your created project, import DataTransformation class.
For example:
```
from data_transformation_marta_miseke1 import DataTransformation
```
**Examples of usage of library functions**:
```
    data = DataTransformation()
    transposed = data.transpose2d([[1.0, 2.0, 3.8], [4.0, 5.5, 6.4],
                                   [1.0, 2.0, 3.8], [4.0, 5.5, 6.4]])
    print('transposed matrix', transposed)
    window = data.window1d(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), 4, 1, 2)
    print('Sliding windows:',window)
    convolution = data.convolution2d(np.array(
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]),
        np.array([[10, 20], [40, 50]]), 2)
    print('convolutional matrix:',convolution)
```
# What could be improved next:
* More unit tests could be written, in order to perform better testing and cover more test cases
* More sophisticated algorithms could be used in package functions
