from typing import TypeVar, Union

TBaseElement = TypeVar("TBaseElement", bound="BaseElement")
TBaseComponent = TypeVar("TBaseComponent", bound="BaseComponent")
TElementOrComponent = TypeVar("TElementOrComponent", bound="Union[BaseComponent, BaseElement]")
TCollectionElementOrComponent = TypeVar("TCollectionElementOrComponent", bound="ElementsCollection[TElementOrComponent]")