import psycopg2
import time
import json
import pyjson2
import plotfi
#
#sudo -u postgres psql
#postgres=# create database mydb;
#postgres=# create user myuser with encrypted password 'mypass';
#postgres=# grant all privileges on database mydb to myuser;
'''
connection = psycopg2.connect(
        user = "postgres",
        password = "novello",
        host = "10.16.1.208",
        port = "5432",
        database = "novello"
    )
'''

class db():
    def __init__(self,hosts="10.16.1.166",database="lab1",user='novello',password='novello',port=5432):
        self.hosts=hosts
        self.database=database
        self.user=user
        self.password=password
        self.port=port
        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        self.cursor = self.conn.cursor()
        print(self.conn.get_dsn_parameters(),"\n")
        self.cursor.execute("SELECT version();")
        record =self.cursor.fetchone()
        self.sql=""
        print("You are connected into the - " ,record)
        print("Database Init Done")
        
	
    def __del__(self):
        #Closing the connection
        self.conn.close()

    def SaveA2d(self,idn,data):
        try:
            binary = psycopg2.Binary(data)
            self.cursor.execute("INSERT INTO DataTable(id,canale,bits, data) VALUES (%d, %s)", i,(binary,) )
            self.conn.commit()
        except:
            if self.conn:
                conn.rollback()
                print('Error ')    
        finally:
            print(" finita connessione con scrittura")
    '''
    Tabella fatta per  json
    CREATE TABLE cards (
    id integer NOT NULL,
    board_id integer NOT NULL,
    data jsonb
    );
    '''
    def MakeJsonTable(self,tablename):
        self.sql =("CREATE TABLE %s(id integer NOT NULL,board_id integer NOT NULL,data jsonb);" %tablename)
        #######self.sql=("CREATE TABLE %s(id integer NOT NULL,NomeTest CHAR(16),date CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),DescrizioneIngresso CHAR(16),NumeroBit INT,TestNr INT ,Banda INT,Fc INT,NumeroCampioni INT,ERRORI CHAR(16),Wave jsonb);" %tablename)
        #                              1                  2                 3              4                    5                        6                         7              8           9       10        11                12                  13   
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
        
    #INSERT INTO cards VALUES (1, 1, '{"name": "Paint house", "tags": ["Improvements", "Office"], "finished": true}');
        
    def InsertJsonRawInTable(self,tablename,filename,idM):
        NomeTest,data,Articolo,Nodo,DescrizIngresso,BitQuant,NumeroCiclo,Banda,Fc,NumeroCampioni,Errori=pyjson2.TestParameterRd(filename)
        jdata=pyjson2.TestParameterRdForDB(filename)
        index=1
        self.sql = ("INSERT INTO %s VALUES (%d,'%s');"%(tablename,idM,jdata))
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
        

    '''
    CREATE TABLE table_name(
    column1 datatype,
    column2 datatype,
    column3 dataty
    .....
    columnN datatype,
    );
    
    Example
    Following example creates a table with name CRICKETERS in PostgreSQL.

    postgres=# CREATE TABLE TestsGiuliano (
    NomeTest VARCHAR(16),
    DataeOra VARCHAR(16),
    NomeArticolo VARCHAR(16),
    NomeRaspberry VARCHAR(16),
    NumeroBitDiQ  INT,
    Banda INT,
    FrequenzaCamp INT,
    TestNumber INT;

    CREATE TABLE
    Test Num
    postgres=#
    '''
    def MakeTestParameterTable(self,TableName):
        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.hosts, port= self.port)
        self.cursor = self.conn.cursor()
        #cmd=("DROP TABLE IF EXISTS %s;"%TableName)
        print(cmd)
        #self.cursor.execute(cmd) NON USO IL COMANDO:::: NON CANCELLO
        self.sql =("CREATE TABLE %s(NomeTest CHAR(16),Data CHAR(16),NomeArticolo CHAR(16),NomeRaspberry CHAR(16),NumeroBit INT,Banda INT,FrequenzaCamp INT,TestNr INT);" %TableName)
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
        
    ''' ritorna il numero di riche presenti nella tabella dati '''
    def GetAllFromtable(self,TableName):
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
        self.sql = ("INSERT INTO %s (NomeTest,Data, NomeArticolo,NomeRaspberry,NumeroBit,Banda,FrequenzaCamp, TestNr) VALUES (%s, %s, %s, %s, %s,%s, %s, %s);"%(TableName,NomeTest,datastarttest,NomeArt,Nodo,Numerodibit,Fc,Res[6],TestID))
        print(self.sql)
        self.cursor.execute(self.sql)
        self.conn.commit()
        
    def InsertParameterInRefTable(self,TableName,NomeTest,datastarttest, NomeArt,Nodo,Numerodibit,Fc):
        TestID=self.GetAllFromtable(TableName)
        self.InsertTestParameterInRefTable(self,TableName,NomeTest,datastarttest, NomeArt,Nodo,Numerodibit,Fc,TestID):
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
