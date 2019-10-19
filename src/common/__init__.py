class TMessage:
    """
    Base class for all request, response and failure messages.

    Messages are passed between GUI clients and backend servers. The clients send requests
    to the server and the server answers with responses to the clients.
    """

    def key_val_or_key_len(self, key, val):
        """Help show (reasonably truncated) key/value pairs to a human"""

        if isinstance(val, list) and len(val) > 3:
            return f"len({key})={len(val)}"
        if isinstance(val, dict) and len(val) > 3:
            return f"len({key})={len(val)}"

        return f"{key}={val}"

    def __repr__(self):
        args = ", ".join(
            self.key_val_or_key_len(key, val) for key, val in self.__dict__.items()
        )

        return self.__class__.__name__ + "(" + args + ")"
