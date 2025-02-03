#!/usr/bin/python3

import sys
import argparse
from PIL import Image

class Steganography:

  @staticmethod
  def __load_image(image):
    with Image.open(image) as img:
      img.load()
      return img
    return None

  @staticmethod
  def __load_txt(text):
    res = []
    for c in text:
      code = ord(c)
      tuple_code = ((code >> 4) & 0b111, (code >> 2) & 0b11, code & 0b11)
      res.append(tuple_code)
    return res

  @staticmethod
  def __get_coord_image(image, idx):
    width, height = image.size
    x = int(idx % width)
    y = int(idx / width)
    return (x, y)

  @staticmethod
  def __check_text_image(image, text):
    width, height = image.size
    if len(text) < ((width * height) - 1):
      return True
    return False

  @staticmethod
  def __encode_bytes(pixel, char):
    byte1 = pixel[0] & 0b11111000
    byte1 = byte1 | char[0]
    byte2 = pixel[1] & 0b11111100
    byte2 = byte2 | char[1]
    byte3 = pixel[2] & 0b11111100
    byte3 = byte3 | char[2]
    return (byte1, byte2, byte3)

  @staticmethod
  def __decode_bytes(pixel):
    byte1 = pixel[0] & 0b111
    byte2 = pixel[1] & 0b11
    byte3 = pixel[2] & 0b11
    value = byte1 << 2
    value = (value | byte2) << 2
    value = value | byte3
    return chr(value)

  @staticmethod
  def __read_text_image(image):
    width, height = image.size
    for i in range(0, width * height):
      char = Steganography.__decode_bytes(image.getpixel(Steganography.__get_coord_image(image, i)))
      if char == '\0':
        print("")
        break
      else:
        print(char, end="")

  @staticmethod
  def __write_text_image(image, text):
    if Steganography.__check_text_image(image, text):
      tuple_arr = Steganography. __load_txt(text)
      i = 0
      for t in tuple_arr:
        pix = image.getpixel(Steganography.__get_coord_image(image, i))
        image.putpixel(Steganography.__get_coord_image(image, i), \
          Steganography.__encode_bytes(pix, t))
        i += 1
      image.putpixel(Steganography.__get_coord_image(image, i), \
        Steganography.__encode_bytes(pix, (0, 0, 0)))

  @staticmethod
  def __get_available_formats():
    Image.init()
    return Image.ID

  @staticmethod
  def __check_format(format):
    format = format.upper()
    if format not in Steganography.__get_available_formats():
      return False
    match format:
      case 'JPEG'   | \
           'BLP'    | \
           'BUFR'   | \
           'CUR'    | \
           'FITS'   | \
           'FLI'    | \
           'FPX'    | \
           'FTEX'   | \
           'GBR'    | \
           'GIF'    | \
           'GRIB'   | \
           'HDF5'   | \
           'ICNS'   | \
           'ICO'    | \
           'MSP'    | \
           'PCD'    | \
           'PIXAR'  | \
           'SPIDER' | \
           'SUN'    | \
           'WEBP'   | \
           'WMF'    | \
           'XBM'    | \
           'XPM'    | \
           'XVTHUMB' :
        return False
      case _:
        return True

  @staticmethod
  def __list_formats():
    formats = Steganography.__get_available_formats()
    print("Formats availables :")
    for format in formats:
      if Steganography.__check_format(format):
        print(format)

  @staticmethod
  def __encode_image(infile, outfile, text, format=None):
    image = Steganography.__load_image(infile)
    if format is None:
      format = image.format
    if Steganography.__check_format(format) is False:
      print("Format \"{0}\" is not supported.".format(format))
      sys.exit(2)
    Steganography.__write_text_image(image, text)
    image.save(outfile, format)

  @staticmethod
  def __decode_image(file):
    image = Steganography.__load_image(file)
    Steganography.__read_text_image(image)

  @staticmethod
  def __check_args(args):
    if args.list is True:
      return True
    elif args.encode is True and args.decode is True:
      print("--decode can't be used when --encode is assigned.")
      return False
    if args.encode is True and args.text is not None and args.infile is not None and args.outfile is not None:
      return True
    elif args.encode is True:
      print("--encode option need --text, --infile and --outfile assigned.")
    if args.decode is True and args.infile is not None:
      return True
    elif args.decode is True:
      print("--decode option need --infile assigned.")
    return False

  @staticmethod
  def __parse_args():
    parser = argparse.ArgumentParser(prog="steganography.py")
    parser.add_argument('-e', '--encode', action='store_true')
    parser.add_argument('-d', '--decode', action='store_true')
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('--infile', type=str)
    parser.add_argument('--outfile', type=str)
    parser.add_argument('--format', type=str)
    parser.add_argument('-t', '--text', type=str)
    args = parser.parse_args()
    if Steganography.__check_args(args) is False:
      parser.print_help()
      sys.exit(1)
    return args

  @staticmethod
  def main(args):
    args = Steganography.__parse_args()
    if args.list:
      Steganography.__list_formats()
    elif args.decode:
      Steganography.__decode_image(args.infile)
    elif args.encode:
      if args.format is not None:
        Steganography.__encode_image(args.infile, args.outfile, args.text, args.format)
      else:
        Steganography.__encode_image(args.infile, args.outfile, args.text)

if __name__ == "__main__":
  Steganography.main(sys.argv)
