Workers
#######

.. tikz::

    \umlsimpleclass[x = 0, y = 0]{QObject}
    \umlclass
        [below = 1.5em of QObject]
        {TWorker}
        {}
        {
            \texttt{+ started}: pyqtSignal \\
            \texttt{+ stopped}: pyqtSignal \\
            \texttt{+ alerted}: pyqtSignal(TFailure) \\
            \texttt{+ work} \\
            \texttt{- create\_session}
        }
    \umlclass
        [below left = 1.5em and 1.5em of TWorker.south]
        {TReader}
        {
            \texttt{+ request}: TFetchRequest
        }
        {
            \texttt{+ fetched}: pyqtSignal(TFetchResponse)
        }
    \umlclass
        [below right = 1.5em and 1.5em of TWorker.south]
        {TWriter}
        {
            \texttt{+ request}: TStashRequest
        }
        {
            \texttt{+ stashed}: pyqtSignal(TStashResponse)
        }

    \umlsimpleclass[below = 1.5em of TReader]{TSlotReader}
    \umlsimpleclass[below left = 1.5em and 1.5em of TSlotReader.south]{TRaySlotReader}
    \umlsimpleclass[below right = 1.5em and 1.5em of TSlotReader.south]{TRaySlotWithTagReader}

    \umlclass
        [below = 1.5em of TWriter]
        {TEntryWriter}
        {
            \texttt{+ items}: List[TEntryModel]
        }
        {}

    \umlinherit[geometry=--]{TWorker}{QObject}
    \umlinherit[geometry=|-]{TWriter}{TWorker}
    \umlinherit[geometry=|-]{TReader}{TWorker}
    \umlinherit[geometry=--]{TSlotReader}{TReader}
    \umlinherit[geometry=|-]{TRaySlotReader}{TSlotReader}
    \umlinherit[geometry=|-]{TRaySlotWithTagReader}{TSlotReader}
