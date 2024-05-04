from __future__ import annotations

import random
import string
from typing import TYPE_CHECKING, Any, Final, Generic, Iterable, Literal, cast

from sqlalchemy import (
    Result,
    Select,
    StatementLambdaElement,
    TextClause,
    any_,
    delete,
    lambda_stmt,
    over,
    select,
    text,
    update,
)
from sqlalchemy import func as sql_func
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import ColumnElement, ColumnExpressionArgument

from advanced_alchemy.exceptions import NotFoundError, RepositoryError, wrap_sqlalchemy_exception
from advanced_alchemy.filters import (
    BeforeAfter,
    CollectionFilter,
    FilterTypes,
    LimitOffset,
    NotInCollectionFilter,
    NotInSearchFilter,
    OnBeforeAfter,
    OrderBy,
    SearchFilter,
)
from advanced_alchemy.operations import Merge
from advanced_alchemy.repository._util import get_instrumented_attr
from advanced_alchemy.repository.typing import MISSING, ModelT
from advanced_alchemy.utils.deprecation import deprecated
from advanced_alchemy.utils.text import slugify

if TYPE_CHECKING:
    from collections import abc
    from datetime import datetime

    from sqlalchemy.engine.interfaces import _CoreSingleExecuteParams
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.ext.asyncio.scoping import async_scoped_session

DEFAULT_INSERTMANYVALUES_MAX_PARAMETERS: Final = 950
POSTGRES_VERSION_SUPPORTING_MERGE: Final = 15

WhereClauseT = ColumnExpressionArgument[bool]


