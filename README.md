# Steganography

This script allows you to hide text in a digital image.  
To do this, it modifies the least significant bits of the RGB components of the image pixels.

# Examples

* Encode text "Hello" in the **test.png** image, the result will be stored in **test2.png** (The format option allows you to specify the format of the image that will be generated.):  
`steganography.py -e --infile /tmp/test.png --outfile /tmp/test2.png --format PNG -t Hello`

* Decode the text contained in **test2.png**:  
`steganography.py -d --infile /tmp/test2.png`

* List the supported image formats for  output's image:  
`steganography.py -l` 

# How it work

## General

A letter of the message is encoded in a pixel of the image.  
The pixels of the image are selected from left to right and from top to bottom.  
For minimal image alteration, the low-order bits of the pixel are modified.  
7 bits are required to encode an ASCII character:  
3 low order bits for the red component, 2 low order bits for the green component, and 2 low order bits for the blue component.  

## Example of modifying a pixel

The example is as follows:  
* **Letter** : A (code ASCII : 0b1000001)
* **White pixel** :
  * **Red** : 255 (in binary : 0b11111111)
  * **Green** : 255 (in binary : 0b11111111)
  * **Blue** : 255 (in binary : 0b11111111)

The pixel will be transformed as follows:
* **Red** : 252 (in binary : 0b11111100)
* **Green** : 252 (in binary : 0b11111100)
* **Blue** : 253 (in binary : 0b11111101)

The pixel can then be read as follows:
  ```ditaa {cmd=true args=["-E"]}
      R               G               B
  11111|100       111111|00       111111|01
       |                |               |
       +----------------+---------------+
                        |
                    100 00 01
  ```
