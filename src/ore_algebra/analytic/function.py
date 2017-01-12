# -*- coding: utf-8 - vim: tw=80
r"""
D-Finite analytic functions

TESTS::

    sage: from ore_algebra import *
    sage: from ore_algebra.analytic.function import DFiniteFunction
    sage: DiffOps, x, Dx = DifferentialOperators()

    sage: f = DFiniteFunction((x^2 + 1)*Dx^2 + 2*x*Dx, [0, 1])

    sage: [f(10^i) for i in range(-3, 4)] # long time (5.6 s)
    [[0.0009999996666...], [0.0099996666866...], [0.0996686524911...],
     [0.7853981633974...], [1.4711276743037...], [1.5607966601082...],
     [1.5697963271282...]]

    sage: f(0)
    [+/- ...]

    sage: f(-1)
    [-0.78539816339744...]

    sage: (f(1.23456) - RBF(1.23456).arctan()).abs() < RBF(1)>>50
    True
    sage: R200 = RealBallField(200)
    sage: (f(1.23456, 100) - R200(1.23456).arctan()).abs() < (RBF(1) >> 99)
    True

    sage: plot(lambda x: RR(f(x, prec=10)), (-3, 3))
    Graphics object consisting of 1 graphics primitive

    sage: g = DFiniteFunction(Dx-1, [1])

    sage: [g(10^i) for i in range(-3, 4)]
    [[1.001000500166...],
     [1.010050167084...],
     [1.105170918075...],
     [2.718281828459...],
     [22026.46579480...],
     [2.688117141816...e+43...],
     [1.9700711140170...+434...]]

"""

import collections, logging

from sage.rings.all import ZZ, QQ, RBF, CBF
from sage.rings.complex_arb import ComplexBall, ComplexBallField
from sage.rings.complex_number import ComplexNumber
from sage.rings.real_arb import RealBall, RealBallField
from sage.rings.real_mpfr import RealNumber

from . import bounds

import ore_algebra.analytic.analytic_continuation as ancont
import ore_algebra.analytic.polynomial_approximation as polapprox
from ore_algebra.analytic.path import Point
from ore_algebra.analytic.safe_cmp import *

logger = logging.getLogger(__name__)

    # NOTES:
    #
    # - Make it possible to “split” a disk (i.e. use non-maximal disks) when the
    #   polynomial approximations become too large???
    #
    # - Introduce separate "Cache" objects?
    #
    # - Support derivatives and make it possible to share the analytic
    #   continuation part (computation of local initial values) between a
    #   function and its derivatives.
    #
    #   -> note : polapprox.doit() already supports that to some extent

RealPolApprox = collections.namedtuple('RealPolApprox', ['pol', 'prec'])

