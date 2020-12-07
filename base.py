
from math import pi, sin, cos, atan, sqrt

tau = (1 + sqrt(5.0)) / 2.0  # a.k.a. phi


class Apex(object):
    """
    Apices decribe the intersections of lines (either perimeter or breakdown)
    within a *Geodesic*'s face triangle.

    There are two coordinate systems and which one is used depends on the
    aspect of the given apex being used.

        - x, y, z coordinates correspond to the perimeter of the triangle,
          with the tics being the terminal ends of breakdown lines.
        - l, r coordinates correspond only to the [l]eft and [r] sides of
          the triangle.

    There is a simple mapping from x, y, z to l, r, but no inverse map.
    """
    def __init__(self, x: int, y: int, z: int):
        self._x = x
        self._y = y
        self._z = z

    def phi(self):
        """Eq. 12.1 - p 74"""
        if self._y == 0:
            return pi / 2
        return atan(self._x / self._y)

    def theta(self):
        """Eq 12.2 - p 74"""
        if self._z == 0:
            return pi / 2
        return atan(sqrt(self._x**2 + self._y**2) / self._z)
        
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def l(self):
        return self._y

    @property
    def r(self):
        return self._x + self._y

    @property
    def xyz(self):
        return [self._x, self._y, self._z]

    @property
    def lr(self):
        return [self._l, self._r]

    def __repr__(self):
        return str([self._x, self._y, self._z])


class Geodesic(object):
    '''
    Base class for calculating geodesic chord factors and angles.
    '''

    def rho(self, v: int=1):
        '''
        Build three arrays representing a Class I, method 1 breakdown
        of a geodesic triangle face. These will be used later to
        construct the (x, y, z) tuples that will become input to the
        function(s) that calculate the spherical coordinates and ultimately
        the chord factors for the given geodesic."

        [ref: Geodesic Mathematics, ch 12]
        '''

        # Sanity check:
        if v < 1:
            raise ValueError("v must be positive integer")
        if v > 8:
            raise ValueError("v > 8?  Seriously???")

        result = list()

        vp1 = v + 1   # Used frequently, so DRY.
        bseq = list(range(vp1))
        brev = bseq[::-1]

        # rho_0
        rho_0 = list()
        for i in range(vp1):
            rho_0.extend(bseq[i:i+1]*(vp1-i))
        result.append(rho_0)

        # rho_1
        rho_1 = list()
        for i in range(vp1):
            rho_1.extend(brev[i:])
        result.append(rho_1)

        # rho_2
        rho_2 = list()
        for i in range(vp1, -1, -1):
            rho_2.extend(bseq[:i])
        result.append(rho_2)

        return result

    def _cvt(self, x, y, z, v):
        """
        1v tetrahedron apices lie on the axes, but the two "lower" icosahedron
        apices do not and thus their coordinates need to be adjusted before
        passing them to the Apex constructor.
        
        The default conversion is simply an identity.
        """
        return x, y, z
        
    def apices(self, v: int=1):
        if v < 1:
            raise ValueError('v must be a positive integer')
        rho_set = self.rho(v)
        result = [Apex(*(self._cvt(rho_set[0][i], rho_set[1][i], rho_set[2][i], v)))
                  for i in range(len(rho_set[0]))]
        return result

    def dist(self, a1, a2):  # r: float = 1
        """
        Calculate the distance between the two apices, a1 and a2,
        given their **spherical** coordinates (phi,theta).
        Radius (r) is assumed to be 1.

        Eq. 9.2 - p 60 (sphere w/ r=1)
        """
        return sqrt(2 - (2 * cos(a1.theta()) * cos(a2.theta()) +
                    cos(a1.phi() - a2.phi()) * sin(a1.theta()) * sin(a2.theta())))



class TetraGeodesic(Geodesic):
    """
    Tetrahedron Geodesic Base
    -------------------------
    Because the tetrahedron is so spacially ineffecient, it is unlikely
    we'll ever use this class.  It is included only for completeness.
    """
    def __init__(self, *args, **kwargs):
        raise TypeError("Unimplemented!")


class OctaGeodesic(Geodesic):
    """
    Octahedron Geodesic Base
    ------------------------
    """
    def phi(self, *args):
        return super().phi(*args)

    def theta(self, *args):
        return super().theta(*args)


class IcosaGeodesic(Geodesic):
    """
    Icosohedron (20-side) Geodesic Base
    -----------------------------------
    """

    ia = 2 * pi / 5

    def _cvt(self, x: float, y: float, z: float, v: int=1):
        """Bottom of page 74, transform req'd for icosa."""
        return (x * sin(self.ia),        # Eq. 12.4 - X1
                y + x * cos(self.ia),    # Eq. 12.5 - Y1
                v / 2 + z / tau)         # Eq. 12.6 - Z1
