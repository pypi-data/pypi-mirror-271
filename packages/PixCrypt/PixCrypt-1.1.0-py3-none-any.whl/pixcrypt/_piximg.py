from PIL import Image
from string import printable
from math import ceil


class PixImage:
	def __init__(self,
				 img: str | Image.Image = ...,
				 text: str = ...) -> None:
		self._img = None
		self._text = text

		if isinstance(img, str):
			with Image.open(img) as i:
				i.load()
				self._img = i
		elif isinstance(img, Image.Image):
			self._img = img

	@property
	def image(self) -> Image.Image:
		return self._img

	@property
	def text(self) -> str:
		return self._text

	@staticmethod
	def _rgb(src: str) -> tuple:
		x = ord(src)
		x = int(bin(x).lstrip('0b'))
		x = hex(x).lstrip('0x')

		return tuple(int(x[i:i+2], 16) for i in (0, 2, 4))

	@staticmethod
	def _char(rgb: tuple) -> str:
		x = ''
		for i in rgb:
			if i == 0:
				x += '0'
				continue
			x += hex(i).lstrip('0x')
		x = int(x, 16)
		x = int(str(x), 2)

		return chr(x)

	def getimage(self, max_width: int = ...) -> Image.Image:
		"""
		Encrypts text into an image.

		:returns: Image class object from Pillow.
		"""

		l = len(self._text)
		width = l
		height = 1

		if max_width is not ...:
			width = max_width
			height = int(ceil(l / max_width))

		img = Image.new('RGB', (width, height))

		x = 0
		y = 0
		for i in range(l):
			if x >= width:
				x = 0
				y += 1

			index = printable.find(self._text[i])
			img.putpixel((x, y), self._rgb(printable[index]))
			x += 1

		return img

	def getstr(self) -> str:
		"""
		Decrypts an image into text.

		:returns: Decrypted string.
		"""

		s = ''
		width = self._img.size[0]
		height = self._img.size[1]

		x = 0
		y = 0
		for i in range(width * height):
			if x >= width:
				x = 0
				y += 1

			rgb = self._img.getpixel((x, y))
			x += 1

			if rgb == (0, 0, 0):
				continue

			s += self._char(rgb)

		return s
