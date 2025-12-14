import socket
import sys
import struct
import time
import configparser
from multiprocessing import shared_memory

def le_int8_to_bin(le_int, unisgned=True):
    if unisgned:
        return struct.pack('<B', le_int)
    else:
        return struct.pack('<b', le_int)

def le_int16_to_bin(le_int):
    return struct.pack('<H', le_int)

def le_int32_to_bin(le_int):
    return struct.pack('<I', le_int)

def le_int64_to_bin(le_int):
    return struct.pack('<Q', le_int)

def le_float_to_bin(le_float):
    return struct.pack('<f', le_float)

def dict_to_bytes(dic: dict) -> bytes:
    bytes = b''
    for i in dic:
        bytes+=dic[i]
    return bytes

def rev_light(buffer, min, max, max_perc):
    int_rev = struct.unpack('<H', buffer)[0]
    if int_rev > min:
        return int((int_rev-min)*(100/(max-min))*max_perc/100)
    else:
        return 0

def pkt_header(pkt_id):
    PacketHeader = {
            'm_packetFormat':           2023,
            'm_gameYear':               23,
            'm_gameMajorVersion':       1,
            'm_gameMinorVersion':       18,
            'm_packetVersion':          1,
            'm_packetId':               pkt_id,
            'm_sessionUID':             1,
            'm_sessionTime':            0,
            'm_frameIdentifier':        0,
            'm_overallFrameIdentifier': 0,
            'm_playerCarIndex':         0,
            'm_secondaryPlayerCarIndex':255
        }

    PacketHeaderBin = {
            'm_packetFormat':           le_int16_to_bin(PacketHeader['m_packetFormat']),
            'm_gameYear':               le_int8_to_bin(PacketHeader['m_gameYear']),
            'm_gameMajorVersion':       le_int8_to_bin(PacketHeader['m_gameMajorVersion']),
            'm_gameMinorVersion':       le_int8_to_bin(PacketHeader['m_gameMinorVersion']),
            'm_packetVersion':          le_int8_to_bin(PacketHeader['m_packetVersion']),
            'm_packetId':               le_int8_to_bin(PacketHeader['m_packetId']),
            'm_sessionUID':             le_int64_to_bin(PacketHeader['m_sessionUID']),
            'm_sessionTime':            le_float_to_bin(PacketHeader['m_sessionTime']),
            'm_frameIdentifier':        le_int32_to_bin(PacketHeader['m_frameIdentifier']),
            'm_overallFrameIdentifier': le_int32_to_bin(PacketHeader['m_overallFrameIdentifier']),
            'm_playerCarIndex':         le_int8_to_bin(PacketHeader['m_playerCarIndex']),
            'm_secondaryPlayerCarIndex':le_int8_to_bin(PacketHeader['m_secondaryPlayerCarIndex'])
        }
    
    return PacketHeaderBin

