Fetch Requests
==============

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
        {TTimerFetchRequest}
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
    \umlinherit[geometry=-|]{TTimerFetchRequest}{TFetchRequest}
    \umlinherit[geometry=|-]{TRaySlotFetchRequest}{TSlotFetchRequest}
    \umlinherit[geometry=|-]{TRaySlotWithTagFetchRequest}{TSlotFetchRequest}
    \umlinherit[geometry=--]{TTagsByNameFetchRequest}{TTagFetchRequest}
