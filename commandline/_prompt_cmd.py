import json
from datetime import datetime
from supabase import create_client, Client
import pytz

writer = "Hossein"

with open('config.json') as config_file:
    config = json.load(config_file)
url = config['API_URL']
key = config['API_KEY']
supabase: Client = create_client(str(url), str(key))
table = "report"
# get time
local_time = datetime.now()
local_tz = pytz.timezone("Asia/Tehran")
local_time = local_tz.localize(local_time)
utc_time = local_time.astimezone(pytz.UTC)
print(local_time)
time = str(local_time)
# TODO adding drug to program
drugs = []

# دارو


def add_drug(name, mass, num, d_type, time):
    global drugs
    y = {"name": name, "number": num,
         "mass": mass, "type": d_type, "time": time}
    drugs.append(y)


add_drug("name", 20, 2, 'n', '20:13')
print(str(drugs))


# ارزیابی وضعیت روان
mood = 'تحریک پذیر'
Illusion = 'شنوایی'
delusion = 'گزند و آسیب'
suicidalthoughts = 'دارد'
psychomotor = 'کاتاتون'
Illusion2 = True
ratespeech = 'پرحرف'
speedspeech = 'کند'
contentspeech = 'سالاد خوشمزه کلمات'
tonespeech = 'طبیعی'
affection = 'متناسب'
eyecontact = True
# تغذیه
weight = 50
height = 100
bmi = weight+height
eat = 'غذا را کامل کوفت کرد'
diet = 'وگان'
# علائم حیاتی
pain = True
bp = 10
p = 1
r = 3
spo2 = 90
t = 90
# شرح
moredetails = 'بیمار روانی مشکل روانی دیوانه و دیوانه و دیوانه !!!'

response = (supabase.table(table).insert(
    {"time": time, "writer": writer, "mood": mood, "Illusion": Illusion, "suicidalthoughts": suicidalthoughts, "psychomotor": psychomotor, "Illusion2": Illusion2, "ratespeech": ratespeech, "speedspeech": speedspeech, "contentspeech": contentspeech, "tonespeech": tonespeech, "affection": affection, "eyecontact": eyecontact, "weight": weight, "height": height, "bmi": bmi, "eat": eat, "diet": diet, "drugs": str(drugs), "pain": pain, "bp": bp, "p": p, "r": r, "spo2": spo2, "t": t, "moredetails": moredetails})).execute()