def car_telemetry(buffer, rpmmin, rpmmax, max_perc):
    CarTelemetryData = {
            'm_speed':                          struct.unpack('<h', buffer[6:8])[0],
            'm_throttle':                       0.0,
            'm_steer':                          0.0,
            'm_brake':                          0.0,
            'm_clutch':                           0,
            'm_gear':                           buffer[14],
            'm_engineRPM':                      struct.unpack('<H', buffer[15:17])[0],
            'm_drs':                              0,
            'm_revLightsPercent':               rev_light(buffer[15:17], rpmmin, rpmmax, max_perc),
            'm_revLightsBitValue':                14,
            'm_brakesTemperature[lr]':            0,
            'm_brakesTemperature[rr]':            0,
            'm_brakesTemperature[lf]':            0,
            'm_brakesTemperature[rf]':            0,
            'm_tyresSurfaceTemperature[lr]':       0,
            'm_tyresSurfaceTemperature[rr]':       0,
            'm_tyresSurfaceTemperature[lf]':       0,
            'm_tyresSurfaceTemperature[rf]':       0,
            'm_tyresInnerTemperature[lr]':         0,
            'm_tyresInnerTemperature[rr]':         0,
            'm_tyresInnerTemperature[lf]':         0,
            'm_tyresInnerTemperature[rf]':         0,
            'm_engineTemperature':                buffer[5],
            'm_tyresPressure[lr]':                 0,
            'm_tyresPressure[rr]':                 0,
            'm_tyresPressure[lf]':                 0,
            'm_tyresPressure[rf]':                 0,
            'm_surfaceType[lr]':                    0,
            'm_surfaceType[rr]':                    0,
            'm_surfaceType[lf]':                    0,
            'm_surfaceType[rf]':                    0
        }

    CarTelemetryDataBin = {
            'm_speed':                          le_int16_to_bin(CarTelemetryData['m_speed']),
            'm_throttle':                       le_float_to_bin(CarTelemetryData['m_throttle']),
            'm_steer':                          le_float_to_bin(CarTelemetryData['m_steer']),
            'm_brake':                          le_float_to_bin(CarTelemetryData['m_brake']),
            'm_clutch':                         le_int8_to_bin(CarTelemetryData['m_clutch']),
            'm_gear':                           le_int8_to_bin(CarTelemetryData['m_gear'], unisgned=False),
            'm_engineRPM':                      le_int16_to_bin(CarTelemetryData['m_engineRPM']),
            'm_drs':                            le_int8_to_bin(CarTelemetryData['m_drs']),
            'm_revLightsPercent':               le_int8_to_bin(CarTelemetryData['m_revLightsPercent']),
            'm_revLightsBitValue':              le_int16_to_bin(CarTelemetryData['m_revLightsBitValue']),
            'm_brakesTemperature[1]':           le_int16_to_bin(CarTelemetryData['m_brakesTemperature[lr]']),
            'm_brakesTemperature[2]':           le_int16_to_bin(CarTelemetryData['m_brakesTemperature[rr]']),
            'm_brakesTemperature[3]':           le_int16_to_bin(CarTelemetryData['m_brakesTemperature[lf]']),
            'm_brakesTemperature[4]':           le_int16_to_bin(CarTelemetryData['m_brakesTemperature[rf]']),
            'm_tyresSurfaceTemperature[1]':     le_int8_to_bin(CarTelemetryData['m_tyresSurfaceTemperature[lr]']),
            'm_tyresSurfaceTemperature[2]':     le_int8_to_bin(CarTelemetryData['m_tyresSurfaceTemperature[rr]']),
            'm_tyresSurfaceTemperature[3]':     le_int8_to_bin(CarTelemetryData['m_tyresSurfaceTemperature[lf]']),
            'm_tyresSurfaceTemperature[4]':     le_int8_to_bin(CarTelemetryData['m_tyresSurfaceTemperature[rf]']),
            'm_tyresInnerTemperature[1]':       le_int8_to_bin(CarTelemetryData['m_tyresInnerTemperature[lr]']),
            'm_tyresInnerTemperature[2]':       le_int8_to_bin(CarTelemetryData['m_tyresInnerTemperature[rr]']),
            'm_tyresInnerTemperature[3]':       le_int8_to_bin(CarTelemetryData['m_tyresInnerTemperature[lf]']),
            'm_tyresInnerTemperature[4]':       le_int8_to_bin(CarTelemetryData['m_tyresInnerTemperature[rf]']),
            'm_engineTemperature':              le_int16_to_bin(CarTelemetryData['m_engineTemperature']),
            'm_tyresPressure[1]':               le_float_to_bin(CarTelemetryData['m_tyresPressure[lr]']),
            'm_tyresPressure[2]':               le_float_to_bin(CarTelemetryData['m_tyresPressure[rr]']),
            'm_tyresPressure[3]':               le_float_to_bin(CarTelemetryData['m_tyresPressure[lf]']),
            'm_tyresPressure[4]':               le_float_to_bin(CarTelemetryData['m_tyresPressure[rf]']),
            'm_surfaceType[1]':                 le_int8_to_bin(CarTelemetryData['m_surfaceType[lr]']),
            'm_surfaceType[2]':                 le_int8_to_bin(CarTelemetryData['m_surfaceType[rr]']),
            'm_surfaceType[3]':                 le_int8_to_bin(CarTelemetryData['m_surfaceType[lf]']),
            'm_surfaceType[4]':                 le_int8_to_bin(CarTelemetryData['m_surfaceType[rf]']),
            'm_mfdPanelIndex':                  le_int8_to_bin(0),
            'm_mfdPanelIndexSecondaryPlayer':   le_int8_to_bin(1),
            'm_suggestedGear':                  le_int8_to_bin(1, unisgned=False)
        }
    return CarTelemetryDataBin

