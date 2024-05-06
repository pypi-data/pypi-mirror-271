import numpy as np
import numba as nb
import random
import matplotlib.pyplot as plt
@nb.njit
def derivs(t, dth, theta, omega, K1, K2, rs1, rs2, rc1, rc2, ra, beta, alpha, n):
    x = 0  
    y = 0
    for i in range(n):
        dth[i] = omega[i] + (ra ** x) * (K1 / n) * (np.cos(theta[i] + alpha) * rs1 - np.sin(theta[i] + alpha) * rc1) + \
                 (K2 / n ** 2) * (ra ** y) * (np.cos(theta[i] + beta) * rs2 * rc1 - np.sin(theta[i] + beta) * rs2 * rs1 -
                                              np.sin(theta[i] + beta) * rc2 * rc1 - np.cos(theta[i] + beta) * rc2 * rs1)

@nb.njit
def rk4(y, dydx, n, x, h, yout, omega, K1, K2, ra, rs1, rs2, rc1, rc2, beta, alpha):
    dym = np.zeros_like(y)
    dyt = np.zeros_like(y)
    yt = np.zeros_like(y)
    hh = h * 0.5
    h6 = h / 6.0
    xh = x + hh
    yt = y + hh * dydx
    derivs(xh, yt, dyt, omega, K1, K2, rs1, rs2, rc1, rc2, ra, beta, alpha, n)
    yt = y + hh * dyt
    derivs(xh, yt, dym, omega, K1, K2, rs1, rs2, rc1, rc2, ra, beta, alpha, n)
    yt = y + h * dym
    dym += dyt
    derivs(x + h, yt, dyt, omega, K1, K2, rs1, rs2, rc1, rc2, ra, beta, alpha, n)
    yout[:] = y + h6 * (dydx + dyt + 2.0 * dym)

class OscillatorsSimulator:
    def __init__(self, k1_start, k1_end, k2, n, tran, niter, h, dk):
        self.k1_start = k1_start
        self.k1_end = k1_end
        self.k2 = k2
        self.n = n
        self.tran = tran
        self.niter = niter
        self.h = h
        self.dk = dk

    def simulate(self):
        pi = np.arctan(1.0) * 4
        random_state = np.random.RandomState(1234568)
        omega = np.tan((np.arange(self.n) * pi) / self.n - ((self.n + 1) * pi) / (2 * self.n))

        # Calculate forward values
        theta = -1.0 * pi + 2.0 * pi * random_state.rand(self.n)
        r1_values_forward = []
        k1_values_forward = []
        for K1 in np.arange(self.k1_start, self.k1_end + 0.01, self.dk):
            r1 = 0.0
            r2 = 0.0
            beta = 0.0
            alpha = 0.0
            for it in range(1, self.niter + 1):
                rc1 = np.cos(theta).sum()
                rs1 = np.sin(theta).sum()
                rc2 = np.cos(2 * theta).sum()
                rs2 = np.sin(2 * theta).sum()
                ra = np.sqrt(rs1 ** 2 + rc1 ** 2) / self.n
                rb = np.sqrt(rs2 ** 2 + rc2 ** 2) / self.n
                dth = np.zeros_like(theta)
                derivs(0, dth, theta, omega, K1, self.k2, rs1, rs2, rc1, rc2, ra, beta, alpha, self.n)
                tho = np.zeros_like(theta)
                rk4(theta, dth, self.n, 0, self.h, tho, omega, K1, self.k2, ra, rs1, rs2, rc1, rc2, beta, alpha)
                theta = np.mod(tho, 2 * pi)
                if it > self.tran:
                    r1 += ra
                    r2 += rb
            r1 /= self.niter - self.tran
            r1_values_forward.append(r1)
            k1_values_forward.append(K1)
            print(f"K1 (Forward): {K1:.2f}, r1: {r1:.6f}")

        # Calculate backward values
        theta = 2 * pi * np.ones(self.n)
        r1_values_backward = []
        k1_values_backward = []
        for K1 in np.arange(self.k1_end, self.k1_start - 0.05, -self.dk):
            r1 = 0.0
            r2 = 0.0
            x = 0
            y = 0
            beta = 0.0
            alpha = 0.0
            for it in range(1, self.niter + 1):
                rc1 = np.cos(theta).sum()
                rs1 = np.sin(theta).sum()
                rc2 = np.cos(2 * theta).sum()
                rs2 = np.sin(2 * theta).sum()
                ra = np.sqrt(rs1 ** 2 + rc1 ** 2) / self.n
                rb = np.sqrt(rs2 ** 2 + rc2 ** 2) / self.n
                dth = np.zeros_like(theta)
                derivs(0, dth, theta, omega, K1, self.k2, rs1, rs2, rc1, rc2, ra, beta, alpha, self.n)
                tho = np.zeros_like(theta)
                rk4(theta, dth, self.n, 0, self.h, tho, omega, K1, self.k2, ra, rs1, rs2, rc1, rc2, beta, alpha)
                theta = np.mod(tho, 2 * pi)
                if it > self.tran:
                    r1 += ra
                    r2 += rb
            r1 /= self.niter - self.tran
            r1_values_backward.append(r1)
            k1_values_backward.append(K1)
            print(f"K1 (Backward): {K1:.2f}, r1: {r1:.6f}")

        return {
            'k1_values_forward': k1_values_forward,
            'r1_values_forward': r1_values_forward,
            'k1_values_backward': k1_values_backward,
            'r1_values_backward': r1_values_backward,
        }
    

def plot_k1_vs_r1(results):
    k1_values_forward = results['k1_values_forward']
    r1_values_forward = results['r1_values_forward']
    k1_values_backward = results['k1_values_backward']
    r1_values_backward = results['r1_values_backward']

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(k1_values_forward, r1_values_forward, 'o-', label='Forward Simulation', markersize=4)
    ax.plot(k1_values_backward, r1_values_backward, 'o-', label='Backward Simulation', markersize=4)

    ax.set_xlabel('K1')
    ax.set_ylabel('r1')
    ax.set_title('K1 vs r1')
    ax.legend()

    plt.show()