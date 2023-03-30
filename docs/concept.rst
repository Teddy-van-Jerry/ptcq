Concept
=======

This simulates the quantization behavior in hardware implementation.

.. important::
    PTCQ is actually **fake** quantization that simulates the quantization behavior.
    There can be some limitations:

    - It does not consider the internal computation quantization process;
    - It does not accelerate the computation, still requiring ``float`` precision;
    - Quantization operations have to be implemented manually.
