
import datetime
import random
import sqlite3
from faker import Faker

def insert_office(office):
    """
    Function to insert an office into the database
    creates and closes the connection to the database

    Input:
    office: dictionary

    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO Offices VALUES ( :OfficeId, \
                :OfficeName, :OfficeAddress,  :OfficeZip, :OfficePhone, \
                :OfficeEmail);", office) 
        conn.commit()
    conn.close()



def insert_agent(agent):
    """
    Function to insert an agent into the database
    creates and closes the connection to the database

    Input:
    agent: dictionary
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO Agents VALUES ( :AgentId, \
                :AgentName, :AgentPhone, :AgentEmail, \
                :AgentAddress);", agent) 
        conn.commit()
    conn.close()

def insert_seller(seller):
    """
    Function to insert a seller into the database
    creates and closes the connection to the database

    Input:
    seller: dictionary
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO Seller VALUES ( :SellerId, \
                :SellerName, :SellerPhone, :SellerEmail, \
                :SellerAddress);", seller) 
        conn.commit()
    conn.close()

def insert_house(house):
    """
    Function to insert a house into the database
    creates and closes the connection to the database

    Input:
    house: dictionary
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO Houses VALUES ( :HouseId, \
                :HouseSellerId, :HouseBedrooms, :HouseBathrooms, \
                :HouseListingPrice, :HouseZipCode, :HouseDateListing, \
                :HouseListingAgent, :HouseOffice, :HouseSold);", house) 
        conn.commit()
    conn.close()



def insert_buyer(buyer):
    """
    Function to insert a buyer into the database
    creates and closes the connection to the database

    Input:
    buyer: dictionary
    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO Buyers VALUES ( :BuyerId, \
                :BuyerName, :BuyerPhone, :BuyerEmail, \
                :BuyerAddress);", buyer) 
        conn.commit()
    conn.close()

def insert_AgentOffice(agent_office):
    """
    Function to insert an agent_office into the database
    creates and closes the connection to the database

    Input:
    agent_office: dictionary

    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO AgentsOffices VALUES ( :AgentId, \
                :OfficeId);", agent_office) 
        conn.commit()
    conn.close()

# Create a transaction for each sale
def insert_sale(sale):
    """
    Function to insert a sale into the database
    Calculates the commission for the agent and the office
    creates and closes the connection to the database

    Input:
    sale: dictionary

    """
    conn = sqlite3.connect('realestateheadoffice.db')
    c = conn.cursor()
    with conn:
        if sale['SalePrice'] < 100000:
            sale['SaleCommission'] = sale['SalePrice']* 0.10
        elif sale['SalePrice'] < 200000:
            sale['SaleCommission'] = sale['SalePrice']* 0.075
        elif sale['SalePrice'] < 500000:
            sale['SaleCommission'] = sale['SalePrice']* 0.06
        elif sale['SalePrice'] < 1000000:
            sale['SaleCommission'] = sale['SalePrice']* 0.05
        else:
            sale['SaleCommission'] = sale['SalePrice']* 0.04
        
        #update the status of the house to sold
        c.execute("UPDATE Houses SET HouseSold = True WHERE HouseId = :HouseId", {'HouseId': sale['SaleHouseId']})
        # The transcations can be store in sale
        c.execute("INSERT INTO Sales VALUES\
                 ( :SaleId, :SaleHouseId, :SaleAgentId, :SaleOffice, \
                    :SalePrice, :SaleDate, :SaleCommission, :SaleBuyerId);", sale) 
        conn.commit()
    conn.close()

    




fake = Faker()

agentsid = []
officesid = []
sellerid = []
buyersid = []
housesid = []
#Set so everycombination only happens once (but we can still run the data multipe times without unique constraint error))  
agentoffice = set()
houseagentofice = set()
sold = set()

offices = []
agents = []
sellers = []
houses = []
buyers = []
sales = []
agentoffice_list = [(2,4), (1,4), (4,2), (1, 5)]

