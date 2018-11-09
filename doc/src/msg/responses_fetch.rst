Fetch Responses
###############

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{TFetchResponse}
    \umlclass
        [above left = 1.5em and 1.5 em of TFetchResponse.north]
        {TTimerFetchResponse}
        {timer: TEntryModel}
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
    \umlinherit[geometry=-|]{TTimerFetchResponse}{TFetchResponse}
    \umlinherit[geometry=|-]{TTagFetchResponse}{TFetchResponse}
    \umlinherit[geometry=--]{TTagsByNameFetchResponse}{TTagFetchResponse}
    \umlinherit[geometry=|-]{TRaySlotFetchResponse}{TSlotFetchResponse}
    \umlinherit[geometry=|-]{TRaySlotWithTagFetchResponse}{TSlotFetchResponse}
