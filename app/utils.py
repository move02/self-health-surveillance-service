from urllib.parse import urlparse, urljoin
from flask import request
import random, datetime
import base64
import pdb

from config import *
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def is_safe_url(target, request):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def generate_random_salt():
    return random.getrandbits(100)

def decode(encoded, salt):
    decoded = base64.b64decode(encoded.encode("UTF-8")).decode("UTF-8")
    if str(salt) in decoded:
        return decoded[0:len(decoded) - len(str(salt))]
    return None