office_list =   [{'OfficeId': 1, 'OfficeName': 'Martinez Ltd', 'OfficeAddress': '58651 Mitchell Parkway\nSouth Robynside, FM 99937', 'OfficeZip': '86014', 'OfficePhone': '109-125-9533', 'OfficeEmail': 'darlene03@example.com'}, {'OfficeId': 2, 'OfficeName': 'Adkins, Garcia and Moore', 'OfficeAddress': '98214 Rangel Well\nPort Ryan, DE 40883', 'OfficeZip': '82998', 'OfficePhone': '468-688-2193x6899', 'OfficeEmail': 'austinowen@example.org'}, {'OfficeId': 3, 'OfficeName': 'Carter, Neal and Warner', 'OfficeAddress': '4158 Benjamin Grove\nEspinozaview, MS 35450', 'OfficeZip': '12680', 'OfficePhone': '592.517.0395', 'OfficeEmail': 'petersstephanie@example.com'}, {'OfficeId': 4, 'OfficeName': 'Meyer-Cohen', 'OfficeAddress': '75541 Hunt Fords Apt. 575\nJuliefort, TN 99759', 'OfficeZip': '60617', 'OfficePhone': '8478772393', 'OfficeEmail': 'halladam@example.net'}, {'OfficeId': 5, 'OfficeName': 'Cole, Phillips and Lane', 'OfficeAddress': '84570 Ortiz Brooks\nNorth Samantha, MA 39391', 'OfficeZip': '99481', 'OfficePhone': '641-518-1172x150', 'OfficeEmail': 'michelleburns@example.net'}]
agent_list = [{'AgentId': 1, 'AgentName': 'Lindsey Turner', 'AgentPhone': '(010)390-4832', 'AgentEmail': 'denisecain@example.net', 'AgentAddress': '2464 Evans Plains Apt. 677\nDavisland, TN 22072'}, {'AgentId': 2, 'AgentName': 'Sheena Cox', 'AgentPhone': '987.532.4163', 'AgentEmail': 'cheyenne55@example.net', 'AgentAddress': '792 Taylor Stream\nAndrewschester, KS 09989'}, {'AgentId': 3, 'AgentName': 'Monica Parsons', 'AgentPhone': '842.160.2579x392', 'AgentEmail': 'denise08@example.net', 'AgentAddress': '49355 Carolyn Views Apt. 993\nPort Joechester, SC 06797'}, {'AgentId': 4, 'AgentName': 'Caleb Navarro', 'AgentPhone': '001-906-723-7206', 'AgentEmail': 'corey59@example.com', 'AgentAddress': '87886 Adams Crest Apt. 438\nLake James, MT 28702'}, {'AgentId': 5, 'AgentName': 'Stephen Santos', 'AgentPhone': '001-781-726-8346x86452', 'AgentEmail': 'ipeters@example.org', 'AgentAddress': '77935 Ashley Harbor\nWest Patrick, GA 78323'}]
seller_list = [{'SellerId': 1, 'SellerName': 'Timothy Williams', 'SellerPhone': '567-415-8662', 'SellerEmail': 'franklindeborah@example.net', 'SellerAddress': '4182 Foster Cliff\nEast Brianshire, CA 67352'}, {'SellerId': 2, 'SellerName': 'Terry Edwards', 'SellerPhone': '(660)601-9050', 'SellerEmail': 'garciarebecca@example.com', 'SellerAddress': '066 Moore Rest\nSouth Erikborough, FL 95895'}, {'SellerId': 3, 'SellerName': 'John Clark', 'SellerPhone': '036.937.5250', 'SellerEmail': 'moorecrystal@example.com', 'SellerAddress': '3926 Chen Row\nChristensenstad, GA 06624'}, {'SellerId': 4, 'SellerName': 'Joshua Brown', 'SellerPhone': '(775)396-1971x1621', 'SellerEmail': 'paulwall@example.com', 'SellerAddress': 'Unit 9102 Box 0728\nDPO AE 57255'}, {'SellerId': 5, 'SellerName': 'Danielle Cooper', 'SellerPhone': '+1-065-489-7545x796', 'SellerEmail': 'murrayjessica@example.com', 'SellerAddress': '907 Stanley Hill Suite 759\nWest Johnmouth, SD 17291'}]

