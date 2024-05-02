# ----------------------------------------------------------------------------
# Description    : IOChannel QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

from typing import List, Union, Tuple, NoReturn
from functools import partial
from qcodes import validators as vals
from qcodes import Instrument, InstrumentChannel
from qblox_instruments.docstring_helpers import partial_with_numpy_doc


# -- class -------------------------------------------------------------------


class IOChannel(InstrumentChannel):
    """
    This class represents a single IO channel. It combines all IO channel
    specific parameters and functions into a single QCoDes InstrumentChannel.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        parent: Union[Instrument, InstrumentChannel],
        name: str,
        io_channel_idx: int,
    ):
        """
        Creates a IO channel class and adds all relevant parameters for the
        IO channel.

        Parameters
        ----------
        parent : Union[Instrument, InstrumentChannel]
            The QCoDeS class to which this IO channel belongs.
        name : str
            Name of this IO channel channel
        io_channel_idx : int
            The index of this IO channel in the parent instrument, representing
            which IO channel is controlled by this class.

        Returns
        ----------

        Raises
        ----------
        """

        # Initialize instrument channel
        super().__init__(parent, name)

        # Store IO channel index
        self._io_channel_idx = io_channel_idx

        # Add required parent attributes for the QCoDeS parameters to function
        for attr_name in IOChannel._get_required_parent_attr_names():
            self._register(attr_name)

        # Add parameters
        # -- Channel map -----------------------------------------------------
        # -- TBD

        # -- IOChannel (QTM-only) --------------------------------------------
        self.add_parameter(
            "out_mode",
            label="Output function of the I/O port for the given channel",
            docstring="Sets/gets the output function of the I/O Port for the given"
            "channel ('disabled' = port is in 50Ohm mode, "
            "'low' = the port drives low-impedance 0V, 'high' = the port "
            "drives low-impedance ~3.3V)",
            unit="",
            vals=vals.Enum("disabled", "low", "high", "sequencer"),
            set_cmd=partial(self._set_io_channel_config_val, ["out_mode"]),
            get_cmd=partial(self._get_io_channel_config_val, ["out_mode"]),
        )

        self.add_parameter(
            "in_threshold_primary",
            label="primary threshold voltage used for digitization of the "
            "input signal for the given channel",
            docstring="Sets/gets the primary threshold voltage used for "
            "digitization of the input signal on the given channel",
            unit="V",
            vals=vals.Numbers(),
            set_parser=float,
            get_parser=float,
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["in_threshold_primary"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["in_threshold_primary"],
            ),
        )

        self.add_parameter(
            "binned_acq_time_source",
            label="timetag data source for acquisitions made on the given channel",
            docstring="Sets/gets the timetag data source for acquisitions made on this channel "
            "using the acquire_timetags instruction",
            unit="",
            vals=vals.Enum("first", "second", "last"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_time_source"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_time_source"],
            ),
        )

        self.add_parameter(
            "binned_acq_time_ref",
            label="time reference that the timetag recorded for each acquire_timetags instruction"
            "is recorded in relation to",
            docstring="Sets/gets the time reference that the timetag recorded for each acquire_timetags "
            "instruction is recorded in relation to",
            unit="",
            vals=vals.Enum(
                "start", "end", "first", *[f"first{x}" for x in range(8)], "sequencer"
            ),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_time_ref"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_time_ref"],
            ),
        )

        self.add_parameter(
            "binned_acq_on_invalid_time_delta",
            label="averaging and binning logic behaviour if/when no valid time delta is available",
            docstring="Sets/gets averaging and binning logic behaviour if/when no valid time delta  "
            "is available, typically because no event occurred in the window",
            unit="",
            vals=vals.Enum(
                "error",
                "record_0",
                "discard",
            ),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_on_invalid_time_delta"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_on_invalid_time_delta"],
            ),
        )

        self.add_parameter(
            "binned_acq_threshold_source",
            label="data source of the threshold recorded by acquire_timetags",
            docstring="Sets/gets the data source of the threshold recorded by "
            "acquire timetags",
            unit="",
            vals=vals.Enum("thresh0", "thresh1"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["binned_acq_threshold_source"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["binned_acq_threshold_source"],
            ),
        )

        self.add_parameter(
            "current_in_level",
            label="current level of the input",
            docstring="Gets the current level of the input. Returns 0 if the input "
            "level is below in_threshold_primary, or 1 if it's above"
            "acquire timetags",
            unit="",
            vals=vals.Ints(0, 1),
            set_cmd=False,
            get_cmd=partial(
                self._get_io_channel_status_val,
                ["io_monitor"],
            ),
            max_val_age=0.0,  # disable read cache
        )

        self.add_parameter(
            "in_counter_mode",
            label="manual control over the counter gate",
            docstring="Sets/gets the manual control over the counter gate",
            unit="",
            vals=vals.Enum("sequencer", "disabled", "enabled"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["in_counter_mode"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["in_counter_mode"],
            ),
        )

        for counter_type in ["rising", "falling"]:
            self.add_parameter(
                f"in_counter_{counter_type}",
                label=f"raw value of the hardware {counter_type}-edge counter",
                docstring=f"Gets the raw value of the hardware {counter_type}-edge counter",
                unit="",
                vals=vals.Ints(),
                set_cmd=False,
                get_cmd=partial(
                    self._get_io_channel_status_val,
                    [f"count_{counter_type}"],
                ),
                max_val_age=0.0,  # disable read cache
            )

        self.add_parameter(
            "in_trigger_en",
            label="sending triggers to the trigger network automatically",
            docstring="Sets/gets the enable that controls sending triggers "
            "to the trigger network automatically or based on direct sampling "
            "of the inputs. The mode is configured by in_trigger_mode, and the "
            "address by in_trigger_address",
            unit="",
            vals=vals.Bool(),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["in_trigger_en"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["in_trigger_en"],
            ),
        )

        self.add_parameter(
            "in_trigger_mode",
            label="which event causes a trigger to be sent if in_trigger_en is enabled",
            docstring="Sets/gets which event causes a trigger to be sent if in_trigger_en "
            "is enabled ",
            unit="",
            vals=vals.Enum("rising", "falling", "sampled-high", "sampled-low"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["in_trigger_mode"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["in_trigger_mode"],
            ),
        )

        self.add_parameter(
            "in_trigger_address",
            label="which event causes a trigger to be sent if in_trigger_en is enabled",
            docstring="Sets/gets which event causes a trigger to be sent if in_trigger_en "
            "is enabled ",
            unit="",
            vals=vals.Ints(1, 15),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["in_trigger_address"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["in_trigger_address"],
            ),
        )

        self.add_parameter(
            "scope_trigger_mode",
            label="how the scope/trace unit for this channel is triggered",
            docstring="Sets/gets how the scope/trace unit for this channel is triggered "
            "is enabled ",
            unit="",
            vals=vals.Enum("sequencer", "external"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["scope_trigger_mode"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["scope_trigger_mode"],
            ),
        )

        self.add_parameter(
            "scope_trigger_level",
            label="how the scope/trace unit for this channel is triggered",
            docstring="Sets/gets how the scope/trace unit for this channel is triggered "
            "is enabled ",
            unit="",
            vals=vals.Enum("any", "low", "high", "rising", "falling"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["scope_trigger_level"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["scope_trigger_level"],
            ),
        )

        self.add_parameter(
            "scope_mode",
            label="what type of data is traced when the scope/trace unit for this channel"
            "is triggered",
            docstring="Sets/gets what type of data is traced when the scope/trace unit for "
            "this channel is triggered",
            unit="",
            vals=vals.Enum("scope", "timetags", "timetags-windowed"),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["scope_mode"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["scope_mode"],
            ),
        )

        self.add_parameter(
            "thresholded_acq_trigger_en",
            label="whether the thresholded acquisition result of acquire_timetags is mapped "
            "to the trigger network for feedback purposes",
            docstring="Sets/gets whether the thresholded acquisition result of acquire_timetags "
            "is mapped to the trigger network for feedback purposes",
            unit="",
            vals=vals.Bool(),
            set_cmd=partial(
                self._set_io_channel_config_val,
                ["thresholded_acq_trigger_en"],
            ),
            get_cmd=partial(
                self._get_io_channel_config_val,
                ["thresholded_acq_trigger_en"],
            ),
        )

        for result in ["low", "mid", "high", "invalid"]:
            self.add_parameter(
                f"thresholded_acq_trigger_address_{result}",
                label=f"whether a trigger is to be sent and which trigger address is to be used when the result is {result}",
                docstring=f"Sets/gets whether a trigger is to be sent and which trigger address is to be used when the result is {result}",
                unit="",
                vals=vals.Ints(0, 15),
                set_cmd=partial(
                    self._set_io_channel_config_val,
                    [f"thresholded_acq_trigger_address_{result}"],
                ),
                get_cmd=partial(
                    self._get_io_channel_config_val,
                    [f"thresholded_acq_trigger_address_{result}"],
                ),
            )

    # ------------------------------------------------------------------------
    @property
    def io_channel_idx(self) -> int:
        """
        Get IO channel index.

        Parameters
        ----------

        Returns
        ----------
        int
            IOChannel index

        Raises
        ----------
        """

        return self._io_channel_idx

    # ------------------------------------------------------------------------
    @staticmethod
    def _get_required_parent_attr_names() -> List:
        """
        Return list of parent attribute names that are required for the QCoDeS
        parameters to function, so that the can be registered to this object
        using the _register method.

        Parameters
        ----------

        Returns
        ----------
        List
            List of parent attribute names to register.

        Raises
        ----------
        """

        # IOChannel attributes
        attr_names = []
        for operation in ["set", "get"]:
            attr_names.append(f"_{operation}_io_channel_config")
            attr_names.append(f"_{operation}_io_channel_config_val")
        attr_names.append("_get_io_channel_status")
        attr_names.append("_get_io_channel_status_val")
        attr_names.append("get_scope_data")

        return attr_names

    # ------------------------------------------------------------------------
    def _register(self, attr_name: str) -> None:
        """
        Register parent attribute to this IO channel using functools.partial
        to pre-select the IO channel index. If the attribute does not exist in
        the parent class, a method that raises a `NotImplementedError`
        exception is registered instead. The docstring of the parent attribute
        is also copied to the registered attribute.

        Parameters
        ----------
        attr_name : str
            Attribute name of parent to register.

        Returns
        ----------

        Raises
        ----------
        """

        if hasattr(self.parent, attr_name):
            parent_attr = getattr(self.parent, attr_name)
            partial_doc = (
                "Note\n"
                + "----------\n"
                + "This method calls {1}.{0} using functools.partial to set the "
                + "IO channel index. The docstring above is of {1}.{0}:\n\n"
            ).format(attr_name, type(self.parent).__name__)
            partial_func = partial_with_numpy_doc(
                parent_attr, self.io_channel_idx, end_with=partial_doc
            )
            setattr(self, attr_name, partial_func)
        else:

            def raise_not_implemented_error(*args, **kwargs) -> None:
                raise NotImplementedError(
                    f'{self.parent.name} does not have "{attr_name}" attribute.'
                )

            setattr(self, attr_name, raise_not_implemented_error)

    # ------------------------------------------------------------------------
    def _invalidate_qcodes_parameter_cache(self) -> None:
        """
        Marks the cache of all QCoDeS parameters on this IO channel as invalid.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        for param in self.parameters.values():
            param.cache.invalidate()
