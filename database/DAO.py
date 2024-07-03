from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.`year` 
        from teams t 
        where t.`year` >=1985"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeams(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID , t.`year` , t.teamCode , t.name 
            from teams t 
            where t.`year` =%s"""

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(s1, s2, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select sum(salary) as peso
        from salaries s, appearances a , teams t 
        where (s.teamID =%s or s.teamID=%s) and s.`year` =%s 
        and s.`year` =a.`year` and t.`year` =a.`year` and t.ID =a.teamID and s.playerID =a.playerID  """

        cursor.execute(query, (s1, s2, anno,))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()
        return result[0]

    @staticmethod
    def getPeso2(anno, idMap):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, sum(s.salary) as tot
        from teams t, salaries s , appearances a 
        where t.`year` =s.`year` and a.`year` =t.`year` 
        and a.`year` =%s
        and a.playerID =s.playerID and t.ID =a.teamID 
        group by t.ID"""

        cursor.execute(query, (anno,))

        for row in cursor:
            result[idMap[row["ID"]]] = row["tot"]

        cursor.close()
        conn.close()
        return result
