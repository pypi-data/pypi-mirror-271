# ----------------------------------------------------------------------------
# Description    : Generic native interface functions
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import copy
import sys
import dis
import numpy
import struct
import re
import time
import json
import fastjsonschema

from builtins import FutureWarning
from enum import Enum
from collections import namedtuple
from functools import wraps, partial
from typing import Any, Callable, Dict, List, Set, Tuple, Optional, Union, Iterator
from inspect import getmembers, isfunction
from qblox_instruments import DeviceInfo
from qblox_instruments.scpi import scpi_error_check
from qblox_instruments.docstring_helpers import add_parameters_to_doc
import warnings

# -- definitions -------------------------------------------------------------


# State enum base class
class StateEnum(Enum):
    """
    State enum base class that arranges child enum string representations.
    """

    def __repr__(self) -> str:
        return "<{}.{}>".format(str(type(self)).split("'")[1], self.name)

    def __str__(self) -> str:
        return str(self.name)

    def __eq__(self, other: Any) -> bool:
        if type(self) == type(other):
            return str(self) == str(other)
        elif other in [str(val) for val in type(self)]:
            return str(self) == other
        else:
            raise KeyError(f"{other} is not of type {type(self)}")

    def __key__(self):
        return str(self)

    def __hash__(self):
        return hash(self.__key__())


class DeprecatedStateEnum(StateEnum):
    """
    State enum class that throws deprecation warning.
    """

    def __init__(self, _warning_message):
        self.warning_message = _warning_message

    def _deprecation_warning(self):
        warnings.warn(
            f"{self.warning_message}",
            FutureWarning,
            stacklevel=2,
        )

    def __str__(self) -> str:
        self._deprecation_warning()
        return StateEnum.__str__(self)

    def __repr__(self) -> str:
        self._deprecation_warning()
        return StateEnum.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        self._deprecation_warning()
        return StateEnum.__eq__(self, other)

    def __key__(self):
        self._deprecation_warning()
        return StateEnum.__key__(self)

    def __hash__(self):
        self._deprecation_warning()
        return StateEnum.__hash__(self)


# It will be deprecated
# State tuple base class
class StateTuple:
    """
    State tuple base class that arranges child tuple string representations.
    """

    def __init__(self, _warning_message):
        self.warning_message = _warning_message

    def _deprecation_warning(self):
        warnings.warn(
            f"{self.warning_message}",
            FutureWarning,
            stacklevel=2,
        )

    def __str__(self) -> str:
        # Status, flags and slot_flags are inherited from the child class
        # using virtual inheritance, so we retrieve these attributes through
        # getattr to not upset Pylint
        status = getattr(self, "status")
        flags = getattr(self, "flags")
        if len(flags) > 0:
            flags = ", ".join([str(flag) for flag in flags])
        else:
            flags = "NONE"
        pretty_str = f"Status: {status}, Flags: {flags}"

        if hasattr(self, "slot_flags"):
            slot_flags = getattr(self, "slot_flags")
            pretty_str += f", Slot flags: {slot_flags}"
        self._deprecation_warning()
        return pretty_str


# State tuple base class
class SystemStatusTuple:
    """
    System Status tuple base class that arranges child tuple string representations.
    """

    def __str__(self) -> str:
        # Status, flags and slot_flags are inherited from the child class
        # using virtual inheritance, so we retrieve these attributes through
        # getattr to not upset Pylint
        status = getattr(self, "status")
        flags = getattr(self, "flags")
        if len(flags) > 0:
            flags = ", ".join([str(flag) for flag in flags])
        else:
            flags = "NONE"
        pretty_str = f"Status: {status}, Flags: {flags}"

        if hasattr(self, "slot_flags"):
            slot_flags = getattr(self, "slot_flags")
            pretty_str += f", Slot flags: {slot_flags}"
        return pretty_str


class StatusTuple:
    """
    Status tuple base class that arranges child tuple string representations.
    """

    def __str__(self) -> str:
        # getattr to not upset Pylint
        state = getattr(self, "state")
        status = getattr(self, "status")
        info_flags = getattr(self, "info_flags")
        warn_flags = getattr(self, "warn_flags")
        err_flags = getattr(self, "err_flags")
        log = getattr(self, "log")

        flags = [info_flags, warn_flags, err_flags]
        for type_idx, type_flags in enumerate(flags):
            if len(type_flags) > 0:
                flags[type_idx] = ", ".join([str(flag) for flag in type_flags])
            else:
                flags[type_idx] = "NONE"

        pretty_str = f"Status: {status}, State: {state}, Info Flags: {flags[0]}, Warning Flags: {flags[1]}, Error Flags: {flags[2]}, Log: {log}"

        return pretty_str


# System status old enum
class SystemStatusOld(DeprecatedStateEnum):
    """
    System status enum.
    """

    BOOTING = "System is booting."
    OKAY = "System is okay."
    RESOLVED = "An error indicated by the flags occured, but has been resolved."
    ERROR = "An error indicated by the flags is occuring."
    CRIT_ERROR = "A critical error indicated by the flags is occurring"

    def __init__(self, *args):
        DeprecatedStateEnum.__init__(
            self,
            """
            After June 2024, this feature is subject to removal in future releases.
            Transition to an alternative is advised.
            See https://qblox-qblox-instruments.readthedocs-hosted.com/en/main/getting_started/deprecated.html
            """,
        )


# All System status enum
class SystemStatuses(StateEnum):
    """
    System status enum.
    """

    BOOTING = "System is booting."
    OKAY = "System is okay."
    RESOLVED = "An error indicated by the flags occured, but has been resolved."
    ERROR = "An error indicated by the flags is occuring."
    CRIT_ERROR = "A critical error indicated by the flags is occurring"


# System status flags enum
class SystemStatusFlags(StateEnum):
    """
    System status flags enum.
    """

    PLL_UNLOCKED = "PLL is unlocked."
    TEMPERATURE_OUT_OF_RANGE = "Temperature is out of range."
    CRIT_TEMPERATURE_OUT_OF_RANGE = "Temperature is critically out of range."
    MODULE_NOT_CONNECTED = "Module is not connected."
    MODULE_FIRMWARE_INCOMPATIBLE = (
        "Module firmware is incompatible with the rest of the system."
    )
    MODULE_FF_CALIB_FAILED = "The feedback network calibration failed."
    HARDWARE_COMPONENT_FAILED = "Hardware component failed"
    TRIGGER_NETWORK_MISSED_EXT_TRIGGER = "Trigger Network Missed External Trigger."


# Namedtuple representing the slot status flags
NUM_SLOTS = 20


class SystemStatusSlotFlags(
    namedtuple(
        "SystemStatusSlotFlags",
        [f"slot{slot}" for slot in range(1, NUM_SLOTS + 1)],
    )
):
    """
    Tuple containing lists of Cluster slot status flag enums of type
    :class:`~qblox_instruments.native.generic_func.SystemStatusFlags`. Each Cluster slot has its
    own status flag list attribute named `slot<X>`.
    """

    __name__ = "SystemStatusSlotFlags"
    __slots__ = ()

    def __new__(cls, slot_flags: Dict = {}):
        slot_flag_lists = [[] for _ in range(NUM_SLOTS)]
        for slot in range(0, NUM_SLOTS):
            slot_str = f"slot{slot + 1}"
            if slot_str in slot_flags:
                slot_flag_lists[slot] = slot_flags[slot_str]
        return super().__new__(cls, *slot_flag_lists)

    def __repr__(self):
        slot_str_list = []
        for slot in range(0, NUM_SLOTS):
            if len(self[slot]) > 0:
                slot_str_list.append(f"slot{slot + 1}={self[slot]}")
        return f"{self.__name__}({', '.join(slot_str_list)})"

    def __str__(self):
        slot_str_list = []
        for slot in range(0, NUM_SLOTS):
            for flag in self[slot]:
                slot_str_list.append(f"SLOT{slot + 1}_{flag}")
        if len(slot_str_list) > 0:
            return ", ".join(slot_str_list)
        else:
            return "NONE"


# Namedtuple representing the system status
class SystemState(
    namedtuple("SystemState", ["status", "flags", "slot_flags"]), StateTuple
):
    """
    System status tuple returned by :func:`!get_system_state`. The tuple
    contains a system status enum of type
    :class:`~qblox_instruments.native.generic_func.SystemStatusOld`, a list of associated system
    status flag enums of type
    :class:`~qblox_instruments.native.generic_func.SystemStatusFlags` and a tuple of type
    :class:`~qblox_instruments.native.generic_func.SystemStatusSlotFlags` containing Cluster slot
    status flags.
    """

    def __init__(self, *args):
        StateTuple.__init__(
            self,
            """
            After June 2024, this feature is subject to removal in future releases.
            Transition to an alternative is advised.
            See https://qblox-qblox-instruments.readthedocs-hosted.com/en/main/getting_started/deprecated.html
            """,
        )


SystemState.status.__doc__ = """
System status enum of type :class:`~qblox_instruments.native.generic_func.SystemStatusOld`.
"""
SystemState.flags.__doc__ = """
List of system status flag enums of type
:class:`~qblox_instruments.native.generic_func.SystemStatusFlags`.
"""
SystemState.slot_flags.__doc__ = """
Tuple of type :class:`~qblox_instruments.native.generic_func.SystemStatusSlotFlags containing
Cluster slot status flags
"""


# Namedtuple representing the system status
class SystemStatus(
    namedtuple("SystemStatus", ["status", "flags", "slot_flags"]), SystemStatusTuple
):
    """
    System status tuple returned by :func:`!get_system_status`. The tuple
    contains a system status enum of type
    :class:`~qblox_instruments.native.generic_func.SystemStatuses`, a list of associated system
    status flag enums of type
    :class:`~qblox_instruments.native.generic_func.SystemStatusFlags` and a tuple of type
    :class:`~qblox_instruments.native.generic_func.SystemStatusSlotFlags` containing Cluster slot
    status flags.
    """

    pass


SystemStatus.status.__doc__ = """
System status enum of type :class:`~qblox_instruments.native.generic_func.SystemStatuses`.
"""
SystemStatus.flags.__doc__ = """
List of system status flag enums of type
:class:`~qblox_instruments.native.generic_func.SystemStatusFlags`.
"""
SystemStatus.slot_flags.__doc__ = """
Tuple of type :class:`~qblox_instruments.native.generic_func.SystemStatusSlotFlags containing
Cluster slot status flags
"""


# This will deprecated in the next releases
# SequencerStates should be used, instead.
# Sequencer status enum
class SequencerStatusOld(DeprecatedStateEnum):
    """
    Sequencer status enum.
    """

    IDLE = "Sequencer waiting to be armed and started."
    ARMED = "Sequencer is armed and ready to start."
    RUNNING = "Sequencer is running."
    Q1_STOPPED = "Classical part of the sequencer has stopped; waiting for real-time part to stop."
    STOPPED = "Sequencer has completely stopped."

    def __init__(self, *args):
        DeprecatedStateEnum.__init__(
            self,
            """
            After June 2024, this feature is subject to removal in future releases.
            Transition to an alternative is advised.
            See https://qblox-qblox-instruments.readthedocs-hosted.com/en/main/getting_started/deprecated.html
            """,
        )


# Sequencer states enum
class SequencerStates(StateEnum):
    """
    Sequencer state enum.
    """

    IDLE = "Sequencer waiting to be armed and started."
    ARMED = "Sequencer is armed and ready to start."
    RUNNING = "Sequencer is running."
    Q1_STOPPED = "Classical part of the sequencer has stopped; waiting for real-time part to stop."
    STOPPED = "Sequencer has completely stopped."


# Sequencer statuses enum
class SequencerStatuses(StateEnum):
    """
    Sequencer status enum.
    """

    OKAY = "OKAY"
    WARNING = "WARNING"
    ERROR = "ERROR"


# Sequencer status flags enum
class SequencerStatusFlags(StateEnum):
    """
    Sequencer status flags enum.
    """

    DISARMED = "Sequencer was disarmed."
    FORCED_STOP = "Sequencer was stopped while still running."
    SEQUENCE_PROCESSOR_Q1_ILLEGAL_INSTRUCTION = (
        "Classical sequencer part executed an unknown instruction."
    )
    SEQUENCE_PROCESSOR_RT_EXEC_ILLEGAL_INSTRUCTION = (
        "Real-time sequencer part executed an unknown instruction."
    )
    SEQUENCE_PROCESSOR_RT_EXEC_COMMAND_UNDERFLOW = (
        "Real-time sequencer part command queue underflow."
    )
    AWG_WAVE_PLAYBACK_INDEX_INVALID_PATH_0 = (
        "AWG path 0 tried to play an unknown waveform."
    )
    AWG_WAVE_PLAYBACK_INDEX_INVALID_PATH_1 = (
        "AWG path 1 tried to play an unknown waveform."
    )
    ACQ_WEIGHT_PLAYBACK_INDEX_INVALID_PATH_0 = (
        "Acquisition path 0 tried to play an unknown weight."
    )
    ACQ_WEIGHT_PLAYBACK_INDEX_INVALID_PATH_1 = (
        "Acquisition path 1 tried to play an unknown weight."
    )
    ACQ_SCOPE_DONE_PATH_0 = "Scope acquisition for path 0 has finished."
    ACQ_SCOPE_OUT_OF_RANGE_PATH_0 = (
        "Scope acquisition data for path 0 was out-of-range."
    )
    ACQ_SCOPE_OVERWRITTEN_PATH_0 = "Scope acquisition data for path 0 was overwritten."
    ACQ_SCOPE_DONE_PATH_1 = "Scope acquisition for path 1 has finished."
    ACQ_SCOPE_OUT_OF_RANGE_PATH_1 = (
        "Scope acquisition data for path 1 was out-of-range."
    )
    ACQ_SCOPE_OVERWRITTEN_PATH_1 = "Scope acquisition data for path 1 was overwritten."
    ACQ_BINNING_DONE = "Acquisition binning completed."
    ACQ_BINNING_FIFO_ERROR = "Acqusition binning encountered internal FIFO error."
    ACQ_BINNING_COMM_ERROR = (
        "Acqusition binning encountered internal communication error."
    )
    ACQ_BINNING_OUT_OF_RANGE = "Acquisition binning data out-of-range."
    ACQ_INDEX_INVALID = "Acquisition tried to process an invalid acquisition."
    ACQ_BIN_INDEX_INVALID = "Acquisition tried to process an invalid bin."
    TRIGGER_NETWORK_CONFLICT = "Trigger network has encountered a conflict."
    TRIGGER_NETWORK_MISSED_INTERNAL_TRIGGER = (
        "Trigger network missed an internal trigger."
    )
    OUTPUT_OVERFLOW = "Output overflow."
    CLOCK_INSTABILITY = "Clock source instability occurred."
    ACQ_INTEGRATOR_OUT_OF_RANGE_PATH_0 = (
        "Acquisition integration input data for path 0 was out-of-range."
    )
    ACQ_INTEGRATOR_OUT_OF_RANGE_PATH_1 = (
        "Acquisition integration input data for path 1 was out-of-range."
    )
    DIO_COMMAND_OVERFLOW = "DIO_COMMAND_OVERFLOW"
    DIO_DELAY_OUT_OF_ORDER = "DIO_DELAY_OUT_OF_ORDER"
    DIO_UNSUPPORTED_PULSE_WIDTH = "DIO_UNSUPPORTED_PULSE_WIDTH"
    DIO_TIMETAG_DEADLINE_MISSED = "DIO_TIMETAG_DEADLINE_MISSED"
    DIO_TIME_DELTA_INVALID = "DIO_TIME_DELTA_INVALID"
    DIO_COUNT_INVALID = "DIO_COUNT_INVALID"
    DIO_THRESHOLD_INVALID = "DIO_THRESHOLD_INVALID"
    DIO_INTERNAL_ERROR = "DIO_INTERNAL_ERROR"


