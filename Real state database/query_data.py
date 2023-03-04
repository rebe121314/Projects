#Shedule a function to run every 5 minutes
import datetime
import time
import sqlite3




def create_index():
    """
    Creates indices for every id value of all the tables.
    The indices with forgein keys will be in multiple tables
    Assuming big memory storage
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    c.execute("""
                CREATE INDEX IF NOT EXISTS HouseIdIndex ON Houses(HouseId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS SaleIdIndex ON Sales(SaleId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS AgentIdIndex ON Agents(AgentId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS OfficeIdIndex ON Offices(OfficeId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS SellerIdIndex ON Seller(SellerId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS BuyerIdIndex ON Buyers(BuyerId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS HouseSellerIdIndex ON Houses(HouseSellerId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS HouseListingAgentIndex ON Houses(HouseListingAgent)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS HouseOfficeIndex ON Houses(HouseOffice)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS SaleHouseIdIndex ON Sales(SaleHouseId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS SaleAgentIdIndex ON Sales(SaleAgentId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS SaleOfficeIndex ON Sales(SaleOffice)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS SaleBuyerIdIndex ON Sales(SaleBuyerId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS AgentOfficeIndex ON AgentsOffices(AgentId)
            """)
    c.execute("""
                CREATE INDEX IF NOT EXISTS OfficeAgentIndex ON AgentsOffices(OfficeId)
            """)
    conn.commit()
    conn.close()


def top5offices(current_month):
    """
    Function filters the sales table for the current month
    Then counts the times an office id appears and returns the result in a list.

    Imput:
    current_month: the current month in the format of a string

    Output:
    top5offices: a list of tuples with the office name, office id and the number of sales
    printing of the values in the list
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    c.execute("""
                SELECT OfficeName,  OfficeId, COUNT(OfficeId) AS OfficeSales, strftime('%m', SaleDate) AS Month
                FROM Sales
                INNER JOIN Offices ON Sales.SaleOffice = Offices.OfficeId
                WHERE Month = ?
                GROUP BY OfficeId
                ORDER BY OfficeSales DESC
                LIMIT 5
            """, (str(current_month),))
    top5offices = c.fetchall()
    print("")
    print("Top 5 Offices with the most sales for the month of", datetime.datetime.now().strftime("%B"), '\n')
    #print(top5offices)
    for office in top5offices:
        print(office[0], "Id", office[1] ,"with", office[2], "sales")
    return top5offices

    


def top5Agents(current_month):
    """
    Function filters the sales table for the current month
    Then counts the times an agent id appears and returns the result in a list.

    Imput:
    current_month: the current month in the format of a string

    Output:
    top5agents: a list of tuples with the agent name, agent id and the number of sales
    printing of the values in the list
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    c.execute("""
                SELECT AgentName, AgentId, COUNT(AgentId) AS AgentSales, strftime('%m', SaleDate) AS Month
                FROM Sales
                INNER JOIN Agents ON Sales.SaleAgentId = Agents.AgentId
                WHERE Month = ?
                GROUP BY AgentId
                ORDER BY AgentSales DESC
                LIMIT 5
            """, (str(current_month),))
    top5Agents = c.fetchall()
    print("")
    print("Top 5 Agents with the most sales for the month of", datetime.datetime.now().strftime("%B"), '\n')
    print(top5Agents)
    for agent in top5Agents:
        print(agent[0], "Id", agent[1] ,"with", agent[2], "sales")
    conn.close()
    return top5Agents


def createMonthlyCommissionTable(name_of_table):
    """
    Function creates a table with the monthly commission for each agent

    Imput:
    name_of_table: the name of the table to be created

    Output:
    None
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    c.execute("""
                CREATE TABLE IF NOT EXISTS {} (
                AgentId INTEGER,
                AgentCommission INTEGER,
                FOREIGN KEY (AgentId) REFERENCES Agents(AgentId))
            """.format(name_of_table))
    conn.commit()
    conn.close()


def monthlyCommission(current_month, name_of_table):
    """
    Function calculates the monthly commission for each agent and inserts the values into a table
    Inserts the values into the created table for the month
    Also prints the results (for vizualizatipn purposes)

    Imput:
    current_month: the current month in the format of a string
    name_of_table: the name of the table to be created

    Output:
    The commission for each agent in the table
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    c.execute("""
                SELECT AgentName, AgentId, SUM(SaleCommission) AS AgentCommission, strftime('%m', SaleDate) AS Month
                FROM Sales
                INNER JOIN Agents ON Sales.SaleAgentId = Agents.AgentId
                WHERE Month = ?
                GROUP BY AgentId
            """, (str(current_month),))
    monthlyCommission = c.fetchall()
    print("")
    print("Monthly Commission for the month of", datetime.datetime.now().strftime("%B"), '\n')
    print(monthlyCommission)
    for agent in monthlyCommission:
        val_id = agent[1]
        val_commission = agent[2]
        val_insert = """INSERT INTO {} (AgentId, AgentCommission) VALUES (?, ?)""".format(name_of_table)
        c.execute(val_insert, (val_id, val_commission))
        conn.commit()
        print(agent[0], "Id", agent[1] ,"with", agent[2], "commission")
    return monthlyCommission

def printComissiontable(name_of_table):
    """
    Function prints the values in the monthly commission table


    Imput:
    name_of_table: the name of the table to be created

    Output:
    The direct reults of the table without formating
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    c.execute("""
                SELECT * FROM {}
            """.format(name_of_table))
    printComissiontable = c.fetchall()
    print("")
    print("Monthly Commission Table for the month of", datetime.datetime.now().strftime("%B"), "without formating" '\n')
    print(printComissiontable)



def AverageDaysMarket(current_month):
    """
    Function calculates the average number of days on the market for the current month

    Imput:
    current_month: the current month in the format of a string

    Output:
    The average number of days on the market for the current month
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    c.execute("""
                SELECT HouseId, SaleDate, HouseDateListing, strftime('%m', SaleDate) AS Month
                FROM Sales
                INNER JOIN Houses ON Sales.SaleHouseId = Houses.HouseId
                WHERE Month = ?
            """, (str(current_month),))
    all_house = c.fetchall()
    print("")
    print("Average number of days on the market for the month of", datetime.datetime.now().strftime("%B"), '\n')
    #print(AverageDaysMarket)
    total = 0
    for house in all_house:
        #print(house[0], house[1], house[2])
        sell = datetime.datetime.strptime(house[1], '%Y-%m-%d %H:%M:%S')
        list = datetime.datetime.strptime(house[2], '%Y-%m-%d %H:%M:%S')
        diff = sell - list
        total += diff.days
    average = total / len(all_house)
    print("The average number of days on the market is", abs(average))
    return average



def AverageSellingPrice(current_month):
    """
    Function calculates the average selling price for the current month

    Imput:
    current_month: the current month in the format of a string

    Output:
    The average selling price for the current month
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    c.execute("""
                SELECT AVG(SalePrice), strftime('%m', SaleDate) AS Month
                FROM Sales
                WHERE Month = ?
            """, (str(current_month),))
    AverageSellingPrice = c.fetchall()
    print("")
    print("The average selling price is", abs(AverageSellingPrice[0][0]))
    return AverageSellingPrice[0][0]


def run_monthly():
    """
    Functions that mimics the monthly report.
    Time of sleep equals to 1 month in minutes. 
    """
    while True:
        conn = sqlite3.connect('realestateheadoffice.db')
        c = conn.cursor()
        print("Date of the analysis", datetime.datetime.now())
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().strftime("%Y")
        name_of_table = "AgentCommission" + str(current_month) + str(current_year)
        create_index()
        top5offices(current_month)
        conn.close()
        top5Agents(current_month)
        conn.close()
        createMonthlyCommissionTable(name_of_table)
        conn.close()
        monthlyCommission(current_month, name_of_table)
        conn.close()
        printComissiontable(name_of_table)
        conn.close()
        AverageDaysMarket(current_month)
        conn.close()
        AverageSellingPrice(current_month)
        conn.close()
        time.sleep(43800.048)


#Initializes the program
if __name__ == '__main__':
    run_monthly()
    

