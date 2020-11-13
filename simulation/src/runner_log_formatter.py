import logzero
from logzero import ForegroundColors, basestring_type, to_unicode
import logging


class RunnerLogFormatter(logging.Formatter):
    """
    Log formatter used in Tornado. Key features of this formatter are:
    * Color support when logging to a terminal that supports it.
    * Timestamps on every log line.
    * Robust against str/bytes encoding problems.
    """

    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    DEFAULT_COLORS = {
        logging.DEBUG: ForegroundColors.CYAN,
        logging.INFO: ForegroundColors.GREEN,
        logging.WARNING: ForegroundColors.YELLOW,
        logging.ERROR: ForegroundColors.RED,
        logging.CRITICAL: ForegroundColors.RED,
    }

    def __init__(self, language, library, gpu_mode, id):
        r"""
        :arg bool color: Enables color support.
        :arg string fmt: Log message format.
          It will be applied to the attributes dict of log records. The
          text between ``%(color)s`` and ``%(end_color)s`` will be colored
          depending on the level if color support is on.
        :arg dict colors: color mappings from logging level to terminal color
          code
        :arg string datefmt: Datetime format.
          Used for formatting ``(asctime)`` placeholder in ``prefix_fmt``.
        .. versionchanged:: 3.2
           Added ``fmt`` and ``datefmt`` arguments.
        """
        logging.Formatter.__init__(self, datefmt=self.DEFAULT_DATE_FORMAT)

        self._fmt = f"%(color)s[%(levelname)1.1s %(asctime)s] [{language}, {library}, gpu {gpu_mode}, {id}]%(end_color)s %(message)s"
        self._colors = self.DEFAULT_COLORS
        self._normal = ForegroundColors.RESET

    def _safe_unicode(self, s):
        try:
            return to_unicode(s)
        except UnicodeDecodeError:
            return repr(s)

    def format(self, record):
        try:
            message = record.getMessage()
            assert isinstance(message, basestring_type)  # guaranteed by logging
            # Encoding notes:  The logging module prefers to work with character
            # strings, but only enforces that log messages are instances of
            # basestring.  In python 2, non-ascii bytestrings will make
            # their way through the logging framework until they blow up with
            # an unhelpful decoding error (with this formatter it happens
            # when we attach the prefix, but there are other opportunities for
            # exceptions further along in the framework).
            #
            # If a byte string makes it this far, convert it to unicode to
            # ensure it will make it out to the logs.  Use repr() as a fallback
            # to ensure that all byte strings can be converted successfully,
            # but don't do it by default so we don't add extra quotes to ascii
            # bytestrings.  This is a bit of a hacky place to do this, but
            # it's worth it since the encoding errors that would otherwise
            # result are so useless (and tornado is fond of using utf8-encoded
            # byte strings wherever possible).
            record.message = self._safe_unicode(message)
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        record.asctime = self.formatTime(record, self.datefmt)

        if record.levelno in self._colors:
            record.color = self._colors[record.levelno]
            record.end_color = self._normal
        else:
            record.color = record.end_color = ""

        formatted = self._fmt % record.__dict__

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            # exc_text contains multiple lines.  We need to self._safe_unicode
            # each line separately so that non-utf8 bytes don't cause
            # all the newlines to turn into '\n'.
            lines = [formatted.rstrip()]
            lines.extend(self._safe_unicode(ln) for ln in record.exc_text.split("\n"))
            formatted = "\n".join(lines)
        return formatted.replace("\n", "\n    ")