# Namedtuple representing the sequencer state
class SequencerState(namedtuple("SequencerState", ["status", "flags"]), StateTuple):
    """
    Sequencer state tuple returned by :func:`!get_sequencer_state`. The tuple
    contains a sequencer state
    enum of type :class:`~qblox_instruments.native.generic_func.SequencerStatusOld` and a list of
    associated sequencer status flag
    enums of type :class:`~qblox_instruments.native.generic_func.SequencerStatusFlags`.
    """

    def __init__(self, *args):
        StateTuple.__init__(
            self,
            """
            After June 2024, this feature is subject to removal in future releases.
            Transition to an alternative is advised.
            See https://qblox-qblox-instruments.readthedocs-hosted.com/en/main/getting_started/deprecated.html
            """,
        )


SequencerState.status.__doc__ = """
Sequencer status enum of type :class:`~qblox_instruments.native.generic_func.SequencerStatusOld`.
"""
SequencerState.flags.__doc__ = """
List of sequencer status flag enums of type
:class:`~qblox_instruments.native.generic_func.SequencerStatusFlags`.
"""


class SequencerStatus(
    namedtuple(
        "SequencerStatus",
        ["status", "state", "info_flags", "warn_flags", "err_flags", "log"],
    ),
    StatusTuple,
):
    """
    Sequencer status tuple returned by :func:`!get_sequencer_status`. The tuple
    contains a sequencer status, state, flags and log. The tuple contains:
    a sequencer status enum of type :class:`~qblox_instruments.native.generic_func.SequencerStatuses`,
    a sequencer state enum of type :class:`~qblox_instruments.native.generic_func.SequencerStates`,
    a list of associated info flags enums of type :class:`~qblox_instruments.native.generic_func.SequencerStatusFlags`,
    a list of associated warning flags enums of type :class:`~qblox_instruments.native.generic_func.SequencerStatusFlags`,
    a list of associated error flags enums of type :class:`~qblox_instruments.native.generic_func.SequencerStatusFlags`,
    a list of informative log message of type :class:`str`.
    """

    pass


SequencerStatus.status.__doc__ = """
Sequencer status enum of type :class:`~qblox_instruments.native.generic_func.SequencerStatuses`.
"""

SequencerStatus.state.__doc__ = """
Sequencer state enum of type :class:`~qblox_instruments.native.generic_func.SequencerStates`.
"""

SequencerStatus.info_flags.__doc__ = """
List of sequencer status flag enums of type
:class:`~qblox_instruments.native.generic_func.SequencerStatusFlags`.
"""

SequencerStatus.warn_flags.__doc__ = """
List of sequencer status flag enums of type
:class:`~qblox_instruments.native.generic_func.SequencerStatusFlags`.
"""

SequencerStatus.err_flags.__doc__ = """
List of sequencer status flag enums of type
:class:`~qblox_instruments.native.generic_func.SequencerStatusFlags`.
"""

SequencerStatus.log.__doc__ = """
List of log message with more detailed information in case of WARNING status.
"""

# Maximum program length allowed
MAX_PROGRAM_LENGTH = 10 * (128 * 1024 * 8 + 1024)

# JSON schema to validate sequence dictionaries with
QCM_SEQUENCE_JSON_SCHEMA = {
    "title": "Sequence container",
    "description": "Contains all waveforms, weights and acquisitions and a program required for a sequence.",
    "type": "object",
    "required": ["program", "waveforms"],
    "properties": {
        "program": {
            "description": "Sequencer assembly program in string format.",
            "type": "string",
        },
        "waveforms": {
            "description": "Waveform dictionary containing one or multiple AWG waveform(s).",
            "type": "object",
        },
        "weights": {
            "description": "Weight dictionary containing one or multiple acquisition weights(s).",
            "type": "object",
        },
        "acquisitions": {
            "description": "Acquisition dictionary containing information about one or multiple acquisition(s).",
            "type": "object",
        },
    },
}

# JSON schema to validate QRM sequence dictionaries with
QRM_SEQUENCE_JSON_SCHEMA = copy.deepcopy(QCM_SEQUENCE_JSON_SCHEMA)
QRM_SEQUENCE_JSON_SCHEMA["required"] = [
    "program",
    "waveforms",
    "weights",
    "acquisitions",
]

# JSON schema to validate wavefrom and weight dictionaries with
WAVE_JSON_SCHEMA = {
    "title": "Waveform/weight container",
    "description": "Waveform/weight dictionary for a single waveform.",
    "type": "object",
    "required": ["data"],
    "properties": {
        "data": {"description": "List of waveform samples.", "type": "array"},
        "index": {"description": "Optional waveform index number.", "type": "number"},
    },
}

# JSON schema to validate acquisition dictionaries with
ACQ_JSON_SCHEMA = {
    "title": "Acquisition container",
    "description": "Acquisition dictionary for a single acquisition.",
    "type": "object",
    "required": ["num_bins"],
    "properties": {
        "num_bins": {"description": "Number of bins in acquisition.", "type": "number"},
        "index": {"description": "Optional waveform index number.", "type": "number"},
    },
}

# JSON schema to validate sequence dictionaries with
# TODO QTM, add more fields here for V2
QTM_SEQUENCE_JSON_SCHEMA = {
    "title": "Sequence container",
    "description": "Contains all acquisitions and a program required for a sequence.",
    "type": "object",
    "required": ["program"],
    "properties": {
        "program": {
            "description": "Sequencer assembly program in string format.",
            "type": "string",
        },
        "acquisitions": {
            "description": "Acquisition dictionary containing information about one or multiple acquisition(s).",
            "type": "object",
        },
    },
}


# -- class -------------------------------------------------------------------


class FuncRefs:
    """
    Function reference container intended to hold references to methods of the
    instrument's SCPI and native interfaces that are called by methods in
    :mod:`~qblox_instruments.native.generic_func`. In effect, this class enables
    passing parametrized methods to the
    :mod:`~qblox_instruments.native.generic_func` functions so that those
    functions can be reused between different instruments.
    """

    # ------------------------------------------------------------------------
    def __init__(self, instrument: Optional[Any] = None):
        """
        Create function reference container.

        Parameters
        ----------
        instrument : Any
            Instrument parent object of the function references.

        Returns
        ----------

        Raises
        ----------
        """

        # Store instrument reference
        self._instrument = instrument

        # Create list of instrument function names referenced in this module's
        # functions and manually add any missing functions that the
        # convenience method failed to pick up.
        func_names = FuncRefs._get_referenced_funcs(sys.modules[__name__])
        func_names.append("_write")
        func_names.append("_flush_line_end")
        func_names.append("_get_awg_waveforms")
        func_names.append("_get_acq_weights")
        func_names.append("_get_acq_acquisition_data")
        func_names.append("_get_acq_acquisitions")
        func_names.append("_get_sequencer_channel_map")
        func_names.append("_set_sequencer_channel_map")
        func_names.append("_get_sequencer_acq_channel_map")
        func_names.append("_set_sequencer_acq_channel_map")
        func_names.append("is_qdm_type")

        # Create dictionary of instrument functions and associated attributes.
        # Initialize the associated attributes to None since they are not
        # registered yet.
        self._funcs = {}
        for name in func_names:
            self._funcs[name] = None

        # Add instrument functions as temporary attributes to this class, so
        # that when called it throws a NotImplemented exception. Do this
        # through a wrapper function to ensure that the function name is
        # unique in each error string. These attributes should be overwritten
        # using the register method after this class is instantiated.
        def create_unique_func(name: str) -> Callable[..., None]:
            def raise_not_implemented_error(*args, **kwargs) -> None:
                raise NotImplementedError(
                    f'"{name}" has not yet been registered to this function reference container.'
                )

            return raise_not_implemented_error

        for name in func_names:
            setattr(self, name, create_unique_func(name))

    # ------------------------------------------------------------------------
    @property
    def instrument(self) -> Any:
        """
        Return function references parent object.

        Parameters
        ----------

        Returns
        ----------
        Any
            Instrument parent object of the function references.

        Raises
        ----------
        """

        return self._instrument

    # ------------------------------------------------------------------------
    @property
    def funcs(self) -> Dict:
        """
        Return dictionary of instrument function names and their associate
        references, referenced in this module's functions so that the
        referenced functions can be registered to this object using the
        register method.

        Parameters
        ----------

        Returns
        ----------
        dict
            Dictionary of required instrument function names and associated
            references.

        Raises
        ----------
        """

        return self._funcs

    # ------------------------------------------------------------------------
    def register(
        self, ref: Callable[[Any], Any], attr_name: Optional[str] = None
    ) -> None:
        """
        Register function reference as attribute to object.

        Parameters
        ----------
        ref : Callable[[Any], Any]
            Function reference to register.
        attr_name : Optional[str]
            Attribute name to register function to. If attribute name
            is not provided. The function is registered to the name of
            the reference argument.

        Returns
        ----------

        Raises
        ----------
        AttributeError
            Could not get name of reference.
        KeyError
            Attribute name is not found in function name list.
        """

        if attr_name is None:
            if hasattr(ref, "__name__"):
                attr_name = ref.__name__
            else:
                raise AttributeError("Could not get name of function reference.")

        if attr_name in self.funcs:
            self.funcs[attr_name] = ref
            setattr(self, attr_name, ref)
        else:
            raise KeyError(
                f"Attribute name that is being registered ({attr_name}) is not in the instrument function list"
            )

    # ------------------------------------------------------------------------
    @staticmethod
    def _get_referenced_funcs(module: Any, arg_name: str = "funcs") -> List:
        """
        Get all referenced instrument function names using FuncRefs for the
        functions in the given Python module. This method looks very
        specifically for the use of the input argument name specified by
        arg_name of type FuncRefs to find any referenced function names. Note
        that this is a convenience method that does not work for all use
        cases. For instance, it does not work for decorated functions.

        Parameters
        ----------
        arg_name : str
            Argurment name to search for.

        Returns
        ----------
        List
            List of required instrument function names.

        Raises
        ----------
        """

        # Get functions from module, disassemble them and search for FuncRefs
        # references using name specified by input argument. Finally split
        # out the function and attribute calls and return the found results.
        funcs = []
        for func in getmembers(module, isfunction):
            instr_list = list(dis.Bytecode(func[1]))
            for idx, instr in enumerate(instr_list):
                if instr.opname == "LOAD_FAST" and instr.argval == arg_name:
                    next_instr = instr_list[idx + 1]
                    if (
                        next_instr.opname == "LOAD_METHOD"
                        or next_instr.opname == "LOAD_ATTR"
                    ) and not hasattr(FuncRefs, next_instr.argval):
                        funcs.append(instr_list[idx + 1].argval)

        return list(set(funcs))


# -- helper functions --------------------------------------------------------


def check_sequencer_index(sequencer: int) -> None:
    """
    Check if sequencer index is within range. We just check if the index is a
    positive integer here, because sending a negative number breaks the
    underlying SCPI command. The upperbound is checked by the instrument.

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------

    Raises
    ----------
    ValueError
        Sequencer index is out-of-range (i.e. < 1).
    """

    if sequencer < 0:
        raise ValueError(f"Sequencer index is out-of-range ({sequencer})")


# ---------------------------------------------------------------------
def check_io_channel_index(io_channel: int) -> None:
    """
    Check if I/O channel index is within range. We just check if the
    index is a positive integer here, because sending a negative number
    breaks the underlying SCPI command. The upperbound is checked by the
    instrument.

    Parameters
    ----------
    io_channel : int
        I/O channel index.

    Returns
    ----------

    Raises
    ----------
    ValueError
        I/O channel index is out-of-range (i.e. < 1).
    """

    if io_channel < 0:
        raise ValueError(f"I/O channel index is out-of-range ({io_channel})")


# ---------------------------------------------------------------------
def _check_program_length(program: str) -> None:
    """
    Checks if the program length is above the limit. If it is, an
    attempt is made to shorten the program by removing comments and
    unnecessary whitespaces. If the program is still too large, a
    Runtime error is raised.

    Parameters
    ----------
    program : str
        Sequence program to be updated to the device

    Returns
    ----------

    Raises
    ----------
    RuntimeError
        Too large program string.
    """

    if len(program.encode("utf-8")) > MAX_PROGRAM_LENGTH:
        checked_program = re.sub(r"#.*|^\s*", "", program, 0, re.MULTILINE)
        checked_program = re.sub(r"[^\S\r\n]+", " ", checked_program)

        if len(checked_program.encode("utf-8")) > MAX_PROGRAM_LENGTH:
            raise RuntimeError(
                f"Program length too large, expected something below {MAX_PROGRAM_LENGTH} bytes but got {len(checked_program.encode('utf-8'))} bytes."
            )
        else:
            return checked_program
    else:
        return program


# ----------------------------------------------------------------------------
def check_qrm_type(is_qrm_type: bool) -> None:
    """
    Check if module is of type QRM. If not throw a NotImplemented exception.
    This helper function can be used to catch execution of QRM functionality
    on non-QRM type modules.

    Parameters
    ----------
    is_qrm_type : bool
        Is QRM module type.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    if not is_qrm_type:
        raise NotImplementedError("This functionality not available on this module.")


# ----------------------------------------------------------------------------
def check_qcm_type(is_qcm_type: bool) -> None:
    """
    Check if module is of type QCM. If not throw a NotImplemented exception.
    This helper function can be used to catch execution of QCM functionality
    on non-QCM type modules.

    Parameters
    ----------
    is_qcm_type : bool
        Is QCM module type.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    if not is_qcm_type:
        raise NotImplementedError("This functionality not available on this module.")


