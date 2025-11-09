inspired to use a fancy programming framework by https://gitlab.com/Locorock/modurf

notes  
in the official DURF pdf the abilities are stylized as such (but not consistently...?)

- **Active.** Does something.
- **_Passive._** Does something.
- **Weapon** 4 dmg.

# flex boxes

avoid using flex boxes where possible. weasyprint does not always play nice with them.

do something like this instead:

```py
"first:mb-0 mb-[5mm]"
```

if you have to use flex boxes, try playing with

```py
"min-w-0"

# or

"min-h-0"
```
