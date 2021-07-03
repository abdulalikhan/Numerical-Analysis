from django.db import models

# Create your models here.


class FormData:
    name: str
    value: str

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Method:
    name: str

    def __init__(self, name):
        self.name = name


class Result:
    name: str
    value: str

    def __init__(self, name, value):
        self.name = name
        self.value = value
