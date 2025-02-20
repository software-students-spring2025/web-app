from app import mongo

class URL:
    @staticmethod
    def create_url(user_id, long_url, short_url):
        mongo.db.urls.insert_one({"user_id": user_id, "long_url": long_url, "short_url": short_url})

    @staticmethod
    def get_user_urls(user_id):
        return mongo.db.urls.find({"user_id": user_id})

    @staticmethod
    def delete_url(short_url):
        mongo.db.urls.delete_one({"short_url": short_url})

    @staticmethod
    def update_url(short_url, new_long_url):
        mongo.db.urls.update_one({"short_url": short_url}, {"$set": {"long_url": new_long_url}})
