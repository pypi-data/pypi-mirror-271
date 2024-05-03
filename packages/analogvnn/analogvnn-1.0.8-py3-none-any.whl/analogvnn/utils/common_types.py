from typing import Callable, Union, Sequence

from torch import Tensor

__all__ = ['TENSOR_OPERABLE', 'TENSOR_CALLABLE', 'TENSORS']

TENSORS = Union[None, Tensor, Sequence[Tensor]]
"""`TENSORS` is a type alias for a tensor or a sequence of tensors. """

TENSOR_OPERABLE = Union[TENSORS, int, float, bool]
"""`TENSOR_OPERABLE` is a type alias for types that can be operated on by a tensor. """

TENSOR_CALLABLE = Callable[[TENSOR_OPERABLE], TENSOR_OPERABLE]
"""`TENSOR_CALLABLE` is a type alias for a function that takes a `TENSOR_OPERABLE` and returns a `TENSOR_OPERABLE`. """
