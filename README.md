# PNGMark

This is a simple python library for planting/extracting/detecting data in the LSB plane of a png image

`NDArraySequenceManipulator` is a Python class for handling sequences of data (in bytes format) written into and read from NumPy arrays. The class operates in a bit-level granularity, and has support for including or excluding headers, allowing for flexible usage.

The class is designed for use with 8-bit sequences and works in conjunction with the utility classes `BitManipulator` and `BitmanIO`.

## Prerequisites:

Ensure that you have `numpy` installed:

```bash
pip install numpy
```

## Usage:

### Initialization:

```python
import bitman

manipulator = bitman.NDArraySequenceManipulator()
```

### Important Methods:

#### 1. `write_sequence(data: bytes, image: np.array, header=True) -> np.array:`

Write a sequence of bytes into a NumPy array. This method embeds the data into the flattened form of the image, and then reshapes the image back to its original shape.

- **Parameters**:
  - `data`: The bytes data to be written.
  - `image`: The NumPy array where the data will be written.
  - `header` (default: True): If True, includes a 8-byte header denoting the length of data.

- **Returns**: A NumPy array with the embedded data.

```python
data = b'Hello World'
image = np.zeros((100, 100), dtype=np.uint8)

new_image = manipulator.write_sequence(data, image)
```

#### 2. `write_max_sequence(data: bytes, image: np.array, header=True) -> np.array:`

Writes the given data into the image repeatedly until the maximum possible sequence length for the given image size is reached.

- **Parameters**: 
  - Same as `write_sequence`.

- **Returns**: A NumPy array with the repeated embedded data.

```python
data = b'AB'
image = np.zeros((100, 100), dtype=np.uint8)

new_image = manipulator.write_max_sequence(data, image)
```

#### 3. `read_sequence(image: np.array, header=True) -> bytes:`

Reads a sequence of bytes from a given NumPy array. If the header flag is set to True, it will first read an 8-byte header to determine the length of the data to be read.

- **Parameters**:
  - `image`: The NumPy array from which data will be read.
  - `header` (default: True): If True, reads a 8-byte header to determine the length of data. Otherwise, reads until the end of the sequence.

- **Returns**: Extracted bytes data.

```python
data = b'Hello World'
image = np.zeros((100, 100), dtype=np.uint8)
new_image = manipulator.write_sequence(data, image)

extracted_data = manipulator.read_sequence(new_image)
print(extracted_data)  # b'Hello World'
```

#### Other Utility Methods:

- `get_max_sequence_length(image: np.array) -> int`: Returns the maximum sequence length (in bytes) that can be embedded into the given NumPy array.

```python
image = np.zeros((100, 100), dtype=np.uint8)
max_len = manipulator.get_max_sequence_length(image)
print(max_len)  # 1250
```
