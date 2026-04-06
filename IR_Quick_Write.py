# IR_Quick_Write.py

class ResidentAssistant:
    role = "Residential Staff"
    
    def __init__(self, first, last, ID, college, gen):
        self.firstName = first
        self.lastName = last
        self.SID = ID
        self.college = college
        self.gender = gen
        self.pronouns = setPronouns(self.gender)

    def fullName(self):
        return f"{self.firstName} {self.lastName}"


class Respondent:
    role = "Resident"
    
    def __init__(self, first, last, ID, gen):
        self.firstName = first
        self.lastName = last
        self.SID = ID
        self.gender = gen
        self.pronouns = setPronouns(self.gender)

    def fullName(self):
        return f"{self.firstName} {self.lastName}"

class UnidentifiedRespondent:
    role = "Resident"

    def __init__(self, desc):
        self.description = desc

class Complaintant:
    pass

class Witness:
    pass

def setPronouns(gender):
    match gender.lower():
        case "male":
            return {"personal": "he", "objective": "him", "possessive": "his"}
        case "female":
            return {"personal": "she", "objective": "her", "possessive": "her"}
        case _: #non-binary, other, etc.
            return {"personal": "they", "objective": "them", "possessive": "their"}

def checkID(who):
    while True:
        print(who, end=" ")
        if who == "Respondent's":
            SID = str(input("student ID: (Enter \"N/A\" if the Respondent is not a UCSC student.)\n")).strip()
        else:
            SID = str(input("student ID:\n")).strip()
        if SID == "N/A":
            SID = "Not a UCSC student"
            return SID
        if not SID.isnumeric():
            print("ERROR: Student ID should only have numeric characters.")
            continue
        elif len(SID) != 7:
            print("ERROR: Student ID should be 7 digits long, not", len(SID), end="")
            print(".")
            continue
        return SID

def checkCollege(who):
    while True:
        print(who, end=" ")
        col = input("college housing unit:\n").title().strip()
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
            print("ERROR: Invalid day. Must be an integer between 1-31.")
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
        if not (hh.isdigit() and mm.isdigit()):
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

def standardath(num):
    match int(num) % 10:
        case 1:
            return "st"
        case 2:
            return "nd"
        case 3:
            return "rd"
        case _:
            return "th"

validCollegeHousing = ("Village", "Delaware", "Stevenson", "Cowell", "Crown", "Merrill",
                       "College Nine", "College 9", "C9", "John R. Lewis", "John R Lewis", "Jrl",
                       "Kresge", "Porter", "Redwood Grove", "Rachel Carson", "Rachel Carson College", "RCC", "Oakes")
validGender = ("male", "female", "nonbinary", "non-binary", "non binary", "other")
validWeekDay = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
validMonth = ("January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December")

raList = []
rspList = []
unRspList = []

print("=== Basic policy violation IR generator ===")

