Thoughts
########

Tag and Task debate
-------------------

Task example: "Flight from New York to Los Angeles"

Potential sets of tags:
0. No tags, self explanatory      -- the task name covers it
1. "Project X", "Business"        -- tags for purpose
2. "Health Checkup", "Personal"   -- same task, different purpose
3. "Time in the air", "Airtravel" -- statistics, book-keeping


Use case "task rename":
.......................

16:00 -- 18:00 March 20th "Flight from New York to Los Angeles" "Project X"
10:00 -- 12:00 April 11th "Flight from New York to Los Angeles" "Personal"

Rename to "Flight from NY to LA" should rename both tasks

Use case "task rename":
.......................

12:00 -- 16:00 March 20th "Exam" "Uni"
10:00 -- 14:00 April 11th "Exam" "Uni"

Rename first to "Biology Exam" should rename one task only, creating
two separate tasks from previously one task.

Use case "task rename":
.......................

12:00 -- 16:00 March 20th "Biology Exam" "Uni"
18:00 -- 20:00 April 29th "Exam"         "Sociology"
10:00 -- 14:00 April 11th "Exam"         "Uni"

Rename first to "Exam" (and maybe later add tag "Biology").
Note how all tags in this use case a probably non-sticky tags.

If tag names are the same and there is a common set of sticky tags,
keep sticky tags.

Use case "new task":
....................

18:00 -- 20:00 April 29th "Exam" "Sociology"
10:00 -- 14:00 April 11th "Exam" "Uni"

Typing "Exam" should suggest "Uni", then "Sociology" (from slot
tags); However, it can suggest nothing.

Use case "new task":
....................

18:00 -- 20:00 April 29th "Exam" "Uni", "Sociology"
10:00 -- 14:00 April 11th "Exam" "Uni"

Typing "Exam" must suggest "Uni" and could suggest "Sociology", though
it probably shouldn't.

Use case "new task":
....................

18:00 -- 20:00 April 29th "Sociology Exam" "Uni"
10:00 -- 14:00 April 11th "Biology Exam" "Uni"

Typing "Exam" or "Uni" should suggest "Uni"

Use case "new task":
....................

18:00 -- 20:00 April 29th "Sociology Exam" "Uni", "Sociology"
10:00 -- 14:00 April 11th "Biology Exam" "Uni", "Biology", "bio"

Typing "Exam" or "Uni" should suggest "Uni", "Sociology", "Biology", "bio"

Task Tags and Slot Tags
-----------------------
If a tag is a Task Tag, it appears at every instance.

All the heuristics for tag suggestions based on task, task name,
current time, etc.

What if Task Tag and Slot Tag have the same name?
.................................................

-- that one time you eat healthy and are proud of it:
13:00 -- 14:00 March 20th "Dinner"      "Cooking", "Veggies", "Health"
10:00 -- 12:00 March 20th "Morning Run" "Health", "Exercise"
13:00 -- 14:00 March 19th "Dinner"      "Cooking"
10:00 -- 12:00 March 19th "Morning Run" "Health", "Exercise"

Yep, still the same tag

The only problem I could think of is words with several meanings:

20:00 -- 21:00 March 21st "Honeymoon" "Engagement"
13:00 -- 14:00 March 20th "Black Ops" "Engagement"

Very rare, don't care. Maybe smth else?

Scroll table layout
-------------------
Times can be either on the left or right (because fixed width).
Scroll direction can be both down (latest on top) or up (latest on bottom).

When asking user questions
--------------------------

Example:
........

Do you want to remove tag "Some Tag" from task "Some Task"?

No -- Yes, for all -- Yes, next (timeout) (time_unit) -- Yes, only this
