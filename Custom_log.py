"""
This module provides a custom logging utility that allows for logging messages
It prints outputs but also saves them to files, which can be useful for debugging and tracking application behavior.
It supports different log levels (INFO, WARNING, ERROR) and allows for thread-specific logging.

Use init_log() at the beginning of your code to initialize the logging system.
Use log() instead of print() to log messages.
Use DEBUG_log() for debug messages that you don't want to print by default.
You can easily disable debug logging by changing the disable_DEBUG parameter to TRUE in the init_log() function.
Use input_log() instead of input() to log user inputs.
"""

import os
import json
from datetime import datetime
import glob
from typing import Callable, Optional
import inspect

def get_caller_info() -> dict:
    """
    Returns information about the caller of the previous function.
    The output is a dictionary with keys 'filename', 'lineno', and 'function'.
    """

    frame = inspect.currentframe()
    # Go back two frames: _get_caller_info -> log -> caller
    outer = inspect.getouterframes(frame, 3)

    output : dict = {
        "filename": "unknown",
        "lineno": 0,
        "function": "unknown"
    }

    if len(outer) > 2:
        caller = outer[2]
        output["filename"] = os.path.basename(caller.filename)
        output["lineno"] = caller.lineno
        output["function"] = caller.function

    return output

class CustomLog:

    COLOR_MAP = {
        "INFO": "\033[0m",        # Default (white)
        "DEBUG": "\033[94m",      # Blue
        "WARNING": "\033[93m",    # Yellow
        "ERROR": "\033[91m",      # Red
        "INPUT": "\033[96m",      # Cyan
    }
    RESET_COLOR = "\033[0m"

    def __init__(
            self,
            base_dir=".",
            base_filename="log",
            clear_logs=True,
            print_debug=True,
            disable_debug=False,
            print_inputs=False,
            debug_by_filename= False
            ):
        """
        Initializes the logging system with the specified parameters.
        :param base_dir: Directory where log files will be stored.
        :param base_filename: Base name for the log files.
        :param clear_logs: If True, clears existing log files in the directory.
        :param print_debug: If True, debug messages will be printed to the console.
        :param disable_debug: If True, debug logging is disabled.
        :param print_inputs: If True, user inputs will be printed.
        :param debug_by_filename: If True, debug messages will use the caller's filename as the thread name.
        """
        
        self.debug_print = print_debug
        self.debug_disabled = disable_debug
        self.print_inputs = print_inputs
        self.base_dir = base_dir
        self.base_filename = base_filename
        self.debug_by_filename = debug_by_filename
        self._last_log_ended_with_personalised_char = False
        self.log_types = {
            "debug": f"{self.base_filename}_debug.txt",
            "all": f"{self.base_filename}_all.txt"
        }

        os.makedirs(self.base_dir, exist_ok=True)

        if clear_logs:
            # Clear all .txt files in the logs directory
            for file in glob.glob(os.path.join(self.base_dir, "*.txt")):
                with open(file, "w") as f:
                    f.write("")

    def _get_timestamp(self):
        return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

    def log(
            self,
            msg,
            *args,
            thread="general",
            level="INFO",
            do_print=True,
            print_timestamp=False,
            end: Optional[str] = None,
            file_stamp : Optional[str] = None
        )-> None:
        """
        Logs the given message (with optional *args) to the specified thread log.
        Level can be INFO, WARNING, ERROR.
        If do_print is True, the message is printed.
        If print_timestamp is True, the timestamp is included in the console print.
        file_stamp is a string that will be prepended to the log _all_ entries file.
        """
        if args:
            msg = " ".join(str(m) for m in (msg,) + args)
        else:
            msg = str(msg)

        timestamp = self._get_timestamp()
        level_str = f"[{level.upper()}]" if level.upper() != "INFO" else ""

        T_L_stamp = f"{level_str} {timestamp}"
        if file_stamp is None:
            file_stamp = ""

        # Write to 'all' log
        # we include the caller's filename and line number in the log entry
        with open(os.path.join(self.base_dir, self.log_types["all"]), "a") as f:
            f.write(T_L_stamp + file_stamp + "\n" + msg + "\n\n")

        # Write to thread-specific log
        thread_file = self.log_types.get(thread)
        if not thread_file:
            # Create a new log file if thread not predefined
            thread_file = f"{self.base_filename}_{thread}.txt"
            self.log_types[thread] = thread_file

        with open(os.path.join(self.base_dir, thread_file), "a") as f:
            f.write(T_L_stamp + msg + (end if end else "\n"))

        # Print if requested
        if do_print:
            color = self.COLOR_MAP.get(level.upper(), "")
            show_timestamp = print_timestamp and not self._last_log_ended_with_personalised_char
            print(color + (T_L_stamp if show_timestamp else "") + msg + self.RESET_COLOR, end=end if end is not None else "\n")
        
        if end is not None:
            # If a custom end character is provided, we set a flag to indicate that the last log ended with it
            self._last_log_ended_with_personalised_char = True
        else:
            # If no custom end character is provided, we reset the flag
            self._last_log_ended_with_personalised_char = False
            
    def get_log_contents(self, log_type="all"):
        if log_type not in self.log_types:
            raise ValueError(f"Unknown log type: {log_type}")
        with open(os.path.join(self.base_dir, self.log_types[log_type]), "r") as f:
            return f.read()

    def search_logs(self, keyword, log_type="all"):
        contents = self.get_log_contents(log_type)
        return [line for line in contents.splitlines() if keyword in line]

    def export_log_as_json(self, log_type="all", output_file=None):
        contents = self.get_log_contents(log_type)
        lines = contents.strip().split("\n")
        log_entries = []

        for line in lines:
            try:
                ts = line[0:21]  # [YYYY-MM-DD HH:MM:SS]
                level_start = line.find('[', 22)
                level_end = line.find(']', level_start)
                level = line[level_start+1:level_end] if level_start != -1 and level_end != -1 else "INFO"
                message = line[level_end+2:] if level_end != -1 else line[22:]
                log_entries.append({
                    "timestamp": ts.strip("[]"),
                    "level": level,
                    "message": message
                })
            except Exception:
                log_entries.append({"raw": line})

        output_path = output_file or os.path.join(self.base_dir, f"{self.base_filename}_{log_type}.json")
        with open(output_path, "w") as f:
            json.dump(log_entries, f, indent=2)
            