# ----------------------------------------------------------------------------
def check_qtm_type(is_qtm_type: bool) -> None:
    """
    Check if module is of type QTM. If not throw a NotImplemented exception.
    This helper function can be used to catch execution of QTM functionality
    on non-QTM type modules.

    Parameters
    ----------
    is_qtm_type : bool
        Is QTM module type.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    if not is_qtm_type:
        raise NotImplementedError("This functionality not available on this module.")


# ----------------------------------------------------------------------------
def check_qdm_type(is_qdm_type: bool) -> None:
    """
    Check if module is of type QDM. If not throw a NotImplemented exception.
    This helper function can be used to catch execution of QDM functionality
    on non-QDM type modules.

    Parameters
    ----------
    is_qdm_type : bool
        Is QDM module type.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    if not is_qdm_type:
        raise NotImplementedError("This functionality not available on this module.")


# ----------------------------------------------------------------------------
def check_is_valid_type(is_type: bool) -> None:
    """
    Check if module type is valid. If not throw a NotImplemented exception.
    This helper function can be used to catch execution of QXM functionality
    that is not implemented.

    Parameters
    ----------
    is_type : bool
        Is module type.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    if not is_type:
        raise NotImplementedError("This functionality not available on this module.")


# ----------------------------------------------------------------------------
def create_read_bin(
    read_bin_func: Callable[[str, bool], bytes], cmd: str
) -> Callable[[Optional[int], Optional[str]], bytes]:
    """
    Create binary read function that can provide a binary read with a
    preconfigured command. This is usefull for functions like
    `_get_awg_waveforms`, that need a specific binary read command to kick
    off a stream of binary blocks.

    Parameters
    ----------
    read_bin_func : Callable[[str, bool], bytes]
        SCPI layer binary read method.
    cmd : str
        Unformated command string.

    Returns
    ----------
    Callable[[Optional[int], Optional[str]], bytes]
        Binary read function with preconfigured command that takes the
        optional sequencer index and optional name string as arguments.

    Raises
    ----------
    """

    def read_bin(sequencer: Optional[int] = None, name: Optional[str] = None) -> bytes:
        if sequencer is None:
            new_cmd = cmd
        else:
            if name is None:
                new_cmd = cmd.format(sequencer)
            else:
                new_cmd = cmd.format(sequencer, name)
        return read_bin_func(new_cmd, False)

    return read_bin


# -- functions ---------------------------------------------------------------

# Note that the arguments in the docstrings of the following functions do not
# reflect the arguments of the functions themselves. Instead they reflect the
# arguments of the native instrument layer's methods that call these
# functions. The copy_docstr decorator is used to copy the docstring to the
# calling method, so that not only the functionality but also the docstring
# can be shared across the methods of the native instrument layers.


def get_scpi_commands(funcs: FuncRefs) -> Dict:
    """
    Get SCPI commands and convert to dictionary.

    Parameters
    ----------

    Returns
    ----------
    dict
        Dictionary containing all available SCPI commands, corresponding
        parameters, arguments and Python methods and finally a descriptive
        comment.

    Raises
    ----------
    """

    # Split function
    def split(cmd_elem: str) -> List:
        if cmd_elem != "None" and cmd_elem != "":
            return cmd_elem.split(",")
        else:
            return []

    # Format command string
    cmds = funcs._get_scpi_commands()
    cmd_elem_list = cmds.split(";")[:-1]
    cmd_list = numpy.reshape(cmd_elem_list, (int(len(cmd_elem_list) / 9), 9))
    cmd_dict = {
        cmd[0]: {
            "scpi_in_type": split(cmd[1]),
            "scpi_out_type": split(cmd[2]),
            "python_func": cmd[3],
            "python_in_type": split(cmd[4]),
            "python_in_var": split(cmd[5]),
            "python_out_type": split(cmd[6]),
            "comment": cmd[8].replace("\t", "\n"),
        }
        for cmd in cmd_list
    }
    return cmd_dict


# ----------------------------------------------------------------------------
def get_idn(funcs: FuncRefs) -> Dict:
    """
    Get device identity and build information and convert them to a
    dictionary.

    Parameters
    ----------

    Returns
    ----------
    dict
        Dictionary containing manufacturer, model, serial number and build
        information. The build information is subdivided into FPGA firmware,
        kernel module software, application software and driver software build
        information. Each of those consist of the version, build date,
        build Git hash and Git build dirty indication.

    Raises
    ----------
    """

    return DeviceInfo.from_idn(funcs._get_idn()).to_idn_dict()


# ----------------------------------------------------------------------------
def get_system_state(funcs: FuncRefs) -> SystemState:
    """
    Get general system state and convert it to a
    :class:`~qblox_instruments.native.generic_func.SystemState`.

    Parameters
    ----------

    Returns
    ----------
    SystemStatus
        Tuple containing general system status and corresponding flags.

    Raises
    ----------
    """

    warnings.warn(
        """
        After June 2024, this feature is subject to removal in future releases.
        Transition to an alternative is advised.
        See https://qblox-qblox-instruments.readthedocs-hosted.com/en/main/getting_started/deprecated.html
        """,
        FutureWarning,
    )

    # Format status string
    state = funcs._get_system_state()
    state_elem_list = re.sub(" |-", "_", state).split(";")
    if state_elem_list[-1] != "":
        state_flag_list = state_elem_list[-1].split(",")[:-1]
    else:
        state_flag_list = []

    # Split system status flags from slot status flags
    system_flags = []
    slot_flags = {}
    for flag in state_flag_list:
        flag_parts = flag.split("_")
        if flag_parts[0] != "SLOT":
            system_flags.append(SystemStatusFlags[flag])
        else:
            slot = "slot" + flag_parts[1]
            flag = SystemStatusFlags["_".join(flag_parts[2:])]
            if slot not in slot_flags:
                slot_flags[slot] = [flag]
            else:
                slot_flags[slot].append(flag)

    return SystemState(
        SystemStatusOld[state_elem_list[0]],
        system_flags,
        SystemStatusSlotFlags(slot_flags),
    )


# ----------------------------------------------------------------------------
def get_system_status(funcs: FuncRefs) -> SystemStatus:
    """
    Get general system status and convert it to a
    :class:`~qblox_instruments.native.generic_func.SystemStatus`.

    Parameters
    ----------

    Returns
    ----------
    SystemStatus
        Tuple containing general system status and corresponding flags.

    Raises
    ----------
    """

    # Format status string
    state = funcs._get_system_state()
    state_elem_list = re.sub(" |-", "_", state).split(";")
    if state_elem_list[-1] != "":
        state_flag_list = state_elem_list[-1].split(",")[:-1]
    else:
        state_flag_list = []

    # Split system status flags from slot status flags
    system_flags = []
    slot_flags = {}
    for flag in state_flag_list:
        flag_parts = flag.split("_")
        if flag_parts[0] != "SLOT":
            system_flags.append(SystemStatusFlags[flag])
        else:
            slot = "slot" + flag_parts[1]
            flag = SystemStatusFlags["_".join(flag_parts[2:])]
            if slot not in slot_flags:
                slot_flags[slot] = [flag]
            else:
                slot_flags[slot].append(flag)

    return SystemStatus(
        SystemStatuses[state_elem_list[0]],
        system_flags,
        SystemStatusSlotFlags(slot_flags),
    )


# ----------------------------------------------------------------------------
def set_acq_scope_config(funcs: FuncRefs, config: Dict) -> None:
    """
    Set configuration of the scope acquisition. The configuration consists of
    multiple parameters in a C struct format. If an invalid sequencer index
    is given or the configation struct does not have the correct format, an
    error is set in system error.

    Parameters
    ----------
    config : dict
        Configuration dictionary.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    funcs._set_acq_scope_config(config)


# ----------------------------------------------------------------------------
def get_acq_scope_config(funcs: FuncRefs) -> Dict:
    """
    Get configuration of the scope acquisition. The configuration consists of
    multiple parameters in a C struct format. If an invalid sequencer index is
    given, an error is set in system error.

    Parameters
    ----------

    Returns
    ----------
    dict
        Configuration dictionary.

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_qrm_type(funcs.is_qrm_type())
    return funcs._get_acq_scope_config()


# --------------------------------------------------------------------------
def set_acq_scope_config_val(funcs: FuncRefs, keys: Any, val: Any) -> None:
    """
    Set value of specific scope acquisition parameter.

    Parameters
    ----------
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof
    val: Any
        Value to set parameter to.

    Returns
    ----------

    Raises
    ----------
    """

    _set_generic_json_config_val(
        funcs, get_acq_scope_config, set_acq_scope_config, keys, val
    )


# --------------------------------------------------------------------------
def get_acq_scope_config_val(funcs: FuncRefs, keys: Any) -> Any:
    """
    Get value of specific scope acquisition parameter.

    Parameters
    ----------
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof

    Returns
    ----------
    Any
        Parameter value.

    Raises
    ----------
    """

    return _get_generic_json_config_val(funcs, get_acq_scope_config, keys)


# ----------------------------------------------------------------------------
def set_io_channel_config(funcs: FuncRefs, channel: int, config: Dict) -> None:
    """
    Set IO channel configuration. The configuration consists of
    multiple parameters in a JSON format. If the configation struct does not
    have the correct format, an error is set in system error.

    Parameters
    ----------
    channel : int
        I/O channel index.
    config : dict
        Configuration dictionary.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """
    check_qtm_type(funcs.is_qtm_type())
    funcs._set_io_channel_config(channel, config)


# ----------------------------------------------------------------------------
def get_io_channel_config(funcs: FuncRefs, channel: int) -> Dict:
    """
    Get IO channel configuration. The configuration consists of
    multiple parameters in a JSON format.

    Parameters
    ----------
    channel : int
        I/O channel index.

    Returns
    ----------
    dict
        Configuration dictionary.

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_qtm_type(funcs.is_qtm_type())
    return funcs._get_io_channel_config(channel)


# --------------------------------------------------------------------------
def set_io_channel_config_val(
    funcs: FuncRefs, channel: int, keys: Any, val: Any
) -> None:
    """
    Set value of specific IO channel configuration parameter.

    Parameters
    ----------
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof.
    channel : int
        I/O channel index.
    val: Any
        Value to set parameter to.

    Returns
    ----------

    Raises
    ----------
    """

    _set_generic_json_config_val(
        funcs,
        lambda funcs: get_io_channel_config(funcs, channel),
        lambda funcs, cfg: set_io_channel_config(funcs, channel, cfg),
        keys,
        val,
    )


# --------------------------------------------------------------------------
def get_io_channel_config_val(funcs: FuncRefs, channel: int, keys: Any) -> Any:
    """
    Get value of specific IO channel configuration parameter.

    Parameters
    ----------
    channel : int
        I/O channel index.
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof

    Returns
    ----------
    Any
        Parameter value.

    Raises
    ----------
    """

    return _get_generic_json_config_val(
        funcs, lambda funcs: get_io_channel_config(funcs, channel), keys
    )


