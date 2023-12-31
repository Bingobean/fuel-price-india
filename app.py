import requests
from bs4 import BeautifulSoup
import datetime
import json
from flask import Flask, request, render_template

app = Flask(__name__)

session = requests.Session()
session.verify = False

FUEL_TYPES = ["PETROL","DIESEL"]

STATES = {
            "AN":["nicobar","north-and-middle-andaman","south-andaman"],
            "AP":["anantapur","chittoor","cuddapah","east-godavari","guntur","krishna","kurnool","nellore","prakasam","srikakulam","vishakhapatnam","vizianagaram","vizianagaram","west-godavari"],
            "AR":['changlang','dibang-valley','east-khameng', 'east-siang', 'lohit', 'longding', 'lower-dibang-valley', 'lower-subansiri', 'namsai', 'papumpare', 'tawang', 'tirap', 'upper-siang', 'upper-sibansiri', 'west-kameng', 'west-siang'],
            "AS":['baksa', 'barpeta', 'biswanath', 'bongaigaon', 'cachar', 'charaideo', 'chirang', 'darrang', 'dhemaji', 'dhuburi', 'dibrugarh', 'dima-hasao', 'goalpara', 'golaghat', 'hailakandi', 'hojai', 'jorhat', 'kamrup', 'kamrup-metro', 'karbi-anglong', 'karimganj', 'kokrajhar', 'lakhimpur', 'majuli', 'morigaon', 'nagaon', 'nalbari', 'sibsagar', 'sonitpur', 'tinsukia', 'udalguri', 'west-karbi-anglong'],
            "BR":['araria', 'arwal', 'aurangabad', 'banka', 'begusarai', 'bhagalpur', 'bhojpur', 'buxar', 'darbhanga', 'east-champaran', 'gaya', 'gopalganj', 'jahanabad', 'jamui', 'kaimur', 'katihar', 'khagaria', 'kishanganj', 'luckeesarai', 'madhepura', 'madhubani', 'munger', 'muzaffarpur', 'nalanda', 'nawada', 'patna', 'purnia', 'rohtas', 'saharsa', 'samastipur', 'saran', 'sewan', 'sheikhpura', 'sheohar', 'sitamarhi', 'supaul', 'vaishali', 'west-champaran'],
            "CH":["chandigarh"],
            "CG":['balod', 'balodabazar', 'balrampur', 'bastar', 'bemetara', 'bijapur', 'bilaspur', 'dantewada', 'dhamtari', 'durg', 'gariyaband', 'janjgir', 'jashpur', 'kanker', 'kawardha', 'kondagaon', 'korba', 'koria', 'mahasamund', 'mungeli', 'raigarh', 'raipur', 'rajnandgaon', 'sukma', 'surajpur', 'surguja'],
            "DH":["silvassa"],
            "DD":["daman","diu"],
            "DL":['central-delhi', 'delhi-shahdara', 'east-delhi', 'new-delhi', 'north-delhi', 'north-east-delhi', 'north-west-delhi', 'south-delhi', 'south-east-delhi', 'south-west-delhi', 'west-delhi'],
            "GA":["north-goa","south-goa"],
            "GJ":['ahmedabad', 'amreli', 'anand', 'aravalli', 'banas-kantha', 'bharuch', 'bhavnagar', 'botad', 'chhotaudepur', 'dahod', 'devbhumi-dwarka', 'gandhi-nagar', 'gir-somnath', 'jamnagar', 'junagadh', 'kheda', 'kutch', 'mahisagar', 'mehsana', 'morbi', 'narmada', 'navsari', 'panch-mahal', 'patan', 'porbander', 'rajkot', 'sabar-kantha', 'surat', 'surendranagar', 'tapi', 'the-dangs', 'vadodara', 'valsad'],
            "HR":['ambala', 'bhiwani', 'charki-dadri', 'faridabad', 'fatehabad', 'gurgaon', 'hisar', 'jhajjar', 'jind', 'kaithal', 'karnal', 'kurukshetra', 'mahendragarh', 'mewat', 'palwal', 'panchkula', 'panipat', 'rewari', 'rohtak', 'sirsa', 'sonipat', 'yamunanagar'],
            "HP":['bilaspur', 'chamba', 'hamirpur', 'kangra', 'kinnaur', 'kullu', 'lahul-spiti', 'mandi', 'shimla', 'sirmaur', 'solan', 'una'],
            "JK":['anantnag', 'badgam', 'bandipora', 'baramullah', 'doda', 'ganderbal', 'jammu', 'kargil', 'kathua', 'kishtwar', 'kulgam', 'kupwara', 'leh', 'poonch', 'pulwama', 'rajouri', 'ramban', 'reasi', 'samba', 'shopian', 'srinagar', 'udhampur'],
            "JH":['bokaro', 'chatra', 'deogarh', 'dhanbad', 'dumka', 'east-singhbhum', 'garhwa', 'giridih', 'godda', 'gumla', 'hazaribagh', 'jamtara', 'khunti', 'koderma', 'latehar', 'lohardaga', 'pakur', 'palamau', 'ramgarh', 'ranchi', 'sahibganj', 'saraikela-kharasawan', 'simdega', 'west-singhbhum'],
            "KA":['bagalkot', 'bangalore', 'bangalore-rural', 'belgaum', 'bellary', 'bidar', 'bijapur', 'chamrajnagar', 'chikkaballapura', 'chikmagalur', 'chitradurga', 'dakshin-kannad', 'davangere', 'dharwad', 'gadag', 'gulbarga', 'hassan', 'haveri', 'kodagu', 'kolar', 'koppal', 'mandya', 'mysore', 'raichur', 'ramanagara', 'shimoga', 'tumkur', 'udupi', 'uttar-kannad', 'yadgir'],
            "KL":['alappuzha', 'ernakulam', 'idukki', 'kannur', 'kasaragod', 'kollam', 'kottayam', 'kozhikode', 'malappuram', 'palakkad', 'pathananthitta', 'thiruvananthapuram', 'thrissur', 'wayanad'],
            "MP":['agar-malwa', 'alirajpur', 'anupur', 'ashoknagar', 'badwani', 'balaghat', 'betul', 'bhind', 'bhopal', 'burhanpur', 'chhatarpur', 'chhindware', 'damoh', 'datia', 'dewas', 'dhar', 'dindori', 'guna', 'gwalior', 'harda', 'hoshangabad', 'indore', 'jabalpur', 'jahbua', 'katni', 'khandwa', 'khargone', 'mandla', 'mandsaur', 'morena', 'narsimhapur', 'neemach', 'panna', 'raisen', 'rajgarh', 'ratlam', 'rewa', 'sagar', 'satna', 'sehore', 'seoni', 'shahdol', 'shajapur', 'sheopur', 'shivpuri', 'sidhi', 'singrauli', 'tikamgarh', 'ujjain', 'umaria', 'vidisha'],
            "MH":['ahmadnagar', 'akola', 'amravati', 'aurangabad', 'bhandara', 'bid', 'buldhana', 'chandrapur', 'dhule', 'gadchiroli', 'gondia', 'greater-mumbai', 'hingoli', 'jalgaon', 'jalna', 'kolhapur', 'latur', 'mumbai-city', 'nagpur', 'nanded', 'nandurbar', 'nashik', 'osmanabad', 'palghar', 'parbhani', 'pune', 'raigarh', 'ratnagiri', 'sangli', 'satara', 'sindhudurg', 'solapur', 'thane', 'wardha', 'washim', 'yavatmal'],
            "MN":['bishnupur', 'chandel', 'churachandpur', 'east-imphal', 'jiribam', 'kakching', 'kangpokpi', 'noney', 'pherzawl', 'senapati', 'tamenglong', 'tengnoupal', 'thoubal', 'ukhrul', 'west-imphal'],
            "ML":['east-garo-hills', 'east-jaintia-hills', 'east-khasi-hills', 'jaintia-hills', 'north-garo-hills', 'ri-bhoi', 'south-garo-hills', 'southwest-khasi-hils', 'west-garo-hills', 'west-khasi-hills'],
            "MZ":['aizawl', 'champhai', 'kolasib', 'lawngtlai', 'lunglei', 'mamit', 'saiha', 'serchhip'],
            "NL":['dimapur', 'kiphere', 'kohima', 'longleng', 'mokokchung', 'mon', 'peren', 'phek', 'tuensang', 'wokha', 'zunheboto'],
            "OR":['angul', 'baleshwar', 'bargarh', 'bhadrak', 'bolangir', 'boudh', 'cuttack', 'deogarh', 'dhenkanal', 'gajapati', 'ganjam', 'jagatsinghpur', 'jajpur', 'jharsuguda', 'kalahandi', 'kandhamal', 'kendrapara', 'keonjhar', 'khordha', 'koraput', 'malkangiri', 'mayurbhanj', 'nabarangapur', 'nayagarh', 'nuaparha', 'puri', 'rayagada', 'sambalpur', 'sonapur', 'sundargarh'],
            "PY":['karaikal', 'mahe', 'pondicherry', 'yanam'],
            "PB":['amritsar', 'barnala', 'bathinda', 'faridkot', 'fatehgarh-sahib', 'fazilka', 'firozpur', 'gurdaspur', 'hoshiarpur', 'jalandhar', 'kapurthala', 'ludhiana', 'mansa', 'moga', 'muktsar', 'pathankot', 'patiala', 'rupnagar', 'sangrur', 'sas-nagar', 'shd-bhagat-singh-ngr', 'tarn-taran'],
            "RJ":['ajmer', 'alwar', 'banswara', 'baran', 'barmer', 'bharatpur', 'bhilwara', 'bikaner', 'bundi', 'chittaurgarh', 'churu', 'dausa', 'dhaulpur', 'dungarpur', 'ganganagar', 'hanumangarh', 'jaipur', 'jaisalmer', 'jalor', 'jhalawar', 'jhunjhunun', 'jodhpur', 'karauli', 'kota', 'nagaur', 'pali', 'pratapgarh', 'rajsamand', 'sawaimadhopur', 'sikar', 'sirohi', 'tonk', 'udaipur'],
            "SK":['east-district', 'north-district', 'south-district', 'west-district'],
            "TN":['ariyalur', 'chennai', 'coimbatore', 'cuddalore', 'dharmapuri', 'dindigul', 'erode', 'kanchipuram', 'kanniyakumari', 'karur', 'krishnagiri', 'madurai', 'nagapattinam', 'namakkal', 'nilgiris', 'perambalur', 'pudukkottai', 'ramanathapuram', 'salem', 'sivaganga', 'teni', 'thanjavur', 'thiruvarur', 'tiruchchirappalli', 'tirunelveli', 'tirupur', 'tiruvallur', 'tiruvannamalai', 'tuticorin', 'vellore', 'viluppuram', 'virudunagar'],
            "TG":['adilabad', 'bhadradri-kothagudem', 'hyderabad', 'jagitial', 'jangaon', 'jayashankar-bhupalpa', 'jogulamba-gadwal', 'kamareddy', 'karim-nagar', 'khammam', 'komram-bheem-asifaba', 'mahabubabad', 'mancherial', 'medak', 'medchal-malkajgiri', 'mehabubnagar', 'mulugu', 'nagarkurnool', 'nalgonda', 'narayanpet', 'nirmal', 'nizamabad', 'peddapalli', 'rajanna-sircilla', 'rangareddi', 'sangareddy', 'siddipet', 'suryapet', 'vikarabad', 'wanaparthy', 'warangal', 'warangal-rural', 'yadadri-bhuvanagiri'],
            "TR":['dhalai', 'gomati', 'khowai', 'north-tripura', 'sepahijhala', 'south-tripura', 'unakoti', 'west-tripura'],
            "UP":['agra', 'aligarh', 'allahabad', 'ambedkarnagar', 'amethi-csm-nagar', 'amroha', 'auraiya', 'azamgarh', 'baghpat', 'bahraich', 'ballia', 'balrampur', 'banda', 'barabanki', 'bareilly', 'basti', 'bijnor', 'budaun', 'bulandshahr', 'chandauli', 'chitrakut', 'deoria', 'etah', 'etawah', 'faizabad', 'farrukkhabad', 'fatehpur', 'firozabad', 'gautam-budh-nagar', 'ghaziabad', 'ghazipur', 'gonda', 'gorakhpur', 'hamirpur', 'hapur', 'hardoi', 'hathras', 'jalaun', 'jaunpur', 'jhansi', 'kannuaj', 'kanpur-rural', 'kanpur-urban', 'kashi-ram-nagar', 'kaushambi', 'kushinagar', 'lakhimpur', 'lalitpur', 'lucknow', 'maharajganj', 'mahoba', 'mainpuri', 'mathura', 'maunathbhanjan', 'meerut', 'mirzapur', 'moradabad', 'muzaffarnagar', 'pilibhit', 'pratapgarh', 'rae-bareli', 'rampur', 'saharanpur', 'sambhal', 'sant-kabir-nagar', 'sant-ravi-nagar', 'shahjahanpur', 'shamli', 'shravasti', 'sidharthnagar', 'sitapur', 'sonbhadra', 'sultanpur', 'unnao', 'varanasi'],
            "UR":['almora', 'bageshwar', 'chamoli', 'champawat', 'dehradun', 'haridwar', 'nainital', 'pauri', 'pithoragarh', 'rudraprayag', 'tehri-garhwal', 'udham-singh-nagar', 'uttarkashi'],
            "WB":['alipurduar', 'bankura', 'birbhum', 'cooch-bihar', 'dakshin-dinajpur', 'darjeeling', 'hooghly', 'howrah', 'jalpaiguri', 'jhargram', 'kalimpong', 'kolkata', 'malda', 'murshidabad', 'nadia', 'north-24-parganas', 'paschim-bardhaman', 'paschim-medinipur', 'purba-bardhaman', 'purba-medinipur', 'purulia', 'south-24-parganas', 'uttar-dinajpur']
            }

