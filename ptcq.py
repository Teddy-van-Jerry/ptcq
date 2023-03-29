import torch
import numpy

def shift_left_(x, n):
    return x * (2 ** n)

def shift_right_(x, n):
    return x / (2 ** n)

def round_(x):
    return torch.round(x) if torch.is_tensor(x) else round(x)

def clip_(x, dwt):
    min_v = -(1 << (dwt - 1))
    max_v = (1 << (dwt - 1)) - 1
    return numpy.clip(x, min_v, max_v) if torch.is_tensor(x) else numpy.clip(x, min_v, max_v)

class FixedQ:
    """Fixed-point quantization.
    """
    def __init__(self, W, D) -> None:
        """Initialize the fixed-point quantization scheme.

        .. Note::
            Currently, the fixed-point quantization behavior is

            - rounding to the nearest
            - clipping with no overflow

            More quantization behavior will be added in the future.

        :param W: Data bit width.
        :type W: unsigned integer
        :param D: Decimal bit width. This is the number of bits after the decimal point. It can be zero or negative.
        :type D: integer

        Example use::

            q1 = ptcq.FixedQ(5, 3) # data width 5, decimal width 3
            # possible values after q1: -2.0, -1.875, -1.75, ..., 1.75, 1.875
            q2 = ptcq.FixedQ(2, -1) # data width 2, decimal width -1 (i.e. interval is 2)
            # possible values after q2: -4.0, -2.0, 0.0, 2.0
        """
        self.W, self.D = W, D
        pass

    def quantize(self, x):
        """Quantize the input with the fixed-point scheme.

        :param x: Input.
        :type x: float or torch.Tensor
        :return: The quantized result.
        :rtype: The same with input.

        Example use::

            >>> q = ptcq.FixedQ(5, 3)
            >>> q.quantize(1.23)
            1.25
            >>> q.quantize(-20)
            -2.0
            >>> a = torch.randn(3)
            >>> print(a)
            tensor([ 0.6144, -0.9529, -0.1797])
            >>> q.quantize(a)
            tensor([ 0.6250, -1.0000, -0.1250])
        """
        y = round_(shift_left_(x, self.D))
        y = clip_(y, self.W)
        y = shift_right_(y, self.D)
        return y
    
    def quantize_self(self, x) -> None:
        """Quantize the input tensor (in place) with the fixed-point scheme.

        :param x: Input.
        :type x: torch.Tensor

        .. Caution::
            The input ``x`` must be a ``torch.Tensor``!
            Otherwise a warning will be raised and the input value is not changed.

        In the following example, we show that this method can quantize a ``torch.Tensor`` but not a ``float``::

            >>> q = ptcq.FixedQ(5, 3)
            >>> a = torch.rand(4) * 2
            >>> print(a)
            tensor([0.7913, 1.1297, 1.4601, 1.3022])
            >>> q.quantize_self(a)
            >>> print(a)
            tensor([0.7500, 1.1250, 1.5000, 1.2500])
            >>> x = -0.333
            >>> q.quantize_self(x)
            Warning: quantize_self can only be used for torch.Tensor!
            >>> print(x)
            -0.333
        """
        if torch.is_tensor(x):
            x[:] = self.quantize(x)
        else:
            raise Warning('quantize_self can only be used for torch.Tensor!')

    q = quantize
    """Alias for :func:`~ptcq.FixedQ.quantize`."""

    qs = quantize_self
    """Alias for :func:`~ptcq.FixedQ.quantize_self`."""

