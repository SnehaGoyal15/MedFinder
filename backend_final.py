from flask import Flask, render_template, request
import csv
from collections import defaultdict
import heapq

app = Flask(_name_)

class CheapMedicine:
    def _init_(self, name, salt, price, unit_size):
        self.name = name
        self.salt = salt
        self.price = float(price)
        self.unit_size = unit_size

    def _lt_(self, other):
        return self.price < other.price

def to_lower(s):
    return s.lower()

def split(s, delimiter):
    return s.split(delimiter)

def load_allergy_data(filename):
    allergy_map = defaultdict(set)
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if len(row) < 2:
                continue
            allergy = to_lower(row[0])
            meds = split(row[1], '|')
            for med in meds:
                allergy_map[allergy].add(to_lower(med))
    return allergy_map

def load_medicine_data(filename):
    med_data = []
    with open(filename, newline='', encoding='utf-8') as med_file:
        reader = csv.reader(med_file)
        next(reader)
        for row in reader:
            if row:
                med_data.append(row)
    return med_data

def search_medicine(medicine_name, allergies, allergy_map, med_data):
    results = []
    warnings = []
    allergies = [to_lower(a.strip()) for a in allergies if a.strip()]
    medicine_name = to_lower(medicine_name)

    for row in med_data:
        if len(row) < 11:
            continue
        med_name = row[1]
        med_name_lower = to_lower(med_name)
        if medicine_name in med_name_lower:
            excluded = any(med_name_lower in allergy_map.get(allergy, set()) for allergy in allergies if allergy != "none")
            if excluded:
                warnings.append(f"'{med_name}' is a possible match but was excluded due to selected allergies.")
                continue

            med_info = {
                "name": row[1],
                "unit": row[2],
                "price": row[3],
                "salts": row[6],
                "effects": row[16] if len(row) > 16 else "Not available",
                "alternatives": []
            }

            cheap_names = split(row[7], '|')
            cheap_salts = split(row[8], '|')
            cheap_prices = split(row[9], '|')
            cheap_units = split(row[10], '|')

            cheap_list = []
            for i in range(len(cheap_names)):
                try:
                    cm = CheapMedicine(cheap_names[i], cheap_salts[i], cheap_prices[i], cheap_units[i])
                    heapq.heappush(cheap_list, cm)
                except Exception:
                    continue

            while cheap_list:
                c = heapq.heappop(cheap_list)
                med_info["alternatives"].append({
                    "name": c.name,
                    "salts": c.salt,
                    "price": c.price,
                    "unit_size": c.unit_size
                })

            results.append(med_info)

    return results, warnings

# Load once
allergy_map = load_allergy_data("grouped_allergies_medicines_salts_CORRECTED.csv")
med_data = load_medicine_data("hashed_med+allergy_separated.csv")

allergy_list = [
    "Allergic rash risk", "Allergic reaction risk", "Allergy risk(injection site)",
    "Cephalosphorin allergy", "Liver toxicity and allergy risk", "NSAID allergy",
    "Penicillin allergy", "Stevens johnson syndrome", "Sulfa allergy",
    "Sulpha allergy with combination", "Tetracycline allergy", "Topical allergy risk"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        medicine = request.form.get('medicine', '')
        allergies = request.form.getlist('allergies')
        results, warnings = search_medicine(medicine, allergies, allergy_map, med_data)
        return render_template('find.html', results=results, warnings=warnings, allergy_list=allergy_list)
    return render_template('find.html', results=None, warnings=None, allergy_list=allergy_list)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if _name_ == "_main_":
    app.run(debug=True)
