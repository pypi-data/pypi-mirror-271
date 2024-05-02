# loggi

logger boilerplate with dataclass models for parsing

## Installation

Install with:

```console
pip install loggi
```

## Usage

```python
>>> import loggi
>>> logger = loggi.getLogger("demo", "logs") 
```

The file "demo.log" will be created inside a folder named "logs" in the current directory.  

loggi wraps the logging level mapping so the log level can be set without importing the logging module

```python
>>> logger.setLevel(loggi.DEBUG)
```

Also loggi imports the logging module when it's initialized, so all logging module features can be utilized without explicity importing logging yourself

```python
>>> print(loggi.logging.getLevelName(loggi.INFO))
INFO
```

loggi uses the format `{level}|-|{date}|-|{message}` where date has the format `%x %X`

```python
>>> logger.info("yeehaw")
```

produces the log

```python
INFO|-|10/26/23 18:48:30|-|yeehaw
```

loggi also contains two dataclasses: `Log` and `Event`.  
A `Log` object contains a list of `Event` objects that can be loaded from a log file (that uses the above format).  
Each `Event` contains `level: str`, `date: datetime`, `message: str` fields.

```python
>>> log = loggi.load_log("logs/demo.log")
>>> print(log)
INFO|-|10/26/23 18:48:30|-|yeehaw
>>> print(log.num_events)
1
>>> print(log.events[0].level)
INFO
```

`Log` objects can be added together.  

Useless examples:

```python
>>> log += log
>>> print(log)
INFO|-|2023-10-26 18:48:30|-|yeehaw
INFO|-|2023-10-26 18:48:30|-|yeehaw
```

New, filtered `Log` objects can be created using the `filter_dates`, `filter_levels`, and `filter_messages` functions.

```python
>>> from datetime import datetime, timedelta
>>> log = loggi.load_log("realistic_log.log")
```

Filtering for events between 24 and 48 hours ago:

```python
>>> filtered_log = log.filter_dates(datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1))
```

Filtering for events with critical and error levels:

```python
>>> filtered_log = log.filter_levels(["CRITICAL", "ERROR"])
```

Filtering for events whose message contains "yeehaw", but not "double yeehaw" or "oopsie":

```python
>>> filtered_log = log.filter_messages(["*yeehaw*"], ["*double yeehaw*", "*oopsie*"])
```

The filtering methods can be chained:

```python
>>> log_slice = log.filter_dates(datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1)).filter_levels(["CRITICAL", "ERROR"])
```

When adding `Log` objects, the `chronosort()` function can be used to reorder the events by date:

```python
>>> log = filtered_log + log_slice
>>> log.chronosort()
```

`log` now contains all critical and error level events between 24 and 48 hours ago,
as well as events from anytime of any level with "yeehaw" in the message, but not "double yeehaw" or "oopsie".  

### LoggerMixin

For convenience, the `LoggerMixin` class can be inherited from to provide initialization of a `logger` attribute:

```python
class Yeehaw(loggi.LoggerMixin):
    def __init__(self):
        self.init_logger()

dummy = Yeehaw()
dummy.logger.info("yeet")
```

By default, the log file will be named after the class inheriting from `LoggerMixin` (`Yeehaw`), but lowercase and stored in a "logs" folder of the current directory. (`logs/yeehaw.log`)  
The logger name, directory, and logging level can be specified with arguments to `self.init_logger()`.  

```python
class Yeehaw(loggi.LoggerMixin):
    def __init__(self):
        self.init_logger(name="yeet", log_dir="top_secret", log_level="DEBUG")
```

Logged messages for the above class will be written to the path `top_secret/yeet.log`.  
