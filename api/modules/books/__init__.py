from flask import Blueprint

books_blu=Blueprint('books',__name__)

from . import book