TOTAL_CITIES = []
for i in STATES:
    for e in STATES[i]:
       TOTAL_CITIES.append(e)

def urlGen(fuelType, CITY_NAME):
    try:
        if(fuelType.upper() == "PETROL"):
            URL_PETROL = f"https://www.ndtv.com/fuel-prices/petrol-price-in-{ CITY_NAME }-city"
            return URL_PETROL
        elif(fuelType.upper() == "DIESEL"):
            URL_DIESEL = f"https://www.ndtv.com/fuel-prices/diesel-price-in-{ CITY_NAME }-city"
            return URL_DIESEL
    except Exception as error:
        print(f"Exception in urlGen:{error}")

def scrapData(fuelType, URL, CITY):
    try:
        fuelData = session.get(URL)

        if(fuelData.status_code != 200):
            print("ERROR RETIVING DATA - E201")
        else:
            html_doc = fuelData.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            fuelPrice = soup.find("span", attrs={'class':'font-b color-blue'}).text.strip().split("₹/L")[0]
            fuelDate = soup.find("h4", attrs={'class':'font-15 color-blue mb-5'}).text.strip().split("Price")[0]
            print(f"Petrol Price:{fuelPrice}")
            print(f"Petrol Date:{fuelDate}")
            fuelPrice = fuelPrice.strip()
            fuelDate = fuelDate.strip()
            fuelDateTime = datetime.datetime.strptime(fuelDate,'%b %d, %Y').strftime('%d/%m/%Y')
            print(fuelDateTime)
            return {
                fuelType:{
                    "date":fuelDateTime,
                    "price":fuelPrice,
                    "currency":"INR",
                    "city":CITY
                }
            }
    except Exception as error:
        print(f"Error:{error}")

