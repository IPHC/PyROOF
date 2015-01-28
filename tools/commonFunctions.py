from math import sqrt, pi

def deltaR(phi1,eta1,phi2,eta2) :

    dEta = eta1 - eta2
    dPhi = angleInIntervalmPipPi(phi1 - phi2)

    return sqrt(dEta*dEta + dPhi*dPhi)

def angleInIntervalmPipPi(angle) :

    while (angle >= pi) : angle -= 2*pi;
    while (angle < -pi) : angle += 2*pi;
    return angle;
