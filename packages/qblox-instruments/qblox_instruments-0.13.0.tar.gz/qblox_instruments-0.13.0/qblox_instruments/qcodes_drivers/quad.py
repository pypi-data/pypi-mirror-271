# ----------------------------------------------------------------------------
# Description    : Quad QCoDeS interface
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


class Quad(InstrumentChannel):
    """
    This class represents a single quad. It combines all quad
    specific parameters and functions into a single QCoDes InstrumentChannel.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        parent: Union[Instrument, InstrumentChannel],
        name: str,
        quad_idx: int,
    ):
        """
        Creates a quad class and adds all relevant parameters for the
        quad.

        Parameters
        ----------
        parent : Union[Instrument, InstrumentChannel]
            The QCoDeS class to which this quad belongs.
        name : str
            Name of this quad channel
        quad_idx : int
            The index of this quad in the parent instrument, representing
            which quad is controlled by this class.

        Returns
        ----------

        Raises
        ----------
        """

        # Initialize instrument channel
        super().__init__(parent, name)

        # Store quad index
        self._quad_idx = quad_idx

        # Add required parent attributes for the QCoDeS parameters to function
        for attr_name in Quad._get_required_parent_attr_names():
            self._register(attr_name)

        # Add parameters
        # -- Channel map -----------------------------------------------------
        # -- TBD

        # -- Quad parameters (QTM-only) --------------------------------------
        self.add_parameter(
            "timetag_oversampling",
            label="Timetag oversampling setting of all channels in the given quad",
            docstring="Sets/gets the timetag oversampling setting of all "
            "channels in the given quad ('disabled' = no oversampling, '2x' = "
            "events are sampled by the converter twice with a typical "
            "single-shot RMS of 15 ps, '4x' = events are sampled by the "
            "converter four times with a typical single-shot RMS of 10 ps)",
            unit="",
            vals=vals.Enum("disabled", "x2", "x4"),
            set_parser=str,
            get_parser=str,
            set_cmd=partial(
                self._set_quad_config_val,
                ["timetag_oversampling"],
            ),
            get_cmd=partial(
                self._get_quad_config_val,
                ["timetag_oversampling"],
            ),
        )

        self.add_parameter(
            "tdc_latency",
            label="Latency of the TDC-capable input path in the given quad",
            docstring="Sets/gets the Latency of the TDC-capable input path "
            "in the given quad. Lower values decrease the feedback latency.",
            unit="ns",
            vals=vals.Numbers(),
            set_parser=float,
            get_parser=float,
            set_cmd=partial(
                self._set_quad_config_val,
                ["tdc_latency"],
            ),
            get_cmd=partial(
                self._get_quad_config_val,
                ["tdc_latency"],
            ),
        )

        self.add_parameter(
            "channel_combine",
            label="Latency of the TDC-capable input path in the given quad",
            docstring="Sets/gets the Latency of the TDC-capable input path "
            "in the given quad. Lower values decrease the feedback latency.",
            unit="",
            vals=vals.Enum("fan-out", "independent"),
            set_parser=str,
            get_parser=str,
            set_cmd=partial(
                self._set_quad_config_val,
                ["channel_combine"],
            ),
            get_cmd=partial(
                self._get_quad_config_val,
                ["channel_combine"],
            ),
        )

    # ------------------------------------------------------------------------
    @property
    def quad_idx(self) -> int:
        """
        Get quad index.

        Parameters
        ----------

        Returns
        ----------
        int
            Quad index

        Raises
        ----------
        """

        return self._quad_idx

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
            attr_names.append(f"_{operation}_quad_config")
            attr_names.append(f"_{operation}_quad_config_val")

        return attr_names

    # ------------------------------------------------------------------------
    def _register(self, attr_name: str) -> None:
        """
        Register parent attribute to this quad using functools.partial
        to pre-select the quad index. If the attribute does not exist in
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
                + "quad index. The docstring above is of {1}.{0}:\n\n"
            ).format(attr_name, type(self.parent).__name__)
            partial_func = partial_with_numpy_doc(
                parent_attr, self.quad_idx, end_with=partial_doc
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
        Marks the cache of all QCoDeS parameters on this quad as invalid.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        for param in self.parameters.values():
            param.cache.invalidate()
