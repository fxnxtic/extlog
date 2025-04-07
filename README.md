# extlog
mini extension for python logging module

### Features
* Modified logger implements TRACE and SUCCESS logging levels
* Additional handler to output your logs into detached commandline
* Modified formatter works by HTML-like tags
* Independently configuration of color, background and text effects
* Opportunity to format exceptions and stack info
* Creation of your own tags with any logic
* Preconfigured default styles to simple start

### Install
Just `pip install extlog`.

### Available tags
**Reset:**

Use `</>` to reset every applied style.

**Colors:**

* Black: `<black>`, `<br-black>`
* Red: `<red>`, `<br-red>`
* Green: `<green>`, `<br-green>`
* Yellow: `<yellow>`, `<br-yellow>`
* Blue: `<blue>`, `<br-blue>`
* Magenta: `<magenta>`, `<br-magenta>`
* Cyan: `<cyan>`, `<br-cyan>`
* White: `<white>`, `<br-white>`

**Background:**

Use prefix `bg-` for override color tag to background. Example like `<bg-green>`.

**Styles:**

* Bold: `<b>`, `<bold>`
* Dim: `<d>`, `<dim>`
* Underline: `<u>`, `<underline>`
* Overline: `<o>`, `<overline>`
* Italic: `<i>`, `<italic>`
* Reverse: `<r>`, `<reverse>`
* Striked: `<s>`, `<striked>`

**Default custom tags:**

* `<level>`: Formats text to preconfigured style depending on logging level
* `<lvlmsg>`: Formats text to preconfigured style depending on logging level

**Adding own tags:**

Transmit dict of your tags to formatter as kwarg `custom_tags`. 
Example:
```python
formatter = extlog.ExtFormatter(
    ...,
    custom_tags={"level": lambda record: level_styles.get(record.levelno)}
)
```

### Example
```python
import sys
import logging

import extlog


formatter = extlog.ExtFormatter(
    fmt="<br-black>%(asctime)s</> [<level>%(levelname)s</>] <i><br-black>%(name)s</> <lvlmsg>%(message)s</>",
    datefmt="%Y-%m-%d %H:%M:%S",
    excfmt="<red>%(exc)s</>",
    stackfmt="<i><br-black>%(stack)s</>"
)
logger = extlog.getLogger(__name__)
logger.setLevel(extlog.TRACE)
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(formatter) 
cmd_handler = extlog.ConsoleHandler("app")
cmd_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(cmd_handler)

logger.critical('System destroyed')
try:
    1/0
except:
    logger.error('Something bad happened', exc_info=True, stack_info=True)
logger.warning('Something may be wrong')
logger.success("Success message")
logger.info('Basically log message and sometimes "12345"')
logger.debug("Database connected")
logger.trace("Tracer")
```

**Output:**

![{CAB46D60-13F5-4AB0-8FD6-0A9B4C962366}](https://github.com/user-attachments/assets/17449f2d-360a-4f35-8295-518cbd27ec12)

### Contacts
**Telegram:** [@TheDinAlt](https://t.me/TheDinAlt)

`with 💜 by TheDinAlt`
