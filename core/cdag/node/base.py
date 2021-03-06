# ----------------------------------------------------------------------
# BaseNode
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Any, Optional, Type, Dict, List, Iterable, Tuple, Set
from enum import Enum
import inspect
from dataclasses import dataclass
import sys

# Third-party modules
from pydantic import BaseModel

# NOC modules
from ..typing import ValueType
from ..tx import Transaction


class Category(str, Enum):
    MATH = "math"
    OPERATION = "operation"
    LOGICAL = "logical"
    ACTIVATION = "activation"
    COMPARE = "compare"
    DEBUG = "debug"
    UTIL = "util"
    STATISTICS = "statistics"
    ML = "ml"
    WINDOW = "window"


@dataclass
class Subscriber(object):
    __slots__ = ("node", "input", "next")
    node: "BaseCDAGNode"
    input: str
    next: Optional["Subscriber"]


class BaseCDAGNodeMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        n = type.__new__(mcs, name, bases, attrs)
        sig = inspect.signature(n.get_value)
        n.allow_dynamic = "kwargs" in sig.parameters
        n.static_inputs = [sys.intern(x) for x in sig.parameters if x not in ("self", "kwargs")]
        # Create slotted config class to optimize memory layout.
        # Slotted classes reduce memory usage by ~400 bytes, compared to Pydantic models
        if hasattr(n, "config_cls"):
            n.config_cls_slot = type(
                f"{n.config_cls.__name__}_Slot",
                (),
                {"__slots__": tuple(sys.intern(x) for x in n.config_cls.__fields__)},
            )
        # Slotted state
        if hasattr(n, "state_cls"):
            n.state_cls_slot = type(
                f"{n.state_cls.__name__}_Slot",
                (),
                {"__slots__": tuple(sys.intern(x) for x in n.state_cls.__fields__)},
            )
        #
        return n


