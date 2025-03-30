# TODO adding drug to program
drugs = []


def add_drug():
    global drugs
    drugname = "استامینوفن"
    drugmass = 12
    drugnum = 1
    drugtype = "local"
    drugtime = "12:31"
    y = {"name": drugname, "number": drugnum,
         "mass": drugmass, "type": drugtype, "time": drugtime}
    drugs.append(y)


add_drug()
print(str(drugs))