def lap_status(buffer, lastLapTime, currentlapTime):

    LapData = {
    'm_lastLapTimeInMS' : lastLapTime,
    'm_currentLapTimeInMS': currentlapTime,
    'm_sector1TimeInMS': 0,
    'm_sector1TimeMinutes': 0,
    'm_sector2TimeInMS': 0,
    'm_sector2TimeMinutes': 0,
    'm_deltaToCarInFrontInMS': 65535 if struct.unpack('<I', buffer[21:25])[0] > 65535 else struct.unpack('<I', buffer[21:25])[0],
    'm_deltaToRaceLeaderInMS': 0,
    'm_lapDistance': -1,
    'm_totalDistance': -1,
    'm_safetyCarDelta': 0,
    'm_carPosition': buffer[2],
    'm_currentLapNum': buffer[1],
    'm_pitStatus': 1 if buffer[0]==1 else 0,                     # 0 = none, 1 = pitting, 2 = in pit area
    'm_numPitStops': 0,                   # Number of pit stops taken in this race
    'm_sector': 0,                        # 0 = sector1, 1 = sector2, 2 = sector3
    'm_currentLapInvalid': 0,             # Current lap invalid - 0 = valid, 1 = invalid
    'm_penalties': 0,                     # Accumulated time penalties in seconds to be added
    'm_totalWarnings': 0,                 # Accumulated number of warnings issued
    'm_cornerCuttingWarnings': 0,         # Accumulated number of corner cutting warnings issued
    'm_numUnservedDriveThroughPens': 0,   # Num drive through pens left to serve
    'm_numUnservedStopGoPens': 0,         # Num stop go pens left to serve
    'm_gridPosition': 0,                  # Grid position the vehicle started the race in
    'm_driverStatus': 0,                  # Status of driver - 0 = in garage, 1 = flying lap
                                          # 2 = in lap, 3 = out lap, 4 = on track
    'm_resultStatus': 0,                  # Result status - 0 = invalid, 1 = inactive, 2 = active
                                          # 3 = finished, 4 = didnotfinish, 5 = disqualified
                                          # 6 = not classified, 7 = retired
    'm_pitLaneTimerActive': 0,            # Pit lane timing, 0 = inactive, 1 = active
    'm_pitLaneTimeInLaneInMS': 0,         # If active, the current time spent in the pit lane in ms
    'm_pitStopTimerInMS': 0,              # Time of the actual pit stop in ms
    'm_pitStopShouldServePen': 0          # Whether the car should serve a penalty at this stop
    }

    LapDataBin = {
    'm_lastLapTimeInMS' :      le_int32_to_bin(LapData['m_lastLapTimeInMS']),
    'm_currentLapTimeInMS':    le_int32_to_bin(LapData['m_currentLapTimeInMS']),
    'm_sector1TimeInMS':       le_int16_to_bin(LapData['m_sector1TimeInMS']),
    'm_sector1TimeMinutes':    le_int8_to_bin(LapData['m_sector1TimeMinutes']),
    'm_sector2TimeInMS':       le_int16_to_bin(LapData['m_sector2TimeInMS']),
    'm_sector2TimeMinutes':    le_int8_to_bin(LapData['m_sector2TimeMinutes']),
    'm_deltaToCarInFrontInMS': le_int16_to_bin(LapData['m_deltaToCarInFrontInMS']),
    'm_deltaToRaceLeaderInMS': le_int16_to_bin(LapData['m_deltaToRaceLeaderInMS']),
    'm_lapDistance':           le_float_to_bin(LapData['m_lapDistance']),
    'm_totalDistance':         le_float_to_bin(LapData['m_totalDistance']),
    'm_safetyCarDelta':        le_float_to_bin(LapData['m_safetyCarDelta']),
    'm_carPosition':           le_int8_to_bin(LapData['m_carPosition']),
    'm_currentLapNum':         le_int8_to_bin(LapData['m_currentLapNum']),
    'm_pitStatus':             le_int8_to_bin(LapData['m_pitStatus']),
    'm_numPitStops':           le_int8_to_bin(LapData['m_numPitStops']),
    'm_sector':                le_int8_to_bin(LapData['m_sector']),
    'm_currentLapInvalid':     le_int8_to_bin(LapData['m_currentLapInvalid']),
    'm_penalties':             le_int8_to_bin(LapData['m_penalties']),
    'm_totalWarnings':         le_int8_to_bin(LapData['m_totalWarnings']),
    'm_cornerCuttingWarnings': le_int8_to_bin(LapData['m_cornerCuttingWarnings']),
    'm_numUnservedDriveThroughPens': le_int8_to_bin(LapData['m_numUnservedDriveThroughPens']),
    'm_numUnservedStopGoPens': le_int8_to_bin(LapData['m_numUnservedStopGoPens']),
    'm_gridPosition':          le_int8_to_bin(LapData['m_gridPosition']),
    'm_driverStatus':          le_int8_to_bin(LapData['m_driverStatus']),
    'm_resultStatus':          le_int8_to_bin(LapData['m_resultStatus']),
    'm_pitLaneTimerActive':    le_int8_to_bin(LapData['m_pitLaneTimerActive']),
    'm_pitLaneTimeInLaneInMS': le_int16_to_bin(LapData['m_pitLaneTimeInLaneInMS']),
    'm_pitStopTimerInMS':      le_int16_to_bin(LapData['m_pitStopTimerInMS']),
    'm_pitStopShouldServePen': le_int8_to_bin(LapData['m_pitStopShouldServePen']),
    }
    return LapDataBin