# ----------------------------------------------------------------------------
def get_io_channel_status(funcs: FuncRefs, channel: int) -> Dict:
    """
    Get IO channel status. The status consists of multiple values in a JSON
    format.

    Parameters
    ----------
    channel : int
        I/O channel index.

    Returns
    ----------
    dict
        Status dictionary.

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_qtm_type(funcs.is_qtm_type())
    return funcs._get_io_channel_status(channel)


# --------------------------------------------------------------------------
def get_io_channel_status_val(funcs: FuncRefs, channel: int, keys: Any) -> Any:
    """
    Get value of specific IO channel status parameter.

    Parameters
    ----------
    channel : int
        I/O channel index.
    keys : Union[List[str], str]
        Status key to access, or hierarchical list thereof

    Returns
    ----------
    Any
        Parameter value.

    Raises
    ----------
    """

    return _get_generic_json_config_val(
        funcs, lambda funcs: get_io_channel_status(funcs, channel), keys
    )


# ----------------------------------------------------------------------------
def set_quad_config(funcs: FuncRefs, quad: int, config: Dict) -> None:
    """
    Set quad configuration. The configuration consists of
    multiple parameters in a JSON format. If the configation struct does not
    have the correct format, an error is set in system error.

    Parameters
    ----------
    quad : int
        I/O quad index.
    config : dict
        Configuration dictionary.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """
    check_qtm_type(funcs.is_qtm_type())
    funcs._set_quad_config(quad, config)


# ----------------------------------------------------------------------------
def get_quad_config(funcs: FuncRefs, quad: int) -> Dict:
    """
    Get quad configuration. The configuration consists of
    multiple parameters in a JSON format.

    Parameters
    ----------
    quad : int
        I/O quad index.

    Returns
    ----------
    dict
        Configuration dictionary.

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """
    check_qtm_type(funcs.is_qtm_type())
    return funcs._get_quad_config(quad)


# --------------------------------------------------------------------------
def set_quad_config_val(funcs: FuncRefs, quad: int, keys: Any, val: Any) -> None:
    """
    Set value of specific quad configuration parameter.

    Parameters
    ----------
    quad : int
        I/O quad index.
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof
    val: Any
        Value to set parameter to.

    Returns
    ----------

    Raises
    ----------
    """

    _set_generic_json_config_val(
        funcs,
        lambda funcs: get_quad_config(funcs, quad),
        lambda funcs, cfg: set_quad_config(funcs, quad, cfg),
        keys,
        val,
    )


# --------------------------------------------------------------------------
def get_quad_config_val(funcs: FuncRefs, quad: int, keys: Any) -> Any:
    """
    Get value of specific quad configuration parameter.

    Parameters
    ----------
    quad : int
        I/O quad index.
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof

    Returns
    ----------
    Any
        Parameter value.

    Raises
    ----------
    """

    return _get_generic_json_config_val(
        funcs, lambda funcs: get_quad_config(funcs, quad), keys
    )


# --------------------------------------------------------------------------
def _set_generic_json_config_val(
    funcs: FuncRefs, get_func, set_func, keys: Any, val: Any
) -> None:
    """
    Generic code used by setters and getters of different configurations
    that are provided in a JSON format.

    Parameters
    ----------
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof
    val: Any
        Value to set parameter to.

    Returns
    ----------

    Raises
    ----------
    """

    # Normalize keys argument.
    if not isinstance(keys, str) and hasattr(keys, "__iter__"):
        keys = tuple(keys)
    else:
        keys = [keys]

    # Get configuration.
    cfg = get_func(funcs)

    # Walk to the right "directory" in the hierarchy.
    d = cfg
    for key in keys[:-1]:
        if (
            isinstance(d, list)
            and (not isinstance(key, int) or key < 0 or key >= len(d))
        ) or (isinstance(d, dict) and (not isinstance(key, str) or key not in d)):
            raise KeyError(
                f'dict[{"][".join(str(e) for e in keys)}] is not a valid path, failed at {key}'
            )
        d = d[key]

    key = keys[-1]
    if (
        isinstance(d, list) and (not isinstance(key, int) or key < 0 or key >= len(d))
    ) or (isinstance(d, dict) and (not isinstance(key, str) or key not in d)):
        raise KeyError(
            f'dict[{"][".join(str(e) for e in keys)}] is not a valid path, failed at {key}'
        )

    # Make sure val has the right JSON type; try casting it if not.
    cur = d[keys[-1]]
    for typ in (int, float, str, bool):
        if isinstance(cur, typ):
            try:
                val = typ(val)
            except (ValueError, TypeError) as e:
                raise TypeError(
                    f'{".".join(str(e) for e in keys)} should be of type {typ.__name__}: {e}'
                )
            break
    else:
        # Probably a dict or array! Can't set those directly.
        raise KeyError(f'{".".join(str(e) for e in keys)} is an incomplete path')

    # Set the new value.
    if isinstance(d[keys[-1]], bool):
        d[keys[-1]] = True if val == 1 else False
    else:
        d[keys[-1]] = val
    set_func(funcs, cfg)


# --------------------------------------------------------------------------
def _get_generic_json_config_val(funcs: FuncRefs, get_func, keys: Any) -> Any:
    """
    Get value of specific scope acquisition parameter.

    Parameters
    ----------
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof

    Returns
    ----------
    Any
        Parameter value.

    Raises
    ----------
    """
    # Normalize keys argument.
    if not isinstance(keys, str) and hasattr(keys, "__iter__"):
        keys = tuple(keys)
    else:
        keys = [keys]

    val = get_func(funcs)
    for key in keys:
        if (
            isinstance(val, list)
            and (not isinstance(key, int) or key < 0 or key >= len(val))
        ) or (isinstance(val, dict) and (not isinstance(key, str) or key not in val)):
            raise KeyError(
                f'cfg_dict[{"][".join(str(e) for e in keys)}] is not a valid path, failed at {key}'
            )
        val = val[key]
    return val


# ----------------------------------------------------------------------------
def set_sequencer_program(funcs: FuncRefs, sequencer: int, program: str) -> None:
    """
    Assemble and set Q1ASM program for the indexed sequencer. If assembling
    failes, an RuntimeError is thrown with the assembler log attached.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    program : str
        Q1ASM program.

    Returns
    ----------

    Raises
    ----------
    RuntimeError
        Assembly failed.
    """

    check_sequencer_index(sequencer)

    try:
        funcs._set_sequencer_program(sequencer, _check_program_length(program))
    except:
        print(funcs.get_assembler_log())
        raise


# ----------------------------------------------------------------------------
def set_sequencer_config(funcs: FuncRefs, sequencer: int, config: Dict) -> None:
    """
    Set configuration of the indexed sequencer. The configuration consists
    dictionary containing multiple parameters that will be converted into a
    JSON object supported by the device.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    config : dict
        Configuration dictionary.

    Returns
    ----------

    Raises
    ----------
    """

    # Get current configuration and merge dictionaries.
    check_sequencer_index(sequencer)

    funcs._set_sequencer_config(sequencer, config)


# ----------------------------------------------------------------------------
def get_sequencer_config(funcs: FuncRefs, sequencer: int) -> Dict:
    """
    Get configuration of the indexed sequencer. The configuration consists
    dictionary containing multiple parameters that will be converted from a
    JSON object provided by the device.

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------
    dict
        Configuration dictionary.

    Raises
    ----------
    """

    check_sequencer_index(sequencer)
    return funcs._get_sequencer_config(sequencer)


# --------------------------------------------------------------------------
def set_sequencer_config_val(
    funcs: FuncRefs, sequencer: int, keys: Any, val: Any
) -> None:
    """
    Set value of specific sequencer parameter.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof
    val : Any
        Value to set parameter to.

    Returns
    ----------

    Raises
    ----------
    """
    # Normalize keys argument.
    if not isinstance(keys, str) and hasattr(keys, "__iter__"):
        keys = tuple(keys)
    else:
        keys = [keys]

    # Get configuration.
    cfg = get_sequencer_config(funcs, sequencer)

    # Walk to the right "directory" in the hierarchy.
    d = cfg
    for key in keys[:-1]:
        if (
            isinstance(d, list)
            and (not isinstance(key, int) or key < 0 or key >= len(d))
        ) or (isinstance(d, dict) and (not isinstance(key, str) or key not in d)):
            raise KeyError(
                f'cfg_dict[{"][".join(str(e) for e in keys)}] is not a valid sequencer path, failed at {key}'
            )
        if key == "acq" or key == "awg":
            d = d[key][0]
        else:
            d = d[key]

    key = keys[-1]
    if (
        isinstance(d, list) and (not isinstance(key, int) or key < 0 or key >= len(d))
    ) or (isinstance(d, dict) and (not isinstance(key, str) or key not in d)):
        raise KeyError(
            f'cfg_dict[{"][".join(str(e) for e in keys)}] is not a valid sequencer path, failed at {key}'
        )

    # Make sure val has the right JSON type; try casting it if not.
    cur = d[keys[-1]]
    for typ in (int, float, str, bool):
        if isinstance(cur, typ):
            try:
                val = typ(val)
            except (ValueError, TypeError) as e:
                raise TypeError(
                    f'{".".join(str(e) for e in keys)} should be of type {typ.__name__}: {e}'
                )
            break
    else:
        # Probably a dict or array! Can't set those directly.
        raise KeyError(
            f'{".".join(str(e) for e in keys)} is an incomplete sequencer path'
        )

    # Set the new value.
    if isinstance(d[keys[-1]], bool):
        d[keys[-1]] = True if val == 1 else False
    else:
        d[keys[-1]] = val
    set_sequencer_config(funcs, sequencer, cfg)


# --------------------------------------------------------------------------
def get_sequencer_config_val(funcs: FuncRefs, sequencer: int, keys: Any) -> Any:
    """
    Get value of specific sequencer parameter.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    keys : Union[List[str], str]
        Configuration key to access, or hierarchical list thereof

    Returns
    ----------
    Any
        Parameter value.

    Raises
    ----------
    """

    # Normalize keys argument.
    if not isinstance(keys, str) and hasattr(keys, "__iter__"):
        keys = tuple(keys)
    else:
        keys = [keys]

    val = get_sequencer_config(funcs, sequencer)
    for key in keys:
        if (
            isinstance(val, list)
            and (not isinstance(key, int) or key < 0 or key >= len(val))
        ) or (isinstance(val, dict) and (not isinstance(key, str) or key not in val)):
            raise KeyError(
                f'cfg_dict[{"][".join(str(e) for e in keys)}] is not a valid sequencer path, failed at {key}'
            )
        if key == "acq" or key == "awg":
            val = val[key][0]
        else:
            val = val[key]
    return val


# ----------------------------------------------------------------------------
def set_sequencer_config_rotation_matrix(
    funcs: FuncRefs, sequencer: int, phase_incr: float
) -> None:
    """
    Sets the integration result phase rotation matrix in the acquisition path.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    phase_incr : float
        Phase increment in degrees.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_qrm_type(funcs.is_qrm_type())

    cfg_dict = get_sequencer_config(funcs, sequencer)

    cfg_dict["acq"][0]["th_acq"]["rotation_matrix_a11"] = numpy.cos(
        numpy.deg2rad(360 - phase_incr)
    )
    cfg_dict["acq"][0]["th_acq"]["rotation_matrix_a12"] = numpy.sin(
        numpy.deg2rad(360 - phase_incr)
    )

    set_sequencer_config(funcs, sequencer, cfg_dict)


# ----------------------------------------------------------------------------
def get_sequencer_config_rotation_matrix(funcs: FuncRefs, sequencer: int) -> float:
    """
    Gets the integration result phase rotation matrix in the acquisition path.

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------
    float
        Phase increment in degrees.

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_qrm_type(funcs.is_qrm_type())
    cfg = get_sequencer_config(funcs, sequencer)
    vector = (
        cfg["acq"][0]["th_acq"]["rotation_matrix_a11"]
        + cfg["acq"][0]["th_acq"]["rotation_matrix_a12"] * 1j
    )
    phase_incr = numpy.angle(vector, deg=True)
    if phase_incr == 0:
        return 0
    elif phase_incr >= 0:
        return 360 - phase_incr
    else:
        return -1.0 * phase_incr


# -----------------------------------------------------------------------------
class _ChannelMapCache:
    AWG = 0
    ACQ = 1

    def __init__(self, funcs: FuncRefs):
        self._funcs = funcs
        self._num_seq = 6
        if self._funcs.is_qrm_type():
            self._num_dac = 2
            self._num_adc = 2
        else:
            self._num_dac = 4
            self._num_adc = 0
        self._current = {
            self.AWG: [None] * self._num_seq,
            self.ACQ: [None] * self._num_seq,
        }
        self._writeback = {
            self.AWG: [None] * self._num_seq,
            self.ACQ: [None] * self._num_seq,
        }

    def _check_direction(self, direction: int):
        if direction not in [self.AWG, self.ACQ]:
            raise ValueError(f"Invalid direction: {direction!r}")

    def _check_seq(self, seq: int):
        if not isinstance(seq, int):
            raise TypeError(f"seq should be int but is {type(seq).__name__}")
        if seq < 0 or seq >= self._num_seq:
            raise ValueError(f"seq is out of range: {seq}")

    def _check_dac(self, dac: int):
        if not isinstance(dac, int):
            raise TypeError(f"dac should be int but is {type(dac).__name__}")
        if dac < 0 or dac >= self._num_dac:
            raise ValueError(f"dac is out of range: {dac}")

    def _check_adc(self, adc: int):
        if not isinstance(adc, int):
            raise TypeError(f"adc should be int but is {type(adc).__name__}")
        if adc < 0 or adc >= self._num_adc:
            raise ValueError(f"adc is out of range: {adc}")

    def _check_channel(self, direction: int, channel: int):
        self._check_direction(direction)
        if direction == self.AWG:
            self._check_dac(channel)
        else:
            self._check_adc(channel)

    def _check_path(self, path: int):
        if not isinstance(path, int):
            raise TypeError(f"path should be int but is {type(path).__name__}")
        if path < 0 or path >= 2:
            raise ValueError(f"path is out of range: {path}")

    def _get_cache(self, direction: int, seq: int):
        """Returns a writable reference to the writeback cache entry for the
        channel map data for the given signal direction and sequencer."""
        self._check_direction(direction)
        self._check_seq(seq)

        # If we already have this in our writeback cache, return that entry.
        if self._writeback[direction][seq] is not None:
            return self._writeback[direction][seq]

        # If we don't know the current state yet, fetch it from the device.
        if self._current[direction][seq] is None:
            # Fetch from the device.
            if direction == self.AWG:
                current = self._funcs._get_sequencer_channel_map(seq)
            elif self._num_adc > 0:
                current = self._funcs._get_sequencer_acq_channel_map(seq)
            else:
                current = [[], []]

            # Convert the inner JSON arrays to the sets they represent.
            # Otherwise the equality check between current and desired
            # can give false negatives.
            for i in range(len(current)):
                current[i] = set(current[i])

            # Update current state cache.
            self._current[direction][seq] = current

        # Make a writeback cache entry for the current state. We make a copy
        # so the caller can update it.
        self._writeback[direction][seq] = copy.deepcopy(self._current[direction][seq])

        return self._writeback[direction][seq]

    def _set_cache(self, direction: int, seq: int, state: List[Set[int]]):
        """Overrides the writeback cache entry for the channel map data for
        the given signal direction and sequencer."""
        self._check_direction(direction)
        self._check_seq(seq)
        self._writeback[direction][seq] = state

    def _flush_cache(self, direction: int, seq: int):
        """Flushes any pending changes for the given direction and sequencer to
        the instrument."""
        self._check_direction(direction)
        self._check_seq(seq)

        writeback = self._writeback[direction][seq]

        # Return if there is no writeback cache entry.
        if writeback is None:
            return

        # Also return if there is a writeback cache entry but it matches the
        # current state already.
        if writeback == self._current[direction][seq]:
            return

        # Convert the sets to lists.
        writeback = list(map(list, writeback))

        # Write to the instrument.
        if direction == self.AWG:
            self._funcs._set_sequencer_channel_map(seq, writeback)
        elif self._num_adc > 0:
            self._funcs._set_sequencer_acq_channel_map(seq, writeback)
        else:
            raise RuntimeError(
                "attempting to set acquisition channel map on instrument with no ADCs"
            )

        # Copy from the writeback cache to the current state cache to reflect
        # the changes made.
        self._current[direction][seq] = copy.deepcopy(self._writeback[direction][seq])

        # Clear the writeback cache entry.
        self._writeback[direction][seq] = None

    def clear_path(self, direction: int, seq: int, path: int):
        """Clears all connections to the given path of the given sequencer in
        the given direction."""
        self._check_direction(direction)
        self._check_seq(seq)
        self._get_cache(direction, seq)[path].clear()

    def clear(self, direction: Optional[int] = None, seq: Optional[int] = None):
        """Clears all connections to the given sequencer (or all of them if
        None) in the given direction (or both if None)."""
        if direction is None:
            self.clear(self.AWG, seq)
            self.clear(self.ACQ, seq)
            return
        if seq is None:
            for seq in range(self._num_seq):
                self.clear(direction, seq)

        self._check_direction(direction)
        self._check_seq(seq)
        self._set_cache(direction, seq, [set(), set()])

    def connect(
        self,
        direction: int,
        seq: int,
        path: int,
        channel: int,
        resolve_conflicts: bool = True,
    ):
        """Updates the (cached) channel map to make the given connection. If
        this connection conflicts with an existing connection, behavior depends
        on resolve_conflicts: if set, the offending connection is first
        disconnected if possible; if cleared, a RuntimeError is raised."""

        self._check_channel(direction, channel)
        self._check_seq(seq)
        self._check_path(path)

        cache = self._get_cache(direction, seq)

        # The I and Q path of a sequencer cannot both be tied to a DAC
        # simultaneously.
        if direction == self.AWG and channel in cache[1 - path]:
            if not resolve_conflicts:
                raise RuntimeError(
                    f"DAC {channel} is already connected to the other I/Q path of sequencer {seq}"
                )
            cache[1 - path].discard(channel)

        # An acquisition input can only be tied to one ADC at a time.
        if direction == self.ACQ and cache[path] and channel not in cache[path]:
            if not resolve_conflicts:
                raise RuntimeError(
                    f"acquisition path {path} ({'IQ'[path]}) is already connected to another input"
                )
            cache[path].clear()

        # Raise if the connection already exists.
        if not resolve_conflicts and channel in cache[path]:
            raise RuntimeError(f"connection already exists")

        cache[path].add(channel)

    def disconnect(self, direction: int, seq: int, path: int, channel: int):
        """Updates the (cached) channel map to disable the given connection."""
        self._check_channel(direction, channel)
        self._check_seq(seq)
        self._check_path(path)
        self._get_cache(direction, seq)[path].discard(channel)

    def is_connected(self, direction: int, seq: int, path: int, channel: int) -> bool:
        """Returns whether the given connection is currently enabled (in
        cache)."""
        self._check_channel(direction, channel)
        self._check_seq(seq)
        self._check_path(path)
        return channel in self._get_cache(direction, seq)[path]

    def get_connected_channels(self, direction: int, seq: int, path: int) -> bool:
        """Returns a list of the channels connected to the given
        direction/sequencer/path triple."""
        self._check_direction(direction)
        self._check_seq(seq)
        self._check_path(path)
        yield from self._get_cache(direction, seq)[path]

    def iter_connections(self) -> Iterator[Tuple[int, str, str]]:
        """Iterates over all enabled connections between ADCs, DACs, and
        sequencers. The four components of each connection are:
         - the index of the sequencer for the connection;
         - the connection point of the sequencer being connected to, being
           one of `I`, `Q`, `acq_I`, or `acq_Q`;
         - the external connection, being either `adc#` or `dac#`, where
           `#` is the zero-based ADC or DAC index."""
        for seq in range(self._num_seq):
            for path, name in [(0, "I"), (1, "Q")]:
                for channel in self.get_connected_channels(self.AWG, seq, path):
                    yield seq, name, f"dac{channel}"
            if self._num_adc:
                for path, name in [(0, "acq_I"), (1, "acq_Q")]:
                    for channel in self.get_connected_channels(self.ACQ, seq, path):
                        yield seq, name, f"adc{channel}"

    def flush(self):
        """Flushes pending changes to the channel map to the instrument."""
        for seq in range(self._num_seq):
            self._flush_cache(self.AWG, seq)
        if self._num_adc:
            for seq in range(self._num_seq):
                self._flush_cache(self.ACQ, seq)

    def __enter__(self):
        """Allow usage as a context manager, such that the instrument will be
        updated when the context closes."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self.flush()


