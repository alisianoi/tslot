Stash Requests
##############

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{TStashRequest}
    \umlclass
        [below left = 1.5em and 3.5em of TStashRequest.south]
        {TEntryStashRequest}
        {items: List[TEntryModel]}
        {}
    \umlclass
        [below right = 1.5em and 3.5em of TStashRequest.south]
        {TTimerStashRequest}
        {tdata: TEntryModel}
        {}

    \umlinherit[geometry=|-]{TEntryStashRequest}{TStashRequest}
    \umlinherit[geometry=|-]{TTimerStashRequest}{TStashRequest}