class BaseCDAGNode(object, metaclass=BaseCDAGNodeMetaclass):
    name: str
    state_cls: Type[BaseModel]
    config_cls: Type[BaseModel]
    static_inputs: List[str]  # Filled by metaclass
    allow_dynamic: bool = False  # Filled by metaclass
    dot_shape: str = "box"
    categories: List[Category] = []
    config_cls_slot: Type  # Filled by metaclass
    state_cls_slot: Type  # Filled by metaclass

    __slots__ = (
        "_node_id",
        "_prefix",
        "description",
        "state",
        "config",
        "_subscribers",
        "bound_inputs",
        "dynamic_inputs",
        "const_inputs",
        "_const_value",
        "sticky",
    )

    def __init__(
        self,
        node_id: str,
        prefix: Optional[str] = None,
        state: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        sticky: bool = False,
    ):
        self._node_id = sys.intern(node_id)
        self._prefix = sys.intern(prefix) if prefix else None
        self.description = description
        self.state = self.clean_state(state)
        self.config = self.clean_config(config)
        self._subscribers: Optional[Subscriber] = None
        self.bound_inputs: Optional[Set[str]] = None  # Lives until .freeze()
        self.dynamic_inputs: Optional[Dict[str, bool]] = None
        # # Pre-calculated inputs
        self.const_inputs: Optional[Dict[str, ValueType]] = None
        self._const_value: Optional[ValueType] = None
        self.sticky = sticky

    @property
    def node_id(self):
        if self._prefix:
            return f"{self._prefix}::{self._node_id}"
        return self._node_id

    @classmethod
    def construct(
        cls,
        node_id: str,
        prefix: Optional[str] = None,
        description: Optional[str] = None,
        state: Optional[BaseModel] = None,
        config: Optional[BaseModel] = None,
        sticky: bool = False,
    ) -> Optional["BaseCDAGNode"]:
        """
        Construct node
        :return:
        """
        return cls(
            node_id,
            prefix=prefix,
            description=description,
            state=state,
            config=config,
            sticky=sticky,
        )

    @staticmethod
    def slotify(slot_cls: Type, data: BaseModel) -> object:
        """
        Convert pydantic model to slotted class instance
        """
        o = slot_cls()
        for k in data.__fields__:
            setattr(o, k, getattr(data, k))
        return o

    def clone(
        self, node_id: str, prefix: Optional[str] = None, state: Optional[Dict[str, Any]] = None
    ) -> Optional["BaseCDAGNode"]:
        node = self.__class__(
            node_id,
            prefix=prefix,
            description=self.description,
            state=state,
            config=self.config if hasattr(self, "config_cls") else None,
            sticky=self.sticky,
        )
        if self.allow_dynamic and self.dynamic_inputs:
            for di, is_key in self.dynamic_inputs.items():
                node.add_input(di, is_key=is_key)
        return node

    def clean_state(self, state: Optional[Dict[str, Any]]) -> Optional[BaseModel]:
        if not hasattr(self, "state_cls"):
            return None
        state = state or {}
        c_state = self.state_cls(**state)
        return self.slotify(self.state_cls_slot, c_state)

    def clean_config(self, config: Optional[Dict[str, Any]]) -> Optional[BaseModel]:
        if not hasattr(self, "config_cls") or config is None:
            return None
        # Shortcut, if config is already cleaned (cloned copies)
        if isinstance(config, BaseModel) or hasattr(config, "__slots__"):
            return config
        # Slotify to reduce memory usage
        cfg = self.config_cls(**config)
        return self.slotify(self.config_cls_slot, cfg)

    def iter_inputs(self) -> Iterable[str]:
        """
        Enumerate all configured inputs
        :return:
        """
        yield from self.static_inputs
        if self.allow_dynamic and self.dynamic_inputs:
            yield from self.dynamic_inputs

    def iter_unbound_inputs(self) -> Iterable[str]:
        """
        Iterate all unbound inputs
        :return:
        """
        if not self.bound_inputs:
            yield from self.iter_inputs()
            return
        for i in self.iter_inputs():
            if i not in self.bound_inputs:
                yield i

    def has_input(self, name: str) -> bool:
        """
        Check if the node has input with given name
        :param name: name of input
        :returns: True, if input exists
        """
        if name in self.static_inputs:
            return True
        if self.allow_dynamic and self.dynamic_inputs and name in self.dynamic_inputs:
            return True
        return False

    def check_input(self, name: str) -> None:
        """
        Check if input exists. Raise KeyError if missed
        """
        if not self.has_input(name):
            raise KeyError(f"Invalid input: {name}")

    def activate(self, tx: Transaction, name: str, value: ValueType) -> None:
        """
        Activate named input with
        :param tx: Transaction instance
        :param name: Input name
        :param value: Input value
        :return:
        """
        self.check_input(name)
        inputs = tx.get_inputs(self)
        if inputs[name] is not None:
            return  # Already activated
        inputs[name] = value  # Activate input
        if any(True for n, v in inputs.items() if v is None and self.is_required_input(n)):
            return  # Non-activated inputs
        # Activate node, calculate value
        value = self.get_value(**inputs)
        if hasattr(self, "state_cls"):
            tx.update_state(self)
        # Notify all subscribers
        if value is not None:
            for s in self.iter_subscribers():
                s.node.activate(tx, s.input, value)

    def is_required_input(self, name: str) -> bool:
        """
        Check if input is required
        """
        return not self.is_dynamic_input(name)

    def is_dynamic_input(self, name: str) -> bool:
        """
        Check if input is dynamic
        :param name:
        :return:
        """
        return self.allow_dynamic and self.dynamic_inputs and name in self.dynamic_inputs

    def is_key_input(self, name: str) -> bool:
        """
        Check if input is key one
        """
        return (
            self.allow_dynamic
            and self.dynamic_inputs
            and bool(self.dynamic_inputs.get(name, False))
        )

    def is_const_input(self, name: str) -> bool:
        """
        Check if input is const
        """
        return self.const_inputs is not None and name in self.const_inputs

    def activate_const(self, name: str, value: ValueType) -> None:
        """
        Activate const input. Called during construction time.

        :param name:
        :param value:
        :return:
        """
        name = sys.intern(name)
        self.check_input(name)
        if self.const_inputs is None:
            self.const_inputs = {}
        self.const_inputs[name] = value
        if self.is_const:
            for s in self.iter_subscribers():
                s.node.activate_const(s.input, self._const_value)

    def subscribe(self, node: "BaseCDAGNode", name: str, dynamic: bool = False) -> None:
        """
        Subscribe to node activation
        :param node: Connected node
        :param name: Connected input name
        :param dynamic: Create input when necessary
        :return:
        """
        if node == self:
            raise ValueError("Cannot subscribe to self")
        name = sys.intern(name)
        if self.has_subscriber(node, name):
            return
        if dynamic:
            node.add_input(name)
        self._subscribers = Subscriber(node=node, input=name, next=self._subscribers)
        node.mark_as_bound(name)
        if self.is_const:
            node.activate_const(name, self._const_value)

    def mark_as_bound(self, name: str) -> None:
        """
        Mark input as bound
        """
        name = sys.intern(name)
        if not self.has_input(name):
            return
        if self.bound_inputs is None:
            self.bound_inputs = {name}
        else:
            self.bound_inputs.add(name)

    def get_value(self, *args, **kwargs) -> Optional[ValueType]:  # pragma: no cover
        """
        Calculate node value. Returns None when input is malformed and should not be propagated
        :return:
        """
        raise NotImplementedError

    def get_state(self) -> Optional[BaseModel]:
        """
        Get current node state
        :return:
        """
        if self.state:
            return self.state_cls(
                **{s: getattr(self.state, s) for s in self.state_cls_slot.__slots__}
            )
        return None

    def iter_subscribers(self) -> Iterable[Subscriber]:
        """
        Iterate all subscribers for node
        """
        s = self._subscribers
        while s:
            yield s
            s = s.next

    def has_subscriber(self, node: "BaseCDAGNode", input: str) -> bool:
        return any(True for s in self.iter_subscribers() if s.node == node and s.input == input)

    @property
    def is_const(self) -> bool:
        """
        Check if the node is constant value
        :return:
        """
        if self._const_value is not None:
            return True
        n_inputs = len(self.static_inputs)
        if self.allow_dynamic and self.dynamic_inputs:
            n_inputs += len(self.dynamic_inputs)
        const_inputs = self.const_inputs if self.const_inputs is not None else {}
        if len(const_inputs) != n_inputs:
            return False
        # Activate const
        self._const_value = self.get_value(**const_inputs)
        return True

    def add_input(self, name: str, is_key: bool = False) -> None:
        """
        Add new dynamic input
        :param name: Input name
        :return:
        """
        if not self.allow_dynamic:
            raise TypeError("Dynamic inputs are not allowed")
        name = sys.intern(name)
        if self.has_input(name):
            return
        if self.dynamic_inputs is None:
            self.dynamic_inputs = {name: is_key}
        else:
            self.dynamic_inputs[name] = is_key

    def iter_config_fields(self) -> Iterable[str]:
        """
        Iterate config field names
        """
        if hasattr(self, "config_cls"):
            yield from self.config_cls_slot.__slots__

    def iter_initial_inputs(self) -> Iterable[Tuple[str, Optional[ValueType]]]:
        """
        Iterate transaction initial inputs
        """
        if self.const_inputs:
            for i in self.iter_inputs():
                yield i, self.const_inputs.get(i)
        else:
            for i in self.iter_inputs():
                yield i, None

    def freeze(self) -> None:
        """
        Freeze the node and reduce memory footprint.
        No further graph construction manipulations are possible after
        the freezing.
        """
        self.description = None
        self.bound_inputs = None  # Only for charting purposes
