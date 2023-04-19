import math

### TLE setup
## Line 1
# 7 Epoch Year
# 8 Epoch Day
# 9 First derivative of mean motion
# 10 Second derivative of mm
# 13 Element set number

## Line 2
# 3 Inclination (deg)
# 4 RAAN (deg)
# 5 Eccentricity (decimal point to be added )
# 6 Argument of perigee (deg)
# 7 Mean anomaly (degrees)
# 8 Mean motion (revolutions/day)
# 9 Revolution # at epoch (revolutions)


## Convert day of the year to month and day (example: dayofyear = 276.34543)
def day_to_monthday(year, dayofyear):
    daynums = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
    if year == 2020 or year ==  2024 or year ==  2028 or year == 2032 or year == 2036 or year == 2040 or year == 2044 or year == 2048: # if it's a leap year, take it into account!
        for i in range(len(daynums) - 2):
            daynums[i + 2] += 1
    if dayofyear >= daynums[0] and dayofyear <= daynums[1]:
        month = 1
    elif dayofyear > daynums[1] and dayofyear <= daynums[2]:
        month = 2
    elif dayofyear > daynums[2] and dayofyear <= daynums[3]:
        month = 3
    elif dayofyear > daynums[3] and dayofyear <= daynums[4]:
        month = 4
    elif dayofyear > daynums[4] and dayofyear <= daynums[5]:
        month = 5
    elif dayofyear > daynums[5] and dayofyear <= daynums[6]:
        month = 6
    elif dayofyear > daynums[6] and dayofyear <= daynums[7]:
        month = 7
    elif dayofyear > daynums[7] and dayofyear <= daynums[8]:
        month = 8   
    elif dayofyear > daynums[8] and dayofyear <= daynums[9]:
        month = 9
    elif dayofyear > daynums[9] and dayofyear <= daynums[10]:
        month = 10
    elif dayofyear > daynums[10] and dayofyear <= daynums[11]:
        month = 11
    elif dayofyear > daynums[11] and dayofyear <= daynums[12]:
        month = 12

    ind = month-1
    dayspassed = daynums[ind] 
    dayofmon = dayofyear - dayspassed # days since month started, example: 5th of May 
    return (month, dayofmon)   # returns month and day


################### TLE Reader # returns epoch and ephemeris
def read_TLE(line1, line2):
    
    # determining epoch
    year = '20' + line1[18:20]
    year = int(year)

    totday = float(line1[20:32]) # XXX.XXXXXX, includes decimal of day
    month, day = day_to_monthday(year, totday)
    
    day = int(day) # strips off decimal

    tothour = (totday%1)*24 # converts decimal (remainder) to hours
    hour = int(tothour)

    totminute = (tothour%1)*60 # converts hour decimal to minutes
    minute = int(totminute)

    second = (totminute%1)*60 # converts minute decimal to second.  Final product is SS.SSSS---, which is what we want.

    # epoch format: [day, month, year, hour, minute, second (ss.sss)]
    epoch = [day, month, year, hour, minute, second]

    
    ## Initializing ephemeris
    #ephem format: mean motion (deg/s), eccentricity, inclination (deg), RAAN(deg), argument of perigee (deg), mean anomaly (deg)
    meanmo = float(line2[52:63])
    inc = float(line2[8:16])
    raan = float(line2[17:25])

    e = float('0.' + line2[26:33])
    
    argper = float(line2[34:42])
    meananom = float(line2[43:51])

    ephem0 = [meanmo, e, inc, raan, argper, meananom]

    return epoch, ephem0


