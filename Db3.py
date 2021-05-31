from os import getenv
import pymssql
import pyjson2

#server = getenv("SRVTSTVITARD\SQLEXPRESS")
#server = "SRVTSTVITARD"
#user = "Lab"
#password = "Lab$2021"
#password = getenv("Lab$2021")
#conn = pymssql.connect(server, user, password, "Lab1")
#cursor = conn.cursor()
'''
cursor.execute("""
IF OBJECT_ID('persons', 'U') IS NOT NULL
    DROP TABLE persons
CREATE TABLE persons (
    id INT NOT NULL,
    name VARCHAR(100),
    salesrep VARCHAR(100),
    PRIMARY KEY(id)
)

cursor.executemany(
    "INSERT INTO persons VALUES (%d, %s, %s)",
    [(1, 'John Smith', 'John Doe'),
     (2, 'Jane Doe', 'Joe Dog'),
     (3, 'Mike T.', 'Sarah H.')])
# you must call commit() to persist your data if you don't set autocommit to True
conn.commit()

cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
row = cursor.fetchone()
while row:
    print("ID=%d, Name=%s" % (row[0], row[1]))
    row = cursor.fetchone()
print("fine!")
conn.close()
'''



class db():
    def __init__(self,server="SRVTSTVITARD",database="Lab1",user="Lab",password="Lab$2021",Debug=True):
        self.server=server
        self.database=database
        self.user=user
        self.password=password
        self.conn = pymssql.connect(server, user, password, database)
        self.cursor = self.conn.cursor()
        self.Debug=Debug
        #print(self.conn.,"\n")
        #self.cursor.execute("SELECT version();")
        #record =self.cursor.fetchone()
        #self.sql=""
        print("You are connected into the - ")
        print("Database Init Done")
        
	
    def __del__(self):
        #Closing the connection
        self.conn.close()
    #questa tabella viene creata per definire i parametri dei test
    # attenzione è da cancellare
    def MakeTestParameterTable(self,TableName):
        #self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        #self.cursor = self.conn.cursor()
        if(self.Debug):
            cmd=("DROP TABLE IF EXISTS %s;"%TableName)
            print(cmd)
            self.cursor.execute(cmd) #NON USO IL COMANDO:::: NON CANCELLO
        self.sql =("CREATE TABLE %s(NomeTest CHAR(16),Dataeora CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),NumeroBit INT,Banda INT,FrequenzaCamp INT,TestNr INT);" %TableName)
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
        
    
    def MakeRefTable(self,TableName):
        #self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        #self.cursor = self.conn.cursor()
        if(self.Debug):
            cmd=("DROP TABLE IF EXISTS %s;"%TableName)
            print(cmd)
            self.cursor.execute(cmd) #Debug cancello la tabella per debug
            self.conn.commit()
        self.sql =("CREATE TABLE %s(NomeTest CHAR(16),Dataeora CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),NumeroBit INT,Banda INT,FrequenzaCamp INT,TestNr INT);" %TableName)
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
    '''
        Data=[NomeTest,Data,NomeArticolo,NomeRasp,NumeroBit,Banda,Frequeza,TestNR]
    '''
    def InsertDataInRefTable(self,TableName,NomeTest,Dataeora,Articolo,NomeRaspberry,NumeroBit,Banda,FreqquenzaCampionamento,TestNr):
        #self.sql = ("INSERT INTO %s (NomeTest,Dataeora, NomeArticolo,NomeRaspberry,NumeroBit,Banda,FrequenzaCamp, TestNr) VALUES (%s, %s, %s, %s, %s,%s, %s, %s);"%(TableName,NomeTest,Dataeora,Articolo,NomeRaspberry,NumeroBit,Banda,FreqquenzaCampionamento,TestNr))
        self.sql = ("insert into %s  VALUES('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s');"%(TableName,NomeTest,Dataeora,Articolo,NomeRaspberry,NumeroBit,Banda,FreqquenzaCampionamento,TestNr))
        print(self.sql)
        Numero=self.cursor.execute(self.sql)
        self.conn.commit()
    
    '''
    Tabella fatta per  json
    CREATE TABLE cards (
    id integer NOT NULL,
    board_id integer NOT NULL,
    data jsonb
    );
    attenzione real is float
    '''
    def MakeSignalTable(self,tablename):
        if(self.Debug):
            cmd=("DROP TABLE IF EXISTS %s;"%tablename)
            print(cmd)
            self.cursor.execute(self.sql)
            self.conn.commit()
        self.sql =("CREATE TABLE %s (id integer,len integer ,JSONFILENAME CHAR(1000));" %tablename)

        #self.sql =("CREATE TABLE %s (id integer NOT NULL,len integer ,Arr  REAL);" %tablename)
        #######self.sql=("CREATE TABLE %s(id integer NOT NULL,NomeTest CHAR(16),date CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),DescrizioneIngresso CHAR(16),NumeroBit INT,TestNr INT ,Banda INT,Fc INT,NumeroCampioni INT,ERRORI CHAR(16),Wave jsonb);" %tablename)
        #                              1                  2                 3              4                    5                        6                         7              8           9       10        11                12                  13   
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
        
    #INSERT INTO cards VALUES (1, 1, '{"name": "Paint house", "tags": ["Improvements", "Office"], "finished": true}');
        
    def InsertSignal(self,tablename,filename,idM):
        NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori=pyjson2.TestParameterRd(filename)
        jdata=pyjson2.TestParameterRdForDB(filename)
        index=1
        self.sql = ("insert  into %s VALUES (%d,'%s');"%(tablename,idM,jdata))
        #########self.sql=("INSERT INTO %s VALUES (id,NomeTest CHAR(16),date CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),DescrizioneIngresso CHAR(16),NumeroBit INT,TestNr INT ,Banda INT,Fc INT,NumeroCampioni INT,ERRORI CHAR(16),Wave jsonb) VALUES (%s , %s ,%s, %s, %s, %s,%s, %s, %s,%s,%s,%s,%s);"%(tablename,index,NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori,jdata))
        #                               1                   2                 3             4                     5                      6                             7             8           9      10     11                  12            13                1   2    3   4   5   6  7  8   9   10 11 1213      1      2   3       4     5       6    7                 8        9          10   11   12              13  14     (unO IN PIU PER TABELLA NOME)
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
    # SELECT data->>'name' AS name FROM cards
    
    def GetFieldinJson(self,colonna,tablename):
        #self.sql= ("SELECT data-> '%s' AS name FROM %s;"%(colonna,tablename))
        
        
        self.sql= ("SELECT data-> '%s' FROM %s;"%(colonna,tablename))
        #self.sql="(SELECT * FROM %s WHERE data->>'ERRORI' = 'true');"%tablename
        print(self.sql)
        #self.cursor.execute(self.sql)
        

    
        
    ''' ritorna il numero di riche presenti nella tabella dati '''
    def GetAllFromtable(self,TableName):
        return 
        #Creating a cursor object using the cursor() method
        self.sql=("SELECT * from %s ;"%TableName)
        #Retrieving data
        print(self.sql)
        self.cursor.execute(self.sql)
        #Fetching 1st row from the table
        result = self.cursor.fetchall();
        #rows = cur.fetchall()
        i=0
        for row in result:
            print(row)
            i=i+1
        return i
    '''
        Data=[NomeTest,Data,NomeArticolo,NomeRasp,NumeroBit,Banda,Frequeza,TestNR]
    '''
    def InsertTestParameterInRefTable(self,TableName,NomeTest,datastarttest, NomeArt,Nodo,Numerodibit,Fc,TestID):
        return 
        self.sql = ("INSERT INTO %s (NomeTest,Data, NomeArticolo,NomeRaspberry,NumeroBit,Banda,FrequenzaCamp, TestNr) VALUES (%s, %s, %s, %s, %s,%s, %s, %s);"%(TableName,NomeTest,datastarttest,NomeArt,Nodo,Numerodibit,Fc,Res[6],TestID))
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
        
    def InsertParameterInRefTable(self,TableName,NomeTest,datastarttest, NomeArt,Nodo,Numerodibit,Fc):
        return 
        TestID=self.GetAllFromtable(TableName)
        self.InsertTestParameterInRefTable(self,TableName,NomeTest,datastarttest, NomeArt,Nodo,Numerodibit,Fc,TestID)
        self.conn.commit()
        return TestID
    
       # Doping EMPLOYEE table if already exists.
       #     cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
       #     sql = '''CREATE TABLE EMPLOYEE(
       #     FIRST_NAME CHAR(20) NOT NULL,
       #     LAST_NAME CHAR(20),
       #     AGE INT,
       #     SEX CHAR(1),
       #     INCOME FLOAT)'''
       #  cursor.execute(sql)
       # '''
    '''

    ATTENZIONE QUESTA TABELLA IS quella che mi fa la gestione...dei dati che arrivano dal Analog device
    numero ciclo
    numero di ingresso char(16)
    stato misura char(16)
    Dati Array di float
    '''
    def MakeDataTable(self,TableName):
        #self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        #self.cursor = self.conn.cursor()
        #print(self.conn.get_dsn_parameters(),"\n")
        self.cursor.execute("DROP TABLE IF EXISTS %s;"%TableName)
        self.sql =("CREATE TABLE %s( NUMEROCICLO INT,INGRESSO CHAR(16),STATOMISURA CHAR(16) ,analog float ARRAY[16000]);" %TableName)
        print(self.sql)
        self.cursor.execute(self.sql)
       
    def InsertDataInTable(self,TableName, ciclo,ingresso ,statomisura,analog):
        self.sql = ("INSERT INTO %s (NUMEROCICLO ,INGRESSO, STATIMISURA,analog) VALUES (%s, %s, %s, %s, %s,%s, %s, %s);"%(TableName,ciclo,ingresso,statomisura,analog))
        print(self.sql)
        self.cursor.execute(self.sql)

    def GetAllFromtable(self,TableName):
        #Creating a cursor object using the cursor() method
        self.sql=("SELECT * from %s ;"%TableName)
        #Retrieving data
        print(self.sql)
        self.cursor.execute(self.sql)
        #Fetching 1st row from the table
        result = self.cursor.fetchall();
        #rows = cur.fetchall()
        for row in result:
            print(row)

        #print(result)
        return result

    def GetoneFromtable(self,TableName):
        #Setting auto commit false
        #Creating a cursor object using the cursor() method
        self.sql="SELECT * from %s;"%TableName
        #Retrieving data
        self.cursor.execute(self.sql)
        #Fetching 1st row from the table
        result = self.cursor.fetchone();
        print(result)
        return result

    


    def DeleteData(self,Data,Soglia):
        pass
        #cursor.execute('''DELETE FROM EMPLOYEE WHERE AGE > 25''')
    
    def InsertData(self,Data):
        pass
        #INSERT INTO exampleTable(exampleArray[3]) VALUES('{1, 2, 3}');
        #INSERT INTO contacts (name, phones)
        #VALUES('John Doe',ARRAY [ '(408)-589-5846','(408)-589-5555' ]);





   
