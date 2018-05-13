from src.msg.base import TMessage


class TMenuRequest(TMessage):

    pass


class THomeMenuRequest(TMenuRequest):

    pass


class TDataMenuRequest(TMenuRequest):

    pass


class TSettingsMenuRequest(TMenuRequest):

    pass


class TAboutMenuRequest(TMenuRequest):

    pass
