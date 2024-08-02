
import requests

rs1 = (
  "https://rata.digitraffic.fi/api/v1" + 
  "/live-trains/station/HKI" +
  "?minutes_before_departure=15" +
  "&minutes_after_departure=15" +
  "&minutes_before_arrival=15" + 
  "&minutes_after_arrival=15")

response = requests.get (rs1)
data = response.json ()

print (data)

[{'trainNumber': 8226, 'departureDate': '2024-07-31', 'operatorUICCode': 10, 'operatorShortCode': 'vr', 'trainType': 'HL', 'trainCategory': 'Commuter', 'commuterLineID': 'A', 'runningCurrently': False, 'cancelled': False, 'version': 288932726507, 'timetableType': 'REGULAR', 'timetableAcceptanceDate': '2024-05-08T10:55:08.000Z', 'timeTableRows': [{'stationShortCode': 'LPV', 'stationUICCode': 68, 'countryCode': 'FI', 'type': 'DEPARTURE', 'trainStopping': True, 'commercialStop': True, 'commercialTrack': '4', 'cancelled': False, 'scheduledTime': '2024-07-31T20:26:00.000Z', 'actualTime': '2024-07-31T20:26:12.000Z', 'differenceInMinutes': 0, 'causes': [], 'trainReady': {'source': 'KUPLA', 'accepted': True, 'timestamp': '2024-07-31T20:24:44.000Z'}}, {'stationShortCode': 'MÄK', 'stationUICCode': 693, 'countryCode': 'FI', 'type': 'ARRIVAL', 'trainStopping': True, 'commercialStop': True, 'commercialTrack': '3', 'cancelled': False, 'scheduledTime': '2024-07-31T20:27:30.000Z', 'actualTime': '2024-07-31T20:28:12.000Z', 'differenceInMinutes': 1, 'causes': []}, {'stationShortCode': 'MÄK', 'stationUICCode': 693, 'countryCode': 'FI', 'type': 'DEPARTURE', 'trainStopping': True, 'commercialStop': True, 'commercialTrack': '3', 'cancelled': False, 'scheduledTime': '2024-07-31T20:28:00.000Z', 'actualTime': '2024-07-31T20:28:39.000Z', 'differenceInMinutes': 1, 'causes': []}, ...







