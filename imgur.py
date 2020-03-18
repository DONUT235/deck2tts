import pyimgur
#TODO upload images to imgur
_CLIENT_ID = '3c5c7ad0b1b3dda'
_imgur = pyimgur.Imgur(_CLIENT_ID)
def upload(image_filename):
    uploaded_image = _imgur.upload_image(image_filename)
    return uploaded_image.link