class SQLAlchemyAsyncRepository(Generic[ModelT]):
    """SQLAlchemy based implementation of the repository interface."""

    model_type: type[ModelT]
    id_attribute: Any = "id"
    match_fields: list[str] | str | None = None
    _prefer_any: bool = False
    prefer_any_dialects: tuple[str] | None = ("postgresql",)
    """List of dialects that prefer to use ``field.id = ANY(:1)`` instead of ``field.id IN (...)``."""

    def __init__(
        self,
        *,
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        session: AsyncSession | async_scoped_session[AsyncSession],
        auto_expunge: bool = False,
        auto_refresh: bool = True,
        auto_commit: bool = False,
        **kwargs: Any,
    ) -> None:
        """Repository pattern for SQLAlchemy models.

        Args:
            statement: To facilitate customization of the underlying select query.
            session: Session managing the unit-of-work for the operation.
            auto_expunge: Remove object from session before returning.
            auto_refresh: Refresh object from session before returning.
            auto_commit: Commit objects before returning.
            **kwargs: Additional arguments.

        """
        super().__init__(**kwargs)
        self.auto_expunge = auto_expunge
        self.auto_refresh = auto_refresh
        self.auto_commit = auto_commit
        self.session = session
        if isinstance(statement, Select):
            self.statement = lambda_stmt(lambda: statement)
        elif statement is None:
            statement = select(self.model_type)
            self.statement = lambda_stmt(lambda: statement)
        else:
            self.statement = statement
        self._dialect = self.session.bind.dialect if self.session.bind is not None else self.session.get_bind().dialect
        self._prefer_any = any(self._dialect.name == engine_type for engine_type in self.prefer_any_dialects or ())

    @classmethod
    def get_id_attribute_value(
        cls,
        item: ModelT | type[ModelT],
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> Any:
        """Get value of attribute named as :attr:`id_attribute <AbstractAsyncRepository.id_attribute>` on ``item``.

        Args:
            item: Anything that should have an attribute named as :attr:`id_attribute <AbstractAsyncRepository.id_attribute>` value.
            id_attribute: Allows customization of the unique identifier to use for model fetching.
                Defaults to `None`, but can reference any surrogate or candidate key for the table.

        Returns:
            The value of attribute on ``item`` named as :attr:`id_attribute <AbstractAsyncRepository.id_attribute>`.
        """
        if isinstance(id_attribute, InstrumentedAttribute):
            id_attribute = id_attribute.key
        return getattr(item, id_attribute if id_attribute is not None else cls.id_attribute)

    @classmethod
    def set_id_attribute_value(
        cls,
        item_id: Any,
        item: ModelT,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> ModelT:
        """Return the ``item`` after the ID is set to the appropriate attribute.

        Args:
            item_id: Value of ID to be set on instance
            item: Anything that should have an attribute named as :attr:`id_attribute <AbstractAsyncRepository.id_attribute>` value.
            id_attribute: Allows customization of the unique identifier to use for model fetching.
                Defaults to `None`, but can reference any surrogate or candidate key for the table.

        Returns:
            Item with ``item_id`` set to :attr:`id_attribute <AbstractAsyncRepository.id_attribute>`
        """
        if isinstance(id_attribute, InstrumentedAttribute):
            id_attribute = id_attribute.key
        setattr(item, id_attribute if id_attribute is not None else cls.id_attribute, item_id)
        return item

    @staticmethod
    def check_not_found(item_or_none: ModelT | None) -> ModelT:
        """Raise :exc:`advanced_alchemy.exceptions.NotFoundError` if ``item_or_none`` is ``None``.

        Args:
            item_or_none: Item (:class:`T <T>`) to be tested for existence.

        Returns:
            The item, if it exists.
        """
        if item_or_none is None:
            msg = "No item found when one was expected"
            raise NotFoundError(msg)
        return item_or_none

    async def add(
        self,
        data: ModelT,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
    ) -> ModelT:
        """Add ``data`` to the collection.

        Args:
            data: Instance to be added to the collection.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_refresh: Refresh object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_refresh <SQLAlchemyAsyncRepository>`
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`

        Returns:
            The added instance.
        """
        with wrap_sqlalchemy_exception():
            instance = await self._attach_to_session(data)
            await self._flush_or_commit(auto_commit=auto_commit)
            await self._refresh(instance, auto_refresh=auto_refresh)
            self._expunge(instance, auto_expunge=auto_expunge)
            return instance

    async def add_many(
        self,
        data: list[ModelT],
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
    ) -> list[ModelT]:
        """Add many `data` to the collection.

        Args:
            data: list of Instances to be added to the collection.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`

        Returns:
            The added instances.
        """
        with wrap_sqlalchemy_exception():
            self.session.add_all(data)
            await self._flush_or_commit(auto_commit=auto_commit)
            for datum in data:
                self._expunge(datum, auto_expunge=auto_expunge)
            return data

    async def delete(
        self,
        item_id: Any,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> ModelT:
        """Delete instance identified by ``item_id``.

        Args:
            item_id: Identifier of instance to be deleted.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`
            id_attribute: Allows customization of the unique identifier to use for model fetching.
                Defaults to `id`, but can reference any surrogate or candidate key for the table.

        Returns:
            The deleted instance.

        Raises:
            NotFoundError: If no instance found identified by ``item_id``.
        """
        with wrap_sqlalchemy_exception():
            instance = await self.get(item_id, id_attribute=id_attribute)
            await self.session.delete(instance)
            await self._flush_or_commit(auto_commit=auto_commit)
            self._expunge(instance, auto_expunge=auto_expunge)
            return instance

    async def delete_many(
        self,
        item_ids: list[Any],
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
        chunk_size: int | None = None,
    ) -> list[ModelT]:
        """Delete instance identified by `item_id`.

        Args:
            item_ids: Identifier of instance to be deleted.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`
            id_attribute: Allows customization of the unique identifier to use for model fetching.
                Defaults to `id`, but can reference any surrogate or candidate key for the table.
            chunk_size: Allows customization of the ``insertmanyvalues_max_parameters`` setting for the driver.
                Defaults to `950` if left unset.

        Returns:
            The deleted instances.

        """

        with wrap_sqlalchemy_exception():
            id_attribute = get_instrumented_attr(
                self.model_type,
                id_attribute if id_attribute is not None else self.id_attribute,
            )
            instances: list[ModelT] = []
            if self._prefer_any:
                chunk_size = len(item_ids) + 1
            chunk_size = self._get_insertmanyvalues_max_parameters(chunk_size)
            for idx in range(0, len(item_ids), chunk_size):
                chunk = item_ids[idx : min(idx + chunk_size, len(item_ids))]
                if self._dialect.delete_executemany_returning:
                    instances.extend(
                        await self.session.scalars(
                            self._get_delete_many_statement(
                                statement_type="delete",
                                model_type=self.model_type,
                                id_attribute=id_attribute,
                                id_chunk=chunk,
                                supports_returning=self._dialect.delete_executemany_returning,
                            ),
                        ),
                    )
                else:
                    instances.extend(
                        await self.session.scalars(
                            self._get_delete_many_statement(
                                statement_type="select",
                                model_type=self.model_type,
                                id_attribute=id_attribute,
                                id_chunk=chunk,
                                supports_returning=self._dialect.delete_executemany_returning,
                            ),
                        ),
                    )
                    await self.session.execute(
                        self._get_delete_many_statement(
                            statement_type="delete",
                            model_type=self.model_type,
                            id_attribute=id_attribute,
                            id_chunk=chunk,
                            supports_returning=self._dialect.delete_executemany_returning,
                        ),
                    )
            await self._flush_or_commit(auto_commit=auto_commit)
            for instance in instances:
                self._expunge(instance, auto_expunge=auto_expunge)
            return instances

    def _get_insertmanyvalues_max_parameters(self, chunk_size: int | None = None) -> int:
        return chunk_size if chunk_size is not None else DEFAULT_INSERTMANYVALUES_MAX_PARAMETERS

    async def exists(
        self,
        *filters: FilterTypes | ColumnElement[bool],
        **kwargs: Any,
    ) -> bool:
        """Return true if the object specified by ``kwargs`` exists.

        Args:
            *filters: Types for specific filtering operations.
            **kwargs: Identifier of the instance to be retrieved.

        Returns:
            True if the instance was found.  False if not found..

        """
        existing = await self.count(*filters, **kwargs)
        return existing > 0

    def _get_base_stmt(
        self,
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        global_track_bound_values: bool = True,
        track_closure_variables: bool = True,
        enable_tracking: bool = True,
        track_bound_values: bool = True,
    ) -> StatementLambdaElement:
        if isinstance(statement, Select):
            return lambda_stmt(
                lambda: statement,
                track_bound_values=track_bound_values,
                global_track_bound_values=global_track_bound_values,
                track_closure_variables=track_closure_variables,
                enable_tracking=enable_tracking,
            )
        return self.statement if statement is None else statement

    def _get_delete_many_statement(
        self,
        model_type: type[ModelT],
        id_attribute: InstrumentedAttribute,
        id_chunk: list[Any],
        supports_returning: bool,
        statement_type: Literal["delete", "select"] = "delete",
    ) -> StatementLambdaElement:
        if statement_type == "delete":
            statement = lambda_stmt(lambda: delete(model_type))
        elif statement_type == "select":
            statement = lambda_stmt(lambda: select(model_type))
        if self._prefer_any:
            statement += lambda s: s.where(any_(id_chunk) == id_attribute)  # type: ignore[arg-type]
        else:
            statement += lambda s: s.where(id_attribute.in_(id_chunk))
        if supports_returning and statement_type != "select":
            statement += lambda s: s.returning(model_type)
        return statement

    async def get(
        self,
        item_id: Any,
        auto_expunge: bool | None = None,
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> ModelT:
        """Get instance identified by `item_id`.

        Args:
            item_id: Identifier of the instance to be retrieved.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`
            statement: To facilitate customization of the underlying select query.
                Defaults to :class:`SQLAlchemyAsyncRepository.statement <SQLAlchemyAsyncRepository>`
            id_attribute: Allows customization of the unique identifier to use for model fetching.
                Defaults to `id`, but can reference any surrogate or candidate key for the table.

        Returns:
            The retrieved instance.

        Raises:
            NotFoundError: If no instance found identified by `item_id`.
        """
        with wrap_sqlalchemy_exception():
            id_attribute = id_attribute if id_attribute is not None else self.id_attribute
            statement = self._get_base_stmt(statement)
            statement = self._filter_select_by_kwargs(statement, [(id_attribute, item_id)])
            instance = (await self._execute(statement)).scalar_one_or_none()
            instance = self.check_not_found(instance)
            self._expunge(instance, auto_expunge=auto_expunge)
            return instance

    async def get_one(
        self,
        auto_expunge: bool | None = None,
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        **kwargs: Any,
    ) -> ModelT:
        """Get instance identified by ``kwargs``.

        Args:
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`
            statement: To facilitate customization of the underlying select query.
                Defaults to :class:`SQLAlchemyAsyncRepository.statement <SQLAlchemyAsyncRepository>`
            **kwargs: Identifier of the instance to be retrieved.

        Returns:
            The retrieved instance.

        Raises:
            NotFoundError: If no instance found identified by `item_id`.
        """
        with wrap_sqlalchemy_exception():
            statement = self._get_base_stmt(statement)
            statement = self._filter_select_by_kwargs(statement, kwargs)
            instance = (await self._execute(statement)).scalar_one_or_none()
            instance = self.check_not_found(instance)
            self._expunge(instance, auto_expunge=auto_expunge)
            return instance

    async def get_one_or_none(
        self,
        auto_expunge: bool | None = None,
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        **kwargs: Any,
    ) -> ModelT | None:
        """Get instance identified by ``kwargs`` or None if not found.

        Args:
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`
            statement: To facilitate customization of the underlying select query.
                Defaults to :class:`SQLAlchemyAsyncRepository.statement <SQLAlchemyAsyncRepository>`
            **kwargs: Identifier of the instance to be retrieved.

        Returns:
            The retrieved instance or None
        """
        with wrap_sqlalchemy_exception():
            statement = self._get_base_stmt(statement)
            statement = self._filter_select_by_kwargs(statement, kwargs)
            instance = cast("Result[tuple[ModelT]]", (await self._execute(statement))).scalar_one_or_none()
            if instance:
                self._expunge(instance, auto_expunge=auto_expunge)
            return instance

    @deprecated(version="0.3.5", alternative="SQLAlchemyAsyncRepository.get_or_upsert", kind="method")
    async def get_or_create(
        self,
        match_fields: list[str] | str | None = None,
        upsert: bool = True,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        **kwargs: Any,
    ) -> tuple[ModelT, bool]:
        """Get instance identified by ``kwargs`` or create if it doesn't exist.

        Args:
            match_fields: a list of keys to use to match the existing model.  When
                empty, all fields are matched.
            upsert: When using match_fields and actual model values differ from
                `kwargs`, perform an update operation on the model.
            attribute_names: an iterable of attribute names to pass into the ``update``
                method.
            with_for_update: indicating FOR UPDATE should be used, or may be a
                dictionary containing flags to indicate a more specific set of
                FOR UPDATE flags for the SELECT
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_refresh: Refresh object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_refresh <SQLAlchemyAsyncRepository>`
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`
            **kwargs: Identifier of the instance to be retrieved.

        Returns:
            a tuple that includes the instance and whether it needed to be created.
            When using match_fields and actual model values differ from ``kwargs``, the
            model value will be updated.
        """
        return await self.get_or_upsert(
            match_fields=match_fields,
            upsert=upsert,
            attribute_names=attribute_names,
            with_for_update=with_for_update,
            auto_commit=auto_commit,
            auto_expunge=auto_expunge,
            auto_refresh=auto_refresh,
            **kwargs,
        )

    async def get_or_upsert(
        self,
        match_fields: list[str] | str | None = None,
        upsert: bool = True,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        **kwargs: Any,
    ) -> tuple[ModelT, bool]:
        """Get instance identified by ``kwargs`` or create if it doesn't exist.

        Args:
            match_fields: a list of keys to use to match the existing model.  When
                empty, all fields are matched.
            upsert: When using match_fields and actual model values differ from
                `kwargs`, automatically perform an update operation on the model.
            attribute_names: an iterable of attribute names to pass into the ``update``
                method.
            with_for_update: indicating FOR UPDATE should be used, or may be a
                dictionary containing flags to indicate a more specific set of
                FOR UPDATE flags for the SELECT
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_refresh: Refresh object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_refresh <SQLAlchemyAsyncRepository>`
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`
            **kwargs: Identifier of the instance to be retrieved.

        Returns:
            a tuple that includes the instance and whether it needed to be created.
            When using match_fields and actual model values differ from ``kwargs``, the
            model value will be updated.
        """
        if match_fields := self._get_match_fields(match_fields=match_fields):
            match_filter = {
                field_name: kwargs.get(field_name, None)
                for field_name in match_fields
                if kwargs.get(field_name, None) is not None
            }
        else:
            match_filter = kwargs
        existing = await self.get_one_or_none(**match_filter)
        if not existing:
            return (
                await self.add(
                    self.model_type(**kwargs),
                    auto_commit=auto_commit,
                    auto_refresh=auto_refresh,
                    auto_expunge=auto_expunge,
                ),
                True,
            )
        if upsert:
            for field_name, new_field_value in kwargs.items():
                field = getattr(existing, field_name, MISSING)
                if field is not MISSING and field != new_field_value:
                    setattr(existing, field_name, new_field_value)
            existing = await self._attach_to_session(existing, strategy="merge")
            await self._flush_or_commit(auto_commit=auto_commit)
            await self._refresh(
                existing,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
                auto_refresh=auto_refresh,
            )
            self._expunge(existing, auto_expunge=auto_expunge)
        return existing, False

    async def get_and_update(
        self,
        match_fields: list[str] | str | None = None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        **kwargs: Any,
    ) -> tuple[ModelT, bool]:
        """Get instance identified by ``kwargs`` and update the model if the arguments are different.

        Args:
            match_fields: a list of keys to use to match the existing model.  When
                empty, all fields are matched.
            attribute_names: an iterable of attribute names to pass into the ``update``
                method.
            with_for_update: indicating FOR UPDATE should be used, or may be a
                dictionary containing flags to indicate a more specific set of
                FOR UPDATE flags for the SELECT
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_refresh: Refresh object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_refresh <SQLAlchemyAsyncRepository>`
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`
            **kwargs: Identifier of the instance to be retrieved.

        Returns:
            a tuple that includes the instance and whether it needed to be updated.
            When using match_fields and actual model values differ from ``kwargs``, the
            model value will be updated.


        Raises:
            NotFoundError: If no instance found identified by `item_id`.
        """
        if match_fields := self._get_match_fields(match_fields=match_fields):
            match_filter = {
                field_name: kwargs.get(field_name, None)
                for field_name in match_fields
                if kwargs.get(field_name, None) is not None
            }
        else:
            match_filter = kwargs
        existing = await self.get_one(**match_filter)
        updated = False
        for field_name, new_field_value in kwargs.items():
            field = getattr(existing, field_name, MISSING)
            if field is not MISSING and field != new_field_value:
                updated = True
                setattr(existing, field_name, new_field_value)
        existing = await self._attach_to_session(existing, strategy="merge")
        await self._flush_or_commit(auto_commit=auto_commit)
        await self._refresh(
            existing,
            attribute_names=attribute_names,
            with_for_update=with_for_update,
            auto_refresh=auto_refresh,
        )
        self._expunge(existing, auto_expunge=auto_expunge)
        return existing, updated

    async def count(
        self,
        *filters: FilterTypes | ColumnElement[bool],
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        **kwargs: Any,
    ) -> int:
        """Get the count of records returned by a query.

        Args:
            *filters: Types for specific filtering operations.
            statement: To facilitate customization of the underlying select query.
                Defaults to :class:`SQLAlchemyAsyncRepository.statement <SQLAlchemyAsyncRepository>`
            **kwargs: Instance attribute value filters.

        Returns:
            Count of records returned by query, ignoring pagination.
        """
        with wrap_sqlalchemy_exception():
            statement = self._get_base_stmt(statement, enable_tracking=False)
            fragment = self.get_id_attribute_value(self.model_type)
            statement = statement.add_criteria(
                lambda s: s.with_only_columns(sql_func.count(fragment), maintain_column_froms=True),
                enable_tracking=False,
            )
            statement = statement.add_criteria(lambda s: s.order_by(None))
            statement = self._filter_select_by_kwargs(statement, kwargs)
            statement = self._apply_filters(*filters, apply_pagination=False, statement=statement)
            results = await self._execute(statement)
            return cast(int, results.scalar_one())

    async def update(
        self,
        data: ModelT,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
        auto_refresh: bool | None = None,
        id_attribute: str | InstrumentedAttribute | None = None,
    ) -> ModelT:
        """Update instance with the attribute values present on `data`.

        Args:
            data: An instance that should have a value for `self.id_attribute` that
                exists in the collection.
            attribute_names: an iterable of attribute names to pass into the ``update``
                method.
            with_for_update: indicating FOR UPDATE should be used, or may be a
                dictionary containing flags to indicate a more specific set of
                FOR UPDATE flags for the SELECT
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_refresh: Refresh object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_refresh <SQLAlchemyAsyncRepository>`
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`
            id_attribute: Allows customization of the unique identifier to use for model fetching.
                Defaults to `id`, but can reference any surrogate or candidate key for the table.

        Returns:
            The updated instance.

        Raises:
            NotFoundError: If no instance found with same identifier as `data`.
        """
        with wrap_sqlalchemy_exception():
            item_id = self.get_id_attribute_value(
                data,
                id_attribute=id_attribute,
            )
            # this will raise for not found, and will put the item in the session
            await self.get(item_id, id_attribute=id_attribute)
            # this will merge the inbound data to the instance we just put in the session
            instance = await self._attach_to_session(data, strategy="merge")
            await self._flush_or_commit(auto_commit=auto_commit)
            await self._refresh(
                instance,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
                auto_refresh=auto_refresh,
            )
            self._expunge(instance, auto_expunge=auto_expunge)
            return instance

    async def update_many(
        self,
        data: list[ModelT],
        auto_commit: bool | None = None,
        auto_expunge: bool | None = None,
    ) -> list[ModelT]:
        """Update one or more instances with the attribute values present on `data`.

        This function has an optimized bulk update based on the configured SQL dialect:
        - For backends supporting `RETURNING` with `executemany`, a single bulk update with returning clause is executed.
        - For other backends, it does a bulk update and then returns the updated data after a refresh.

        Args:
            data: A list of instances to update.  Each should have a value for `self.id_attribute` that exists in the
                collection.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`

        Returns:
            The updated instances.

        Raises:
            NotFoundError: If no instance found with same identifier as `data`.
        """
        data_to_update: list[dict[str, Any]] = [v.to_dict() if isinstance(v, self.model_type) else v for v in data]  # type: ignore[misc]
        with wrap_sqlalchemy_exception():
            supports_returning = self._dialect.update_executemany_returning and self._dialect.name != "oracle"
            statement = self._get_update_many_statement(self.model_type, supports_returning)
            if supports_returning:
                instances = list(
                    await self.session.scalars(
                        statement,
                        cast("_CoreSingleExecuteParams", data_to_update),  # this is not correct but the only way
                        # currently to deal with an SQLAlchemy typing issue. See
                        # https://github.com/sqlalchemy/sqlalchemy/discussions/9925
                    ),
                )
                await self._flush_or_commit(auto_commit=auto_commit)
                for instance in instances:
                    self._expunge(instance, auto_expunge=auto_expunge)
                return instances
            await self.session.execute(statement, data_to_update)
            await self._flush_or_commit(auto_commit=auto_commit)
            return data

    @staticmethod
    def _get_update_many_statement(model_type: type[ModelT], supports_returning: bool) -> StatementLambdaElement:
        statement = lambda_stmt(lambda: update(model_type))
        if supports_returning:
            statement += lambda s: s.returning(model_type)
        return statement

    async def list_and_count(
        self,
        *filters: FilterTypes | ColumnElement[bool],
        auto_expunge: bool | None = None,
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        force_basic_query_mode: bool | None = None,
        **kwargs: Any,
    ) -> tuple[list[ModelT], int]:
        """List records with total count.

        Args:
            *filters: Types for specific filtering operations.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            statement: To facilitate customization of the underlying select query.
                Defaults to :class:`SQLAlchemyAsyncRepository.statement <SQLAlchemyAsyncRepository>`
            force_basic_query_mode: Force list and count to use two queries instead of an analytical window function.
            **kwargs: Instance attribute value filters.

        Returns:
            Count of records returned by query, ignoring pagination.
        """
        if self._dialect.name in {"spanner", "spanner+spanner"} or force_basic_query_mode:
            return await self._list_and_count_basic(*filters, auto_expunge=auto_expunge, statement=statement, **kwargs)
        return await self._list_and_count_window(*filters, auto_expunge=auto_expunge, statement=statement, **kwargs)

    def _expunge(self, instance: ModelT, auto_expunge: bool | None) -> None:
        if auto_expunge is None:
            auto_expunge = self.auto_expunge

        return self.session.expunge(instance) if auto_expunge else None

    async def _flush_or_commit(self, auto_commit: bool | None) -> None:
        if auto_commit is None:
            auto_commit = self.auto_commit

        return await self.session.commit() if auto_commit else await self.session.flush()

    async def _refresh(
        self,
        instance: ModelT,
        auto_refresh: bool | None,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
    ) -> None:
        if auto_refresh is None:
            auto_refresh = self.auto_refresh

        return (
            await self.session.refresh(instance, attribute_names=attribute_names, with_for_update=with_for_update)
            if auto_refresh
            else None
        )

    async def _list_and_count_window(
        self,
        *filters: FilterTypes | ColumnElement[bool],
        auto_expunge: bool | None = None,
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        **kwargs: Any,
    ) -> tuple[list[ModelT], int]:
        """List records with total count.

        Args:
            *filters: Types for specific filtering operations.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`
            statement: To facilitate customization of the underlying select query.
                Defaults to :class:`SQLAlchemyAsyncRepository.statement <SQLAlchemyAsyncRepository>`
            **kwargs: Instance attribute value filters.

        Returns:
            Count of records returned by query using an analytical window function, ignoring pagination.
        """
        statement = self._get_base_stmt(statement)
        field = self.get_id_attribute_value(self.model_type)
        statement = statement.add_criteria(lambda s: s.add_columns(over(sql_func.count(field))), enable_tracking=False)
        statement = self._apply_filters(*filters, statement=statement)
        statement = self._filter_select_by_kwargs(statement, kwargs)
        with wrap_sqlalchemy_exception():
            result = await self._execute(statement)
            count: int = 0
            instances: list[ModelT] = []
            for i, (instance, count_value) in enumerate(result):
                self._expunge(instance, auto_expunge=auto_expunge)
                instances.append(instance)
                if i == 0:
                    count = count_value
            return instances, count

    async def _list_and_count_basic(
        self,
        *filters: FilterTypes | ColumnElement[bool],
        auto_expunge: bool | None = None,
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        **kwargs: Any,
    ) -> tuple[list[ModelT], int]:
        """List records with total count.

        Args:
            *filters: Types for specific filtering operations.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`
            statement: To facilitate customization of the underlying select query.
                Defaults to :class:`SQLAlchemyAsyncRepository.statement <SQLAlchemyAsyncRepository>`
            **kwargs: Instance attribute value filters.

        Returns:
            Count of records returned by query using 2 queries, ignoring pagination.
        """
        statement = self._get_base_stmt(statement)
        statement = self._apply_filters(*filters, statement=statement)
        statement = self._filter_select_by_kwargs(statement, kwargs)

        with wrap_sqlalchemy_exception():
            count_result = await self.session.execute(self._get_count_stmt(statement))
            count = count_result.scalar_one()
            result = await self._execute(statement)
            instances: list[ModelT] = []
            for (instance,) in result:
                self._expunge(instance, auto_expunge=auto_expunge)
                instances.append(instance)
            return instances, count

    def _get_count_stmt(self, statement: StatementLambdaElement) -> StatementLambdaElement:
        fragment = self.get_id_attribute_value(self.model_type)
        statement = statement.add_criteria(
            lambda s: s.with_only_columns(sql_func.count(fragment), maintain_column_froms=True),
            enable_tracking=False,
        )
        return statement.add_criteria(lambda s: s.order_by(None))

    async def upsert(
        self,
        data: ModelT,
        attribute_names: Iterable[str] | None = None,
        with_for_update: bool | None = None,
        auto_expunge: bool | None = None,
        auto_commit: bool | None = None,
        auto_refresh: bool | None = None,
        match_fields: list[str] | str | None = None,
    ) -> ModelT:
        """Update or create instance.

        Updates instance with the attribute values present on `data`, or creates a new instance if
        one doesn't exist.

        Args:
            data: Instance to update existing, or be created. Identifier used to determine if an
                existing instance exists is the value of an attribute on `data` named as value of
                `self.id_attribute`.
            attribute_names: an iterable of attribute names to pass into the ``update`` method.
            with_for_update: indicating FOR UPDATE should be used, or may be a
                dictionary containing flags to indicate a more specific set of
                FOR UPDATE flags for the SELECT
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_refresh: Refresh object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_refresh <SQLAlchemyAsyncRepository>`
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`
            match_fields: a list of keys to use to match the existing model.  When
                empty, all fields are matched.

        Returns:
            The updated or created instance.

        Raises:
            NotFoundError: If no instance found with same identifier as `data`.
        """
        if match_fields := self._get_match_fields(match_fields=match_fields):
            match_filter = {
                field_name: getattr(data, field_name, None)
                for field_name in match_fields
                if getattr(data, field_name, None) is not None
            }
        elif getattr(data, self.id_attribute, None) is not None:
            match_filter = {self.id_attribute: getattr(data, self.id_attribute, None)}
        else:
            match_filter = data.to_dict(exclude={self.id_attribute})
        existing = await self.get_one_or_none(**match_filter)
        if not existing:
            return await self.add(data, auto_commit=auto_commit, auto_expunge=auto_expunge, auto_refresh=auto_refresh)
        with wrap_sqlalchemy_exception():
            for field_name, new_field_value in data.to_dict(exclude={self.id_attribute}).items():
                field = getattr(existing, field_name, MISSING)
                if field is not MISSING and field != new_field_value:
                    setattr(existing, field_name, new_field_value)
            instance = await self._attach_to_session(existing, strategy="merge")
            await self._flush_or_commit(auto_commit=auto_commit)
            await self._refresh(
                instance,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
                auto_refresh=auto_refresh,
            )
            self._expunge(instance, auto_expunge=auto_expunge)
            return instance

    def _supports_merge_operations(self, force_disable_merge: bool = False) -> bool:
        return (
            (
                self._dialect.server_version_info is not None
                and self._dialect.server_version_info[0] >= POSTGRES_VERSION_SUPPORTING_MERGE
                and self._dialect.name == "postgresql"
            )
            or self._dialect.name == "oracle"
        ) and not force_disable_merge

    def _get_merge_stmt(
        self,
        into: Any,
        using: Any,
        on: Any,
    ) -> Merge:
        return Merge(into=into, using=using, on=on)

    async def upsert_many(
        self,
        data: list[ModelT],
        auto_expunge: bool | None = None,
        auto_commit: bool | None = None,
        no_merge: bool = False,
        match_fields: list[str] | str | None = None,
    ) -> list[ModelT]:
        """Update or create instance.

        Update instances with the attribute values present on `data`, or create a new instance if
        one doesn't exist.

        !!! tip
            In most cases, you will want to set `match_fields` to the combination of attributes, excluded the primary key, that define uniqueness for a row.

        Args:
            data: Instance to update existing, or be created. Identifier used to determine if an
                existing instance exists is the value of an attribute on ``data`` named as value of
                :attr:`~advanced_alchemy.repository.AbstractAsyncRepository.id_attribute`.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`.
            auto_commit: Commit objects before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`
            no_merge: Skip the usage of optimized Merge statements
                :class:`SQLAlchemyAsyncRepository.auto_commit <SQLAlchemyAsyncRepository>`
            match_fields: a list of keys to use to match the existing model.  When
                empty, automatically uses ``self.id_attribute`` (`id` by default) to match .

        Returns:
            The updated or created instance.

        Raises:
            NotFoundError: If no instance found with same identifier as ``data``.
        """
        instances: list[ModelT] = []
        data_to_update: list[ModelT] = []
        data_to_insert: list[ModelT] = []
        match_fields = self._get_match_fields(match_fields=match_fields)
        if match_fields is None:
            match_fields = [self.id_attribute]
        match_filter: list[FilterTypes | ColumnElement[bool]] = []
        if match_fields:
            for field_name in match_fields:
                field = get_instrumented_attr(self.model_type, field_name)
                matched_values = [
                    field_data for datum in data if (field_data := getattr(datum, field_name)) is not None
                ]
                if self._prefer_any:
                    match_filter.append(any_(matched_values) == field)  # type: ignore[arg-type]
                else:
                    match_filter.append(field.in_(matched_values))

        with wrap_sqlalchemy_exception():
            existing_objs = await self.list(
                *match_filter,
                auto_expunge=False,
            )
            for field_name in match_fields:
                field = get_instrumented_attr(self.model_type, field_name)
                matched_values = [getattr(datum, field_name) for datum in existing_objs if datum is not None]
                if self._prefer_any:
                    match_filter.append(any_(matched_values) == field)  # type: ignore[arg-type]
                else:
                    match_filter.append(field.in_(matched_values))
            existing_ids = self._get_object_ids(existing_objs=existing_objs)
            data = self._merge_on_match_fields(data, existing_objs, match_fields)
            for datum in data:
                if getattr(datum, self.id_attribute, None) in existing_ids:
                    data_to_update.append(datum)
                else:
                    data_to_insert.append(datum)
            if data_to_insert:
                instances.extend(
                    await self.add_many(data_to_insert, auto_commit=False, auto_expunge=False),
                )
            if data_to_update:
                instances.extend(
                    await self.update_many(data_to_update, auto_commit=False, auto_expunge=False),
                )
            await self._flush_or_commit(auto_commit=auto_commit)
            for instance in instances:
                self._expunge(instance, auto_expunge=auto_expunge)
        return instances

    def _get_object_ids(self, existing_objs: list[ModelT]) -> list[Any]:
        return [obj_id for datum in existing_objs if (obj_id := getattr(datum, self.id_attribute)) is not None]

    def _get_match_fields(
        self,
        match_fields: list[str] | str | None = None,
        id_attribute: str | None = None,
    ) -> list[str] | None:
        id_attribute = id_attribute or self.id_attribute
        match_fields = match_fields or self.match_fields
        if isinstance(match_fields, str):
            match_fields = [match_fields]
        return match_fields

    def _merge_on_match_fields(
        self,
        data: list[ModelT],
        existing_data: list[ModelT],
        match_fields: list[str] | str | None = None,
    ) -> list[ModelT]:
        match_fields = self._get_match_fields(match_fields=match_fields)
        if match_fields is None:
            match_fields = [self.id_attribute]
        for existing_datum in existing_data:
            for row_id, datum in enumerate(data):
                match = all(
                    getattr(datum, field_name) == getattr(existing_datum, field_name) for field_name in match_fields
                )
                if match and getattr(existing_datum, self.id_attribute) is not None:
                    setattr(data[row_id], self.id_attribute, getattr(existing_datum, self.id_attribute))
        return data

    async def list(
        self,
        *filters: FilterTypes | ColumnElement[bool],
        auto_expunge: bool | None = None,
        statement: Select[tuple[ModelT]] | StatementLambdaElement | None = None,
        **kwargs: Any,
    ) -> list[ModelT]:
        """Get a list of instances, optionally filtered.

        Args:
            *filters: Types for specific filtering operations.
            auto_expunge: Remove object from session before returning. Defaults to
                :class:`SQLAlchemyAsyncRepository.auto_expunge <SQLAlchemyAsyncRepository>`
            statement: To facilitate customization of the underlying select query.
                Defaults to :class:`SQLAlchemyAsyncRepository.statement <SQLAlchemyAsyncRepository>`
            **kwargs: Instance attribute value filters.

        Returns:
            The list of instances, after filtering applied.
        """
        statement = self._get_base_stmt(statement)
        statement = self._apply_filters(*filters, statement=statement)
        statement = self._filter_select_by_kwargs(statement, kwargs)

        with wrap_sqlalchemy_exception():
            result = await self._execute(statement)
            instances = list(result.scalars())
            for instance in instances:
                self._expunge(instance, auto_expunge=auto_expunge)
            return instances

    def filter_collection_by_kwargs(
        self,
        collection: Select[tuple[ModelT]] | StatementLambdaElement,
        /,
        **kwargs: Any,
    ) -> StatementLambdaElement:
        """Filter the collection by kwargs.

        Args:
            collection: statement to filter
            **kwargs: key/value pairs such that objects remaining in the collection after filtering
                have the property that their attribute named `key` has value equal to `value`.
        """
        with wrap_sqlalchemy_exception():
            collection = lambda_stmt(lambda: collection)
            collection += lambda s: s.filter_by(**kwargs)
            return collection

    @classmethod
    async def check_health(cls, session: AsyncSession | async_scoped_session[AsyncSession]) -> bool:
        """Perform a health check on the database.

        Args:
            session: through which we run a check statement

        Returns:
            ``True`` if healthy.
        """

        return (  # type: ignore[no-any-return]
            await session.execute(cls._get_health_check_statement(session))
        ).scalar_one() == 1

    @staticmethod
    def _get_health_check_statement(session: AsyncSession | async_scoped_session[AsyncSession]) -> TextClause:
        if session.bind and session.bind.dialect.name == "oracle":
            return text("SELECT 1 FROM DUAL")
        return text("SELECT 1")

    async def _attach_to_session(
        self,
        model: ModelT,
        strategy: Literal["add", "merge"] = "add",
        load: bool = True,
    ) -> ModelT:
        """Attach detached instance to the session.

        Args:
            model: The instance to be attached to the session.
            strategy: How the instance should be attached.
                - "add": New instance added to session
                - "merge": Instance merged with existing, or new one added.
            load: Boolean, when False, merge switches into
                a "high performance" mode which causes it to forego emitting history
                events as well as all database access.  This flag is used for
                cases such as transferring graphs of objects into a session
                from a second level cache, or to transfer just-loaded objects
                into the session owned by a worker thread or process
                without re-querying the database.

        Returns:
            Instance attached to the session - if `"merge"` strategy, may not be same instance
            that was provided.
        """
        if strategy == "add":
            self.session.add(model)
            return model
        if strategy == "merge":
            return await self.session.merge(model, load=load)
        msg = "Unexpected value for `strategy`, must be `'add'` or `'merge'`"  # type: ignore[unreachable]
        raise ValueError(msg)

    async def _execute(self, statement: Select[Any] | StatementLambdaElement) -> Result[Any]:
        return await self.session.execute(statement)

    def _apply_limit_offset_pagination(
        self,
        limit: int,
        offset: int,
        statement: StatementLambdaElement,
    ) -> StatementLambdaElement:
        statement += lambda s: s.limit(limit).offset(offset)
        return statement

    def _apply_filters(
        self,
        *filters: FilterTypes | ColumnElement[bool],
        apply_pagination: bool = True,
        statement: StatementLambdaElement,
    ) -> StatementLambdaElement:
        """Apply filters to a select statement.

        Args:
            *filters: filter types to apply to the query
            apply_pagination: applies pagination filters if true
            statement: select statement to apply filters

        Keyword Args:
            select: select to apply filters against

        Returns:
            The select with filters applied.
        """
        for filter_ in filters:
            if isinstance(filter_, (LimitOffset,)):
                if apply_pagination:
                    statement = self._apply_limit_offset_pagination(filter_.limit, filter_.offset, statement=statement)
            elif isinstance(filter_, (BeforeAfter,)):
                statement = self._filter_on_datetime_field(
                    field_name=filter_.field_name,
                    before=filter_.before,
                    after=filter_.after,
                    statement=statement,
                )
            elif isinstance(filter_, (OnBeforeAfter,)):
                statement = self._filter_on_datetime_field(
                    field_name=filter_.field_name,
                    on_or_before=filter_.on_or_before,
                    on_or_after=filter_.on_or_after,
                    statement=statement,
                )

            elif isinstance(filter_, (NotInCollectionFilter,)):
                if filter_.values is not None:
                    if self._prefer_any:
                        statement = self._filter_not_any_collection(
                            filter_.field_name,
                            filter_.values,
                            statement=statement,
                        )
                    else:
                        statement = self._filter_not_in_collection(
                            filter_.field_name,
                            filter_.values,
                            statement=statement,
                        )

            elif isinstance(filter_, (CollectionFilter,)):
                if filter_.values is not None:
                    if self._prefer_any:
                        statement = self._filter_any_collection(filter_.field_name, filter_.values, statement=statement)
                    else:
                        statement = self._filter_in_collection(filter_.field_name, filter_.values, statement=statement)
            elif isinstance(filter_, (OrderBy,)):
                statement = self._order_by(statement, filter_.field_name, sort_desc=filter_.sort_order == "desc")
            elif isinstance(filter_, (SearchFilter,)):
                statement = self._filter_by_like(
                    statement,
                    filter_.field_name,
                    value=filter_.value,
                    ignore_case=bool(filter_.ignore_case),
                )
            elif isinstance(filter_, (NotInSearchFilter,)):
                statement = self._filter_by_not_like(
                    statement,
                    filter_.field_name,
                    value=filter_.value,
                    ignore_case=bool(filter_.ignore_case),
                )
            elif isinstance(filter_, ColumnElement):
                statement = self._filter_by_expression(expression=filter_, statement=statement)
            else:
                msg = f"Unexpected filter: {filter_}"  # type: ignore[unreachable]
                raise RepositoryError(msg)
        return statement

    def _filter_in_collection(
        self,
        field_name: str | InstrumentedAttribute,
        values: abc.Collection[Any],
        statement: StatementLambdaElement,
    ) -> StatementLambdaElement:
        if not values:
            statement += lambda s: s.where(text("1=-1"))
            return statement
        field = get_instrumented_attr(self.model_type, field_name)
        statement += lambda s: s.where(field.in_(values))
        return statement

    def _filter_not_in_collection(
        self,
        field_name: str | InstrumentedAttribute,
        values: abc.Collection[Any],
        statement: StatementLambdaElement,
    ) -> StatementLambdaElement:
        if not values:
            return statement
        field = get_instrumented_attr(self.model_type, field_name)
        statement += lambda s: s.where(field.notin_(values))
        return statement

    def _filter_any_collection(
        self,
        field_name: str | InstrumentedAttribute,
        values: abc.Collection[Any],
        statement: StatementLambdaElement,
    ) -> StatementLambdaElement:
        if not values:
            statement += lambda s: s.where(text("1=-1"))
            return statement
        field = get_instrumented_attr(self.model_type, field_name)
        statement += lambda s: s.where(any_(values) == field)  # type: ignore[arg-type]
        return statement

    def _filter_not_any_collection(
        self,
        field_name: str | InstrumentedAttribute,
        values: abc.Collection[Any],
        statement: StatementLambdaElement,
    ) -> StatementLambdaElement:
        if not values:
            return statement
        field = get_instrumented_attr(self.model_type, field_name)
        statement += lambda s: s.where(any_(values) != field)  # type: ignore[arg-type]
        return statement

    def _filter_on_datetime_field(
        self,
        field_name: str | InstrumentedAttribute,
        statement: StatementLambdaElement,
        before: datetime | None = None,
        after: datetime | None = None,
        on_or_before: datetime | None = None,
        on_or_after: datetime | None = None,
    ) -> StatementLambdaElement:
        field = get_instrumented_attr(self.model_type, field_name)
        if before is not None:
            statement += lambda s: s.where(field < before)
        if after is not None:
            statement += lambda s: s.where(field > after)
        if on_or_before is not None:
            statement += lambda s: s.where(field <= on_or_before)
        if on_or_after is not None:
            statement += lambda s: s.where(field >= on_or_after)
        return statement

    def _filter_select_by_kwargs(
        self,
        statement: StatementLambdaElement,
        kwargs: dict[Any, Any] | Iterable[tuple[Any, Any]],
    ) -> StatementLambdaElement:
        for key, val in kwargs.items() if isinstance(kwargs, dict) else kwargs:
            statement = self._filter_by_where(statement, key, val)  # pyright: ignore[reportGeneralTypeIssues]
        return statement

    def _filter_by_expression(
        self,
        statement: StatementLambdaElement,
        expression: ColumnElement[bool],
    ) -> StatementLambdaElement:
        statement += lambda s: s.where(expression)
        return statement

    def _filter_by_where(
        self,
        statement: StatementLambdaElement,
        field_name: str | InstrumentedAttribute,
        value: Any,
    ) -> StatementLambdaElement:
        field = get_instrumented_attr(self.model_type, field_name)
        statement += lambda s: s.where(field == value)
        return statement

    def _filter_by_like(
        self,
        statement: StatementLambdaElement,
        field_name: str | InstrumentedAttribute,
        value: str,
        ignore_case: bool,
    ) -> StatementLambdaElement:
        field = get_instrumented_attr(self.model_type, field_name)
        search_text = f"%{value}%"
        if ignore_case:
            statement += lambda s: s.where(field.ilike(search_text))
        else:
            statement += lambda s: s.where(field.like(search_text))
        return statement

    def _filter_by_not_like(
        self,
        statement: StatementLambdaElement,
        field_name: str | InstrumentedAttribute,
        value: str,
        ignore_case: bool,
    ) -> StatementLambdaElement:
        field = get_instrumented_attr(self.model_type, field_name)
        search_text = f"%{value}%"
        if ignore_case:
            statement += lambda s: s.where(field.not_ilike(search_text))
        else:
            statement += lambda s: s.where(field.not_like(search_text))
        return statement

    def _order_by(
        self,
        statement: StatementLambdaElement,
        field_name: str | InstrumentedAttribute,
        sort_desc: bool = False,
    ) -> StatementLambdaElement:
        field = get_instrumented_attr(self.model_type, field_name)
        if sort_desc:
            statement += lambda s: s.order_by(field.desc())
        else:
            statement += lambda s: s.order_by(field.asc())
        return statement


class SQLAlchemyAsyncSlugRepository(
    SQLAlchemyAsyncRepository[ModelT],
):
    """Extends the repository to include slug model features.."""

    async def get_by_slug(
        self,
        slug: str,
        **kwargs: Any,
    ) -> ModelT | None:
        """Select record by slug value."""
        return await self.get_one_or_none(slug=slug)

    async def get_available_slug(
        self,
        value_to_slugify: str,
        **kwargs: Any,
    ) -> str:
        """Get a unique slug for the supplied value.

        If the value is found to exist, a random 4 digit character is appended to the end.

        Override this method to change the default behavior

        Args:
            value_to_slugify (str): A string that should be converted to a unique slug.
            **kwargs: stuff

        Returns:
            str: a unique slug for the supplied value.  This is safe for URLs and other unique identifiers.
        """
        slug = slugify(value_to_slugify)
        if await self._is_slug_unique(slug):
            return slug
        random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))  # noqa: S311
        return f"{slug}-{random_string}"

    async def _is_slug_unique(
        self,
        slug: str,
        **kwargs: Any,
    ) -> bool:
        return await self.exists(slug=slug) is False