def car_status(buffer):
    flag = 0
    if buffer[0] == 8:
        flag = 2 # Blue flag
    elif buffer[0] == 4:
        flag = 3 # Yellow flag
    elif buffer[0] in [1, 2]:
        flag = 1 # Warning
    CarStatusData = {
        'm_tractionControl':          0,
        'm_antiLockBrakes':           0,
        'm_fuelMix':                  0,
        'm_frontBrakeBias':           0,
        'm_pitLimiterStatus':         0,
        'm_fuelInTank':               struct.unpack('<H', buffer[3:5])[0]/10,
        'm_fuelCapacity':             99.0,
        'm_fuelRemainingLaps':        struct.unpack('<H', buffer[3:5])[0]/10,
        'm_maxRPM':                   17000,
        'm_idleRPM':                  9000,
        'm_maxGears':                 7,
        'm_drsAllowed':               0,
        'm_drsActivationDistance':    0,
        'm_actualTyreCompound':       0,
        'm_visualTyreCompound':       0,
        'm_tyresAgeLaps':             0,
        'm_vehicleFiaFlags':          flag,
        'm_enginePowerICE':           0.0,
        'm_enginePowerMGUK':          0.0,
        'm_ersStoreEnergy':           0.0,
        'm_ersDeployMode':            0,
        'm_ersHarvestedThisLapMGUK':  0.0,
        'm_ersHarvestedThisLapMGUH':  0.0,
        'm_ersDeployedThisLap':       0.0,
        'm_networkPaused':            0
    }

    CarStatusDataBin = {
        'm_tractionControl':          le_int8_to_bin(CarStatusData['m_tractionControl']),
        'm_antiLockBrakes':           le_int8_to_bin(CarStatusData['m_antiLockBrakes']),
        'm_fuelMix':                  le_int8_to_bin(CarStatusData['m_fuelMix']),
        'm_frontBrakeBias':           le_int8_to_bin(CarStatusData['m_frontBrakeBias']),
        'm_pitLimiterStatus':         le_int8_to_bin(CarStatusData['m_pitLimiterStatus']),
        'm_fuelInTank':               le_float_to_bin(CarStatusData['m_fuelInTank']),
        'm_fuelCapacity':             le_float_to_bin(CarStatusData['m_fuelCapacity']),
        'm_fuelRemainingLaps':        le_float_to_bin(CarStatusData['m_fuelRemainingLaps']),
        'm_maxRPM':                   le_int16_to_bin(CarStatusData['m_maxRPM']),
        'm_idleRPM':                  le_int16_to_bin(CarStatusData['m_idleRPM']),
        'm_maxGears':                 le_int8_to_bin(CarStatusData['m_maxGears']),
        'm_drsAllowed':               le_int8_to_bin(CarStatusData['m_drsAllowed']),
        'm_drsActivationDistance':    le_int16_to_bin(CarStatusData['m_drsActivationDistance']),
        'm_actualTyreCompound':       le_int8_to_bin(CarStatusData['m_actualTyreCompound']),
        'm_visualTyreCompound':       le_int8_to_bin(CarStatusData['m_visualTyreCompound']),
        'm_tyresAgeLaps':             le_int8_to_bin(CarStatusData['m_tyresAgeLaps']),
        'm_vehicleFiaFlags':          le_int8_to_bin(CarStatusData['m_vehicleFiaFlags'], unisgned=False),
        'm_enginePowerICE':           le_float_to_bin(CarStatusData['m_enginePowerICE']),
        'm_enginePowerMGUK':          le_float_to_bin(CarStatusData['m_enginePowerMGUK']),
        'm_ersStoreEnergy':           le_float_to_bin(CarStatusData['m_ersStoreEnergy']),
        'm_ersDeployMode':            le_int8_to_bin(CarStatusData['m_ersDeployMode']),
        'm_ersHarvestedThisLapMGUK':  le_float_to_bin(CarStatusData['m_ersHarvestedThisLapMGUK']),
        'm_ersHarvestedThisLapMGUH':  le_float_to_bin(CarStatusData['m_ersHarvestedThisLapMGUH']),
        'm_ersDeployedThisLap':       le_float_to_bin(CarStatusData['m_ersDeployedThisLap']),
        'm_networkPaused':            le_int8_to_bin(CarStatusData['m_networkPaused'])
    }
    return CarStatusDataBin

