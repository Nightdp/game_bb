import pymongo


# 数据库管理
class DBManager(object):

    def __init__(self):
        # 数据库
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        game_db = client["game_bb"]
        self.map_info_dao = game_db["map_info"]

    # 查询指定坐标的位置信息
    def get_land_info(self, location):
        land_info = self.map_info_dao.find_one({"x": location[0], "y": location[1]})
        print("数据查询：" + str(land_info))
        return land_info
