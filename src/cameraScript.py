import time, base64, os

from picamera2 import Picamera2, Preview

def camera():
	picam2 = Picamera2()
	picam2.start_preview(Preview.QTGL)

	preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
	picam2.configure(preview_config)

	picam2.start()
	time.sleep(2)

	picam2.capture_file("food.png")

	with open("food.png", "rb") as food:
		encoded_img = base64.b64encode(food.read())

	print(encoded_img)
	with open('encode.bin','wb') as file:
		file.write(encoded_img)

	if os.path.exists("food.png"):
		os.remove("food.png")
