import tkinter as tk
import os

IMAGE_MARKERS = {
	"JPG": (b"\xff\xd8", b"\xff\xd9"),  # 0th is BOF, 1st is EOF
	"b": ("b", "g")
}

WOLFE_BOF = b"\xff\x77"
WOLFE_EOF = b"\xff\x66"


def image_filetype(file):
	file.seek(-2, 2)  # additional argument specifies positioning; this moves to two bytes before EOF
	eof_marker = file.read(2)

	file.seek(0)
	bof_marker = file.read(2)
	marker_type = None
	for k, v in IMAGE_MARKERS.items():
		if bof_marker in v:
			marker_type = k
	if not marker_type:
		raise ValueError(f"Image not of supported image type (expected BOF marker in {IMAGE_MARKERS.values()}, found {bof_marker})")

	if eof_marker != WOLFE_EOF:
		assert(IMAGE_MARKERS[marker_type][1] == eof_marker)  # sanity check
		return marker_type, None
	else:
		return marker_type, "wolfed"


def _reverse_read(file, size: int, chunk_size=4):
	# NOTE: FUNCTION ONLY WORKS FOR MULTIPLES OF CHUNK_SIZE, FLOORED FROM SIZE TO NEAREST MULTIPLE
	data = []
	file.seek(-chunk_size, 2)
	try:
		for x in range(0, size // chunk_size):
			data.append(file.read(chunk_size))
			file.seek(-chunk_size - chunk_size * (x + 1), 2)
	except OSError:
		raise ValueError(f"Size {size} exceeds size of file")
	return data


def _seek_marker(file, marker: bytes):
	# reads a limited reverse segment first because 90% of the time we're looking for WOLF_BOF anyway
	try:
		data = _reverse_read(file, os.stat(file.name).st_size // 5)
		return next((x for x in data if marker in x), None)
	except NotImplementedError:
		pass


def inject(file):
	filetype, wolfed = image_filetype(file)
	if wolfed:
		raise ValueError("Image already wolfed")

	file.seek(0, 2)
	file.write(WOLFE_BOF)
	file.seek(-2, 2)


def extract(file):
	pass


def unwolf(file):
	filetype, wolfed = image_filetype(file)
	if not wolfed:
		raise ValueError("Image not already wolfed")

	file.seek(0, 2)


if __name__ == "__main__":
	with open(input("Directory: "), "rb+") as f:
		# inject(f)
		# unwolf(f)
		print(_seek_marker(f, IMAGE_MARKERS["JPG"][1]))
