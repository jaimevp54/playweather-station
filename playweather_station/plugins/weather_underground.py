import logging
import requests


def _send_request(id, password, dateutc=None, winddir=None, windspeedmph=None, windgustmph=None, humidity=None,
                  tempf=None, rainin=None, dailyrainin=None, baromin=None, dewptf=None, weather=None, clouds=None,
                  softwaretype=None):
    request_url = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?action=updateraw&ID={id}&PASSWORD={password}".format(
        id=id, password=password)

    if dateutc:
        request_url += "&dateutc=" + str(dateutc)
    if winddir:
        request_url += "&winddir=" + str(winddir)
    if windspeedmph:
        request_url += "&windspeedmph=" + str(windspeedmph)
    if windgustmph:
        request_url += "&windgustmph=" + str(windgustmph)
    if humidity:
        request_url += "&humidity=" + str(humidity)
    if tempf:
        request_url += "&tempf=" + str(tempf)
    if rainin:
        request_url += "&rainin=" + str(rainin)
    if dailyrainin:
        request_url += "&dailyrainin=" + str(dailyrainin)
    if baromin:
        request_url += "&baromin=" + str(baromin)
    if dewptf:
        request_url += "&dewptf=" + str(dewptf)
    if weather:
        request_url += "&weather=" + str(weather)
    if clouds:
        request_url += "&clouds=" + str(clouds)
    if softwaretype:
        request_url += "&softwaretype=" + str(softwaretype)

    return requests.get(request_url)


def deliver_data(wunderground_id, wunderground_key, data_definitions, data):
    def last_value(param):
        return readings[data_definitions[param]][-1]['value'] if param in data_definitions else None
    logging.info('Sending data to weather underground')
    readings = data['readings']
    winddir = last_value('winddir')
    windspeedmph = last_value('windspeedmph')
    windgustmph = last_value('windgustmph')
    humidity = last_value('humidity')
    tempf = last_value('tempf')
    rainin = last_value('rainin')
    dailyrainin = last_value('dailyrainin')
    baromin = last_value('baromin')
    dewptf = last_value('dewptf')
    weather = last_value('weather')
    softwaretype=None

    response = _send_request(
        wunderground_id,
        wunderground_key,
        dateutc="now",
        winddir=winddir,
        windspeedmph=windspeedmph,
        windgustmph=windgustmph,
        humidity=humidity,
        tempf=tempf,
        rainin=rainin,
        dailyrainin=dailyrainin,
        baromin=baromin,
        dewptf=dewptf,
        weather=weather,
        softwaretype=softwaretype,
    )

    logging.info('Weather underground responded with:')
    logging.info("    Code: "+str(response.status_code))
    logging.info("    "+response.text)