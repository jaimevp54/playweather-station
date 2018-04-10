import logging
import requests

last_sent= {
    "dateutc" : None,
    "winddir" : None,
    "windspeedmph" : None,
    "windgustmph" : None,
    "humidity" : None,
    "tempf" : None,
    "rainin" : None,
    "dailyrainin" : None,
    "baromin" : None,
    "dewptf" : None,
    "weather" : None,
    "clouds" : None,
    "softwaretype" : None,
    }

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
    def last_value(param, convertion_method=lambda x: x):
        try:
            value = readings[data_definitions[param]][-1]['value'] if param in data_definitions else None
            last_sent[param]=value
            return convertion_method(value) if value else None
        except IndexError:
            logging.warning('No data to available for: {} -> {}'.format(param,data_definitions[param]))
            return convertion_method(last_sent[param]) if last_sent[param] else None
        except KeyError:
            logging.exception('Key not found in given data')
        
    logging.info('Sending data to weather underground')
    readings = data['readings']
    winddir = last_value('winddir')
    windgustmph = last_value('windgustmph')
    humidity = last_value('humidity')
    rainin = last_value('rainin')
    dailyrainin = last_value('dailyrainin')
    baromin = last_value('baromin')
    dewptf = last_value('dewptf')
    weather = last_value('weather')
    softwaretype="Playweather"
    tempf = last_value('tempf', convertion_method=lambda x: x * 1.8 + 32)
    windspeedmph = last_value('windspeedmph', convertion_method=lambda x: x*0.621371)

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
    logging.debug("    "+response.text)
