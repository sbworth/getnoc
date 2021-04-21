# ----------------------------------------------------------------------
# BaseResourceAPI
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from typing import Any, Optional, Callable, Dict, DefaultDict, TypeVar, Generic, List, Iterable
import inspect
from http import HTTPStatus
from abc import ABCMeta, abstractmethod
from collections import defaultdict

# Third-party modules
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Security, Response

# NOC modules
from noc.config import config
from noc.aaa.models.user import User
from noc.core.service.deps.user import get_user_scope
from ...models.label import LabelItem
from ...models.status import StatusResponse


T = TypeVar("T")  # , bound=Model)
GET = ["GET"]
POST = ["POST"]
PUT = ["PUT"]
DELETE = ["DELETE"]
X_NOC_TOTAL = "X-NOC-Total"
X_NOC_LIMIT = "X-NOC-Limit"
X_NOC_OFFSET = "X-NOC-Offset"


class BaseResourceAPI(Generic[T], metaclass=ABCMeta):
    """
    Generic Abstract REST api.

    Data can be retrieved using different `views`, each having own Pydantic model.
    Following views are set by default:
    * default - suitable for listing items
    * label - id + label
    * form - editing form.

    `item_to_<view>` methods convert Django models to Pydantic models.
    Add own `item_to_<view>` methods to define own customized views.
    """

    prefix: str
    model: T

    def __init__(self):
        if not getattr(self, "prefix", None):
            raise ValueError("prefix is not set")
        if not getattr(self, "model", None):
            raise ValueError("model is not set")
        self.router = APIRouter()
        self.api_name = self.prefix.split("/")[-1]
        self.openapi_tags = ["ui", self.api_name]
        self.cleaners: DefaultDict[str, List[Callable[[Any], Any]]] = defaultdict(list)
        # Setup endpoints
        for name, fn in inspect.getmembers(self):
            if name.startswith("item_to_"):
                self.setup_view(name[8:])
        self.setup_write()
        if self.has_delete:
            self.setup_delete()

    @classmethod
    @abstractmethod
    def item_to_default(cls, item: T) -> BaseModel:
        """
        Convert model item to response model for view `default`
        :param item:
        :return:
        """

    @classmethod
    def item_to_label(cls, item: T) -> LabelItem:
        """
        Convert model item to response model for view `label`
        :param item:
        :return:
        """
        return LabelItem(id=str(item.id), label=str(item))

    @classmethod
    @abstractmethod
    def item_to_form(cls, item: T) -> BaseModel:
        return cls.item_to_default(item)

    def get_scope_read_default(self):
        """
        Returns scope for view access to default view
        :return:
        """
        return f"{self.api_name}:read:default"

    def get_scope_read_label(self):
        """
        Returns scope for view access to label view
        :return:
        """
        return f"{self.api_name}:read:default"

    def get_scope_read(self, view: str) -> str:
        """
        Get read scope for view
        :param view:
        :return:
        """
        return getattr(self, f"get_scope_read_{view}", self.get_scope_read_default)()

    def get_scope_write(self) -> str:
        """
        Get write scope
        :param view:
        :return:
        """
        return f"{self.api_name}:write"

    def get_scope_delete(self) -> str:
        """
        Get delete scope
        :param view:
        :return:
        """
        return f"{self.api_name}:delete"

    @classmethod
    def get_form_model(cls) -> BaseModel:
        """
        Get pydantic model for form
        :return:
        """
        # Get form model
        sig = inspect.signature(cls.item_to_form)
        form_model = sig.return_annotation
        if form_model is BaseModel:
            raise ValueError("item_to_form has incorrect return type annotation")
        return form_model

    @abstractmethod
    def get_total_items(self, user: User) -> int:
        """
        Calculate total amount of items, satisfying criteria
        :param user:
        :return:
        """

    @abstractmethod
    def get_items(
        self, user: User, limit: int = config.ui.max_rest_limit, offset: int = 0
    ) -> List[T]:
        """
        Get list of items, satisfying criteria
        :param user:
        :param limit:
        :param offset:
        :return:
        """

    @abstractmethod
    def get_item(self, id: str, user: User) -> Optional[T]:
        """
        Get item by id, if accessible to user
        :param id:
        :param user:
        :return:
        """

    @abstractmethod
    def delete_item(self, id: str, user: User) -> bool:
        """
        Delete item if accessible by user. Returns True if item is deleted.
        :param id:
        :param user:
        :return:
        """

    @abstractmethod
    def create_item(self, user: User, **kwargs) -> None:
        """
        Create item from given parameters
        :param user:
        :param kwargs:
        :return:
        """

    @abstractmethod
    def update_item(self, id: str, user: User, **kwargs) -> None:
        """
        Update item with given parameters
        :param id:
        :param user:
        :param kwargs:
        :return:
        """

    def clean(self, data: BaseModel, id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process data to be stored, perform additional checks
        :param data: Pydantic model with store request
        :param id: Record id for update operations, None for create
        :return:
        """
        r = {}
        for name, value in data.dict().items():
            for fn in self.cleaners[name]:
                value = fn(value)
            r[name] = value
        return r

    def add_cleaner(self, name: str, cleaner: Callable[[Any], Any]):
        self.cleaners[name].append(cleaner)

    def setup_cleaners(self):
        """
        Install model cleaners
        :return:
        """

    @property
    def has_delete(self) -> bool:
        """
        Returns True if defined delete_item
        :return:
        """
        return "delete_item" not in self.__abstractmethods__

    def setup_view(self, view: str) -> None:
        def inner_list(
            response: Response,
            limit: int = config.ui.max_rest_limit,
            offset: int = 0,
            user: User = Security(get_user_scope, scopes=[self.get_scope_read(view)]),
        ):
            total = self.get_total_items(user)
            if total:
                items = self.get_items(user=user, limit=limit, offset=offset)
            else:
                items = []
            # Set headers
            response.headers[X_NOC_TOTAL] = str(total)
            response.headers[X_NOC_LIMIT] = str(limit)
            response.headers[X_NOC_OFFSET] = str(offset)
            return [fmt(item) for item in items]

        def inner_get(
            id: str, user: User = Security(get_user_scope, scopes=[self.get_scope_read(view)])
        ):
            item = self.get_item(id=id, user=user)
            if not item:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
            return fmt(item)

        def iter_list_paths() -> Iterable[str]:
            if view == "default":
                yield self.prefix
            yield f"{self.prefix}/v/{view}"

        def iter_get_paths() -> Iterable[str]:
            if view == "default":
                yield f"{self.prefix}/{{id}}"
            yield f"{self.prefix}/{{id}}/v/{view}"

        fmt = getattr(self, f"item_to_{view}", None)
        if not fmt:
            raise ValueError(f"item_to_{view} is not defined")
        sig = inspect.signature(fmt)
        if sig.return_annotation is BaseModel:
            raise ValueError(f"item_to_{view} has incorrect return type annotation")
        # List
        for path in iter_list_paths():
            # List
            self.router.add_api_route(
                path=path,
                endpoint=inner_list,
                methods=GET,
                response_model=List[sig.return_annotation],
                tags=self.openapi_tags,
                name=f"{self.api_name}_list_{view}",
                description=f"List items with {view} view",
            )
        # Get
        for path in iter_get_paths():
            self.router.add_api_route(
                path=path,
                endpoint=inner_get,
                methods=GET,
                response_model=sig.return_annotation,
                tags=self.openapi_tags,
                name=f"{self.api_name}_get_{view}",
                description=f"Get item with {view} view",
            )

    def setup_write(self):
        """
        Setup write endpoints
        :return:
        """
        ITEM_MODEL = self.get_form_model()

        def inner_create(
            item: ITEM_MODEL, user: User = Security(get_user_scope, scopes=[self.get_scope_write()])
        ):
            data = self.clean(item)
            self.create_item(user=user, **data)
            return StatusResponse(status=True)

        def inner_update(
            item: ITEM_MODEL,
            id: str,
            user: User = Security(get_user_scope, scopes=[self.get_scope_write()]),
        ):
            data = self.clean(item)
            self.update_item(id=id, user=user, **data)
            return StatusResponse(status=True)

        self.setup_cleaners()
        # Install routes
        self.router.add_api_route(
            path=self.prefix,
            endpoint=inner_create,
            methods=POST,
            tags=self.openapi_tags,
            name=f"{self.api_name}_create",
            description="Create item",
            status_code=HTTPStatus.CREATED,
            response_model=StatusResponse,
        )
        self.router.add_api_route(
            path=f"{self.prefix}/{{id}}",
            endpoint=inner_update,
            methods=PUT,
            tags=self.openapi_tags,
            name=f"{self.api_name}_update",
            description="Update item",
            response_model=StatusResponse,
        )

    def setup_delete(self):
        """
        Setup delete endpoint
        :return:
        """

        def inner_delete(
            id: str,
            user: User = Security(get_user_scope, scopes=[self.get_scope_delete()]),
        ):
            deleted = self.delete_item(id=id, user=user)
            if not deleted:
                raise HTTPException(status_code=404)
            return StatusResponse(status=True)

        self.router.add_api_route(
            path=f"{self.prefix}/{{id}}",
            endpoint=inner_delete,
            methods=DELETE,
            tags=self.openapi_tags,
            name=f"{self.api_name}_delete",
            description="delete item",
            response_model=StatusResponse,
        )