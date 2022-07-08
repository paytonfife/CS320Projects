import json
import csv
import zipfile as z
import io

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            try:
                self.race.add(race_lookup[r])
            except:
                pass
    
    def __repr__(self):
        self.race = list(self.race)
        return f"Applicant('{self.age}', {self.race})"
    
    def lower_age(self):
        age = self.age.replace("<", "")
        age = age.replace(">", "")
        age = age.split("-")
        return int(age[0])
    
    def __lt__(self, other):
        return Applicant.lower_age(self) < Applicant.lower_age(other)

class Loan:
    def __init__(self, fields):
        try:
            self.loan_amount = float(fields["loan_amount"])
        except:
            self.loan_amount = -1
        try:
            self.property_value = float(fields["property_value"]) 
        except:
            self.property_value = -1
        try:
            self.interest_rate = float(fields["interest_rate"])
        except:
            self.interest_rate = -1
            
        applicant_races = []
        for n in range(1, 6):
            string = "applicant_race-" + str(n)
            try:
                applicant_races.append(fields[string])
            except:
                pass
        applicants_list = []
        applicants_list.append(Applicant(fields["applicant_age"], applicant_races))
                               
        if fields["co-applicant_age"] != "9999":
            coapp_races = [] 
            for n in range(1, 6):
                string = "co-applicant_race-" + str(n)
                try:
                    coapp_races.append(fields[string])
                except:
                    pass
            applicants_list.append(Applicant(fields["co-applicant_age"], coapp_races))
                               
        self.applicants = applicants_list

    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        assert (self.interest_rate > 0 and self.loan_amount > 0)
        amt = self.loan_amount
        
        while amt > 0:
            yield amt
            amt += (self.interest_rate/100) * amt
            amt -= yearly_payment
                   
class Bank:
    def __init__(self, name):
        self.loans = []
        
        with open("banks.json") as f:
            data = f.read()
        for i in json.loads(data):
            if i["name"] == name:
                self.name = name
                self.lei = i["lei"]
                
        with z.ZipFile("wi.zip") as zf:
            with zf.open("wi.csv", "r") as file:
                reader = csv.DictReader(io.TextIOWrapper(file, "utf-8"))
                for row in reader:
                    if self.lei == row["lei"]:
                        l = Loan(row)
                        self.loans.append(l)
                        
    def __len__(self):
        return len(self.loans)
    
    def __getitem__(self, value):
        return self.loans[value]
                         
race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}            