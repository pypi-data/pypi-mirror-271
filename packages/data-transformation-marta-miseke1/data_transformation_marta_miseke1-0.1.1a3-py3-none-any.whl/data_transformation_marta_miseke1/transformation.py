import numpy as np
import logging


class DataTransformation:
    """
    A class for data transformation.
    """
    def setup_logging(log_filename: str = 'my_app.log') -> logging.Logger:
        """
        Sets up the logger for logging messages to a file.
        Args:
            log_filename (str): The desired log file name.
        Returns:
            logging.Logger: Logger instance.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        # Create a file handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    @staticmethod
    def transpose2d(input_matrix: list[list[float]]) -> list:
        """
        Transposes a 2D matrix of float values (list of lists).
        Args:
            input_matrix (list[list[float]]): The input matrix to be transposed.
        Returns:
            list: The transposed matrix.
        """
        # Validate input_matrix
        for row in input_matrix:
            for element in row:
                if not isinstance(element, float):
                    raise ValueError('Input matrix should contain only floats.')
        if (min(len(row) for row in input_matrix) !=
                max(len(row) for row in input_matrix)):
            raise ValueError('Input matrix is not 2D matrix, rows has different'
                             ' number of elements')
        my_logger = DataTransformation.setup_logging()
        my_logger.info(f'Provided input matrix:{input_matrix}')
        try:
            transposed_matrix = []
            a = min(len(row) for row in input_matrix)
            b = len(input_matrix)
            i = 0
            while i != a:
                j = 0
                tranposed_line = []
                while j != b:
                    tranposed_line.append(input_matrix[j][i])
                    j += 1
                transposed_matrix.append(tranposed_line)
                i += 1
            my_logger.info(f'Transposed matrix:{transposed_matrix}')
            return transposed_matrix
        except Exception as e:
            my_logger.info(f'Error during matrix transposition: {e}')
            return None

    def window1d(self, input_array: np.ndarray, size: int, shift: int = 1,
                 stride: int = 1) -> np.ndarray:
        """
        Creates a sliding window over a 1D input array.
        Args:
            input_array (np.ndarray): The 1D input array.
            size (int): The size of the sliding window.
            shift (int, optional): The step size for shifting the window
                                    (default is 1).
            stride (int, optional): The step size for selecting elements within
                                    the window (default is 1).
        Returns:
            np.ndarray: A matrix of overlapping windows extracted from the input
                        array.
        """
        # Validate input_array
        if not isinstance(input_array, np.ndarray):
            raise ValueError('Input must be a NumPy array')
        try:
            window_matrix = []
            a = len(input_array)
            if size > a or stride > a or shift > a:
                raise ValueError('Defined size or stride or shift is larger than'
                                 ' the provided input array')
            else:
                j = 0
                while j <= size:
                    shifted = input_array[j:]
                    if len(shifted) >= size:
                        strided = shifted[stride-1::stride]
                        sized = strided[:size]
                        if len(sized) == size:
                            window_matrix.append(sized)
                        j += shift
            my_logger = DataTransformation.setup_logging()
            my_logger.info(f'Sliding window: {window_matrix}')
            return np.array(window_matrix)
        except Exception as e:
            my_logger.error(f'Error during creation of sliding window: {e}')
            return None

    def convolution2d(self, input_matrix: np.ndarray, kernel: np.ndarray,
                      stride: int = 1) -> np.ndarray:
        """
        Applies 2D convolution to an input matrix using the given kernel.
        Args:
            input_matrix (np.ndarray): The input 2D matrix.
            kernel (np.ndarray): The convolution kernel (2D filter).
            stride (int, optional): The step size for shifting the kernel
                                    (default is 1).
        Returns:
            np.ndarray: A matrix resulting from the 2D convolution.
        """
        if not (isinstance(input_matrix, np.ndarray) or
                isinstance(kernel, np.ndarray)):
            raise ValueError('Input must be a NumPy array')
        kernel_height, kernel_width = kernel.shape
        input_height, input_width = input_matrix.shape
        convolution_matrix = (
            np.zeros(((input_height - kernel_height + stride) // stride,
                      (input_height - kernel_height + stride) // stride)))
        try:
            if kernel_width > input_width or kernel_height > input_height:
                raise ValueError('Kernel is bigger than input matrix')
            else:
                for i in (range
                    ((input_height - kernel_height + stride) // stride)):
                    for j in (range((input_height - kernel_height + stride)
                                    // stride)):
                        input_trimmed = input_matrix[i * stride:
                                                     i * stride + kernel_width,
                                                     j * stride:
                                                     j * stride + kernel_width]
                        print('Matrix, which will be multiplied by kernel:',
                              input_trimmed)
                        convolution_matrix[i, j] =\
                            (input_trimmed * kernel).sum()
            my_logger = DataTransformation.setup_logging()
            my_logger.info(f'Convolution matrix: {convolution_matrix}')
            return np.array(convolution_matrix)
        except Exception as e:
            my_logger.error(f'Error during creation of convolution matrix: {e}')
            return None