CUSTOM_LOG : CustomLog | None = None

def init_log(
        base_dir = ".",
        base_filename = "log",
        clear_logs = True,
        print_debug = True,
        disable_debug = False,
        print_inputs = False,
        debug_by_filename= False
        ) -> None:
    """
    Initializes the logging system with the specified parameters.
    :param base_dir: Directory where log files will be stored.
    :param base_filename: Base name for the log files.
    :param clear_logs: If True, clears existing log files in the directory.
    :param print_debug: If True, debug messages will be printed to the console.
    :param disable_debug: If True, debug logging is disabled.
    :param print_inputs: If True, user inputs will be printed.
    :param debug_by_filename: If True, debug messages will use the caller's filename as the thread name.
    """
    
    global CUSTOM_LOG
    CUSTOM_LOG = CustomLog(
        base_dir= base_dir,
        base_filename= base_filename,
        clear_logs= clear_logs,
        print_debug=print_debug,
        disable_debug=disable_debug,
        print_inputs=print_inputs,
        debug_by_filename= debug_by_filename
    )

def log(
        msg,
        *args,
        thread="general",
        level="INFO",
        do_print=True,
        print_timestamp=False,
        end: Optional[str] = None,
        file_stamp: Optional[str] = None
    ) -> None:
    """
    Logs the given message (with optional *args) to the specified thread log.
    Level can be INFO, WARNING, ERROR.
    If do_print is True, the message is printed.
    If print_timestamp is True, the timestamp is included in the console print.
    If caller_info is provided, it will be used to stamp the log entry with the caller's filename and line number.
    The caller_info dictionary should have keys 'filename', 'lineno', and 'function'.
    """

    global CUSTOM_LOG
    if CUSTOM_LOG is None:
        #initialise the function if not already done in this session.
        init_log()
        DEBUG_log (
            "WARNING - The log function has not been initialised, initialising automatically with default values",
            level= "WARNING",
            thread= "LOG_WARNING",
            do_print= True
        )

    CUSTOM_LOG.log(msg, *args, thread= thread, level=level, do_print=do_print, print_timestamp= print_timestamp, end=end, file_stamp=file_stamp)

def DEBUG_log(
        msg,
        *args,
        thread : Optional[str] = None,
        level="DEBUG",
        end: Optional[str] = None,
        do_print : Optional [bool] = None,
    ) -> None:
    """
    Shortcut for logging debug messages to the debug thread.
    Does not print to console by default.
    if do_print is True, it will print the message to console regardless of initialization setting.
    If debug_by_filename is True, it will use the caller's filename as the thread name.
    It will also include the caller's filename and line number in the log entry in this case.
    """
    global CUSTOM_LOG
    if CUSTOM_LOG is None:
        #initialise the function if not already done in this session.
        init_log()
        print("ERROR - The log funcion has not been initialised, initialising automatically with default values")
    if CUSTOM_LOG.debug_disabled:
        return None  # Skip debug logging if disabled
    
    if do_print is None:
        do_print = CUSTOM_LOG.debug_print

    if CUSTOM_LOG.debug_by_filename:
        # If debug_by_filename is True, use the caller's filename as the thread name
        caller_info = get_caller_info()
        if thread is None:
            thread = caller_info["filename"]

        caller_stamp = f"<{caller_info['filename']} - line {caller_info['lineno']}> "

    if thread is None:
        thread = "DEBUG"

    log(
        msg,
        *args,
        thread=thread,
        level=level,
        do_print=do_print,
        end=end,
        print_timestamp=True,
        file_stamp=caller_stamp if CUSTOM_LOG.debug_by_filename else None
        )

def log_input(
        prompt: str,
        thread="input",
        level="DEBUG",
        do_print: Optional[bool] = None,
        print_timestamp = False
    ) -> str:
    """
    Custom input function that logs the input text.
    If the user does not provide input, it logs "<NO INPUT>".
    """
    if prompt is not None:
        try:
            str(prompt)
        except ValueError:
            raise ValueError("ERROR in log_input, prompt must be convertible to a string!")

    input_text = input(prompt)

    if not input_text:
        input_text = "<NO INPUT>"

    input_text_log = "<input>" + str(input_text)

    global CUSTOM_LOG
    if CUSTOM_LOG is None:
        #initialise the function if not already done in this session.
        init_log()
        print("ERROR - The log funcion has not been initialised, initialising automatically with default values")
    
    if do_print is None:
        do_print = CUSTOM_LOG.print_inputs
    
    log(input_text_log, thread=thread, level=level, do_print=do_print, print_timestamp=print_timestamp)
    
    return input_text