# <p align="center">PixCrypt</p>
### <p align="center">Library for encrypting text into an image</p>

## Usage
### Encrypting text to image
```py
from pixcrypt import PixImage

src = 'Hello World!'
pix = PixImage(text=src)
img = pix.getimage()

img.save('hello_world.png')
```
If you will be decrypting the image, save the file in PNG format. You can also specify a maximum width for the image:
```py
img = pix.getimage(max_width=12)
```
### Decrypting image into text
```py
from pixcrypt import PixImage

pix = PixImage('hello_world.png')
text = pix.getstr()

print(text) # Hello World!
```
```PixImage``` can take an Image class object from Pillow as an argument:
```py
pix = PixImage(text='some info')
pix2 = PixImage(pix.getimage())
text = pix2.getstr()

print(text) # some info
```
