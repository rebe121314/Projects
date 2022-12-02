import unittest
import sqlite3
import query_data
import datetime
from create_tables import create_tables
#Specific order to garanteee an empty table to start the test in
#For larger projects where we want to preserve the integrity of teh data in the database,
#we can create a duplicate testing database

create_tables()
conn = sqlite3.connect('realestateheadoffice.db')
c = conn.cursor()
c.execute("DROP TABLE Offices")
c.execute("DROP TABLE Agents")
c.execute("DROP TABLE AgentsOffices")
c.execute("DROP TABLE Seller")
c.execute("DROP TABLE Houses")
c.execute("DROP TABLE Buyers")
c.execute("DROP TABLE Sales")
conn.commit()
conn.close()
create_tables()
from insert_data import create_sample_data

"""
Because it uses the same dtabase: we need to delete the database before each test

"""

class TestDatabase(unittest.TestCase):
    """
        def test_insert_office(self):
        office = {'OfficeId': 1, 'OfficeName': 'Office 1', 'OfficeAddress': 'Office Address 1', 'OfficeZip': 12345, 'OfficePhone': '1234567890',\
             'OfficeEmail': 'ofice@email.com'}

        insert_data.insert_office(office)
        c.execute("SELECT * FROM Offices WHERE OfficeId = 1")
        result = c.fetchone()
        self.assertEqual(result, (1, 'Office 1', 'Office Address 1', 12345, '1234567890', 'ofice@email.com'))

    def test_insert_agent(self):
        agent = {'AgentId': 1, 'AgentName': 'Agent 1', 'AgentPhone': '1234567890', 'AgentEmail': ' agent@email.com', 'AgentAddress': 'Agent Address 1'}

        insert_data.insert_agent(agent)
        c.execute("SELECT * FROM Agents WHERE AgentId = 1")
        result = c.fetchone()
        self.assertEqual(result, (1, 'Agent 1', '1234567890', '1234567890', ' agent@email.com', 'Agent Address 1'))

    """

    def setUp(self):
        #start the database
        conn = sqlite3.connect('realestateheadoffice.db')
        c = conn.cursor()
        c.execute("DROP TABLE Offices")
        c.execute("DROP TABLE Agents")
        c.execute("DROP TABLE AgentsOffices")
        c.execute("DROP TABLE Seller")
        c.execute("DROP TABLE Houses")
        c.execute("DROP TABLE Buyers")
        c.execute("DROP TABLE Sales")
        conn.commit()
        conn.close()
        create_tables()
        create_sample_data()
        

        #insert_data.create_sample_data()

    def tearDown(self):
        #Delete the database
        pass

    def test_top5offices(self):
        current_month = datetime.datetime.now().month
        top5office = [('Meyer-Cohen', 4, 3, '12'), ('Adkins, Garcia and Moore', 2, 2, '12')]
        res = query_data.top5offices(current_month)
        self.assertEqual(res, top5office)

    def test_top5Agents(self):
        current_month = datetime.datetime.now().month
        top5agents = [('Caleb Navarro', 4, 2, '12'), ('Sheena Cox', 2, 2, '12'), ('Lindsey Turner', 1, 1, '12')]
        res = query_data.top5Agents(current_month)
        self.assertEqual(res, top5agents)

    def test_monthlyCommission(self):
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        name_of_table = name_of_table = "AgentCommission" + str(current_month) + str(current_year)
        query_data.createMonthlyCommissionTable(name_of_table)
        query_data.createMonthlyCommissionTable(name_of_table)
        monthlyCommission = [('Lindsey Turner', 1, 55250.08, '12'), ('Sheena Cox', 2, 77944.72, '12'), ('Caleb Navarro', 4, 81110.86000000002, '12')]
        res = query_data.monthlyCommission(current_month, name_of_table)
        self.assertEqual(res, monthlyCommission)

    def test_AverageDaysMarket(self):
        current_month = datetime.datetime.now().month
        AverageDaysMarket = 773.4
        res = query_data.AverageDaysMarket(current_month)
        self.assertEqual(res, AverageDaysMarket)

    def test_AveragePrice(self):
        current_month = datetime.datetime.now().month
        AveragePrice = 1018544.8
        res = query_data.AverageSellingPrice(current_month)
        self.assertEqual(res, AveragePrice)


if __name__ == '__main__':
    unittest.main()