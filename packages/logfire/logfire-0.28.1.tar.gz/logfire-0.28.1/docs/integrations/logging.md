# Standard Library Logging

**Logfire** can act as a sink for [standard library logging][logging] by emitting a **Logfire** log for
every standard library log record.

```py title="main.py"
from logging import basicConfig, getLogger

from logfire.integrations.logging import LogfireLoggingHandler

basicConfig(handlers=[LogfireLoggingHandler()])

logger = getLogger(__name__)

logger.error("Hello %s!", "Fred")
# 10:05:06.855 Hello Fred!
```

[logging]: https://docs.python.org/3/library/logging.html