# -----------------------------------------------------------------------------
def set_sequencer_connect_out(
    funcs: FuncRefs, sequencer: int, output: int, state: Union[str, bool]
) -> None:
    """
    Set whether the output of the indexed sequencer is connected to the given
    output and if so with which path.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    output : int
        Zero-based output index.
    state : str | bool
        - For baseband modules, one of:
            - "off": the output is not connected.
            - "I": the output is connected to path0/I.
            - "Q": the output is connected to path1/Q.
        - For RF modules, one of:
            - "off" or False: the RF output is not connected.
            - "IQ" or True: the RF output is connected.

    Returns
    ----------

    Raises
    ----------
    """
    check_sequencer_index(sequencer)

    with _ChannelMapCache(funcs) as channel_map:
        # Note that for RF modules, each connect_out parameter controls the
        # configuration for two DACs, hardwired to the I and Q input of the
        # RF mixer on the front end. It doesn't make sense to control the
        # DACs individually in this case.
        if funcs.is_rf_type():
            if state is False or state == "off":
                channel_map.disconnect(_ChannelMapCache.AWG, sequencer, 0, output * 2)
                channel_map.disconnect(
                    _ChannelMapCache.AWG, sequencer, 0, output * 2 + 1
                )
                channel_map.disconnect(_ChannelMapCache.AWG, sequencer, 1, output * 2)
                channel_map.disconnect(
                    _ChannelMapCache.AWG, sequencer, 1, output * 2 + 1
                )
            elif state is True or state == "IQ":
                channel_map.connect(_ChannelMapCache.AWG, sequencer, 0, output * 2)
                channel_map.connect(_ChannelMapCache.AWG, sequencer, 1, output * 2 + 1)
            else:
                raise ValueError(
                    f"invalid new connection state {state!r} for RF device"
                )
        else:
            if state == "off":
                channel_map.disconnect(_ChannelMapCache.AWG, sequencer, 0, output)
                channel_map.disconnect(_ChannelMapCache.AWG, sequencer, 1, output)
            elif state == "I":
                channel_map.connect(_ChannelMapCache.AWG, sequencer, 0, output)
                channel_map.disconnect(_ChannelMapCache.AWG, sequencer, 1, output)
            elif state == "Q":
                channel_map.disconnect(_ChannelMapCache.AWG, sequencer, 0, output)
                channel_map.connect(_ChannelMapCache.AWG, sequencer, 1, output)
            else:
                raise ValueError(
                    f"invalid new connection state {state!r} for baseband device"
                )


# -----------------------------------------------------------------------------
def get_sequencer_connect_out(funcs: FuncRefs, sequencer: int, output: int) -> str:
    """
    Returns whether the output of the indexed sequencer is connected to the
    given output and if so with which path.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    output : int
        Zero-based output index.

    Returns
    ----------
    str
        - For baseband modules, one of:
            - "off": the output is not connected.
            - "I": the output is connected to path0/I.
            - "Q": the output is connected to path1/Q.
        - For RF modules, one of:
            - "off": the RF output is not connected.
            - "IQ": the RF output is connected.

    Raises
    ----------
    """
    check_sequencer_index(sequencer)

    with _ChannelMapCache(funcs) as channel_map:
        # Note that for RF modules, each connect_out parameter controls the
        # configuration for two DACs, hardwired to the I and Q input of the
        # RF mixer on the front end. It doesn't make sense to control the
        # DACs individually in this case, and as such the user isn't given
        # that level of control, but nevertheless the channel map state
        # could hypothetically be in some weird in-between state. However,
        # since we have to return something either way, just checking one
        # of the paths should be good enough.
        if funcs.is_rf_type():
            if channel_map.is_connected(_ChannelMapCache.AWG, sequencer, 0, output * 2):
                return "IQ"
        elif channel_map.is_connected(_ChannelMapCache.AWG, sequencer, 0, output):
            return "I"
        elif channel_map.is_connected(_ChannelMapCache.AWG, sequencer, 1, output):
            return "Q"
    return "off"


# -----------------------------------------------------------------------------
def set_sequencer_connect_acq(
    funcs: FuncRefs, sequencer: int, path: int, state: Union[str, bool]
) -> None:
    """
    Set whether the input of the indexed sequencer's acquisition path is
    connected to an external input and if so which.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    path : int
        Path index: 0 for baseband path0/I, 1 for baseband path1/Q, ignored for
        RF.
    state : str | bool
        - One of:
            - "off" or False: connection disabled.
            - "in#": the acquisition input path is connected to external input #, where # is a zero-based input index.
            - True: if there is only one option other than off, True is allowed as alias.

    Returns
    ----------

    Raises
    ----------
    """
    check_sequencer_index(sequencer)
    check_qrm_type(funcs.is_qrm_type())

    # Desugar state input.
    if state is False:
        input = None
    elif state is True and funcs.is_rf_type():
        input = 0  # only 1 input
    elif state == "off":
        input = None
    elif m := re.fullmatch(r"in(0|[1-9][0-9]*)", state):
        input = int(m.group(1))
    else:
        raise ValueError(f"invalid new connection state {state!r}")

    with _ChannelMapCache(funcs) as channel_map:
        # Note that for RF modules, each connect_acq parameter controls the
        # configuration for both paths of the acquisition engine, because
        # each input maps to two ADCs.
        if funcs.is_rf_type():
            channel_map.clear(_ChannelMapCache.ACQ, sequencer)
            if input is not None:
                channel_map.connect(_ChannelMapCache.ACQ, sequencer, 0, input * 2)
                channel_map.connect(_ChannelMapCache.ACQ, sequencer, 1, input * 2 + 1)
        else:
            channel_map.clear_path(_ChannelMapCache.ACQ, sequencer, path)
            if input is not None:
                channel_map.connect(_ChannelMapCache.ACQ, sequencer, path, input)


# -----------------------------------------------------------------------------
def get_sequencer_connect_acq(funcs: FuncRefs, sequencer: int, path: int) -> str:
    """
    Get whether the input of the indexed sequencer's acquisition path is
    connected to an external input and if so which.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    path : int
        Path index: 0 for baseband path0/I, 1 for baseband path1/Q, ignored for
        RF.

    Returns
    ----------
    str
        -One of:
            - "off": connection disabled.
            - "in#": the acquisition input path is connected to external input #, where # is a zero-based input index.

    Raises
    ----------
    """
    check_sequencer_index(sequencer)
    check_qrm_type(funcs.is_qrm_type())

    with _ChannelMapCache(funcs) as channel_map:
        channels = list(
            channel_map.get_connected_channels(_ChannelMapCache.ACQ, sequencer, path)
        )

    if not channels:
        return "off"

    # If multiple inputs are connected to the same acquisition path in the
    # channel map (an illegal configuration), do the same thing the firmware
    # does, which is prioritizing lower-indexed channels because there is no
    # good error path here.
    channel = min(channels)

    # Divide by two for RF modules to map from ADC channel to input, as there
    # are two ADCs per input (I and Q). For baseband modules the mapping is
    # one to one.
    if funcs.is_rf_type():
        channel //= 2

    return f"in{channel}"


# -----------------------------------------------------------------------------
def disconnect_outputs(funcs: FuncRefs) -> None:
    """
    Disconnects all outputs from the sequencers.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """
    with _ChannelMapCache(funcs) as channel_map:
        channel_map.clear(_ChannelMapCache.AWG)


# -----------------------------------------------------------------------------
def disconnect_inputs(funcs: FuncRefs) -> None:
    """
    Disconnects all inputs from the sequencers.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """
    check_qrm_type(funcs.is_qrm_type())
    with _ChannelMapCache(funcs) as channel_map:
        channel_map.clear(_ChannelMapCache.ACQ)


# -----------------------------------------------------------------------------
def iter_connections(funcs: FuncRefs) -> Iterator[Tuple[int, str, str]]:
    """
    Iterates over all enabled connections between ADCs, DACs, and
    sequencers.

    Parameters
    ----------

    Returns
    ----------
    Iterator[tuple[int, str, str]]
        An iterator of connections. The four components of each connection
        are:

            - the index of the sequencer for the connection;
            - the connection point of the sequencer being connected to, being one of `I`, `Q`, `acq_I`, or `acq_Q`;
            - the external connection, being either `adc#` or `dac#`, where `#` is the zero-based ADC or DAC index.

        Note that these are ADC and DAC indices. For baseband modules,
        these indices map one-to-one to the external SMA ports, but for RF
        modules they don't: each pair of DACs or ADCs maps to a single RF
        port, the I component being generated by ADC/DAC index 0/2/... and
        the Q component being generated by ADC/DAC index 1/3/...

    Raises
    ----------
    """
    return _ChannelMapCache(funcs).iter_connections()


# -----------------------------------------------------------------------------
def sequencer_connect(funcs: FuncRefs, sequencer: int, *connections: str) -> None:
    """
    Makes new connections between the indexed sequencer and some inputs and/or
    outputs. This will fail if a requested connection already existed, or if
    the connection could not be made due to a conflict with an existing
    connection (hardware constraints). In such a case, the channel map will
    not be affected.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    *connections : str
        Zero or more connections to make, each specified using a string. The
        string should have the format `<direction><channel>` or
        `<direction><I-channel>_<Q-channel>`. `<direction>` must be `in` to
        make a connection between an input and the acquisition path, `out` to
        make a connection from the waveform generator to an output, or `io` to
        do both. The channels must be integer channel indices. If only one
        channel is specified, the sequencer operates in real mode; if two
        channels are specified, it operates in complex mode.

    Returns
    ----------

    Raises
    ----------
    RuntimeError
        If the connection command could not be completed due to a conflict.
    ValueError
        If parsing of a connection fails.
    """

    # Intentionally don't use the context manager: in case of an exception,
    # do not make *any* changes.
    channel_map = _ChannelMapCache(funcs)
    is_rf = funcs.is_rf_type()

    for index, connection in enumerate(connections):
        try:
            # Parse syntax.
            m = re.fullmatch(
                r"(in|out|io)(0|[1-9][0-9]*)(?:_(0|[1-9][0-9]*))?", connection
            )
            if not m:
                raise ValueError(f"syntax error")

            # Decode direction.
            directions = []
            if m.group(1) != "in":
                directions.append(_ChannelMapCache.AWG)
            if m.group(1) != "out":
                directions.append(_ChannelMapCache.ACQ)

            # Decode channel indices.
            i_channel = int(m.group(2))
            q_channel = m.group(3)
            if q_channel is not None:
                q_channel = int(q_channel)

            # Catch some expected mistakes gracefully.
            if i_channel == q_channel:
                suggestion = m.group(1) + m.group(2)
                raise ValueError(
                    "cannot connect I and Q path to the same I/O port "
                    f"(did you mean {suggestion!r}?)"
                )
            if is_rf and q_channel is not None:
                message = "for RF connections, only one I/O port should be specified"
                if i_channel % 2 == 0 and q_channel == i_channel + 1:
                    # they're probably thinking in terms of DAC/ADC indices
                    suggestion = f"{m.group(1)}{i_channel // 2}"
                    message += f" (you may be confused with DAC/ADC indices, did you mean {suggestion!r}?)"
                raise ValueError(message)

            # Convert from I/O indices to DAC/ADC indices on RF devices.
            if is_rf:
                q_channel = i_channel * 2 + 1
                i_channel = i_channel * 2

            # Try to apply the changes.
            for direction in directions:
                channel_map.connect(direction, sequencer, 0, i_channel, False)
                if q_channel is not None:
                    channel_map.connect(direction, sequencer, 1, q_channel, False)

        except RuntimeError as e:
            raise RuntimeError(
                f"connection command {connection!r} (index {index}): {e}"
            )
        except ValueError as e:
            raise ValueError(f"connection command {connection!r} (index {index}): {e}")

    # Everything seems to have worked: write new configuration to the
    # instrument.
    channel_map.flush()