class DFiniteFunction(object):
    r"""
    At the moment, this class just provides a simple caching mechanism for
    repeated evaluations of a D-Finite function on the real line. It may
    evolve to support evaluations on the complex plane, branch cuts, ring
    operations on D-Finite functions, and more. Do not expect any API stability.
    """

    # Stupid, but simple and deterministic caching strategy:
    #
    # - To any center c = m·2^k with k ∈ ℤ and m *odd*, we associate the disk of
    #   radius 2^k. Any two disks with the same k have at most one point in
    #   common.
    #
    # - Thus, in the case of an equation with at least one finite singular
    #   point, there is a unique largest disk of the previous collection that
    #   contains any given ordinary x ∈ ℝ \ ℤ·2^(-∞) while staying “far enough”
    #   from the singularities.
    #
    # - When asked to evaluate f at x, we actually compute and store a
    #   polynomial approximation on (the real trace of) the corresponding disk
    #   and/or a vector of initial conditions at its center, which can then be
    #   reused for subsequent evaluations.
    #
    # - We may additionally want to allow disks (of any radius?) centered at
    #   real regular singular points, and perhaps, as a special case, at 0.
    #   These would be used when possible, and one would revert to the other
    #   family otherwise.

    def __init__(self, dop, ini, max_prec=256, max_rad=RBF('inf')):
        self.dop = dop
        if not isinstance(ini, dict):
            ini = {0: ini}
        if len(ini) != 1:
            # In the future, we should support specifying several vectors of
            # initial values.
            raise NotImplementedError
        self.ini = ini

        # Global maximum width for the approximation intervals. In the case of
        # equations with no finite singular point, we try to avoid cancellation
        # and interval blowup issues by taking polynomial approximations on
        # intervals on which the general term of the series doesn't grow too
        # large. The expected order of magnitude of the “top of the hump” is
        # about exp(κ·|αx|^(1/κ)) and doesn't depend on the base point. We also
        # let the user impose a maximum width, even in other cases.
        self.max_rad = RBF(max_rad)
        if dop.leading_coefficient().is_constant():
            kappa, alpha = _growth_parameters(dop)
            self.max_rad = self.max_rad.min(1/(alpha*RBF(kappa)**kappa))
        self.max_prec = max_prec

        self._inivecs = {}
        self._polys = {}

    def _disk(self, pt):
        assert pt.is_real()
        # Since approximation disks satisfy 2·rad ≤ dist(center, sing), any
        # approximation disk containing pt must have rad ≤ dist(pt, sing)
        max_rad = pt.dist_to_sing().min(self.max_rad)
        # What we want is the largest such disk containing pt
        expo = ZZ(max_rad.log(2).upper().ceil()) # rad = 2^expo
        logger.debug("max_rad = %s, expo = %s", max_rad, expo)
        while True:
            approx_pt = pt.approx_abs_real(-expo)
            mantissa = (approx_pt.squash() >> expo).floor()
            if ZZ(mantissa) % 2 == 0:
                mantissa += 1
            center = mantissa << expo
            dist = Point(center, pt.dop).dist_to_sing()
            rad = RBF.one() << expo
            logger.debug("candidate disk: approx_pt = %s, mantissa = %s, "
                         "center = %s, dist = %s, rad = %s",
                         approx_pt, mantissa, center, dist, rad)
            if safe_ge(dist >> 1, rad):
                break
            expo -= 1
        logger.debug("disk for %s: center=%s, rad=%s", pt, center, rad)
        # pt may be a ball with nonzero radius: check that it is contained in
        # our candidate disk
        log = approx_pt.abs().log(2)
        F = RealBallField(ZZ((expo - log).max(0).upper().ceil()) + 10)
        dist_to_center = (F(approx_pt) - F(center)).abs()
        if not safe_le(dist_to_center, rad):
            assert not safe_gt((approx_pt.squash() - center).squash(), rad)
            return None, None
        # exactify center so that subsequent computations are not limited by the
        # precision of its parent
        center = QQ(center)
        return center, rad

    def _path_to(self, dest, prec=None):
        r"""
        Find a path from a point with known "initial" values to pt
        """
        # TODO:
        # - attempt to start as close as possible to the destination
        #   [and perhaps add logic to change for a starting point with exact
        #   initial values if loosing too much precision]
        # - return a path passing through "interesting" points (and cache the
        #   associated initial vectors)
        start, ini = self.ini.items()[0]
        return ini, [start, dest]

    def approx(self, pt, prec=None):
        if prec is None:
            prec = _guess_prec(pt)
        pt = Point(pt, self.dop)
        eps = RBF.one() >> prec
        if prec >= self.max_prec or not pt.is_real():
            ini, path = self._path_to(pt)
            return self.dop.numerical_solution(ini, path, eps)
        center, rad = self._disk(pt)
        if center is None:
            raise NotImplementedError
        approx = self._polys.get(center)
        Balls = RealBallField(prec)
        reduced_pt = Balls(pt.value) - Balls(center)
        if approx is None or approx.prec < prec:
            ini, path = self._path_to(center, prec)
            ctx = ancont.Context(self.dop, path, eps, keep="all")
            pairs = ancont.analytic_continuation(ctx, ini=ini)
            for (vert, val) in pairs:
                known = self._inivecs.get(vert)
                if known is None or known[0].accuracy() < val[0][0].accuracy():
                    self._inivecs[vert] = [c[0] for c in val]
            logger.debug("computing a polynomial approximation: "
                         "ini = %s, path = %s, rad = %s, eps = %s",
                         ini, path, rad, eps)
            pol = polapprox.on_interval(self.dop, ini, path, eps, rad)
            self._polys[center] = approx = RealPolApprox(pol=pol, prec=prec)
        return approx.pol(reduced_pt)

    def __call__(self, x, prec=None):
        return self.approx(x, prec=prec)

    def plot(self, xmin, xmax):
        pass

    def plot_known(self):
        pass

def _guess_prec(pt):
    if isinstance(pt, (RealNumber, ComplexNumber, RealBall, ComplexBall)):
        return pt.parent().precision()
    else:
        return 53

def _growth_parameters(dop):
    r"""
    Find κ, α such that the solutions of dop grow at most like
    sum(α^n*x^n/n!^κ) ≈ exp(κ*(α·x)^(1/κ)).

    EXAMPLES::

        sage: from ore_algebra import *
        sage: DiffOps, x, Dx = DifferentialOperators()
        sage: from ore_algebra.analytic.function import _growth_parameters
        sage: _growth_parameters(Dx^2 + 2*x*Dx) # erf(x)
        (1/2, [1.4...])
        sage: _growth_parameters(Dx^2 + 8*x*Dx) # erf(2*x)
        (1/2, [2.82 +/- 8.45e-3])
        sage: _growth_parameters(Dx^2 - x) # Airy
        (2/3, [1.0 +/- 3.62e-3])

        XXX: todo - add an example with several slopes

    """
    # Newton polygon. In terms of the coefficient sequence,
    # (S^(-j)·((n+1)S)^i)(α^n/n!^κ) ≈ α^(i-j)·n^(i+κ(j-i)).
    # In terms of asymptotics at infinity,
    # (x^j·D^i)(exp(κ·(α·x)^(1/κ))) ≈ α^(i/κ)·x^((i+κ(j-i))/κ)·exp(...).
    # The upshot is that we want the smallest κ s.t. i+κ(j-i) is max and reached
    # twice, and then the largest |α| with sum[edge](a[i,j]·α^(i/κ))=0.
    # (Note that the equation on α resulting from the first formulation
    # simplifies thanks to i+κ(j-i)=cst on the edge.)
    points = [(ZZ(j-i), ZZ(i), c) for (i, pol) in enumerate(dop)
                                  for (j, c) in enumerate(pol)
                                  if not c.is_zero()]
    h0, i0, _ = min(points, key=lambda (h, i, c): (h, -j))
    slope = max((i-i0)/(h-h0) for (h, i, c) in points if h > h0)
    Pol = dop.base_ring()
    eqn = Pol({i: c for (h, i, c) in points if i == i0 + slope*(h-h0)})
    expo_growth = bounds.abs_min_nonzero_root(eqn)**(-slope)
    return -slope, expo_growth
