from utils.db import db
# from data import GroupType


class readDb:
    def get_network():
        query = "SELECT * FROM network"
        try:
            result = db.query_data(query)
            return result
        except Exception as e:
            print(f"Error fetching network data: {e}")
            return None