## Orbit Propagator, 2 body.  Takes in initial ephemeris from TLE and the current time since.
def orbit_propagator_2body(ephem0, t):   # ***** t is the time since the simulation began, need a clock.
    # two-body orbit propagator
    d2r = (math.pi)/180 

    # input ephemeris at epoch
    n0 = ephem0[0]*d2r  # mean motion, rad/sec
    e0 = ephem0[1]  # eccentricity
    i0 = ephem0[2]*d2r  # inclination, rad
    OMEGA0 = ephem0[3]*d2r  # longitude of ascending node, rad
    omega0 = ephem0[4]*d2r  # argument of perigee, rad
    M0 = ephem0[5]*d2r  # mean anonaly, rad
    #t  =  time of interest, sec

    # constants used
    #Re = 6.37814e6  # earth equatorial radius, m
    #mu = 3.986005e14  # earth gravitational parameter, m^3/s^2
    t0 = 0  # time at epoch
    # derived constants
    e = e0  # no varaition
    i = i0  # no variation
    n = n0  # novariation

    # propagate orbit
    # mean anomaly at time t, rad
    M = M0 + n*(t-t0) 
    # longitude of ascending node at time t, rad
    OMEGA = OMEGA0  # no variation
    # argument of perigee at time t, rad
    omega = omega0  # no variation

    # solve Kepler's eqn. for eccentric anomaly E
    Eold  =  M 
    Enew = 0 
    delta  =  Eold 
    while delta >=  .0000001:
        Enew  =  Eold+(M-Eold+e*(math.sin(Eold)))/(1-e*(math.cos(Eold))) 
        delta  =  abs(Eold-Enew) 
        Eold  =  Enew 
    E  =  Enew 

    # true anomaly
    sinv  =  math.sqrt(1-e**2)*math.sin(E)  #/(1-e*cos(E))       
    cosv  =  (math.cos(E)-e)  #/(1-e*cos(E)) 
    nu  =  math.atan2(sinv,cosv)                        # new true anomaly (radians)

    if nu < 0:
        nu = nu+2*math.pi  # to make 0 < nu < 2*pi

    # orbit radius
    # r = a*(1-e^2)/(1+e*cos(nu)) 

    ephem_nu = [n,e,i,OMEGA,omega,M,nu] 
    return ephem_nu

###########################################################

def JD_GMST(epoch0, t):

    # epoch0=[yr0,mo0,day0,hr0,min0,sec0] 
    Y=epoch0[0]
    M=epoch0[1]
    D=epoch0[2]
    HOURS=epoch0[3]
    MINUTES=epoch0[4]
    SECONDS=epoch0[5]+t 

    #D=u(1)  M=u(2)  Y=u(3) 
    #HOURS=u(4)  MINUTES=u(5)  SECONDS=u(6) 

    IJD=367*Y-int(7*(Y+int((M+9)/12))/4)+int(275*M/9)+D+1721013.5 
    DFRACT =  (HOURS/24 + MINUTES/1440 + SECONDS/86400) 
    JD = IJD + DFRACT 

    # GREENWICH Mean Sidereal ANGLE
    # JULIAN CENTURIES FROM 2000 JAN 1, 12H UT1
    TIME_J2000 = JD - 2451545. 
    T = TIME_J2000/36525. 
    GMST=67310.54841+(876600*3600+8640184.812866)*T+0.093104*(T**2)-((6.2)*(10**(-6)))*(T**3) 
    # print('GMST' + str(GMST))
    remGMST= GMST - 86400 * (int(GMST/86400)) # pretty sure this line is right. // used to be rem(GMST, 86400)
    # print('remgmst:' + str(remGMST))
    thetaGMST=remGMST/240 
    print(thetaGMST)
    if thetaGMST < 0:
        thetaGMST = thetaGMST + 360 
    
    JD_thetaGMST=[JD, thetaGMST] 
    return JD_thetaGMST


####################################################### 
# RECI and VECI

def rv_eci(ephem_nu):

    d2r=math.pi/180 
    # input: orbital parameters propagated to t
    n=ephem_nu[0]   # mean motion, rad/sec
    e=ephem_nu[1]   # eccentricity
    i=ephem_nu[2]   # inclination, rad
    OMEGA=ephem_nu[3]   # longitude of ascending node, rad
    omega=ephem_nu[4]   # argument of perigee, rad
    M=ephem_nu[5]   # mean anonaly, rad
    nu=ephem_nu[6]   # true anomaly, rad

    # constants used
    mu=3.986005*(10**14)  # earth gravitational parameter, m^3/s^2
    a=(mu/n**2)**(1/3)   # semi major axis, no variation
    p=a*(1-e**2)   # semi-latus rectum

    # orbit radius
    r=a*(1-e**2)/(1+e*math.cos(nu)) 

    # r and v in the perifocal frame (pqw)
    rpqw = [r*math.cos(nu), r*math.sin(nu), r*0]

    vpqw = [-math.sin(nu)*math.sqrt(mu/p), math.sqrt(mu/p)*(e+math.cos(nu)), math.sqrt(mu/p)*0]


    # r and v in ECI
    sO=math.sin(OMEGA)
    cO=math.cos(OMEGA) 
    so=math.sin(omega)
    co=math.cos(omega) 
    si=math.sin(i)
    ci=math.cos(i) 
    eciCpqw = [[cO*co-sO*so*ci,-cO*so-sO*co*ci,sO*si], [sO*co+cO*so*ci,-sO*so+cO*co*ci,-cO*si], [so*si,co*si,ci]]
    # reci=(eciCpqw*rpqw)
    reci = [[rpqw[0]*eciCpqw[0][0] + rpqw[1]*eciCpqw[0][1] + rpqw[2]*eciCpqw[0][2]], [rpqw[0]*eciCpqw[1][0] + rpqw[1]*eciCpqw[1][1] + rpqw[2]*eciCpqw[1][2]], [rpqw[0]*eciCpqw[2][0] + rpqw[1]*eciCpqw[2][1] + rpqw[2]*eciCpqw[2][2]]]       
    veci= [[vpqw[0]*eciCpqw[0][0] + vpqw[1]*eciCpqw[0][1] + vpqw[2]*eciCpqw[0][2]], [vpqw[0]*eciCpqw[1][0] + vpqw[1]*eciCpqw[1][1] + vpqw[2]*eciCpqw[1][2]], [vpqw[0]*eciCpqw[2][0] + vpqw[1]*eciCpqw[2][1] + vpqw[2]*eciCpqw[2][2]]]

    rveci = (reci, veci)
    # output
    #rvECI=[reci',veci'] 
    return rveci


