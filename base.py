
from math import pi, sin, cos, atan, sqrt

class Geodesic(object):
    '''
    Base class for calculating geodesic chord factors and angles.
    '''
    
    def rho(self, v : int = 1):
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

    def points(self, v: int = 1):
        rho_set = self.rho(v)
        result = [[rho_set[j][i] for j in range(3)] for i in range(len(rho_set[0]))]
        return result
        
    def dist(self, p1, p2):
        """
        Calculate the distance between the two points, 
        given their **spherical** coordinates (phi,theta).
        Radius (r) is assumed to be 1.
        
        Eq. 9.2 - p 60 (sphere w/ r=1)
        """
        return sqrt(2 - 2 * cos(p1[1]) * cos(p2[1]) + \
                    cos(p1[0] - p2[0]) * sin(p1[1]) * sin(p2[1]))
        
                                                                   
class GeodesicAngleMixin(object):
    """
    These are the angle calculations for TetraGeodesic.  They
    can also be used for IcosaGeodesic with the angle correction functions.
    """
        
class TetraGeodesic(Geodesic, GeodesicAngleMixin):
    """
    Tetrahedron Geodesic Base
    -------------------------
    Because the tetrahedron is so spacially ineffecient, it is unlikely
    we'll ever use this class.  It is included only for completeness.
    """
    
    def phi(self, x: float, y: float, z: float):
        """Eq. 12.1 - p 74"""
        if y == 0:
            return pi / 2
        return atan(x / y)

    def theta(self, x: float, y: float, z: float):
        """Eq 12.2 - p 74"""
        if z == 0:
            return pi / 2
        return atan(sqrt(x**2 + y**2) / z)
            
                                                                   
class OctaGeodesic(Geodesic):
    """
    Octahedron Geodesic Base
    ------------------------
    """
    
    
    
class IcosaGeodesic(Geodesic, GeodesicAngleMixin):
    """
    Icosohedron (20-side) Geodesic Base
    -----------------------------------
    """
    
    ia = 2 * pi / 5
    tau = (1 + sqrt(5)) / 2  # aka phi
    
    def _cvt(self, x: float, y: float, z: float, v: int):
        """Bottom of page 74, transform req'd for icosa."""
        x1 = x * math.sin(self.ia)   # Eq. 12.4
        y1 = y + x * math.cos(ia)    # Eq. 12.5
        z1 = v / 2 + z / self.tau    # Eq. 12.6
        return (x1, y1, z1)
       
    def phi(self, x: float, y: float, z: float, v: int):
        """Eq. 12.1 - p 74"""
        x1, y1, z1 = self._cvt(x, y, z, v)
        if y1 == 0:
            return pi / 2
        return atan(x1 / y1)

    def theta(self, x: float, y: float, z: float, v: int):
        """Eq 12.2 - p 74"""
        x1, y1, z1 = self._cvt(x, y, z, v)
        if z == 0:
            return pi / 2
        return atan(sqrt(x1**2 + y1**2) / z1)
        
