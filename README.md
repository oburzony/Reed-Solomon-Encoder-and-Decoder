# Reed-Solomon Encoder/Decoder
Welcome to the Reed-Solomon encoder and decoder project repository!

<img width="1200" alt="image" src="Rerad-image\image-program.png">

## Description
This project provides an implementation of the Reed-Solomon (15,9) code encoder and decoder. The Reed-Solomon code is capable of encoding and decoding input data, with a codeword size of 15 units, where 9 units represent the input data. Each unit consists of 4 bits and serves as a coefficient of the polynomial. The program operates on a Galois field of size 2^4 (16 elements) and has an error correction capability of detecting and correcting up to 3 errors in data transmission.

## Features

- **Reed-Solomon Encoder/Decoder:** Complete implementation of the Reed-Solomon (15,9) code encoder and decoder.
  
- **Input Data Support:** Ability to process input data consisting of 9 information units.

- **Polynomial Encoding:** Encoding and decoding of input data using polynomial representation.

- **Galois Field Operations:** Utilization of mathematical operations on a Galois field of size 2^4.

- **Error Correction:** Capability to detect and correct up to 3 errors in data transmission.

- **User Interface:** A simple user interface facilitates data input, encoding, decoding, and result display.

## Usage

To utilize the Reed-Solomon Encoder/Decoder, follow these steps:

1. Clone the repository.
2. Input your data consisting of 9 information units.
3. Encode the data to generate the codeword.
4. Optionally, simulate errors in the transmission of the data.
5. Decode the received data to recover the original information.

## License 
This project is licensed under the MIT License. You are free to use, modify, and distribute the code as per
the terms of the license.