house_list = [{'HouseId': 1, 'HouseSellerId': 3, 'HouseBedrooms': 4, 'HouseBathrooms': 4, 'HouseListingPrice': 762257, 'HouseZipCode': '41446', 'HouseDateListing': datetime.datetime(2020, 11, 14, 18, 28, 56), 'HouseListingAgent': 1, 'HouseOffice': 5, 'HouseSold': False}, {'HouseId': 2, 'HouseSellerId': 1, 'HouseBedrooms': 3,'HouseBathrooms': 4, 'HouseListingPrice': 666276, 'HouseZipCode': '40001', 'HouseDateListing': datetime.datetime(2020, 10, 6, 2, 50, 10), 'HouseListingAgent': 2, 'HouseOffice': 4, 'HouseSold': False}, {'HouseId': 3, 'HouseSellerId': 5, 'HouseBedrooms': 5, 'HouseBathrooms': 5, 'HouseListingPrice': 892188, 'HouseZipCode': '79562', 'HouseDateListing': datetime.datetime(2020, 1, 27, 8, 0, 56), 'HouseListingAgent': 1, 'HouseOffice': 4, 'HouseSold': False}, {'HouseId': 4, 'HouseSellerId': 1, 'HouseBedrooms':1, 'HouseBathrooms': 4, 'HouseListingPrice': 606264, 'HouseZipCode': '36059', 'HouseDateListing': datetime.datetime(2020, 6, 1, 16, 47, 59),'HouseListingAgent': 4, 'HouseOffice': 2, 'HouseSold': False}, {'HouseId': 5, 'HouseSellerId': 5, 'HouseBedrooms': 1, 'HouseBathrooms': 3, 'HouseListingPrice': 491528, 'HouseZipCode': '22552', 'HouseDateListing': datetime.datetime(2022, 3, 6, 14, 17, 45), 'HouseListingAgent': 4, 'HouseOffice': 2, 'HouseSold': False}]

buyer_list = [{'BuyerId': 1, 'BuyerName': 'Daniel Keith', 'BuyerPhone': '(898)401-9010x4315', 'BuyerEmail': 'stacy46@example.org', 'BuyerAddress': '69051 Donald Neck\nNew Brandyland, KS 34112'}, {'BuyerId': 2, 'BuyerName': 'Dylan Solis', 'BuyerPhone':'090.487.3534x5434', 'BuyerEmail': 'brandy83@example.net', 'BuyerAddress': '1145 Keith Creek\nNew Emma, AL 92642'}, {'BuyerId': 3, 'BuyerName': 'Anthony Brewer', 'BuyerPhone': '(528)986-1359x35435', 'BuyerEmail': 'xcamacho@example.net', 'BuyerAddress': '6129 Nicholas  Cove\nJoshuabury, OR 63095'}, {'BuyerId': 4, 'BuyerName': 'Erica Salazar', 'BuyerPhone': '(228)833-1303x640', 'BuyerEmail': 'gouldthomas@example.org', 'BuyerAddress': '1802 Johnson Land Apt. 205\nMunozville, TN 12257'}, {'BuyerId': 5, 'BuyerName': 'Nicholas Mitchell', 'BuyerPhone': '001-963-675-2043x4418', 'BuyerEmail': 'brittany98@example.com', 'BuyerAddress': '1571 Nicole Wells Suite 748\nWest Gloria, OR 08540'}]

sale_list = [{'SaleId': 1, 'SaleHouseId': 1, 'SaleAgentId': 2, 'SaleOffice': 4, 'SalePrice': 1463161, 'SaleDate': datetime.datetime(2022, 12, 28, 10, 21, 51), 'SaleCommission': 58526.44, 'SaleBuyerId': 1},{'SaleId': 2, 'SaleHouseId': 2, 'SaleAgentId': 1, 'SaleOffice': 4, 'SalePrice': 1381252, 'SaleDate': datetime.datetime(2022, 12, 14, 22, 22, 1), 'SaleCommission': 55250.08, 'SaleBuyerId': 2}, {'SaleId': 3, 'SaleHouseId': 3, 'SaleAgentId': 2, 'SaleOffice': 4, 'SalePrice': 323638, 'SaleDate': datetime.datetime(2022, 12, 24, 13, 0, 12), 'SaleCommission': 19418.28, 'SaleBuyerId': 3}, {'SaleId': 4, 'SaleHouseId': 4, 'SaleAgentId': 4, 'SaleOffice': 2, 'SalePrice': 206197, 'SaleDate': datetime.datetime(2022, 12, 30, 10, 49, 58), 'SaleCommission': 12371.82, 'SaleBuyerId': 4}, {'SaleId': 5, 'SaleHouseId': 5, 'SaleAgentId': 4, 'SaleOffice':2, 'SalePrice': 1718476, 'SaleDate': datetime.datetime(2022, 12, 24, 7, 44, 8), 'SaleCommission': 68739.04000000001, 'SaleBuyerId':5}]


