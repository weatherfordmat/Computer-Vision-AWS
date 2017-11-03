# Computer-Vision-AWS

This AWS/API gateway function allows you to take two images (urls or base64 encoded strings), combine them, and translate them with the Google OCR.

It works best on flat surfaces, I'd like to add functionality for mapping to other surfaces, such as cylinders. It uses Zappa for deployment and OpenCV for the image functionality.