# ----------------------------------------------------------------------------
def arm_sequencer(funcs: FuncRefs, scpi_cmd_prefix: str) -> None:
    """
    Prepare the indexed sequencer to start by putting it in the armed state.
    If no sequencer index is given, all sequencers are armed. Any sequencer
    that was already running is stopped and rearmed. If an invalid sequencer
    index is given, an error is set in system error.

    Parameters
    ----------
    sequencer : Optional[int]
        Sequencer index.

    Returns
    ----------

    Raises
    ----------
    RuntimeError
        An error is reported in system error and debug <= 1.
        All errors are read from system error and listed in the exception.
    """

    # The SCPI command prefix is set by the native instrument layer so that
    # it can select to arm a specific sequencer (e.g. "SLOT1:SEQuencer0") or
    # all sequencers (e.g. "SLOT:SEQuencer")
    # The actual SCPI call is wrapped in a function to make use of the
    # scpi_error_check method.
    @scpi_error_check
    def arm_sequencer_func(instrument: Any):
        funcs._write(f"{scpi_cmd_prefix}:ARM")

    arm_sequencer_func(funcs.instrument)


# ----------------------------------------------------------------------------
def start_sequencer(funcs: FuncRefs, scpi_cmd_prefix: str) -> None:
    """
    Start the indexed sequencer, thereby putting it in the running state.
    If an invalid sequencer index is given or the indexed sequencer was not
    yet armed, an error is set in system error. If no sequencer index is
    given, all armed sequencers are started and any sequencer not in the armed
    state is ignored. However, if no sequencer index is given and no
    sequencers are armed, and error is set in system error.

    Parameters
    ----------
    sequencer : Optional[int]
        Sequencer index.

    Returns
    ----------

    Raises
    ----------
    RuntimeError
        An error is reported in system error and debug <= 1.
        All errors are read from system error and listed in the exception.
    """

    # The SCPI command prefix is set by the native instrument layer so that
    # it can select to start a specific sequencer (e.g. "SLOT1:SEQuencer0") or
    # all sequencers (e.g. "SLOT:SEQuencer")
    # The actual SCPI call is wrapped in a function to make use of the
    # scpi_error_check method.
    @scpi_error_check
    def start_sequencer_func(instrument: Any):
        funcs._write(f"{scpi_cmd_prefix}:START")

    start_sequencer_func(funcs.instrument)


# ----------------------------------------------------------------------------
def stop_sequencer(funcs: FuncRefs, scpi_cmd_prefix: str) -> None:
    """
    Stop the indexed sequencer, thereby putting it in the stopped state. If
    an invalid sequencer index is given, an error is set in system error. If
    no sequencer index is given, all sequencers are stopped.

    Parameters
    ----------
    sequencer : Optional[int]
        Sequencer index.

    Returns
    ----------

    Raises
    ----------
    RuntimeError
        An error is reported in system error and debug <= 1.
        All errors are read from system error and listed in the exception.
    """

    # The SCPI command prefix is set by the native instrument layer so that
    # it can select to stop a specific sequencer (e.g. "SLOT1:SEQuencer0") or
    # all sequencers (e.g. "SLOT:SEQuencer")
    # The actual SCPI call is wrapped in a function to make use of the
    # scpi_error_check method.
    @scpi_error_check
    def stop_sequencer_func(instrument: Any):
        funcs._write(f"{scpi_cmd_prefix}:STOP")

    stop_sequencer_func(funcs.instrument)


# ----------------------------------------------------------------------------
def clear_sequencer_flags(funcs: FuncRefs, scpi_cmd_prefix: str) -> None:
    """
    Clear flags

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------
    """

    # The SCPI command prefix is set by the native instrument layer so that
    # it can select to clear a specific sequencer flag (e.g. "SLOT1:SEQuencer0") or
    # all sequencers (e.g. "SLOT:SEQuencer")
    # The actual SCPI call is wrapped in a function to make use of the
    # scpi_error_check method.
    @scpi_error_check
    def clear_sequencer_flags(instrument: Any):
        funcs._write(f"{scpi_cmd_prefix}:CLR:FLAGS")

    clear_sequencer_flags(funcs.instrument)


def _parse_sequencer_status(full_status_str: str) -> tuple([list, list, list, list]):
    """
    Private helper funtion to parse the output of sequencer status cmd.

    Parameters
    ----------
    full_status_str : str
        Full string from command response.

    Returns
    ----------
        status Status parsed string
        state  State parsed string
        flags_list List of all flags
        log Extra log parsed from the cmd
    """

    full_status_list = re.sub(" |-", "_", full_status_str).split(";")

    # STATUS;STATE;INFO_FLAGS;WARN_FLAGS;ERR_FLAGS;LOG
    status = full_status_list[0]  # They are always present
    state = full_status_list[1]  # They are always present

    if full_status_list[2] != "":
        info_flag_list = full_status_list[2].split(",")[:-1]
    else:
        info_flag_list = []

    if full_status_list[3] != "":
        warn_flag_list = full_status_list[3].split(",")[:-1]
    else:
        warn_flag_list = []

    if full_status_list[4] != "":
        err_flag_list = full_status_list[4].split(",")[:-1]
    else:
        err_flag_list = []

    if full_status_list[5] != "":
        log = full_status_list[5]
    else:
        log = []

    return status, state, info_flag_list, warn_flag_list, err_flag_list, log


# ----------------------------------------------------------------------------
def get_sequencer_state(
    funcs: FuncRefs, sequencer: int, timeout: int = 0, timeout_poll_res: float = 0.02
) -> SequencerState:
    """
    Get the sequencer state. If an invalid sequencer index is given, an error
    is set in system error. If the timeout is set to zero, the function
    returns the state immediately. If a positive non-zero timeout is set, the
    function blocks until the sequencer completes. If the sequencer hasn't
    stopped before the timeout expires, a TimeoutError is thrown.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    timeout : int
        Timeout in minutes.
    timeout_poll_res : float
        Timeout polling resolution in seconds.

    Returns
    ----------
    SequencerState
        Tuple containing sequencer status and corresponding flags.

    Raises
    ----------
    TimeoutError
        Timeout
    """
    warnings.warn(
        """
        After June 2024, this feature is subject to removal in future releases.
        Transition to an alternative is advised.
        See https://qblox-qblox-instruments.readthedocs-hosted.com/en/main/getting_started/deprecated.html
        """,
        FutureWarning,
    )
    # Format status string
    check_sequencer_index(sequencer)
    full_status = funcs._get_sequencer_state(sequencer)
    status, state, info_flags, warn_flags, err_flags, log = _parse_sequencer_status(
        full_status
    )

    state_flags = info_flags + warn_flags + err_flags
    state_tuple = SequencerState(
        SequencerStatusOld[state],
        [SequencerStatusFlags[flag] for flag in state_flags],
    )

    elapsed_time = 0.0
    start_time = time.time()
    timeout = timeout * 60.0
    while (
        state_tuple.status == SequencerStatusOld.RUNNING
        or state_tuple.status == SequencerStatusOld.Q1_STOPPED
    ) and elapsed_time < timeout:
        time.sleep(timeout_poll_res)

        state_tuple = get_sequencer_state(funcs, sequencer)
        elapsed_time = time.time() - start_time

        if elapsed_time >= timeout:
            raise TimeoutError(
                f"Sequencer {sequencer} did not stop in timeout period of {int(timeout / 60)} minutes."
            )

    return state_tuple


# ----------------------------------------------------------------------------
def get_sequencer_status(
    funcs: FuncRefs, sequencer: int, timeout: int = 0, timeout_poll_res: float = 0.02
) -> SequencerStatus:
    """
    Get the sequencer status. If an invalid sequencer index is given, an error
    is set in system error. If the timeout is set to zero, the function
    returns the state immediately. If a positive non-zero timeout is set, the
    function blocks until the sequencer completes. If the sequencer hasn't
    stopped before the timeout expires, a TimeoutError is thrown.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    timeout : int
        Timeout in minutes.
    timeout_poll_res : float
        Timeout polling resolution in seconds.

    Returns
    ----------
    SequencerState
        Tuple containing sequencer status and corresponding flags.

    Raises
    ----------
    TimeoutError
        Timeout
    """

    # Format status string
    check_sequencer_index(sequencer)
    full_status = funcs._get_sequencer_state(sequencer)

    status, state, info_flags, warn_flags, err_flags, log = _parse_sequencer_status(
        full_status
    )

    state_tuple = SequencerStatus(
        SequencerStatuses[status],
        SequencerStates[state],
        [SequencerStatusFlags[flag] for flag in info_flags],
        [SequencerStatusFlags[flag] for flag in warn_flags],
        [SequencerStatusFlags[flag] for flag in err_flags],
        log,
    )

    elapsed_time = 0.0
    start_time = time.time()
    timeout = timeout * 60.0
    while (
        state_tuple.state == SequencerStates.RUNNING
        or state_tuple.state == SequencerStates.Q1_STOPPED
    ) and elapsed_time < timeout:
        time.sleep(timeout_poll_res)

        state_tuple = get_sequencer_status(funcs, sequencer)
        elapsed_time = time.time() - start_time

        if elapsed_time >= timeout:
            raise TimeoutError(
                f"Sequencer {sequencer} did not stop in timeout period of {int(timeout / 60)} minutes."
            )

    return state_tuple


# ----------------------------------------------------------------------------
def arm_scope_trigger(funcs: FuncRefs) -> None:
    """
    Prepare the scope trigger to start by putting it in the armed state.
    If it was already running, it is stopped and rearmed.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    RuntimeError
        An error is reported in system error and debug <= 1.
        All errors are read from system error and listed in the exception.
    """

    check_qtm_type(funcs.is_qtm_type())
    funcs._arm_scope_trigger()


# ----------------------------------------------------------------------------
def _add_awg_waveform(
    funcs: FuncRefs,
    sequencer: int,
    name: str,
    waveform: List[float],
    index: Optional[int] = None,
) -> None:
    """
    Add new waveform to AWG waveform list of indexed sequencer's AWG path. If
    an invalid sequencer index is given or if the waveform causes the waveform
    memory limit to be exceeded or if the waveform samples are out-of-range,
    an error is set in the system error. The waveform names 'all' and 'ALL'
    are reserved and adding waveforms with those names will also result in an
    error being set in system error. The optional index argument is used to
    specify an index for the waveform in the waveform list which is used by
    the sequencer Q1ASM program to refer to the waveform. If no index is
    given, the next available waveform index is selected (starting from 0).
    If an invalid waveform index is given, an error is set in system error.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    name : str
        Waveform name.
    waveform : list
        List of floats in the range of 1.0 to -1.0 representing the waveform.
    index : Optional[int]
        Waveform index of the waveform in the waveform list.

    Returns
    ----------

    Raises
    ----------
    """

    funcs._add_awg_waveform(sequencer, name, len(waveform), False)
    funcs._set_awg_waveform_data(sequencer, name, waveform)
    if index is not None:
        funcs._set_awg_waveform_index(sequencer, name, index)


# ----------------------------------------------------------------------------
# Note: decorator uses instrument argument
@scpi_error_check
def _get_awg_waveforms(instrument: Any, funcs: FuncRefs, sequencer: int) -> Dict:
    """
    Get all waveforms in waveform list of indexed sequencer's AWG path. If an
    invalid sequencer index is given, an error is set in system error.

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------
    dict
        Dictionary with waveforms.

    Raises
    ----------
    RuntimeError
        An error is reported in system error and debug <= 1.
        All errors are read from system error and listed in the exception.
    """

    # SCPI call
    num_waveforms = struct.unpack("I", funcs._get_awg_waveforms(sequencer))[0]
    if num_waveforms == 0:
        funcs._flush_line_end()

    waveform_dict = {}
    for wave_it in range(0, num_waveforms):
        # Get name and index
        name = str(funcs._read_bin("", False), "utf-8")
        index = struct.unpack("I", funcs._read_bin("", False))[0]

        # Get data
        data = funcs._read_bin("", wave_it >= (num_waveforms - 1))
        data = struct.unpack("f" * int(len(data) / 4), data)

        # Add to dictionary
        waveform_dict[name] = {"index": index, "data": list(data)}

    return waveform_dict


# ----------------------------------------------------------------------------
def _add_acq_weight(
    funcs: FuncRefs,
    sequencer: int,
    name: str,
    weight: List[float],
    index: Optional[int] = None,
) -> None:
    """
    Add new weight to acquisition weight list of indexed sequencer's
    acquisition path. If an invalid sequencer index is given or if the weight
    causes the weight memory limit to be exceeded or if the weight samples are
    out-of-range, an error is set in the system error. The weight names 'all'
    and 'ALL' are reserved and adding weights with those names will also
    result in an error being set in system error. The optional index argument
    is used to specify an index for the weight in the weight list which is
    used by the sequencer Q1ASM program to refer to the weight. If no index
    is given, the next available weight index is selected (starting from 0).
    If an invalid weight index is given, an error is set in system error.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    name : str
        Weight name.
    weight : list
        List of floats in the range of 1.0 to -1.0 representing the weight.
    index : Optional[int]
        Weight index of the weight in the weight list.

    Returns
    ----------

    Raises
    ----------
    """

    funcs._add_acq_weight(sequencer, name, len(weight), False)
    funcs._set_acq_weight_data(sequencer, name, weight)
    if index is not None:
        funcs._set_acq_weight_index(sequencer, name, index)


# ----------------------------------------------------------------------------
# Note: decorator uses instrument argument
@scpi_error_check
def _get_acq_weights(instrument: Any, funcs: FuncRefs, sequencer: int) -> Dict:
    """
    Get all weights in weight list of indexed sequencer's acquisition path.
    If an invalid sequencer index is given, an error is set in system error.

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------
    dict
        Dictionary with weights.

    Raises
    ----------
    RuntimeError
        An error is reported in system error and debug <= 1.
        All errors are read from system error and listed in the exception.
    """

    # SCPI call
    num_weights = struct.unpack("I", funcs._get_acq_weights(sequencer))[0]
    if num_weights == 0:
        funcs._flush_line_end()

    weight_dict = {}
    for weight_it in range(0, num_weights):
        # Get name and index
        name = str(funcs._read_bin("", False), "utf-8")
        index = struct.unpack("I", funcs._read_bin("", False))[0]

        # Get data
        data = funcs._read_bin("", weight_it >= (num_weights - 1))
        data = struct.unpack("f" * int(len(data) / 4), data)

        # Add to dictionary
        weight_dict[name] = {"index": index, "data": list(data)}

    return weight_dict