################ shatECI

def SunVectorECI(JD):
    def mag(x):
        return math.sqrt(sum(i**2 for i in x))
    # input: JD at the current time
    

    # JD is a list... GHA is the second element in the list.  For this function, we only need JD (first element).
    JD = JD[0]


    # J2000 Julian Days
    n = JD - 2451545. 
    T = n/36525.  # Julian Centuries

    # #   Astronomical Almanac 2008
    # #   Page C24 Low Prec Formulas for the Sun's Coordinates
    # 
    # # Obliquity of the ecliptic, deg
    # obl=23.439-0.0000004*n 
    # obl=obl*d2r 
    # 
    # # mean longitude of the sun in the ecliptic from the mean equinox, deg
    # lon_mean=280.460+0.9856474*n 
    # # mean anomaly of the sun, deg
    # Msun=357.528+0.9856003*n 
    # # longitude of the sun
    # lon=lon_mean+1.915*sin(Msun*d2r)+0.02*sin(2*Msun*d2r) 

    #   Vallado's Book
    #   Page 279 sun position vector

    # Obliquity of the ecliptic, deg
    obl=23.439-0.0130042*T 
    # mean longitude of the sun in the ecliptic from the mean equinox, deg
    lon_mean=280.460+36000.771*T 
    # mean anomaly of the sun, deg
    Msun=357.528+35999.05034*T 

    Msun = math.radians(Msun)

    # longitude of the sun
    lon=lon_mean+1.914666471*math.sin(Msun)+0.019994643*math.sin(2*Msun) 
    # 0<lon<360
    lon = lon - 360 * int(lon/360)  # this should work.  Used to be rem(lon,360) in MATLAB
    if lon < 0:
        lon=lon+360 

    lon = math.radians(lon)
    obl = math.radians(obl)
    
    # compute sun vector in ECI frame
    # sun vector is from the earth to the sun
    shat_eci = [-1*math.cos(lon), -1*math.sin(lon)*math.cos(obl), -1*math.sin(lon)*math.sin(obl)]

    shat_eci = [shat_eci[0]/(mag(shat_eci)), shat_eci[1]/(mag(shat_eci)), shat_eci[2]/(mag(shat_eci))] # normalize again


    return shat_eci

################# EXECUTABLE CODE

# Initial epoch and ephemeris, taken from TLE

#ephem format: mean motion (deg/s), eccentricity, inclination (deg), RAAN(deg), argument of perigee (deg), mean anomaly (deg)
#epoch format: day, month, year, hour, minute, second (ss.sss)
line1 = '1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927'
line2 = '2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537'
epoch, ephem = read_TLE(line1, line2)

# time passed since epoch, [seconds]
t = 3405

# track 1 - RECI and VECI
ephem_nu = orbit_propagator_2body(ephem, t)
reci, veci = rv_eci(ephem_nu)

# track 2 - Sun Vector
jd = JD_GMST(epoch, t)
shat_ECI = SunVectorECI(jd)


# Print statements to check operation
print(orbit_propagator_2body(ephem, t))
print(jd)
print(reci)
print(veci)
print(shat_ECI)


