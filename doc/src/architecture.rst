Architecture
############

Messages
--------

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

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{TFetchRequest}
    \umlsimpleclass
        [below left  = 3.5em and 1.5em of TFetchRequest.north]
        {TSlotFetchRequest}
    \umlsimpleclass
        [above right = 3.5em and 1.5em of TFetchRequest.south]
        {TTagFetchRequest}
    \umlsimpleclass
        [above left = 3.5em and 1.5em of TFetchRequest.south]
        {TTimerRequest}
    \umlsimpleclass
        [below left = 3.5em and 1.5em of TSlotFetchRequest.north]
        {TRaySlotFetchRequest}
    \umlsimpleclass
        [below right = 3.5em and 1.5em of TSlotFetchRequest.north]
        {TRaySlotWithTagFetchRequest}
    \umlclass
        [above = 1.5em of TTagFetchRequest]
        {TTagsByNameFetchRequest}
        {name: str \\ exact: bool}
        {}

    \umlinherit[geometry=|-]{TSlotFetchRequest}{TFetchRequest}
    \umlinherit[geometry=|-]{TTagFetchRequest}{TFetchRequest}
    \umlinherit[geometry=-|]{TTimerRequest}{TFetchRequest}
    \umlinherit[geometry=|-]{TRaySlotFetchRequest}{TSlotFetchRequest}
    \umlinherit[geometry=|-]{TRaySlotWithTagFetchRequest}{TSlotFetchRequest}
    \umlinherit[geometry=--]{TTagsByNameFetchRequest}{TTagFetchRequest}

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{TFetchResponse}
    \umlclass
        [above left = 1.5em and 1.5 em of TFetchResponse.north]
        {TTimerResponse}
        {entry: TEntryModel}
        {}
    \umlclass
        [above right = 1.5em and 1.5em of TFetchResponse.north]
        {TTagFetchResponse}
        {tags: List[TagModel]}
        {}
    \umlsimpleclass
        [above = 1.5em of TTagFetchResponse]
        {TTagsByNameFetchResponse}
    \umlclass
        [below left = 1.5em and 1.5em of TFetchResponse.south]
        {TSlotFetchResponse}
        {items: List[TEntryModel]}
        {is\_empty \\ in\_timezone \\ in\_times\_dir \\ in\_dates\_dir}
    \umlclass
        [below left = 1.5em and 1.5em of TSlotFetchResponse.south]
        {TRaySlotFetchResponse}
        {dt\_offset: Date \\ direction: str}
        {in\_timezone \\ from\_model \\ from\_params}
    \umlclass
        [below right = 1.5em and 1.5em of TSlotFetchResponse.south]
        {TRaySlotWithTagFetchResponse}
        {dt\_offset: Date \\ direction: str \\ flat\_tags: bool}
        {in\_timezone \\ from\_model \\ from\_params \\ condense\_tags}

    \umlinherit[geometry=|-]{TSlotFetchResponse}{TFetchResponse}
    \umlinherit[geometry=-|]{TTimerResponse}{TFetchResponse}
    \umlinherit[geometry=|-]{TTagFetchResponse}{TFetchResponse}
    \umlinherit[geometry=--]{TTagsByNameFetchResponse}{TTagFetchResponse}
    \umlinherit[geometry=|-]{TRaySlotFetchResponse}{TSlotFetchResponse}
    \umlinherit[geometry=|-]{TRaySlotWithTagFetchResponse}{TSlotFetchResponse}

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{TStashRequest}
    \umlclass
        [below = 1.5em of TStashRequest.south]
        {TEntryStashRequest}
        {items: List[TEntryModel]}
        {}

    \umlinherit[geometry=--]{TEntryStashRequest}{TStashRequest}

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{TStashResponse}
    \umlclass
        [below = 1.5em of TStashResponse.south]
        {TEntryStashResponse}
        {items: List[TEntryModel]}
        {}

    \umlinherit[geometry=--]{TEntryStashResponse}{TStashResponse}
