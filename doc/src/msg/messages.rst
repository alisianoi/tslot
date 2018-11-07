Messages
########

.. tikz::

    \umlclass
        [x = 0, y = 0]
        {TMessage}
        {logger}
        {}
    \umlclass
        [below = 1.5em of TMessage]
        {TFailure}
        {message}
        {}
    \umlsimpleclass[below left  = 1.5em and 6em of TFailure.west]{TRequest}
    \umlsimpleclass[below right = 1.5em and 6em of TFailure.east]{TResponse}
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