while True:
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
    
    # How many RAs?
    print("")
    while True:
        raCount = input("How many RAs addressed the incident?\n")
        if not raCount.isdigit():
            print("ERROR: Quantity must be numeric.")
            continue
        elif int(raCount) <= 0:
            print("ERROR: Quantity must be at least 1.")
            continue
        else:
            raCount = int(raCount)
            print("Let's get the info of all the RAs who helped out, starting with the one who led the interaction.")
            break

    # RAs' info
    for i in range(raCount):
        raFirstName = input("RA's FIRST name:\n").title()
        raLastName = input("RA's LAST name:\n").title()
        raSID = "(" + checkID("RA's") + ")"
        raCollege = checkCollege("RA's")
        raGender = checkGender("RA's")

        newRA = ResidentAssistant(raFirstName, raLastName, raSID, raCollege, raGender) # Create new instance of RA
        raList.append(newRA) # Append instance of RA as list item
        print(f"{i+1}{standardath(i+1)} RA's info added!", end=" ")
        if not i+1 >= raCount:
            print(f"Onto the {i+2}{standardath(i+2)} RA...")

    # How many identified Respondents?
    print("")
    while True:
        rspCount = input("How many respondents at the incident were FULLY IDENTIFIED?\n")
        if not rspCount.isdigit():
            print("ERROR: Quantity must be numeric.")
            continue
        elif int(rspCount) <= 0:
            print("Zero??? Damn okay. Moving on then.")
            break
        else:
            rspCount = int(rspCount)
            print("Let's get the info of all the identified respondents present at the scene.")
            break

    # Identified Respondents' info
    for i in range(rspCount):
        if rspCount <= 0:
            break
        rspFirstName = input("Respondent's FIRST name:\n").title()
        rspLastName = input("Respondent's LAST name:\n").title()
        rspSID = "(" + checkID("Respondent's") + ")"
        rspGender = checkGender("Respondent's")

        newRSP = Respondent(rspFirstName, rspLastName, rspSID, rspGender) # Create new instance of respondent
        rspList.append(newRSP) # Append instance of respondent as list item
        print(f"{i+1}{standardath(i+1)} Respondent's info added!", end=" ")
        if not i+1 >= rspCount:
            print(f"Onto the {i+2}{standardath(i+2)} Respondent...")

    # How many unidentified Respondents?
    print("")
    while True:
        unRspCount = input("How many respondents at the incident were NOT fully identified?\n")
        if not unRspCount.isdigit():
            print("ERROR: Quantity must be numeric.")
            continue
        elif int(unRspCount) <= 0:
            print("Zero??? Damn okay. Moving on then.")
        else:
            unRspCount = int(unRspCount)
            print("Let's get a physical description of all the unidentified Respondents.")
            break

    # Unidentified Respondents' descriptions
    for i in range(unRspCount):
        if unRspCount <= 0:
            break
        unRspDescription = input("Respondent's physical description:\n")
        
        newUnRsp = UnidentifiedRespondent(unRspDescription) # Create
        unRspList.append(newUnRsp) # Append
        print(f"{i+1}{standardath(i+1)} unidentified Respondent's info added!", end=" ")
        if not i+1 >= unRspCount:
            print(f"Onto the {i+2}{standardath(i+2)} unidentified Respondent...")

    # Compliance
    print("")
    while True:
        comply = str(input("Did ALL Respondents comply with ALL the RA's instructions? (Y/N)\n"))
        if comply.upper() == "N":
            while True:
                instruction = input("Which instruction did any of the Respondents not comply with?\n"
                      "[1] Substance disposal\n"
                      "[2] Identification\n"
                      "[3] Both\n").strip()
                if instruction not in ["1", "2", "3",]:
                    print("ERROR: Invalid input.")
                    continue
                match instruction:
                    case "1":
                        complyDisposal = False
                        complyIdentify = True
                    case "2":
                        complyDisposal = True
                        complyIdentify = False
                    case "3":
                        complyDisposal = False
                        complyIdentify = False
                break
            break
        elif comply.upper() == "Y":
            complyDisposal = True
            complyIdentify = True
            break
        else:
            print("ERROR: Invalid response.")
            continue

    # Last minute assignments
    totalRsp = len(rspList) + len(unRspList)
    leadingRA = raList[0]
    
    print("GENERATING INCIDENT REPORT...")
    print("\n")
    print("=== Here is your incident report ===")
    
    # Print process
    print(f"This incident report documents {incident} {location}\n")
    print(f"On {weekday}, {month} {day}, {year}, at approximately {startTime}, "
          f"Resident Assistant (RA) {leadingRA.fullName()} {leadingRA.SID} "
          f"observed {totalRsp} individuals {location} engaging in {incident}.") # TODO special print cases for singular vs plurals
    print("")
    
    print(f"RA {leadingRA.lastName} introduced {leadingRA.pronouns['objective']}self as a {leadingRA.college} RA, "
          f"informed the individuals of the policy violation, "
          f"and instructed the individuals to dispose of the substance.", end=" ")
    if complyDisposal == True:
        print(f"All individuals complied with RA {leadingRA.lastName}'s instruction and disposed of the substance.")
    elif complyDisposal == False: 
        print(f"The individuals did not comply with RA {leadingRA.lastName}'s instruction to dispose of the substance.")
    print("")
    
    print(f"RA {leadingRA.lastName} instructed the individuals to provide identification.")
    if complyIdentify == True:
        print(f"All individuals complied with RA {leadingRA.lastName}'s instruction and provided identification.")
    elif complyIdentify == False: 
        print(f"The individuals did not comply with RA {leadingRA.lastName}'s instruction to dispose of the substance.")
    print("")
    
    print("The following individuals were identified:")
    for rsp in rspList:
        print(f"- {rsp.fullName()} {rsp.SID}")
    print("")

    print("The following individuals were not identified:")
    for i in range(len(unRspList)):
        print(f"- Individual #{i+1} physical description: {unRspList[i].description}")
    print("")

    print(f"The interaction concluded at approximately {endTime}.\n")
    print("No additional incidents were observed at the time of this report.\n")
    print("End of report.\n")

    print("=== ===")
    cont = input("Write another incident report? (Y/N)\n")
    if cont.upper() == "Y":
        raList = []
        rspList = []
        unRspList = []
        continue
    else:
        print("PROGRAM TERMINATED")
        exit()
