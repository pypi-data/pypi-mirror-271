# ----------------------------------------------------------------------------
# Description    : Cluster native interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import warnings
from typing import Any, Dict, Optional, Tuple, Union, Iterable, Iterator
from functools import partial
from qblox_instruments import InstrumentClass, InstrumentType, TypeHandle
from qblox_instruments import DeviceInfo, resolve
from qblox_instruments.ieee488_2 import IpTransport, ClusterDummyTransport
from qblox_instruments.ieee488_2 import (
    DummyBinnedAcquisitionData,
    DummyScopeAcquisitionData,
)
from qblox_instruments.scpi import Cluster as ClusterScpi

import qblox_instruments.native.generic_func as gf
from qblox_instruments.docstring_helpers import copy_docstr, partial_with_numpy_doc

SLOT_DESCRIPTION = "The slot index of the module being referred to."
SLOT_PARAM_DICT_INT = {"slot": ("int", SLOT_DESCRIPTION)}
SLOT_PARAM_DICT_OPT = {"slot": ("Optional[int]", SLOT_DESCRIPTION)}

# -- class -------------------------------------------------------------------


class Cluster(ClusterScpi):
    """
    Class that provides the native API for the Cluster. It provides methods
    to control all functions and features provided by the Cluster.

    Note that the bulk of the functionality of this class is contained in the
    :mod:`~qblox_instruments.native.generic_func` module so that this
    functionality can be shared between instruments.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        identifier: str,
        port: Optional[int] = None,
        debug: Optional[int] = None,
        dummy_cfg: Optional[Dict] = None,
    ):
        """
        Creates Cluster native interface object.

        Parameters
        ----------
        identifier : str
            Instrument identifier. See :func:`~qblox_instruments.resolve()`
            for more information.
        port : Optional[int]
            Instrument port. If None, this will be determined automatically.
        debug : Optional[int]
            Debug level (0 | None = normal, 1 = no version check, >1 = no
            version or error checking).
        dummy_cfg : Optional[Dict]
            Configure as dummy using this configuration. For each slot that
            needs to be occupied by a module add the slot index as key and
            specify the type of module in the slot using the type
            :class:`~qblox_instruments.ClusterType`.

        Returns
        ----------

        Raises
        ----------
        RuntimeError
            Instrument cannot be reached due to invalid IP configuration.
        ConnectionError
            Instrument type is not supported.
        """

        # Create transport layer (dummy or socket interface)
        if dummy_cfg is not None:
            self._transport = ClusterDummyTransport(dummy_cfg)
            if debug is None:
                debug = 1
        else:
            addr_info = resolve(identifier)
            if addr_info.protocol != "ip":
                raise RuntimeError(
                    f"Instrument cannot be reached due to invalid IP configuration. Use qblox-pnp tool to rectify; serial number is {addr_info.address}"
                )
            host = addr_info.address
            if port is None:
                port = addr_info.scpi_port
            self._transport = IpTransport(host=host, port=port)
            if debug is None:
                debug = 0

        # Initialize parent class.
        super().__init__(self._transport, debug)

        # Set instrument type handle
        cmm_dev_info = DeviceInfo.from_idn(super()._get_idn())
        model = cmm_dev_info.model
        self._type_handle = TypeHandle(model)
        if not self._type_handle.is_mm_type:
            raise ConnectionError(
                f"Unsupported instrument type detected ({self.instrument_type})"
            )

        # Get a dictionary of SCPI and native functions that the functions in
        # the generic_func module require to operate. Create a function
        # reference container that we use to pass references to those functions
        # to functions in the generic_func module.
        self._funcs = gf.FuncRefs(self)
        for attr_name in self._funcs.funcs.keys():
            if self._funcs.funcs[attr_name] is None and hasattr(super(), attr_name):
                self._funcs.register(getattr(super(), attr_name))

        # Set module specific type and FuncRefs handles
        self._mod_handles = {}
        slot_info = self._get_mods_info()
        cmm_sw_version = cmm_dev_info.sw_build.version_str
        for slot_str, info in slot_info.items():
            slot = int(slot_str.split(" ")[1])
            slot_idn = info.get("IDN", "")

            # Compare firmware version with CMM
            mod_dev_info = DeviceInfo.from_idn(slot_idn)
            mod_sw_version = mod_dev_info.sw_build.version_str
            if mod_sw_version != cmm_sw_version:
                if not debug:
                    raise ConnectionError(
                        f"Application version mismatch between Cluster Management Module (CMM) and module at slot {slot}. "
                        f"CMM is at version {cmm_sw_version} whereas module is at version {mod_sw_version}. "
                        f"Please run a firmware update for the entire cluster with the desired firmware version."
                    )
                else:
                    warnings.warn(
                        f"Application version mismatch between Cluster Management Module (CMM) and module at slot {slot}. "
                        f"CMM is at version {cmm_sw_version} whereas module is at version {mod_sw_version}. "
                        f"Please double-check the firmware version before proceeding. You are currently "
                        f"connected using debug = {debug} mode. "
                    )

            # Module type handle
            model = mod_dev_info.model
            mod_type_handle = TypeHandle(model)
            mod_type_handle._is_rf_type = bool(info["RF"])

            # Module FuncRefs
            mod_funcs = self._create_module_funcrefs(slot)

            # Update module handles dictionary
            self._mod_handles[str(slot)] = {
                "type_handle": mod_type_handle,
                "func_refs": mod_funcs,
            }

    # ------------------------------------------------------------------------
    def _create_module_funcrefs(self, slot: int) -> gf.FuncRefs:
        """
        Create function reference container object for a specific slot. This
        means that SCPI and native layer methods are customized using
        functools.partial to operate on a specific slot. The resulting methods
        are added to the function reference container, so that they can be used
        by the generic_func module.

        Parameters
        ----------
        slot : int
            Slot index to create function reference container for.

        Returns
        ----------
        FuncRefs
            Function reference container specific to single slot.


        Raises
        ----------
        """

        # Non-slot specific attributes
        funcs = gf.FuncRefs(self)
        funcs.register(getattr(super(), "_write"))
        funcs.register(getattr(super(), "_read_bin"))
        funcs.register(getattr(super(), "_flush_line_end"))

        # Slot specific attributes
        rb = super()._read_bin
        part_cmd = f"SLOT{slot}:SEQuencer"
        awg_wlist_rb = gf.create_read_bin(rb, part_cmd + "{}:AWG:WLISt?")
        acq_wlist_rb = gf.create_read_bin(rb, part_cmd + "{}:ACQ:WLISt?")
        acq_data_rb = gf.create_read_bin(
            rb, part_cmd + '{}:ACQ:ALISt:ACQuisition:DATA? "{}"'
        )
        acq_list_rb = gf.create_read_bin(rb, part_cmd + "{}:ACQ:ALISt?")

        funcs.register(awg_wlist_rb, "_get_awg_waveforms")
        funcs.register(acq_wlist_rb, "_get_acq_weights")
        funcs.register(acq_data_rb, "_get_acq_acquisition_data")
        funcs.register(acq_list_rb, "_get_acq_acquisitions")

        funcs.register(partial_with_numpy_doc(self._is_qcm_type, slot), "is_qcm_type")
        funcs.register(partial_with_numpy_doc(self._is_qrm_type, slot), "is_qrm_type")
        funcs.register(partial_with_numpy_doc(self._is_qtm_type, slot), "is_qtm_type")
        funcs.register(partial_with_numpy_doc(self._is_qdm_type, slot), "is_qdm_type")
        funcs.register(partial_with_numpy_doc(self._is_rf_type, slot), "is_rf_type")

        # Remaining slot specific attributes
        for attr_name in funcs.funcs.keys():
            if funcs.funcs[attr_name] is None and hasattr(super(), attr_name):
                attr = partial(getattr(super(), attr_name), slot)
                funcs.register(attr, attr_name)

        return funcs

    # ------------------------------------------------------------------------
    @property
    def instrument_class(self) -> InstrumentClass:
        """
        Get instrument class (e.g. Cluster).

        Parameters
        ----------

        Returns
        ----------
        InstrumentClass
            Instrument class

        Raises
        ----------
        """

        return self._type_handle.instrument_class

    # ------------------------------------------------------------------------
    @property
    def instrument_type(self) -> InstrumentType:
        """
        Get instrument type (e.g. MM, QRM, QCM).

        Parameters
        ----------

        Returns
        ----------
        InstrumentType
            Instrument type

        Raises
        ----------
        """

        return self._type_handle.instrument_type

    # ------------------------------------------------------------------------
    def _present_at_init(self, slot: int) -> Tuple:
        """
        Get an indication of module presence during initialization of this
        object for a specific slot in the Cluster and return the associated
        module type handle and function reference container if present.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        TypeHandle
            Module type handle
        FuncRefs
            Function reference container

        Raises
        ----------
        KeyError
            Module is not available.
        """

        if str(slot) in self._mod_handles:
            return (
                self._mod_handles[str(slot)]["type_handle"],
                self._mod_handles[str(slot)]["func_refs"],
            )
        else:
            raise KeyError(f"Module at slot {slot} is not available.")

    # ------------------------------------------------------------------------
    def _module_type(self, slot: int) -> InstrumentType:
        """
        Get indexed module's type (e.g. QRM, QCM, QTM, QDM).

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        InstrumentType
            Module type

        Raises
        ----------
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.instrument_type

    # ------------------------------------------------------------------------
    def _is_qcm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QCM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool
            True if module is of type QCM.

        Raises
        ----------
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_qcm_type

    # ------------------------------------------------------------------------
    def _is_qrm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QRM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QRM.

        Raises
        ----------
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_qrm_type

    # ------------------------------------------------------------------------
    def _is_qtm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QTM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QTM.

        Raises
        ----------
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_qtm_type

    # ------------------------------------------------------------------------
    def _is_qdm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QDM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QDM.

        Raises
        ----------
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_qdm_type

    # ------------------------------------------------------------------------
    def _is_rf_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QCM-RF or QRM-RF.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QCM-RF or QRM-RF.

        Raises
        ----------
        """

        type_handle, _ = self._present_at_init(slot)
        return type_handle.is_rf_type

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_scpi_commands)
    def _get_scpi_commands(self) -> Dict:
        return gf.get_scpi_commands(self._funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_idn)
    def get_idn(self) -> Dict:
        return gf.get_idn(self._funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_system_state)
    def get_system_state(self) -> gf.SystemState:
        return gf.get_system_state(self._funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_system_status)
    def get_system_status(self) -> gf.SystemStatus:
        return gf.get_system_status(self._funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_acq_scope_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_acq_scope_config(self, slot: int, config: Dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_acq_scope_config(funcs, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acq_scope_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_acq_scope_config(self, slot: int) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_acq_scope_config(funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_acq_scope_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_acq_scope_config_val(self, slot: int, keys: Any, val: Any) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_acq_scope_config_val(funcs, keys, val)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acq_scope_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_acq_scope_config_val(self, slot: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_acq_scope_config_val(funcs, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_io_channel_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_io_channel_config(self, slot: int, channel: int, config: Dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_io_channel_config(funcs, channel, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_channel_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_channel_config(self, slot: int, channel: int) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_channel_config(funcs, channel)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_channel_status, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_channel_status(self, slot: int, channel: int) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_channel_status(funcs, channel)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_io_channel_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_io_channel_config_val(
        self, slot: int, channel: int, keys: Any, val: Any
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_io_channel_config_val(funcs, channel, keys, val)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_channel_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_channel_config_val(self, slot: int, channel: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_channel_config_val(funcs, channel, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_io_channel_status_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_io_channel_status_val(self, slot: int, channel: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_io_channel_status_val(funcs, channel, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_quad_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_quad_config(self, slot: int, quad: int, config: Dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_quad_config(funcs, quad, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_quad_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_quad_config(self, slot: int, quad: int) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_quad_config(funcs, quad)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_quad_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_quad_config_val(self, slot: int, quad: int, keys: Any, val: Any) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_quad_config_val(funcs, quad, keys, val)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_quad_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_quad_config_val(self, slot: int, quad: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_quad_config_val(funcs, quad, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_program, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_program(self, slot: int, sequencer: int, program: str) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_program(funcs, sequencer, program)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_config(self, slot: int, sequencer: int, config: Dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_config(funcs, sequencer, config)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_config, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_sequencer_config(self, slot: int, sequencer: int) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_config(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_config_val(
        self, slot: int, sequencer: int, keys: Any, val: Any
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_config_val(funcs, sequencer, keys, val)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_config_val, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_sequencer_config_val(self, slot: int, sequencer: int, keys: Any) -> Any:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_config_val(funcs, sequencer, keys)

    # ------------------------------------------------------------------------
    @copy_docstr(
        gf.set_sequencer_config_rotation_matrix,
        params_to_add=SLOT_PARAM_DICT_INT,
    )
    def _set_sequencer_config_rotation_matrix(
        self, slot: int, sequencer: int, phase_incr: float
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_config_rotation_matrix(funcs, sequencer, phase_incr)

    # ------------------------------------------------------------------------
    @copy_docstr(
        gf.get_sequencer_config_rotation_matrix,
        params_to_add=SLOT_PARAM_DICT_INT,
    )
    def _get_sequencer_config_rotation_matrix(self, slot: int, sequencer: int) -> float:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_config_rotation_matrix(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_connect_out, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_connect_out(
        self, slot: int, sequencer: int, output: int, state: str
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_connect_out(funcs, sequencer, output, state)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_connect_out, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_sequencer_connect_out(self, slot: int, sequencer: int, output: int) -> str:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_connect_out(funcs, sequencer, output)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequencer_connect_acq, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequencer_connect_acq(
        self, slot: int, sequencer: int, path: int, state: str
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequencer_connect_acq(funcs, sequencer, path, state)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_connect_acq, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_sequencer_connect_acq(self, slot: int, sequencer: int, path: int) -> str:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_connect_acq(funcs, sequencer, path)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.disconnect_outputs, params_to_add=SLOT_PARAM_DICT_INT)
    def _disconnect_outputs(self, slot: int) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.disconnect_outputs(funcs)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.disconnect_inputs, params_to_add=SLOT_PARAM_DICT_INT)
    def _disconnect_inputs(self, slot: int) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.disconnect_inputs(funcs)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.iter_connections, params_to_add=SLOT_PARAM_DICT_INT)
    def _iter_connections(self, slot: int) -> Iterator[Tuple[int, str, str]]:
        _, funcs = self._present_at_init(slot)
        return gf.iter_connections(funcs)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.sequencer_connect, params_to_add=SLOT_PARAM_DICT_INT)
    def _sequencer_connect(self, slot: int, sequencer: int, *connections: str) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.sequencer_connect(funcs, sequencer, *connections)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.arm_sequencer, params_to_add=SLOT_PARAM_DICT_OPT)
    def arm_sequencer(
        self, slot: Optional[int] = None, sequencer: Optional[int] = None
    ) -> None:
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Arm sequencers across all modules

        if sequencer is not None:
            gf.check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Arm all sequencers within a module

        return gf.arm_sequencer(self._funcs, f"SLOT{slot}:SEQuencer{sequencer}")

    # ------------------------------------------------------------------------
    @copy_docstr(gf.start_sequencer, params_to_add=SLOT_PARAM_DICT_OPT)
    def start_sequencer(
        self, slot: Optional[int] = None, sequencer: Optional[int] = None
    ) -> None:
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Start sequencers across all modules

        if sequencer is not None:
            gf.check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Start all sequencers within a module

        return gf.start_sequencer(self._funcs, f"SLOT{slot}:SEQuencer{sequencer}")

    # ------------------------------------------------------------------------
    @copy_docstr(gf.stop_sequencer, params_to_add=SLOT_PARAM_DICT_OPT)
    def stop_sequencer(
        self, slot: Optional[int] = None, sequencer: Optional[int] = None
    ) -> None:
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Stop sequencers across all modules

        if sequencer is not None:
            gf.check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Stop all sequencers within a module

        return gf.stop_sequencer(self._funcs, f"SLOT{slot}:SEQuencer{sequencer}")

    # ------------------------------------------------------------------------
    @copy_docstr(gf.clear_sequencer_flags, params_to_add=SLOT_PARAM_DICT_OPT)
    def clear_sequencer_flags(
        self, slot: Optional[int] = None, sequencer: Optional[int] = None
    ) -> None:
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Clear sequencer flags across all modules

        if sequencer is not None:
            gf.check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Clear all sequencers flags within a module

        return gf.clear_sequencer_flags(self._funcs, f"SLOT{slot}:SEQuencer{sequencer}")

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_state, params_to_add=SLOT_PARAM_DICT_INT)
    def get_sequencer_state(
        self,
        slot: int,
        sequencer: int,
        timeout: int = 0,
        timeout_poll_res: float = 0.02,
    ) -> gf.SequencerState:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_state(funcs, sequencer, timeout, timeout_poll_res)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_sequencer_status, params_to_add=SLOT_PARAM_DICT_INT)
    def get_sequencer_status(
        self,
        slot: int,
        sequencer: int,
        timeout: int = 0,
        timeout_poll_res: float = 0.02,
    ) -> gf.SequencerStatus:
        _, funcs = self._present_at_init(slot)
        return gf.get_sequencer_status(funcs, sequencer, timeout, timeout_poll_res)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.arm_scope_trigger, params_to_add=SLOT_PARAM_DICT_OPT)
    def arm_scope_trigger(self, slot: Optional[int] = None) -> None:
        if slot is not None:
            _, funcs = self._present_at_init(slot)
        else:
            slot = ""  # Arm scope triggers across all modules
            funcs = self._funcs

        return gf.arm_scope_trigger(funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.add_waveforms, params_to_add=SLOT_PARAM_DICT_INT)
    def _add_waveforms(self, slot: int, sequencer: int, waveforms: Dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.add_waveforms(funcs, sequencer, waveforms)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.delete_waveform, params_to_add=SLOT_PARAM_DICT_INT)
    def _delete_waveform(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.delete_waveform(funcs, sequencer, name, all)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_waveforms, params_to_add=SLOT_PARAM_DICT_INT)
    def get_waveforms(self, slot: int, sequencer: int) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_waveforms(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.add_weights, params_to_add=SLOT_PARAM_DICT_INT)
    def _add_weights(self, slot: int, sequencer: int, weights: Dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.add_weights(funcs, sequencer, weights)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.delete_weight, params_to_add=SLOT_PARAM_DICT_INT)
    def _delete_weight(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.delete_weight(funcs, sequencer, name, all)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_weights, params_to_add=SLOT_PARAM_DICT_INT)
    def get_weights(self, slot: int, sequencer: int) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_weights(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acquisition_state, params_to_add=SLOT_PARAM_DICT_INT)
    def get_acquisition_state(
        self,
        slot: int,
        sequencer: int,
        timeout: int = 0,
        timeout_poll_res: float = 0.02,
    ) -> bool:
        _, funcs = self._present_at_init(slot)
        return gf.get_acquisition_state(funcs, sequencer, timeout, timeout_poll_res)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acquisition_status, params_to_add=SLOT_PARAM_DICT_INT)
    def get_acquisition_status(
        self,
        slot: int,
        sequencer: int,
        timeout: int = 0,
        timeout_poll_res: float = 0.02,
    ) -> bool:
        _, funcs = self._present_at_init(slot)
        return gf.get_acquisition_status(funcs, sequencer, timeout, timeout_poll_res)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.add_acquisitions, params_to_add=SLOT_PARAM_DICT_INT)
    def _add_acquisitions(self, slot: int, sequencer: int, acquisitions: Dict) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.add_acquisitions(funcs, sequencer, acquisitions)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.delete_acquisition, params_to_add=SLOT_PARAM_DICT_INT)
    def _delete_acquisition(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.delete_acquisition(funcs, sequencer, name, all)

    # --------------------------------------------------------------------------
    @copy_docstr(gf.delete_acquisition_data, params_to_add=SLOT_PARAM_DICT_INT)
    def delete_acquisition_data(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.delete_acquisition_data(funcs, sequencer, name, all)

    # -------------------------------------------------------------------------
    @copy_docstr(gf.store_scope_acquisition, params_to_add=SLOT_PARAM_DICT_INT)
    def store_scope_acquisition(self, slot: int, sequencer: int, name: str) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.store_scope_acquisition(funcs, sequencer, name)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acq_acquisition_data, params_to_add=SLOT_PARAM_DICT_INT)
    def _get_acq_acquisition_data(self, slot: int, sequencer: int, name: str) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_acq_acquisition_data(self, funcs, sequencer, name)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_acquisitions, params_to_add=SLOT_PARAM_DICT_INT)
    def get_acquisitions(self, slot: int, sequencer: int) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_acquisitions(funcs, sequencer)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.scope_trigger_arm, params_to_add=SLOT_PARAM_DICT_INT)
    def scope_trigger_arm(self, slot: int) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.scope_trigger_arm(funcs)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.get_scope_data, params_to_add=SLOT_PARAM_DICT_INT)
    def get_scope_data(self, slot: int, io_channel: int) -> Dict:
        _, funcs = self._present_at_init(slot)
        return gf.get_scope_data(funcs, io_channel)

    # --------------------------------------------------------------------------
    def delete_dummy_binned_acquisition_data(
        self,
        slot_idx: int,
        sequencer: Optional[int] = None,
        acq_index_name: Optional[str] = None,
    ):
        """
        Delete all dummy binned acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : Optional[int]
            Sequencer.
        acq_index_name : Optional[str]
            Acquisition index name.

        Returns
        ----------

        Raises
        ----------
        """

        self._transport.delete_dummy_binned_acquisition_data(
            slot_idx, sequencer, acq_index_name
        )

    # --------------------------------------------------------------------------
    def set_dummy_binned_acquisition_data(
        self,
        slot_idx: int,
        sequencer: int,
        acq_index_name: str,
        data: Iterable[Union[DummyBinnedAcquisitionData, None]],
    ):
        """
        Set dummy binned acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : int
            Sequencer.
        acq_index_name : str
            Acquisition index name.
        data : Iterable[Union[DummyBinnedAcquisitionData, None]]
            Dummy data for the binned acquisition.
            An iterable of all the bin values.

        Returns
        ----------

        Raises
        ----------
        """

        self._transport.set_dummy_binned_acquisition_data(
            slot_idx, sequencer, acq_index_name, data
        )

    # --------------------------------------------------------------------------
    def delete_dummy_scope_acquisition_data(
        self, slot_idx: int, sequencer: Union[int, None]
    ):
        """
        Delete dummy scope acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : Union[int, None]
            Sequencer.

        Returns
        ----------

        Raises
        ----------
        """

        self._transport.delete_dummy_scope_acquisition_data(slot_idx)

    # --------------------------------------------------------------------------
    def set_dummy_scope_acquisition_data(
        self,
        slot_idx: int,
        sequencer: Union[int, None],
        data: DummyScopeAcquisitionData,
    ):
        """
        Set dummy scope acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : Union[int, None]
            Sequencer.
        data : DummyScopeAcquisitionData
             Dummy data for the scope acquisition.

        Returns
        ----------

        Raises
        ----------
        """

        self._transport.set_dummy_scope_acquisition_data(slot_idx, data)

    # ------------------------------------------------------------------------
    @copy_docstr(gf.set_sequence, params_to_add=SLOT_PARAM_DICT_INT)
    def _set_sequence(
        self,
        slot: int,
        sequencer: int,
        sequence: Union[str, Dict[str, Any]],
        validation_enable: bool = True,
    ) -> None:
        _, funcs = self._present_at_init(slot)
        return gf.set_sequence(funcs, sequencer, sequence, validation_enable)

    # ------------------------------------------------------------------------
    def _get_modules_present(self, slot: int) -> bool:
        """
        Get an indication of module presence for a specific slot in the Cluster.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool
            Module presence.

        Raises
        ----------
        """

        return (int(super()._get_modules_present()) >> (slot - 1)) & 1 == 1
