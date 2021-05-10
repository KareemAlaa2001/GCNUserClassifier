import re

# file = open("output.txt", "r")

# lines = file.readlines()


# relevantLinesStr = ""
# for i in range(72,79):
#     relevantLinesStr += lines[i].strip()

# lettersremoved = re.sub (r'[A-Za-z):]','', relevantLinesStr)
# commasinsteadofleft = re.sub('\(',',', lettersremoved)
# commasinsteadofleft = re.sub(' 1 ','',commasinsteadofleft)
# print(commasinsteadofleft)

res = [[(0.8111550934667412, 0.012775490073686039), (0.897289972899729, 0.009766965073731176), (0.8519531030420129, 0.006423795528965165)], [(0.492791133040745, 0.043079173381040885), (0.4358974358974359, 0.046115139761363666), (0.4621732829138612, 0.04278487823483633)], [(0.3003168743880818, 0.08581508805870662), (0.10253061224489796, 0.03313409845952692), (0.1511351591885133, 0.04403602721490713)], [(0.679875090585289, 0.027106250902023246), (0.7271892497200448, 0.03813887554515876), (0.702528636150061, 0.02980104794884903)]]

for a in res:
    lst = []
    for i in range(len(a)):
        lst.append(a[i][0])
        lst.append(a[i][1])

    print(lst)

# res = str(res)

# nobracks = re.sub('[()]','', res )

# print(nobracks)