def main():

    print('''
          
    ### Welcome to UDPrix v1.0 for GP4 ###
          Author SATLAB
    
    ''')

    try: 
        config = configparser.ConfigParser()
        config.read('UDPrixconfig.ini')

        UDP_IP = config['Network']['UDP_IP']
        UDP_PORT = int(config['Network']['UDP_PORT'])
        UDP_FREQ = int(config['Network']['UDP_FREQ'])
        MIN_RPM = int(config['Wheel_leds']['MIN_RPM'])
        MAX_RPM = int(config['Wheel_leds']['MAX_RPM'])
        MAX_PERC = int(config['Wheel_leds']['MAX_PERC'])

    except Exception:
        print('ERROR during config.ini reading: Check if UDPrixconfig.ini is in the same UDPrix folder!!')
        time.sleep(3)
        sys.exit(1)

    print(f'''
    UDPrix configuration (from ini):
          
        [Network]
        UDP_IP:     {UDP_IP}
        UDP_PORT:   {UDP_PORT}
        UDP_FREQ:   {UDP_FREQ}
        
        [Wheel_leds]
        MIN_RPM:    {MIN_RPM}
        MAX_RPM:    {MAX_RPM}
        MAX_PERC:   {MAX_PERC}  
    
    Waiting for GP4 to start. No GPx Info Data available. Make sure 'Export' is enabled in GPxCinfo.

    ''')

    sock_udp_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            # Accessing GPx shared memory
            shm = shared_memory.SharedMemory(name='GPxCInfo')
            print('''GP4 SESSION FOUND! Sending UDP Packets...
                  
                  Press Ctrl+C to close the program.

                  ''')
            break
        except:
            pass


    buffer = shm.buf
    lastLapTime = 0
    currentlapTime = 0

    try:
        while True:

            last_lap_num = buffer[1]
            currentlapTime = struct.unpack('<I', buffer[17:21])[0]

            # Sending CAR TELEMETRY packets to the wheel
            header = dict_to_bytes(pkt_header(6))
            car_tmry = dict_to_bytes(car_telemetry(buffer, MIN_RPM, MAX_RPM, MAX_PERC))
            sock_udp_send.sendto(header+car_tmry, (UDP_IP, UDP_PORT))
            time.sleep(1/UDP_FREQ)

            # Sending LAP STATUS packets to the wheel
            header = dict_to_bytes(pkt_header(2))
            lap_sts = dict_to_bytes(lap_status(buffer, lastLapTime, currentlapTime))
            sock_udp_send.sendto(header+lap_sts, (UDP_IP, UDP_PORT))
            time.sleep(1/UDP_FREQ)

            # Sending CAR STATUS packets to the wheel
            header = dict_to_bytes(pkt_header(7))
            car_sts = dict_to_bytes(car_status(buffer))
            sock_udp_send.sendto(header+car_sts, (UDP_IP, UDP_PORT))
            time.sleep(1/UDP_FREQ)

            # Show last lap time only after crossing the line (otherwise it will show the split)
            if last_lap_num < buffer[1] and last_lap_num != 0:
                lastLapTime = struct.unpack('<I', buffer[10:14])[0]

    except KeyboardInterrupt:
        print('Closing Program...')
    finally:
        sock_udp_send.close()
        print('Successfully closed UDP session.')
        shm.close()
        print('Successfully closed GPxCInfo shared memory access.')

if __name__ == '__main__':
    main()
    print('Goodbye cruel world!')
    time.sleep(2)