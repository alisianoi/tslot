#!/usr/bin/env python

class Singleton(type):

    instances = {}

    def __call__(cls, *args, **kwargs):
        print(f'Meta.__call__({cls}, {args}, {kwargs})')

        if cls not in Singleton.instances:
            Singleton.instances[cls] = super().__call__(*args, *kwargs)

        return Singleton.instances[cls]


class TFontService(metaclass=Singleton):

    pass

class RFontService(metaclass=Singleton):

    pass


if __name__ == '__main__':

    tfont_service0 = TFontService()
    tfont_service1 = TFontService()

    rfont_service0 = RFontService()
    rfont_service1 = RFontService()

    print(tfont_service0)
    print(tfont_service1)
    print(rfont_service0)
    print(rfont_service1)
