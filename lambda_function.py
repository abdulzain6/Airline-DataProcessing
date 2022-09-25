from get_prices import Get_Prices
from datetime import datetime, date, time, timedelta
from expertflyer import ExpertFlyer
import random, re, csv, pytz, time_zone, json, boto3, contextlib
from typing import List, Dict


price_getter = Get_Prices(is_lamda=True)



def get_prices_and_seats(flights: List) -> List[List[Dict[str, str]]]:
    """
    Get the prices and booking classes from a list of flights.
    """
    airlines = ["UA", "FR", "DL", "WN"]
    airports = get_all_airports()
    prices_and_seats = []

    for flight in flights:
        airline = flight["flight"].replace(" ","")[:2]
        if airline not in airlines:
            continue

        try:
            time_zone_of_depart_airport = pytz.timezone(airports[flight["depart_airport"]])
        except KeyError:
            continue

        current_time_and_date = datetime.now(time_zone_of_depart_airport)
        current_time = current_time_and_date.time()
        current_time = datetime.combine(date.min, current_time) - datetime.min
        current_date = current_time_and_date.date()

        depart_time = flight["depart_time"]
        depart_time = datetime.strptime(depart_time, "%I:%M %p").time()
        depart_time = datetime.combine(date.min, depart_time) - datetime.min


        if flight["frequency"] != "Daily":
            parsed_frequency = flight["frequency"].split(",")
            time_differences = []
            for frequency in parsed_frequency:
                diff_bw_today_and_flight_day = time_zone.time_between_given_date_and_next_weekday(time_zone.weekdays[frequency], current_date, time_zone_of_depart_airport)
                time_till_flight = (diff_bw_today_and_flight_day - current_time) + depart_time
                time_differences.append(time_till_flight.total_seconds())

            index_of_least_difference = time_differences.index(min(time_differences))
            time_to_departure = time_differences[index_of_least_difference]
            date_of_departure = time_zone.get_next_weekday(time_zone.weekdays[parsed_frequency[index_of_least_difference]], time_zone_of_depart_airport)
        else:
            time_to_departure = depart_time - current_time
            time_to_departure = time_to_departure.total_seconds()
            date_of_departure = current_time_and_date.date()

        date_str = date_of_departure.strftime("%Y-%m-%d")

        bracket_free_flight_name = re.sub(r"[\(\[].*?[\)\]]", "", flight["flight"])
        try:
            if 0 < time_to_departure < 6 * 3600:
                price_and_classes = price_getter.get_flight_prices_online_specific(airline, bracket_free_flight_name.replace(" ",""), flight["depart_airport"], flight["arriving_airport"], date_str)
                print(price_and_classes, flight["flight"])
                prices_and_seats.extend(price_and_classes)
        except Exception as e:
            print(e)


    return prices_and_seats




'''
Loads all airports from a CSV stored in S3 in folder script-data/
'''
def get_all_airports() -> List:
    # These airports should be loaded from S3, for now I'm just hard coding some for testing
    airports = {}
    with open('/home/zain/Documents/airline_stats.csv') as fileObject:
        next(fileObject)
        reader_obj = csv.reader(fileObject)
        for row in reader_obj:
            airports[row[0]] = row[1]
    return airports

def get_all_flights() -> List:
    print("Getting all flights")

    airports = get_all_airports()
    expertflyer = ExpertFlyer()
    flights = []
    for airport in airports:
        timetables = expertflyer.flight_timetables_from_airport(airport)
        flights.extend(timetables)
        data = json.dumps(timetables)
        with open("flights.json", "a") as fp:
            fp.write(data)
    return flights

'''
Stores all the flights in S3 in a folder called script-data/
'''
def store_flights(flights):
    pass


'''
Loads the flights a folder script-data in S3
'''
def load_flights():
    flights = None
    return flights

'''
Stores the prices_and_seats data to S3 in raw-data/api/
'''
def store_prices_and_seats(prices_and_seats):
    with open("prices_classes.json", "w") as fp:
        fp.write(json.dumps(prices_and_seats))

def handle_errors(exception):
    subject = "ERROR in META script"
    body = str(exception)
    # Connect to AWS SES and send an email to "johan.land@gmail.com" with the subject and body above

    sender_email = 'johan.land@gmail.com'
    ses = boto3.client('ses')

    ses.send_email(
        Source=sender_email,
        Destination={
            "ToAddresses": ["gachhadar.anand@gmail.com", "johan.land@gmail.com"]
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': body,
                    'Charset': 'UTF-8'
                }
            }
        }
    )

def lambda_handler(event, context):
    #try:

    if event["action"] == "GetAllFlights":
        flights = get_all_flights()
        store_flights(flights)
    elif event["action"] == "GetPricesAndSeats":
        #flights = load_flights()
        #flights = get_all_flights()
        with open("flights.json") as fp:
            airport_flights = json.loads(fp.read())

        prices = []
        for flight in airport_flights:
            data = get_prices_and_seats(flight)
            prices.append(data)
            store_prices_and_seats(prices)
    else:
        print("Bad action")
        return {
            'statusCode': 202,
            'body': "Error: Bad action"
        }

    return {
        'statusCode': 200,
        'body': "Completed Successfully."
    }
    '''
    except Exception as e:
        handle_errors(e)
        return {
            'statusCode': 202,
            'body': "Error."
        }
    '''

#lambda_handler({"action":"GetAllFlights"}, None)
lambda_handler({"action":"GetPricesAndSeats"}, None)