# ----------------------------------------------------------------------------
def _add_acq_acquisition(
    funcs: FuncRefs,
    sequencer: int,
    name: str,
    num_bins: int,
    index: Optional[int] = None,
) -> None:
    """
    Add new acquisition to acquisition list of indexed sequencer's acquisition
    path. If an invalid sequencer index is given or if the required
    acquisition memory cannot be allocated, an error is set in system error.
    The acquisition names 'all' and 'ALL' are reserved and adding those will
    also result in an error being set in system error. If no index is given,
    the next available weight index is selected (starting from 0). If an
    invalid weight index is given, an error is set in system error.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    name : str
        Acquisition name.
    num_bins : int
        Number of bins in acquisition. Maximum is 2^24.
    index : Optional[int]
        Waveform index of the acquisition in the acquisition list.

    Returns
    ----------

    Raises
    ----------
    """

    funcs._add_acq_acquisition(sequencer, name, num_bins)
    if index is not None:
        funcs._set_acq_acquisition_index(sequencer, name, index)


# ----------------------------------------------------------------------------
def _get_acq_data_and_convert(
    funcs: FuncRefs,
    init_read_func: Callable[[Optional[int], Optional[str]], bytes],
    flush_line_end: bool,
) -> Dict:
    """
    Get acquisition data and convert it to a dictionary.

    Parameters
    ----------
    init_read_func : Callable[[Optional[int], Optional[str]], bytes]
        Function that performs the initial binary read.
    flush_line_end : bool
        Indication to flush final characters after final read.

    Returns
    ----------
    dict
        Dictionary with data of single acquisition.

    Raises
    ----------
    """

    acquisition_dict = {
        "scope": {
            "path0": {"data": [], "out-of-range": False, "avg_cnt": 0},
            "path1": {"data": [], "out-of-range": False, "avg_cnt": 0},
        },
        "bins": {
            "integration": {"path0": [], "path1": []},
            "threshold": [],
            "avg_cnt": [],
        },
    }

    sample_width = 12
    max_sample_value = 2 ** (sample_width - 1) - 1
    max_sample_value_sqrd = max_sample_value**2

    # Retrieve scope data
    (
        path0_scope_raw,
        path0_avg_cnt,
        path0_oor,
        path1_scope_raw,
        path1_avg_cnt,
        path1_oor,
    ) = _read_acquisition_raw_data(funcs, init_read_func)

    # Normalize scope data (Ignore division by 0)
    with numpy.errstate(divide="ignore", invalid="ignore"):
        path0_scope = numpy.where(
            path0_avg_cnt > 0,
            path0_scope_raw / max_sample_value / path0_avg_cnt,
            path0_scope_raw / max_sample_value,
        )
        path1_scope = numpy.where(
            path1_avg_cnt > 0,
            path1_scope_raw / max_sample_value / path1_avg_cnt,
            path1_scope_raw / max_sample_value,
        )

    # Retrieve bin data and convert to long values
    path0_raw, path1_raw, valid, avg_cnt, thres_raw = _read_bin_raw_data(
        funcs, flush_line_end
    )

    # Specific data manipultation for QRM
    path0_data = numpy.where(valid, path0_raw / max_sample_value_sqrd, numpy.nan)
    path1_data = numpy.where(valid, path1_raw / max_sample_value_sqrd, numpy.nan)
    thres_data = numpy.where(valid, thres_raw, numpy.nan)
    avg_cnt_data = numpy.where(valid, avg_cnt, 0)

    # Set final results
    acquisition_dict["scope"]["path0"]["data"] = path0_scope.tolist()
    acquisition_dict["scope"]["path0"]["out-of-range"] = path0_oor
    acquisition_dict["scope"]["path0"]["avg_cnt"] = path0_avg_cnt

    acquisition_dict["scope"]["path1"]["data"] = path1_scope.tolist()
    acquisition_dict["scope"]["path1"]["out-of-range"] = path1_oor
    acquisition_dict["scope"]["path1"]["avg_cnt"] = path1_avg_cnt

    acquisition_dict["bins"]["integration"]["path0"] = path0_data.tolist()
    acquisition_dict["bins"]["integration"]["path1"] = path1_data.tolist()
    acquisition_dict["bins"]["threshold"] = thres_data.tolist()
    acquisition_dict["bins"]["avg_cnt"] = avg_cnt_data.tolist()

    return acquisition_dict


# ----------------------------------------------------------------------------
# Next two functions are meant to be used only inside _get_acq_data_* functions
# because they are tighted together of how firmware sends raw scope and bin data
# QTM fix end
# ----------------------------------------------------------------------------
def _read_bin_raw_data(funcs, flush_line_end):
    bins = funcs._read_bin("", flush_line_end)
    bin_data = numpy.frombuffer(bins, dtype=numpy.int64).reshape(-1, 4)
    valid = bin_data[:, 0].astype(bool)
    path0_raw = bin_data[:, 1]
    path1_raw = bin_data[:, 2]
    thres_avg_cnt_raw = bin_data[:, 3].astype(numpy.uint64)

    # Thresholded and average count are stored in the same long value so need
    # to be separated. Thresholded is first in stream, thus lower 32 bits.
    thres_raw = thres_avg_cnt_raw & 0xFFFFFFFF
    avg_cnt = thres_avg_cnt_raw >> 32

    # Normalize bin data (Ignore division by 0)
    with numpy.errstate(divide="ignore", invalid="ignore"):
        path0_raw = numpy.where(avg_cnt > 0, path0_raw / avg_cnt, path0_raw)
        path1_raw = numpy.where(avg_cnt > 0, path1_raw / avg_cnt, path1_raw)
        thres_raw = numpy.where(avg_cnt > 0, thres_raw / avg_cnt, thres_raw)

    return path0_raw, path1_raw, valid, avg_cnt, thres_raw


# ----------------------------------------------------------------------------
def _read_acquisition_raw_data(funcs, init_read_func):
    # Retrieve scope data
    scope_data = init_read_func()
    path0_scope_raw = numpy.array(
        struct.unpack("i" * int(len(scope_data) / 4), scope_data)
    )
    path0_oor = struct.unpack("?", funcs._read_bin("", False))[0]
    path0_avg_cnt = struct.unpack("I", funcs._read_bin("", False))[0]
    scope_data = funcs._read_bin("", False)
    path1_scope_raw = numpy.array(
        struct.unpack("i" * int(len(scope_data) / 4), scope_data)
    )
    path1_oor = struct.unpack("?", funcs._read_bin("", False))[0]
    path1_avg_cnt = struct.unpack("I", funcs._read_bin("", False))[0]

    return (
        path0_scope_raw,
        path0_avg_cnt,
        path0_oor,
        path1_scope_raw,
        path1_avg_cnt,
        path1_oor,
    )


# ----------------------------------------------------------------------------
# QTM fix end
# ----------------------------------------------------------------------------
def _get_acq_data(
    funcs: FuncRefs,
    init_read_func: Callable[[Optional[int], Optional[str]], bytes],
    flush_line_end: bool,
) -> Dict:
    """
    Get acquisition data and convert it to a dictionary.

    Parameters
    ----------
    init_read_func : Callable[[Optional[int], Optional[str]], bytes]
        Function that performs the initial binary read.
    flush_line_end : bool
        Indication to flush final characters after final read.

    Returns
    ----------
    dict
        Dictionary with data of single acquisition.

    Raises
    ----------
    """

    # TODO this is only needed here because of the consecutive calls to _read_bin
    # which retrieves data from the socket.
    # So scope_data is not used all in this function
    (
        path0_scope_raw,
        path0_avg_cnt,
        path0_oor,
        path1_scope_raw,
        path1_avg_cnt,
        path1_oor,
    ) = _read_acquisition_raw_data(funcs, init_read_func)

    # Retrieve bin data and convert to long values
    path0_raw, path1_raw, valid, avg_cnt, thres_raw = _read_bin_raw_data(
        funcs, flush_line_end
    )

    # Specific data manipultation for QTM
    path0_data = numpy.where(valid, path0_raw, numpy.nan)
    path1_data = numpy.where(valid, path1_raw, numpy.nan)
    thres_data = numpy.where(valid, thres_raw, numpy.nan)
    avg_cnt_data = numpy.where(valid, avg_cnt, 0)

    # Set final results
    acquisition_dict = {
        "bins": {
            "count": path0_data.tolist(),
            "timedelta": path1_data.tolist(),
            "threshold": thres_data.tolist(),
            "avg_cnt": avg_cnt_data.tolist(),
        },
    }

    return acquisition_dict


# ----------------------------------------------------------------------------
# Note: decorator uses instrument argument
@scpi_error_check
def get_acq_acquisition_data(
    instrument: Any, funcs: FuncRefs, sequencer: int, name: str
) -> Dict:
    """
    Get acquisition data of acquisition in acquisition list of indexed
    sequencer's acquisition path. The acquisition scope and bin data is
    normalized to a range of -1.0 to 1.0 taking both the bit widths of the
    processing path and average count into considaration. For the binned
    integration results, the integration length is not handled during
    normalization and therefore these values have to be divided by their
    respective integration lenghts. If an invalid sequencer index is given or
    if a non-existing acquisition name is given, an error is set in system
    error.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    name : str
        Acquisition name.

    Returns
    ----------
    dict
        Dictionary with data of single acquisition.

    Raises
    ----------
    RuntimeError
        An error is reported in system error and debug <= 1.
        All errors are read from system error and listed in the exception.
    """

    # SCPI call
    check_sequencer_index(sequencer)
    return _get_acq_data_and_convert(
        funcs,
        partial(funcs._get_acq_acquisition_data, sequencer, name),
        True,
    )


# ----------------------------------------------------------------------------
# Note: decorator uses instrument argument
@scpi_error_check
def _get_acq_acquisitions(instrument: Any, funcs: FuncRefs, sequencer: int) -> Dict:
    """
    Get all acquisitions in acquisition list of indexed sequencer's
    acquisition path. If an invalid sequencer index is given, an error is set
    in system error.

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------
    dict
        Dictionary with acquisitions.

    Raises
    ----------
    RuntimeError
        An error is reported in system error and debug <= 1.
        All errors are read from system error and listed in the exception.
    """

    # SCPI call
    num_acq = struct.unpack("I", funcs._get_acq_acquisitions(sequencer))[0]
    if num_acq == 0:
        funcs._flush_line_end()

    acquisition_dict = {}
    for acq_it in range(0, num_acq):
        # Get name and index
        name = str(funcs._read_bin("", False), "utf-8")
        index = struct.unpack("I", funcs._read_bin("", False))[0]

        # Get data
        if funcs.is_qtm_type():
            acq = _get_acq_data(
                funcs, partial(funcs._read_bin, "", False), acq_it >= (num_acq - 1)
            )
        else:
            acq = _get_acq_data_and_convert(
                funcs, partial(funcs._read_bin, "", False), acq_it >= (num_acq - 1)
            )

        # Add to dictionary
        acquisition_dict[name] = {"index": index, "acquisition": acq}

    return acquisition_dict


# ----------------------------------------------------------------------------
def add_waveforms(funcs: FuncRefs, sequencer: int, waveforms: Dict) -> None:
    """
    Add all waveforms in JSON compatible dictionary to the AWG waveform list
    of indexed sequencer. The dictionary must be structured as follows:

    - name: waveform name.

        - data: waveform samples in a range of 1.0 to -1.0.
        - index: optional waveform index used by the sequencer Q1ASM program to refer to the waveform.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    waveforms : dict
        JSON compatible dictionary with one or more waveforms and weigths.

    Returns
    ----------

    Raises
    ----------
    KeyError
        Missing waveform data of waveform in dictionary.
    """

    check_sequencer_index(sequencer)
    for name in waveforms:
        if "data" in waveforms[name]:
            if "index" in waveforms[name]:
                _add_awg_waveform(
                    funcs,
                    sequencer,
                    name,
                    waveforms[name]["data"],
                    waveforms[name]["index"],
                )
            else:
                _add_awg_waveform(funcs, sequencer, name, waveforms[name]["data"])
        else:
            raise KeyError(f"Missing data key for {name} in AWG waveform dictionary")


# ----------------------------------------------------------------------------
def delete_waveform(
    funcs: FuncRefs, sequencer: int, name: str = "", all: bool = False
) -> None:
    """
    Delete a waveform specified by name in the AWG waveform list of indexed
    sequencer or delete all waveforms if `all` is True.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    name : str
        Waveform name
    all : bool
        All waveforms

    Returns
    ----------

    Raises
    ----------
    """

    check_sequencer_index(sequencer)
    funcs._delete_awg_waveform(sequencer, "all" if all else name)


# ----------------------------------------------------------------------------
def get_waveforms(funcs: FuncRefs, sequencer: int) -> Dict:
    """
    Get all waveforms and weigths in the AWG waveform list of indexed
    sequencer. The returned dictionary is structured as follows:

    - name: waveform name.

        - data: waveform samples in a range of 1.0 to -1.0.
        - index: waveform index used by the sequencer Q1ASM program to refer
                 to the waveform.

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------
    dict
        Dictionary with waveforms.

    Raises
    ----------
    """

    check_sequencer_index(sequencer)
    return _get_awg_waveforms(funcs.instrument, funcs, sequencer)


# ----------------------------------------------------------------------------
def add_weights(funcs: FuncRefs, sequencer: int, weights: Dict) -> None:
    """
    Add all weights in JSON compatible dictionary to the aquisition weight
    list of indexed sequencer. The dictionary must be structured as follows:

    - name : weight name.

        - data: weight samples in a range of 1.0 to -1.0.
        - index: optional waveweightform index used by the sequencer Q1ASM program to refer to the weight.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    weights : dict
        JSON compatible dictionary with one or more weigths.

    Returns
    ----------

    Raises
    ----------
    KeyError
        Missing weight data of weight in dictionary.
    NotImplementedError
        Functionality not available on this module.
    """

    check_qrm_type(funcs.is_qrm_type())
    check_sequencer_index(sequencer)
    for name in weights:
        if "data" in weights[name]:
            if "index" in weights[name]:
                _add_acq_weight(
                    funcs,
                    sequencer,
                    name,
                    weights[name]["data"],
                    weights[name]["index"],
                )
            else:
                _add_acq_weight(funcs, sequencer, name, weights[name]["data"])
        else:
            raise KeyError(
                f"Missing data key for {name} in acquisiton weight dictionary"
            )


