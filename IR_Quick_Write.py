# IR_Quick_Write.py

def setPronouns(who, gender):
    match gender.lower():
        case "male":
            who["personal"] = "he"
            who["objective"] = "him"
            who["possessive"] = "his"
        case "female":
            who["personal"] = "she"
            who["objective"] = "her"
            who["possessive"] = "her"
        case _: # non-binary or other
            who["personal"] = "they"
            who["objective"] = "them"
            who["possessive"] = "their"

def checkID(who):
    while True:
        print(who, end=" ")
        SID = str(input("student ID:\n")).strip()
        if not SID.isnumeric():
            print("ERROR: Student ID should only have numeric characters.")
            continue
        elif len(SID) != 7:
            print("ERROR: Student ID should be 7 digits long, not", len(SID), end="")
            print(".")
            continue
        return SID

def checkCollege():
    while True:
        col = input("Your college housing unit:\n").title().strip()
        if col not in validCollegeHousing:
            print("ERROR: Invalid college housing unit. Please double check the spelling and capitalization.")
            continue
        return col

def checkGender(who):
    while True:
        print(who, end=" ")
        gen = input("gender identity for pronoun purposes: (male, female, nonbinary, other)\n").strip()
        if gen.lower() not in validGender:
            print("ERROR: Invalid gender.")
            continue
        return gen

def checkWeekDay():
    while True:
        wd = input("Day of the week:\n").title().strip()
        if wd not in validWeekDay:
            print("ERROR: Invalid day of the week. Please double check spelling.")
            continue
        return wd
    
def checkMonth():
    while True:
        m = input("Month:\n").title().strip()
        if m not in validMonth:
            print("ERROR: Invalid month. Please double check spelling.")
            continue
        return m

def checkDay():
    while True:
        d = input("Day of the month:\n").strip().lstrip("0")
        if not d.isdigit():
            print("ERROR: Invalid day. Input must be numeric.")
            continue
        d = int(d)
        if d not in range(1, 32):
            print("ERROR: Invalid day. Must be an integer between between 1-31.")
            continue
        return d
    
def checkYear():
    while True:
        y = input("Year:\n").strip().lstrip("0")
        if not y.isdigit():
            print("ERROR: Invalid year. Input must be numeric.")
            continue
        y = int(y)
        if y not in range(1965, 10000):
            print("ERROR: Invalid year. Must be an integer between between 1965 and 9999.")
            continue
        return y

def checkTime(when):
    while True:
        t = input(f"Approximate {when} time of encounter: (with AM/PM)\n").strip()
        t = t.split()
        if len(t) != 2 or ":" not in t[0]:
            print("ERROR: Invalid format.")
            continue
        clock, meridiem = t
        meridiem = meridiem.upper().replace(".", "")
        if meridiem not in ("AM", "PM"):
            print("ERROR: Invalid meridiem.")
            continue
        hh, mm = clock.split(":")
        if not (hh.isdigit() or mm.isdigit()):
            print("ERROR: Invalid clock format.")
            continue
        hh = int(hh)
        mm = int(mm)
        if not 1 <= hh <= 12:
            print("ERROR: Hour must be between 1-12.")
            continue
        if not 0 <= mm <= 59:
            print("ERROR: Minute must be between 0-59.")
            continue

        return f"{hh}:{mm:02d} {meridiem}"
        

validCollegeHousing = ("Village", "Delaware", "Stevenson", "Cowell", "Crown", "Merill",
                       "College Nine", "College 9", "C9", "John R. Lewis", "John R Lewis", "Jrl",
                       "Kresge", "Porter", "Redwood Grove", "Rachel Carson", "Rachel Carson College", "RCC", "Oakes")
validGender = ("male", "female", "nonbinary", "non-binary", "non binary", "other")
validWeekDay = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
validMonth = ("January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December")

RAGenderPronoun = {
    "personal": "",
    "objective": "",
    "possessive": ""}
rspGenderPronoun = {
    "personal": "",
    "objective": "",
    "possessive": ""}

print("=== Basic policy violation IR generator ===")

while True:
    # RA info
    raFirstName = input("Your FIRST name:\n").title()
    raLastName = input("Your LAST name:\n").title()
    raSID = "(" + checkID("Your") + ")"
    raCollege = checkCollege()
    raGender = checkGender("Your")
    setPronouns(RAGenderPronoun, raGender)

    # Respondent info
    while True:
        rspIdentified = str(input("Was the respondent fully identified? (Y/N)\n"))
        if rspIdentified.upper() not in ("Y", "N"):
            print("ERROR: Invalid response.")
        else:
            break
    if rspIdentified.upper() == "Y":
        rspFirstName = input("Respondent FIRST name:\n").title()
        rspLastName = input("Respondent LAST name:\n").title()
        rspSID = "(" + checkID("Respondent's") + ")"
        rspGender = checkGender("Respondent's")
        setPronouns(rspGenderPronoun, rspGender)
    elif rspIdentified.upper() == "N":
        rspDescription = input("Respondent physical description: (The individual was described as __[INSERT DESCRIPTION]__.)\n")
        
    # Basic details
    incident = input("Incident type: (smoking, vaping, cannabis, alcohol)\n")
    location = input("Location: (outside Kresge Residence Hall B, in front of Porter Apartment G, etc.)\n")

    # Time
    weekday = checkWeekDay()
    month = checkMonth()
    day = str(checkDay())
    year = str(checkYear())
    
    startTime = checkTime("START")
    endTime = checkTime("END")

    # Compliance
    comply = str(input("Did the individual comply with instructions? (Y/N)\n"))
    print("GENERATING INCIDENT REPORT...")
    print("\n")
    print("=== Here is your incident report ===")
    
    # Print process
    print("This incident report documents", incident, location + ".\n")
    print("On", weekday + ",", month, day + ",", year + ", at approximately", startTime + ",",
          "Resident Assistant", raFirstName, raLastName, raSID, "observed an individual", location, incident + ".",
          "RA", raLastName, "introduced", RAGenderPronoun["objective"] + "self as a", raCollege,
          "RA, informed the individual of the policy violation, and instructed the individual to dispose of the substance.\n")

    print("RA", raLastName, "instructed the individual to provide identification.", end=" ")
    if rspIdentified.upper() == "N":
        print("The individual did not provide identification. The individual was described as", rspDescription + ".\n")
    else:
        print("The individual was identified as Resident", rspFirstName, rspLastName, rspSID + ".\n")

    if comply.upper() == "Y" and rspIdentified.upper() == "Y":
        print("Resident", rspLastName, "complied with RA", raLastName + "'s instructions without resistance or delay.")
    else:
        try:
            print("Resident", rspLastName, "delayed instructions and did not comply with RA", raLastName + "'s instructions.")
        except:
            print("The individual delayed instructions and did not comply with RA", raLastName + "'s instructions.")

    print("The interaction concluded at approximately", endTime + ".\n")
    print("No additional incidents were observed at the time of this report.\n")
    print("End of report.\n")

    print("=== ===")
    cont = input("Write another incident report? (Y/N)\n")
    if cont.upper() == "Y":
        continue
    else:
        print("PROGRAM TERMINATED")
        exit()