@app.route('/', methods=["GET"])
def homeRoute():
    try:
        response = {
            "message":"Welcome to fuel INR API.",
            "API routes": ["/states","/state/<stateCode>","/cities","/price/<city>/<inpType>"],
            "InpTypes":["petrol","diesel"]
        }
        return response, 200
    except Exception as a:
        response = {
            "message":f"Error from /: {e}"
        }
        return response, 503

@app.route("/states", methods=['GET'])
def getStates():
    try:
        return {
            "states":STATES
        }
    except Exception as error:
        print(f"Error in getStates:{error}")
        return {
            "message":f"Error getting states: {e}"
        }, 503

@app.route("/state/<city>", methods=['GET'])
def getCities(city):
    try:
        city = city.upper()
        if city in STATES:
            return {
                "cities":STATES[city]
            }
        else:
            return {
                "message":f"City:{city} not found!"
            }
    except Exception as error:
        print(f"Error in getCities: {error}")
        return {
            "message":f"Error getting state values: {e}"
        }, 503

@app.route("/cities")
def totalCities():
    response = {
        "totalCities":TOTAL_CITIES,
        "numberOfCities":len(TOTAL_CITIES)
    }
    return response, 200
            
@app.route('/price/<city>/<inpType>', methods=["GET"])
def cityWisePrice(city, inpType):
    try:
        if (inpType == None):
            # return "INVALID PARAMETER - E100"
            return {
                    "message":f"INVALID PARAMETER - E100"
                }
        
        elif (inpType != None and inpType.upper() not in FUEL_TYPES):
            # return "INVALID PARAMETER - E101"
            return {
                    "message":f"INVALID PARAMETER - E101 - Wrong fuel type"
                }
        
        elif (city not in TOTAL_CITIES):
            return {
                    "message":f"INVALID PARAMETER - E102 - Incorrect City"
                }
        
        else:
            if (inpType.upper() == "PETROL"):
                inpType = "PETROL"
                data = scrapData(inpType, urlGen(inpType, city), city)
                return data
            if (inpType.upper() == "DIESEL"):
                inpType = "DIESEL"
                data = scrapData(inpType, urlGen(inpType, city), city)
                return data
            if (inpType.upper() == "EV"):
                inpType = "EV"
                # return f"Pending data retival for {inpType}"
                return {
                    "message":f"Pending data retival for {inpType}"
                }
            if (inpType.upper() == "CNG"):
                inpType = "CNG"
                # return f"Pending data retival for {inpType}"
                return {
                    "message":f"Pending data retival for {inpType}"
                }
    except Exception as e:
        print(f"Error in cityWisePrice:{e}")
        return {
            "message":f"Error retrieving data: {e}"
        }, 503

@app.errorhandler(404)
def internal_server_error_404(e):
    response = {
        "message":f"The page you are looking for does not exist 😰",
        "redirect":f"https://fuelinr.vercel.app/"
    }
    print(f"Error in server - 404 :{e}")
    return response, 404

@app.errorhandler(500)
def internal_server_error_500(e):
    print(f"Error in server - 500 :{e}")
    return render_template('500.html'), 500
