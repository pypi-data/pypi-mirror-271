import numpy as np
import numba as nb
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

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

class OscillatorsView(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        # Get parameters from the request data
        k1_start = request.data.get('k1_start', 1.0)
        k1_end = request.data.get('k1_end', 3.0)
        lambda2 = request.data.get('k2', 8.0)
        n = request.data.get('n', 1000)
        tran = 90000
        niter = 100000
        h = 0.01
        dk = 0.1
        K2 = lambda2
        pi = np.arctan(1.0) * 4
        random_state = np.random.RandomState(1234568)
        omega = np.tan((np.arange(n) * pi) / n - ((n + 1) * pi) / (2 * n))

        # Calculate forward values
        theta = -1.0 * pi + 2.0 * pi * random_state.rand(n)
        num_k1_values_forward = int((k1_end - k1_start) / dk) + 1
        r1_values_forward = []
        k1_values_forward = []
        for K1 in np.arange(k1_start, k1_end + 0.1, 0.1):
            r1 = 0.0
            r2 = 0.0
            beta = 0.0
            alpha = 0.0
            for it in range(1, niter + 1):
                rc1 = np.cos(theta).sum()
                rs1 = np.sin(theta).sum()
                rc2 = np.cos(2 * theta).sum()
                rs2 = np.sin(2 * theta).sum()
                ra = np.sqrt(rs1 ** 2 + rc1 ** 2) / n
                rb = np.sqrt(rs2 ** 2 + rc2 ** 2) / n
                dth = np.zeros_like(theta)
                derivs(0, dth, theta, omega, K1, K2, rs1, rs2, rc1, rc2, ra, beta, alpha, n)
                tho = np.zeros_like(theta)
                rk4(theta, dth, n, 0, h, tho, omega, K1, K2, ra, rs1, rs2, rc1, rc2, beta, alpha)
                theta = np.mod(tho, 2 * pi)
                if it > tran:
                    r1 += ra
                    r2 += rb
            r1 /= niter - tran
            r1_values_forward.append(r1)
            k1_values_forward.append(K1)
            print(f"K1 (Forward): {K1:.2f}, r1: {r1:.6f}")

        # Calculate backward values
        theta = 2 * pi * np.ones(n)
        r1_values_backward = []
        k1_values_backward = []
        for K1 in np.arange(k1_end, k1_start - 0.05, -0.05):
            r1 = 0.0
            r2 = 0.0
            x = 0
            y = 0
            beta = 0.0
            alpha = 0.0
            for it in range(1, niter + 1):
                rc1 = np.cos(theta).sum()
                rs1 = np.sin(theta).sum()
                rc2 = np.cos(2 * theta).sum()
                rs2 = np.sin(2 * theta).sum()
                ra = np.sqrt(rs1 ** 2 + rc1 ** 2) / n
                rb = np.sqrt(rs2 ** 2 + rc2 ** 2) / n
                dth = np.zeros_like(theta)
                derivs(0, dth, theta, omega, K1, K2, rs1, rs2, rc1, rc2, ra, beta, alpha, n)
                tho = np.zeros_like(theta)
                rk4(theta, dth, n, 0, h, tho, omega, K1, K2, ra, rs1, rs2, rc1, rc2, beta, alpha)
                theta = np.mod(tho, 2 * pi)
                if it > tran:
                    r1 += ra
                    r2 += rb
            r1 /= niter - tran
            r1_values_backward.append(r1)
            k1_values_backward.append(K1)
            print(f"K1 (Backward): {K1:.2f}, r1: {r1:.6f}")

        data = {
            'k1_values_forward': k1_values_forward,
            'r1_values_forward': r1_values_forward,
            'k1_values_backward': k1_values_backward,
            'r1_values_backward': r1_values_backward,
        }
        return Response(data)