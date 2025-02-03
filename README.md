# Steganography

This script allows you to hide text in a digital image. \\
To do this, it modifies the least significant bits of the RGB components of the image pixels.

# Examples

* Encode text "Hello" in the **test.png** image, the result will be stored in **test2.png** (The format option allows you to specify the format of the image that will be generated.):  
`steganography.py -e --infile /tmp/test.png --outfile /tmp/test2.png --format PNG -t Hello`

* Decode the text contained in **test2.png**:  
`steganography.py -d --infile /tmp/test2.png`

* List the supported image formats for  output's image:  
`steganography.py -l` 
