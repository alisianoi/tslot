Introduction
############

TimeSlot is the current placeholder name for a time tracking application
which can read your mind. Right now it is in such an alpha version that
nothing hardly works. Future plans include:

#. Smart suggestion system based on historic data
#. Companion mobile app
#. Voice activation
#. Checklists
#. Night mode

Since this is a *free and open source desktop app*, you can be sure:

#. You do not have to have internet access
#. Private data does not have to leave your computer
#. Private data is stored in encrypted form (not right now)
#. You cannot be forced to update to a version you don't like
#. You can always report bugs/suggest features in open and clear way
#. You can always inverst some time/effort and fix minor things yourself

Invariants
##########

Recorded time slots must not overlap

Duration of One Day
===================

#. Each day lasts a fixed N number of hours (N=24 hours by default)
#. One table corresponds to one day, holds at most N hours of slots
#. A slot should be split if:

   - it lasts longer than one day
   - it lasts less than one day but begins "late"

#. Identical tables should be merged together by default

   - likely to happen if one slot spans 2 or more days
   - unlikely: if all of the entries start/stop at very close times

Editing a Single Time Slot
==========================

#. When editing task name:

   - if the new name does not exist, create it, otherwise reuse it

#. When editing tag name(s):

   - if the new name does not exist, create it, otherwise reuse it

#. When editing slot times:

   - do not allow new fst to overlap with preceeding lst times
   - suggest preceeding lst time as new value for current fst time
   - do not allow new lst to overlap with subsequent fst times
   - suggest subsequent fst time as new value for current lst time
