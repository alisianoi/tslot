Stash Responses
###############

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{TStashResponse}
    \umlclass
        [below = 1.5em of TStashResponse.south]
        {TEntryStashResponse}
        {items: List[TEntryModel]}
        {}

    \umlinherit[geometry=--]{TEntryStashResponse}{TStashResponse}
