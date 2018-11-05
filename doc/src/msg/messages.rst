Messages
########

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{TMessage}
    \umlsimpleclass[below = 1.5em of TMessage]{TFailure}
    \umlsimpleclass[left = 6em of TFailure]{TRequest}
    \umlsimpleclass[right = 6em of TFailure]{TResponse}
    \umlsimpleclass[below left  = 3.5em and 1.5em of TRequest.north]{TFetchRequest}
    \umlsimpleclass[below right = 3.5em and 1.5em of TRequest.north]{TStashRequest}
    \umlsimpleclass[below left  = 3.5em and 1.5em of TResponse.north]{TFetchResponse}
    \umlsimpleclass[below right = 3.5em and 1.5em of TResponse.north]{TStashResponse}

    \umlinherit[geometry=|-]{TRequest}{TMessage}
    \umlinherit[geometry=-|]{TFailure}{TMessage}
    \umlinherit[geometry=|-]{TResponse}{TMessage}

    \umlinherit[geometry=|-]{TFetchRequest}{TRequest}
    \umlinherit[geometry=|-]{TStashRequest}{TRequest}

    \umlinherit[geometry=|-]{TFetchResponse}{TResponse}
    \umlinherit[geometry=|-]{TStashResponse}{TResponse}
