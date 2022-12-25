import numpy as np

x = [2.00001170e+00, 4.07814649e-10, 1.70309422e+00, 6.80773469e-01, 2.16405374e+00, 8.51819552e-01]

Vr = np.array([[x[i]] for i in range(0, len(x), 2)])
Vi = np.array([[x[i]] for i in range(1, len(x), 2)])
V = Vr + 1j*Vi

print(V)