# ----------------------------------------------------------------------------
def delete_weight(
    funcs: FuncRefs, sequencer: int, name: str = "", all: bool = False
) -> None:
    """
    Delete a weight specified by name in the acquisition weight list of
    indexed sequencer or delete all weights if `all` is True.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    name : str
        Weight name
    all : bool
        All weights

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_qrm_type(funcs.is_qrm_type())
    check_sequencer_index(sequencer)
    funcs._delete_acq_weight(sequencer, "all" if all else name)


# ----------------------------------------------------------------------------
def get_weights(funcs: FuncRefs, sequencer: int) -> Dict:
    """
    Get all weigths in the acquisition weight lists of indexed sequencer.
    The returned dictionary is structured as follows:

    -name : weight name.

        - data: weight samples in a range of 1.0 to -1.0.
        - index: weight index used by the sequencer Q1ASM program to refer
                 to the weight.

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------
    dict
        Dictionary with weights.

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_qrm_type(funcs.is_qrm_type())
    check_sequencer_index(sequencer)
    return _get_acq_weights(funcs.instrument, funcs, sequencer)


# ----------------------------------------------------------------------------
def get_acquisition_state(
    funcs: FuncRefs,
    sequencer: int,
    timeout: int = 0,
    timeout_poll_res: float = 0.02,
    check_seq_state: bool = True,
) -> bool:
    """
    Return acquisition binning completion state of the indexed sequencer. If
    an invalid sequencer is given, an error is set in system error. If the
    timeout is set to zero, the function returns the state immediately. If a
    positive non-zero timeout is set, the function blocks until the acquisition
    binning completes. If the acquisition hasn't completed before the timeout
    expires, a TimeoutError is thrown. Note that when sequencer state checking
    is enabled, the sequencer state is checked using get_sequencer_state with
    the selected timeout period first and then the acquisition state is checked
    with the same timeout period. This means that the total timeout period is
    two times the set timeout period.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    timeout : int
        Timeout in minutes.
    timeout_poll_res : float
        Timeout polling resolution in seconds.
    check_seq_state : bool
        Check if sequencer is done before checking acquisition state.

    Returns
    ----------
    bool
        Indicates the acquisition binning completion state (False = uncompleted,
        True = completed).

    Raises
    ----------
    TimeoutError
        Timeout
    NotImplementedError
        Functionality not available on this module.
    """
    warnings.warn(
        """
        After June 2024, this feature is subject to removal in future releases.
        Transition to an alternative is advised.
        See https://qblox-qblox-instruments.readthedocs-hosted.com/en/main/getting_started/deprecated.html
        """,
        FutureWarning,
    )
    # Check if sequencer has stopped
    check_is_valid_type(funcs.is_qrm_type() or funcs.is_qtm_type())
    if check_seq_state:
        seq_state = get_sequencer_state(funcs, sequencer, timeout, timeout_poll_res)
        if seq_state.status != SequencerStatusOld.STOPPED:
            return False
    else:
        seq_state = get_sequencer_state(funcs, sequencer)

    # Get acquisition status
    acq_state = SequencerStatusFlags.ACQ_BINNING_DONE in seq_state.flags
    elapsed_time = 0.0
    timeout = timeout * 60.0
    while acq_state is False and elapsed_time < timeout:
        time.sleep(timeout_poll_res)

        seq_state = get_sequencer_state(funcs, sequencer)
        acq_state = SequencerStatusFlags.ACQ_BINNING_DONE in seq_state.flags
        elapsed_time += timeout_poll_res

        if elapsed_time >= timeout:
            raise TimeoutError(
                f"Acquisitions on sequencer {sequencer} did not complete in timeout period of {int(timeout / 60)} minutes."
            )

    return acq_state


# ----------------------------------------------------------------------------
def get_acquisition_status(
    funcs: FuncRefs,
    sequencer: int,
    timeout: int = 0,
    timeout_poll_res: float = 0.02,
    check_seq_state: bool = True,
) -> bool:
    """
    Return acquisition binning completion status of the indexed sequencer. If
    an invalid sequencer is given, an error is set in system error. If the
    timeout is set to zero, the function returns the status immediately. If a
    positive non-zero timeout is set, the function blocks until the acquisition
    binning completes. If the acquisition hasn't completed before the timeout
    expires, a TimeoutError is thrown. Note that when sequencer state checking
    is enabled, the sequencer state is checked using get_sequencer_status with
    the selected timeout period first and then the acquisition status is checked
    with the same timeout period. This means that the total timeout period is
    two times the set timeout period.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    timeout : int
        Timeout in minutes.
    timeout_poll_res : float
        Timeout polling resolution in seconds.
    check_seq_state : bool
        Check if sequencer is done before checking acquisition status.

    Returns
    ----------
    bool
        Indicates the acquisition binning completion status (False = uncompleted,
        True = completed).

    Raises
    ----------
    TimeoutError
        Timeout
    NotImplementedError
        Functionality not available on this module.
    """

    # Check if sequencer has stopped
    check_is_valid_type(funcs.is_qrm_type() or funcs.is_qtm_type())
    if check_seq_state:
        seq_status = get_sequencer_status(funcs, sequencer, timeout, timeout_poll_res)
        if seq_status.state != SequencerStates.STOPPED:
            return False
    else:
        seq_status = get_sequencer_status(funcs, sequencer)

    # Get acquisition status
    acq_status = SequencerStatusFlags.ACQ_BINNING_DONE in seq_status.info_flags
    elapsed_time = 0.0
    timeout = timeout * 60.0
    while acq_status is False and elapsed_time < timeout:
        time.sleep(timeout_poll_res)

        seq_status = get_sequencer_status(funcs, sequencer)
        acq_status = SequencerStatusFlags.ACQ_BINNING_DONE in seq_status.info_flags
        elapsed_time += timeout_poll_res

        if elapsed_time >= timeout:
            raise TimeoutError(
                f"Acquisitions on sequencer {sequencer} did not complete in timeout period of {int(timeout / 60)} minutes."
            )

    return acq_status


# ----------------------------------------------------------------------------
def add_acquisitions(funcs: FuncRefs, sequencer: int, acquisitions: Dict) -> None:
    """
    Add all waveforms and weights in JSON compatible dictionary to AWG
    waveform and aquisition weight lists of indexed sequencer. The dictionary
    must be structured as follows:

    - name: acquisition name.
        - num_bins: number of bins in acquisition.
        - index: optional acquisition index used by the sequencer Q1ASM program to refer to the acquition.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    acquisitions : dict
        JSON compatible dictionary with one or more acquisitions.

    Returns
    ----------

    Raises
    ----------
    KeyError
        Missing dictionary key in acquisitions.
    NotImplementedError
        Functionality not available on this module.
    """

    check_is_valid_type(funcs.is_qrm_type() or funcs.is_qtm_type())
    check_sequencer_index(sequencer)
    for name in acquisitions:
        if "num_bins" in acquisitions[name]:
            if "index" in acquisitions[name]:
                _add_acq_acquisition(
                    funcs,
                    sequencer,
                    name,
                    acquisitions[name]["num_bins"],
                    acquisitions[name]["index"],
                )
            else:
                _add_acq_acquisition(
                    funcs, sequencer, name, acquisitions[name]["num_bins"]
                )
        else:
            raise KeyError(f"Missing num_bins key for {name} in acquisition dictionary")


# ----------------------------------------------------------------------------
def delete_acquisition(
    funcs: FuncRefs, sequencer: int, name: str = "", all: bool = False
) -> None:
    """
    Delete an acquisition specified by name in the acquisition list of indexed
    sequencer or delete all acquisitions if `all` is True.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    name : str
        Weight name
    all : bool
        All weights

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_is_valid_type(funcs.is_qrm_type() or funcs.is_qtm_type())
    check_sequencer_index(sequencer)
    funcs._delete_acq_acquisition(sequencer, "all" if all else name)


# ----------------------------------------------------------------------------
def delete_acquisition_data(
    funcs: FuncRefs, sequencer: int, name: str = "", all: bool = False
) -> None:
    """
    Delete data from an acquisition specified by name in the acquisition list
    of indexed sequencer or delete data in all acquisitions if `all` is True.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    name : str
        Weight name

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_is_valid_type(funcs.is_qrm_type() or funcs.is_qtm_type())
    check_sequencer_index(sequencer)
    funcs._delete_acq_acquisition_data(sequencer, "all" if all else name)


# ----------------------------------------------------------------------------
def store_scope_acquisition(funcs: FuncRefs, sequencer: int, name: str) -> None:
    """
    After an acquisition has completed, store the scope acquisition results
    in the acquisition specified by name of the indexed sequencers. If an
    invalid sequencer index is given an error is set in system error. To get
    access to the acquisition results, the sequencer will be stopped when
    calling this function.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    name : str
        Acquisition name.

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_is_valid_type(funcs.is_qrm_type() or funcs.is_qtm_type())
    check_sequencer_index(sequencer)
    funcs._set_acq_acquisition_data(sequencer, name)


# ----------------------------------------------------------------------------
def get_acquisitions(funcs: FuncRefs, sequencer: int) -> Dict:
    """
    Get all acquisitions in acquisition lists of indexed sequencer. The
    acquisition scope and bin data is normalized to a range of -1.0 to 1.0
    taking both the bit widths of the processing path and average count into
    considaration. For the binned integration results, the integration length
    is not handled during normalization and therefore these values have to be
    divided by their respective integration lenghts. The returned dictionary
    is structured as follows:

    - name: acquisition name

        - index: acquisition index used by the sequencer Q1ASM program to refer to the acquisition.
        - acquisition: acquisition dictionary

            - scope: Scope data

                - path0: input path 0

                    - data: acquisition samples in a range of 1.0 to -1.0.
                    - out-of-range: out-of-range indication for the entire acquisition (False = in-range, True = out-of-range).
                    - avg_cnt: number of averages.

                - path1: input path 1

                    - data: acquisition samples in a range of 1.0 to -1.0.
                    - out-of-range: out-of-range indication for the entire acquisition (False = in-range, True = out-of-range).
                    - avg_cnt: number of averages.

            - bins: bin data

                - integration: integration data

                    - path_0: input path 0 integration result bin list
                    - path_1: input path 1 integration result bin list

                - threshold: threshold result bin list
                - valid: list of valid indications per bin
                - avg_cnt: list of number of averages per bin

    Parameters
    ----------
    sequencer : int
        Sequencer index.

    Returns
    ----------
    dict
        Dictionary with acquisitions.

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_is_valid_type(funcs.is_qrm_type() or funcs.is_qtm_type())
    check_sequencer_index(sequencer)
    return _get_acq_acquisitions(funcs.instrument, funcs, sequencer)


# ----------------------------------------------------------------------------
def scope_trigger_arm(funcs: FuncRefs) -> Dict:
    """
    Arms the external scope trigger logic on a QTM, such that it will send
    a trigger to scope acquisition blocks in the I/O channels when the trigger
    condition is satisfied.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_is_valid_type(funcs.is_qtm_type())
    funcs._scope_trigger_arm()


# ----------------------------------------------------------------------------
def get_scope_data(funcs: FuncRefs, io_channel: int) -> Dict:
    """
    Returns the QTM I/O channel scope data for the given slot and channel
    acquired since the previous call.

    Parameters
    ----------
    io_channel : int
        I/O channel you want to get the data for.

    Returns
    ----------
    list
        The acquired data. Empty if no data acquired since last call.

    Raises
    ----------
    NotImplementedError
        Functionality not available on this module.
    """

    check_is_valid_type(funcs.is_qtm_type())
    check_io_channel_index(io_channel)
    return funcs._get_io_channel_scope_data(io_channel)


# --------------------------------------------------------------------------
_validate_qcm_sequence = fastjsonschema.compile(QCM_SEQUENCE_JSON_SCHEMA)
_validate_qrm_sequence = fastjsonschema.compile(QRM_SEQUENCE_JSON_SCHEMA)
_validate_qtm_sequence = fastjsonschema.compile(QTM_SEQUENCE_JSON_SCHEMA)
_validat_wave = fastjsonschema.compile(WAVE_JSON_SCHEMA)
_validate_acq = fastjsonschema.compile(ACQ_JSON_SCHEMA)


def set_sequence(
    funcs: FuncRefs,
    sequencer: int,
    sequence: Union[str, Dict[str, Any]],
    validation_enable: bool = True,
) -> None:
    """
    Set sequencer program, AWG waveforms, acquisition weights and acquisitions
    from a JSON file or from a dictionary directly. The JSON file or
    dictionary need to apply the schema specified by
    `QCM_SEQUENCE_JSON_SCHEMA`, `QRM_SEQUENCE_JSON_SCHEMA`, `WAVE_JSON_SCHEMA`
    and `ACQ_JSON_SCHEMA`.

    Parameters
    ----------
    sequencer : int
        Sequencer index.
    sequence : Union[str, Dict[str, Any]]
        Path to sequence file or dictionary.
    validation_enable : bool
        Enable JSON schema validation on sequence.

    Returns
    ----------

    Raises
    ----------
    JsonSchemaValueException
        Invalid JSON object.
    """

    # Set dictionary
    if isinstance(sequence, dict):
        sequence_dict = sequence
    else:
        with open(sequence, "r") as file:
            sequence_dict = json.load(file)

    # Validate dictionary
    if validation_enable:
        if funcs.is_qrm_type():
            _validate_qrm_sequence(sequence_dict)
        elif funcs.is_qcm_type():
            _validate_qcm_sequence(sequence_dict)
        elif funcs.is_qtm_type():
            _validate_qtm_sequence(sequence_dict)
        else:
            raise TypeError("Device type not supported")

        if funcs.is_qcm_type() or funcs.is_qrm_type():
            for name in sequence_dict["waveforms"]:
                _validat_wave(sequence_dict["waveforms"][name])

        if funcs.is_qrm_type():
            for name in sequence_dict["weights"]:
                _validat_wave(sequence_dict["weights"][name])

        if funcs.is_qrm_type() or funcs.is_qtm_type():
            for name in sequence_dict["acquisitions"]:
                _validate_acq(sequence_dict["acquisitions"][name])

    # Set sequence
    set_sequencer_program(funcs, sequencer, sequence_dict["program"])
    if funcs.is_qcm_type() or funcs.is_qrm_type():
        delete_waveform(funcs, sequencer, all=True)
        add_waveforms(funcs, sequencer, sequence_dict["waveforms"])

    if funcs.is_qrm_type():
        delete_weight(funcs, sequencer, all=True)
        add_weights(funcs, sequencer, sequence_dict["weights"])

    if funcs.is_qrm_type() or funcs.is_qtm_type():
        delete_acquisition(funcs, sequencer, all=True)
        add_acquisitions(funcs, sequencer, sequence_dict["acquisitions"])
