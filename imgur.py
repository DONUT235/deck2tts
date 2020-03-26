import pyimgur
import webbrowser
#TODO upload images to imgur
_CLIENT_ID = '3c5c7ad0b1b3dda'
_CLIENT_SECRET = 'da3334752bd9c83eb07a68691d9ca961aaf9b820'
_imgur = pyimgur.Imgur(_CLIENT_ID, _CLIENT_SECRET)
def authorize():
    _auth_url = _imgur.authorization_url('pin')
    webbrowser.open(_auth_url)
    pin = input('Imgur Authorization pin? ')
    _imgur.exchange_pin(pin)
def upload(image_filename):
    uploaded_image = _imgur.upload_image(image_filename)
    return uploaded_image.link
