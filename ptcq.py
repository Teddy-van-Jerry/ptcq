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
        :rtype: The same as input

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
        :raises Warning: Nothing will be done if the input is not a torch.Tensor.

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
        
    def complex_quantize(self, x):
        """Quantize the complex input with the fixed-point scheme.

        :param x: Input.
        :type x: complex float or complex torch.Tensor
        :return: The quantized result.
        :rtype: The same as input

        The following example shows the quantization of a normal complex number::

            >>> q = ptcq.FixedQ(5, 3)
            >>> a = torch.complex(torch.randn(2) * 3, torch.randn(2) * 2)
            >>> print(a)
            tensor([-0.2857-2.7639j, -4.3387-1.2555j])
            >>> q.complex_quantize(a)
            tensor([-0.2500-2.0000j, -2.0000-1.2500j])
        """
        if torch.is_tensor(x):
            assert torch.is_complex(x)
            return torch.complex(self.quantize(x.real), self.quantize(x.imag))
        else:
            return self.quantize(x.real) + 1j * self.quantize(x.imag)
        
    def complex_quantize_self(self, x):
        """Quantize the input complex tensor (in place) with the fixed-point scheme.

        :param x: Input
        :type x: complex torch.Tensor
        :raises Warning: Nothing will be done if the input is not a torch.Tensor.

        .. Caution::
            The input ``x`` must be a ``torch.Tensor``!
            Otherwise a warning will be raised and the input value is not changed.
            This is similar to :func:`~ptcq.FixedQ.quantize_self`.

        Example use for a 2D ``torch.Tensor``::

            >>> q = ptcq.FixedQ(5, 3)
            >>> a = torch.complex(torch.randn((2, 3)), torch.randn((2, 3)))
            >>> print(a)
            tensor([[-0.6809-0.8707j,  0.5028+1.0862j,  1.3537+0.3411j],
                    [ 0.1614-0.6922j, -0.4002-1.1781j,  1.5799-0.1048j]])
            >>> q.complex_quantize_self(a)
            >>> a
            tensor([[-0.6250-0.8750j,  0.5000+1.1250j,  1.3750+0.3750j],
                    [ 0.1250-0.7500j, -0.3750-1.1250j,  1.6250-0.1250j]])
        """
        if torch.is_tensor(x):
            assert(torch.is_complex(x))
            x[:] = self.complex_quantize(x)
        else:
            raise Warning('complex_quantize_self can only be used for torch.Tensor!')

    q = quantize
    """Alias for :func:`~ptcq.FixedQ.quantize`."""

    qs = quantize_self
    """Alias for :func:`~ptcq.FixedQ.quantize_self`."""

    cq = complex_quantize
    """Alias for :func:`~ptcq.FixedQ.complex_quantize`."""

    cqs = complex_quantize_self
    """Alias for :func:`~ptcq.FixedQ.complex_quantize_self`"""

class FixedCQ:
    """Fixed-point complex quantization. (Supplement to :class:`.FixedQ`.)
    """

    def __init__(self, W, D) -> None:
        """Initialize the fixed-point complex quantization scheme.

        :param W: Data bit width.
        :type W: unsigned integer
        :param D: Decimal bit width. This is the number of bits after the decimal point. It can be zero or negative.
        :type D: integer

        .. seealso:: Please refer to :func:`ptcq.FixedQ.__init__`.
        """
        self.W, self.D = W, D
        pass

    def real_quantize(self, x):
        """Quantize the real input with a fixed-point quantization scheme.

        :param x: Input
        :type x: real float or torch.Tensor
        :return: The quantized result.
        :rtype: The same as input

        .. tip::
            This is the same implementation of :func:`ptcq.FixedQ.quantize`.
            It is mostly useful for the class internal implementation.
            You are encouraged to use :func:`ptcq.FixedQ.quantize` over this method.
        """
        y = round_(shift_left_(x, self.D))
        y = clip_(y, self.W)
        y = shift_right_(y, self.D)
        return y

    def quantize(self, x):
        """Quantize the complex input with the fixed-point scheme.

        :param x: Input.
        :type x: complex float or complex torch.Tensor
        :return: The quantized result.
        :rtype: The same as input

        .. seealso:: This is equivalent to :func:`ptcq.FixedQ.complex_quantize`.

        The following example shows the quantization of a normal complex number::

            >>> q = ptcq.FixedCQ(5, 3)
            >>> q.quantize(1.23 + 4.56j)
            (1.25+1.875j)
        """
        if torch.is_tensor(x):
            assert torch.is_complex(x)
            return torch.complex(self.real_quantize(x.real), self.real_quantize(x.imag))
        else:
            return self.real_quantize(x.real) + 1j * self.real_quantize(x.imag)
        
    def quantize_self(self, x):
        """Quantize the input complex tensor (in place) with the fixed-point scheme.

        :param x: Input
        :type x: complex torch.Tensor
        :raises Warning: Nothing will be done if the input is not a torch.Tensor.

        .. seealso::
            This is equivalent to :func:`ptcq.FixedQ.complex_quantize_self`.

        Example use for a 2D ``torch.Tensor``::

            >>> a = torch.complex(torch.randn((2, 3)) * 20, torch.randn((2, 3)) * 30)
            >>> q = ptcq.FixedCQ(4, -1)
            >>> print(a)
            tensor([[-13.4490-8.0800j, -17.3926+42.9472j, -42.3367+26.1402j],
                    [  3.0652-27.2726j,  -4.9342-23.8858j,  15.8632+23.2699j]])
            >>> q.quantize_self(a)
            >>> print(a)
            tensor([[-14.-8.j, -16.+14.j, -16.+14.j],
                    [  4.-16.j,  -4.-16.j,  14.+14.j]])
        """
        if torch.is_tensor(x):
            assert(torch.is_complex(x))
            x[:] = self.quantize(x)
        else:
            raise Warning('complex_quantize_self can only be used for torch.Tensor!')
        
    complex_quantize = quantize
    """Alias for :func:`~ptcq.FixedCQ.quantize`."""

    complex_quantize_self = quantize_self
    """Alias for :func:`~ptcq.FixedCQ.quantize_self`."""

    q = quantize
    """Alias for :func:`~ptcq.FixedCQ.quantize`."""

    qs = quantize_self
    """Alias for :func:`~ptcq.FixedCQ.quantize_self`."""

    cq = quantize
    """Alias for :func:`~ptcq.FixedCQ.quantize`."""

    cqs = quantize_self
    """Alias for :func:`~ptcq.FixedCQ.quantize_self`"""