def main():
    print("Start")
    D=db()
    TableName="LabTests"
    D.MakeRefTable(TableName)
    D.InsertDataInRefTable(TableName=TableName,NomeTest="Test1",Dataeora="111",Articolo="ART1",NomeRaspberry="RA1",NumeroBit=16,Banda=4000,FreqquenzaCampionamento=16000,TestNr=1)
    D.MakeSignalTable("JT2") #creo la JSON TABLE
    #!!!! Non Usato come quello sopra D.MakeTestParameterTable(TableName)
        
    return
    D.MakeJsonTable("JTN2")# test name
    data=plotfi.findjsonfile('demo*.json','/home/novello/NWZep/DB')
    print(data)
    i=10000
    while(i<len(data)):
        ####a=pyjson2.TestParameterRd(data[i])
        ####print("json====>>>>>",a)
        D.InsertJsonRawInTable("JTN2",data[i])
        i=i+1
    print(D.GetFieldinJson("NomeTest","JTN2"))
    #D.GetAllFromtable("JT")
    D.GetoneFromtable("JTN2")
    #D.GetAllFromtable("JT")
    #D.MakeRefTable(TableName="AutecTestType")
    #D.InsertDataInRefTable(TableName="AutecTestType",Res=[1,2,3,4,5,6,7,8])
    #D.InsertDataInRefTable(TableName="AutecTestType",Res=[10,11,11,11,11,11,11,11])
    #D.GetAllFromtable(TableName="AutecTestType")
    #D.GetoneFromtable(TableName="AutecTestType")
    #D.MakeDataTable(TableName="AAAA")
    global ts
    k=0
    #print(Py.Up())
    #print(Py.Down())
    while(k<10000000):
        print(" k is",k)
        time.sleep(1)
        if((k%10)==0):
            ts=k
        k=k+1
        #print("Ciclo is",k)
    print("Fine")
     #######
if __name__ == '__main__':
    main()
