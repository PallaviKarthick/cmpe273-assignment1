import uuid 

class Menu(object):
    def __init__(self, storeName):
        self.menu_id = str(uuid.uuid4())
        print self.menu_id
        self.store_name = storeName
        self.selection = {}
        self.size = {}
        self.price = {}
        self.store_hours = {}
        self.status = "status not defined"
        self.message = "message not available"