def create_sample_data():
    """
    Create sample data for the database
    """
    # Create offices
    for i in office_list:
        insert_office(i)

    # Create agents
    for i in agent_list:
        insert_agent(i)

    # Create sellers
    for i in seller_list:
        insert_seller(i)

    # Create buyers
    for i in buyer_list:
        insert_buyer(i)

    # Create houses
    for i in house_list:
        insert_house(i)

    # Create sales
    for i in sale_list:
        insert_sale(i)

    for i in agentoffice_list:
        insert_AgentOffice(i)






def create_complex_data():
    #Create offices
    for i in range(1, 51):
        office = {"OfficeId": fake.random_int(min=1, max=1000000, step=1) + datetime.datetime.now().microsecond, 
                  "OfficeName": fake.company(),
                  "OfficeAddress": fake.address(),
                  "OfficeZip": fake.zipcode(),
                  "OfficePhone": fake.phone_number(),
                  "OfficeEmail": fake.email()}
        offices.append(office)
        officesid.append(office['OfficeId'])
        insert_office(office)
    
    # Create Agents
    for i in range(1, 51):
        agent = {"AgentId": fake.random_int(min=1, max=1000000, step=1) + datetime.datetime.now().microsecond,
                 "AgentName": fake.name(),
                 "AgentPhone": fake.phone_number(),
                 "AgentEmail": fake.email(),
                 "AgentAddress": fake.address()}
        agentsid.append(agent['AgentId'])
        agents.append(agent)
        insert_agent(agent)
    
    # Create Sellers
    for i in range(1, 51):
        seller = {"SellerId": fake.random_int(min=1, max=1000000, step=1) + datetime.datetime.now().microsecond,
                  "SellerName": fake.name(),
                  "SellerPhone": fake.phone_number(),
                  "SellerEmail": fake.email(),
                  "SellerAddress": fake.address()}
        sellerid.append(seller['SellerId'])
        sellers.append(seller)
        insert_seller(seller)
    
    # Create Houses
    for i in range(1, 51):
        house = {"HouseId": fake.random_int(min=1, max=1000000, step=1) + datetime.datetime.now().microsecond,
                 "HouseSellerId": random.choice(sellerid),
                 "HouseBedrooms": fake.random_int(min=1, max=5),
                 "HouseBathrooms": fake.random_int(min=1, max=5),
                 "HouseListingPrice": fake.random_int(min=70000, max=1000000),
                 "HouseZipCode": fake.zipcode(), 
                 "HouseDateListing": fake.date_time_between(start_date="-1y", end_date="now"),
                 "HouseListingAgent": random.choice(agentsid),
                 "HouseOffice": random.choice(officesid),
                 "HouseSold": False}
        housesid.append(house['HouseId'])
        agentoffice.add((house['HouseListingAgent'], house['HouseOffice']))
        houseagentofice.add((house['HouseId'], house['HouseListingAgent'], house['HouseOffice']))
        houses.append(house)
        insert_house(house)
    
    # Create sample data for Buyers
    for i in range(1, 51):
        buyer = {"BuyerId": fake.random_int(min=1, max=1000000, step=1) + datetime.datetime.now().microsecond,
                 "BuyerName": fake.name(),
                 "BuyerPhone": fake.phone_number(),
                 "BuyerEmail": fake.email(),
                 "BuyerAddress": fake.address()}
        buyersid.append(buyer['BuyerId'])
        buyers.append(buyer)
        insert_buyer(buyer)

    # Create sample data for Sales
    for i in range(1, 51):
        hao = random.choice(list(houseagentofice))

        sale = {"SaleId": fake.random_int(min=1, max=1000000, step=1) + datetime.datetime.now().microsecond,
                "SaleHouseId": hao[0],
                "SaleAgentId": hao[1],
                "SaleOffice": hao[2],
                "SalePrice": fake.random_int(min=70000, max=2000000),
                #fake date in current year for the sake of quary
                "SaleDate": fake.date_time_between(start_date="-1y", end_date="now"),
                "SaleCommission": 1,
                "SaleBuyerId": random.choice(buyersid)}
        sales.append(sale)
        insert_sale(sale)

    for i in agentoffice:
        insert_AgentOffice(i)

    
 

create_complex_data()

#print(offices)
#print(agents)
#print(sellers)
#print(houses)
#print(buyers)
#print(sales)





