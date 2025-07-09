from database.DB_connect import DBConnect
from model.edge import Edge
from model.method import Method
from model.node import Node


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getMethods():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select *
                    from go_methods gm """

        cursor.execute(query)

        for row in cursor:
            res.append(Method(**row))
        conn.close()
        cursor.close()
        return res

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """select distinct YEAR(gds.`Date`) as year
                    from go_daily_sales gds 
                    order by year asc"""

        cursor.execute(query)

        for row in cursor:
            res.append(row["year"])
        conn.close()
        cursor.close()
        return res

    @staticmethod
    def getNodes(method, year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select distinct gds.Product_number as product_number, SUM(gds.Unit_sale_price * gds.Quantity) as ricavoTot
                    from go_daily_sales gds, go_methods gm 
                    where gds.Order_method_code = gm.Order_method_code
                    and gm.Order_method_type = %s
                    and YEAR(gds.`Date` ) = %s
                    group by gds.Product_number 
                    order by ricavoTot desc"""

        cursor.execute(query, (method, year))
        res = []
        for row in cursor:
            res.append(Node(**row))
        conn.close()
        cursor.close()
        return res

    @staticmethod
    def getEdges(method, year, s):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        res = []
        query = """with ricavi as 
                    (select gds.Product_number, SUM(gds.Unit_sale_price * gds.Quantity) as ricavoTot
                    from go_daily_sales gds
                    join go_methods gm on gds.Order_method_code = gm.Order_method_code
                    where gm.Order_method_type = %s
                    and YEAR(gds.`Date` ) = %s
                    group by gds.Product_number)
                    
                    select r1.Product_number as product_number1, r2.Product_number as product_number2
                    from ricavi r1, ricavi r2 
                    where r1.Product_number != r2.Product_number
                    and r2.ricavoTot >= (1+%s)*r1.ricavoTot """

        cursor.execute(query, (method, year, s))

        for row in cursor:
            res.append(Edge(**row))
        conn.close()
        cursor.close()
        return res