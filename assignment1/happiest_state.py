import sys
import json
import math
import heapq
import operator

def determine_state(tweet):
    if "coordinates" in tweet and tweet["coordinates"] != None and "coordinates" in tweet["coordinates"]:
        lat, lon = tweet["coordinates"]["coordinates"]
        closest = []
        for state in state_geo_centers:
            state_lon, state_lat = state_geo_centers[state]
            diff = math.hypot(lat-state_lat, lon-state_lon)
            heapq.heappush(closest, (diff, state))
        return heapq.heappop(closest)[1]
    ## TODO: You can add more parsing intelligence if tweets are not geocoded by looking at origin of user
    return None

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    sent_scores = parse_sentiment_scores(sent_file)
    tweets = parse_tweets(tweet_file)

    state_happiness = {}

    for tweet in tweets:
        if "place" in tweet \
        and tweet["place"] != None \
        and "country_code" in tweet["place"] \
        and tweet["place"]["country_code"] != None \
        and "US" == tweet["place"]["country_code"]:
            state = determine_state(tweet)
            if state != None:
                sentiment = tweet_sentiment(tweet, sent_scores)
                if not state in state_happiness: 
                    state_happiness[state] = []
                state_happiness[state].append(-sentiment)

    for state in state_happiness:
        state_happiness[state] = float(reduce(lambda x,y: x+y, state_happiness[state]))/len(state_happiness[state])

    print heapq.nsmallest(1, state_happiness.iteritems(), operator.itemgetter(1))[0][0]
    #map(prn, heapq.nsmallest(len(state_happiness), state_happiness.iteritems(), operator.itemgetter(1)))
    

def word_map_fn(word_dict, no_match_value=None):
    def word_map(word):
        if word in word_dict:
            return word_dict[word]
        else:
            return no_match_value
    return word_map

def parse_sentiment_scores(sent_file):
    sent_scores = {}
    for line in sent_file:
        term, score = line.split('\t')
        sent_scores[term] = int(score)
    return sent_scores

def parse_tweets(tweet_file):
    tweets = []
    for line in tweet_file:
        jsonTweet = json.loads(line)
        tweets.append(jsonTweet)
    return tweets

def tweet_sentiment(tweet, sent_scores):
    sentiment_map = word_map_fn(sent_scores, 0)
    return reduce(
        lambda x,y: x+y, 
        map(sentiment_map, 
            (tweet['text'].split() if 'text' in tweet else [0])),
        0)

def not_in_filter_fn(dictionary):
    def not_in_filter(entry):
        return not entry in dictionary
    return not_in_filter  


def prn(x):
    print x     

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

state_geo_centers = {   
    'AK': (61.3850,-152.2683),
    'AL': (32.7990,-86.8073),
    'AR': (34.9513,-92.3809),
    'AS': (14.2417,-170.7197),
    'AZ': (33.7712,-111.3877),
    'CA': (36.1700,-119.7462),
    'CO': (39.0646,-105.3272),
    'CT': (41.5834,-72.7622),
    'DC': (38.8964,-77.0262),
    'DE': (39.3498,-75.5148),
    'FL': (27.8333,-81.7170),
    'GA': (32.9866,-83.6487),
    'HI': (21.1098,-157.5311),
    'IA': (42.0046,-93.2140),
    'ID': (44.2394,-114.5103),
    'IL': (40.3363,-89.0022),
    'IN': (39.8647,-86.2604),
    'KS': (38.5111,-96.8005),
    'KY': (37.6690,-84.6514),
    'LA': (31.1801,-91.8749),
    'MA': (42.2373,-71.5314),
    'MD': (39.0724,-76.7902),
    'ME': (44.6074,-69.3977),
    'MI': (43.3504,-84.5603),
    'MN': (45.7326,-93.9196),
    'MO': (38.4623,-92.3020),
    'MP': (14.8058,145.5505),
    'MS': (32.7673,-89.6812),
    'MT': (46.9048,-110.3261),
    'NC': (35.6411,-79.8431),
    'ND': (47.5362,-99.7930),
    'NE': (41.1289,-98.2883),
    'NH': (43.4108,-71.5653),
    'NJ': (40.3140,-74.5089),
    'NM': (34.8375,-106.2371),
    'NV': (38.4199,-117.1219),
    'NY': (42.1497,-74.9384),
    'OH': (40.3736,-82.7755),
    'OK': (35.5376,-96.9247),
    'OR': (44.5672,-122.1269),
    'PA': (40.5773,-77.2640),
    'PR': (18.2766,-66.3350),
    'RI': (41.6772,-71.5101),
    'SC': (33.8191,-80.9066),
    'SD': (44.2853,-99.4632),
    'TN': (35.7449,-86.7489),
    'TX': (31.1060,-97.6475),
    'UT': (40.1135,-111.8535),
    'VA': (37.7680,-78.2057),
    'VI': (18.0001,-64.8199),
    'VT': (44.0407,-72.7093),
    'WA': (47.3917,-121.5708),
    'WI': (44.2563,-89.6385),
    'WV': (38.4680,-80.9696),
    'WY': (42.7475,-107.2085)
}

if __name__ == '__main__':
    main()
