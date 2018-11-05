Stash Requests
##############

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{TStashRequest}
    \umlclass
        [below = 1.5em of TStashRequest.south]
        {TEntryStashRequest}
        {items: List[TEntryModel]}
        {}

    \umlinherit[geometry=--]{TEntryStashRequest}{TStashRequest}
