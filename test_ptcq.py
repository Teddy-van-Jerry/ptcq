import ptcq
import torch

fixed_q = ptcq.FixedQ(5, 3)
a = torch.rand(5)
print(a)
fixed_q.quantize_self(a)
print(a)

b = 1.214
print(b)
print(fixed_q.quantize(b))

print(ptcq.fixed_quantize(1.234, 5, 3))
