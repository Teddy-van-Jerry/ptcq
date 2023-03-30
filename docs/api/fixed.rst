Fixed-Point
===========

The :class:`.FixedQ` class provides a unified way for fixed-point quantization.

.. currentmodule:: ptcq

.. autoclass:: FixedQ

.. automethod:: FixedQ.__init__

.. automethod:: FixedQ.quantize

.. automethod:: FixedQ.quantize_self

.. automethod:: FixedQ.complex_quantize

.. automethod:: FixedQ.complex_quantize_self

To simplify the use, several method aliases are defined.

.. automethod:: FixedQ.q

.. automethod:: FixedQ.qs

.. automethod:: FixedQ.cq

.. automethod:: FixedQ.cqs

----

The :class:`.FixedCQ` class provides a unified way for fixed-point complex quantization.
This is a supplement to :class:`.FixedQ` where both real and complex versions are supported.

.. autoclass:: FixedCQ

.. automethod:: FixedCQ.__init__

.. automethod:: FixedCQ.real_quantize

.. automethod:: FixedCQ.quantize

.. automethod:: FixedCQ.quantize_self

.. automethod:: FixedCQ.complex_quantize

.. automethod:: FixedCQ.complex_quantize_self

To simplify the use, several method aliases are defined.

.. automethod:: FixedCQ.q

.. automethod:: FixedCQ.qs

.. automethod:: FixedCQ.cq

.. automethod:: FixedCQ.cqs

----

Standalone Functions
--------------------

There are also standalone functions available.

.. autofunction:: fixed_quantize
