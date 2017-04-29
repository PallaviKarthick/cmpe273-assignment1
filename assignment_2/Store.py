import uuid 

class Store(object):
    def __init__(self, storeName):
        self.store_id = str(uuid.uuid4)
        print self.store_id
        self.store_name = storeName
        self.store_hours = {}
        self.status = "status not defined"
        self.message = "message not available"