import json
def TestParameter(NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,Dati):
    TestGuiliano = '{"NomeTest": %s,"data":%s,"Articolo":%s,"NodoRasp":%s, "DescrizioneIngresso": %s,"BitQuantiz":%s ,"NumeroCiclo":%s,"BandaFiltro" :%s,"FrequenzadiCampionamento",NumeroCampioni": %s,"ERRORI":%s, "Dati": []}'%(NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori
    Dati_dict = json.loads(TestGuiliano)
    print(Dati_dict)                                                                                                                                                                                                                               

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print( person_dict)

# Output: ['English', 'French']
print(person_dict['languages'])


with open('aaa.json') as f:
  data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
print(data)






with open("aaa.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

product = jsonObject['name']
overall = jsonObject['languages']
#text = jsonObject['text']

print(product)
print(overall)
#print(text)




io = open("in.json","r")
string = io.read()
# json.loads(str)
dictionary = json.loads(string)

# or one-liner
# dictionary = json.loads(open("in.json","r").read())

print(dictionary)


json_data = {
    "product":"Python book",
    "overall":"4.0",
    "text":"Nice book"
}

with open('writed_json.json', 'w') as jsonFile:
    json.dump(json_data, jsonFile)
    jsonFile.close()
