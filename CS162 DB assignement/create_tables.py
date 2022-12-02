
import sqlite3



#Create the database and the current connection


def create_tables():
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS Offices 
            (OfficeId INTEGER PRIMARY KEY,
            OfficeName TEXT,
            OfficeAddres TEXT,
            OfficeZipCode INTEGER,
            OfficePhone TEXT,
            OfficeEmail TEXT)
        """)

    # Agent table where they can work in multiple offices
    c.execute("""
            CREATE TABLE IF NOT EXISTS Agents 
            (AgentId INTEGER PRIMARY KEY,
            AgentName TEXT,
            AgentPhone TEXT,
            AgentEmail TEXT,
            AgentAddress TEXT)
        """)


    # Table for Agents and Offices
    c.execute("""
            CREATE TABLE IF NOT EXISTS AgentsOffices 
            (AgentId INTEGER,
            OfficeId INTEGER,
            FOREIGN KEY (AgentId) REFERENCES Agents(AgentId),
            FOREIGN KEY (OfficeId) REFERENCES Offices(OfficeId))
        """)

    #  Saller Table
    c.execute("""
            CREATE TABLE IF NOT EXISTS Seller 
            (SellerId INTEGER PRIMARY KEY,
            SellerName TEXT,
            SellerPhone TEXT,
            SellerEmail TEXT,
            SellerAddress TEXT)
        """)


    # House Table
    c.execute("""
            CREATE TABLE IF NOT EXISTS Houses 
            (HouseId INTEGER PRIMARY KEY,
            HouseSellerId INTEGER,
            HouseBedrooms INTEGER,
            HouseBathrooms INTEGER,
            HouseListingPrice NUMERIC(20, 2),
            HouseZipCode INTEGER,
            HouseDateListing DATETIME,
            HouseListingAgent INTEGER,
            HouseOffice INTEGER,
            HouseSold BOOLEAN,
            FOREIGN KEY (HouseSellerId) REFERENCES Seller(SellerId),
            FOREIGN KEY (HouseListingAgent) REFERENCES Agents(AgentId),
            FOREIGN KEY (HouseOffice) REFERENCES Offices(OfficeId))
        """)

    # Buyer Table
    c.execute("""
            CREATE TABLE IF NOT EXISTS Buyers 
            (BuyerId INTEGER PRIMARY KEY,
            BuyerName TEXT,
            BuyerPhone TEXT,
            BuyerEmail TEXT,
            BuyerAddress TEXT)
        """)

    # Sales Table
    c.execute("""
            CREATE TABLE IF NOT EXISTS Sales 
            (SaleId INTEGER PRIMARY KEY,
            SaleHouseId INTEGER,
            SaleAgentId INTEGER,
            SaleOffice INTEGER,
            SalePrice NUMERIC(20, 2),
            SaleDate DATETIME,
            SaleCommission NUMERIC(20, 2),
            SaleBuyerId INTEGER,
            FOREIGN KEY (SaleHouseId) REFERENCES Houses(HouseId),
            FOREIGN KEY (SaleAgentId) REFERENCES Agents(AgentId),
            FOREIGN KEY (SaleOffice) REFERENCES Offices(OfficeId),
            FOREIGN KEY (SaleBuyerId) REFERENCES Buyers(BuyerId))
        """)
    conn.commit()
    # Close the connection
    conn.close()



if __name__ == '__main__':
    create_tables()
    