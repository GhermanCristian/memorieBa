import shelve
from constants import TABLE_ENTRIES

def tableInit():
    table = shelve.open("Leaderboards//tables", writeback = True)
    if not ("fast" in table.keys() or "smart" in table.keys()):
        #print ("created new table")
        table["fast"] = [    
            ("Emil Boc", 400000), 
            ("e un tampit", 400010), 
            ("piperalord2000", 500000), 
            ("fifti", 600000), 
            ("connectar", 750000), 
            ("fasole", 800000), 
            ("Drake Gardescu", 850000), 
            ("slabanogu de chimita", 900000), 
            ("Kazi cu k", 950000), 
            ("Dragos Tudorache", 1000000)
        ]
        table["smart"] = [
            ("Emil Boc", 200), 
            ("e un tampit", 201), 
            ("piperalord2000", 275), 
            ("fifti", 300), 
            ("connectar", 325), 
            ("fasole", 350), 
            ("Drake Gardescu", 375), 
            ("slabanogu de chimita", 400), 
            ("Kazi cu k", 425), 
            ("Dragos Tudorache", 450)
        ]
    table.close()

def checkResult(ms, moves):
    table = shelve.open("Leaderboards//tables")
    inside = (ms <= table["fast"][TABLE_ENTRIES - 1][1] or moves <= table["smart"][TABLE_ENTRIES - 1][1])
    table.close()
    return inside

def insertResult(table, name, count):
    index = TABLE_ENTRIES - 1
    
    while index >= 0 and table[index][1] >= count:
        index -= 1
        
    table.insert(index + 1, (name, count))
    del table[TABLE_ENTRIES]

def addResult(name, ms, moves):
    table = shelve.open("Leaderboards//tables", writeback = True)
    
    insertResult(table["fast"], name, ms)
    insertResult(table["smart"], name, moves)
    
    table.close()
    
def resetTable():
    table = shelve.open("Leaderboards//tables")
    
    del table["fast"]
    del table["smart"]
    
    table.close()
