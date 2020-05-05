import datetime

#datetime.datetime.now()
class Shop:
    def __init__(self, shopdesc='',shopname='',shoppic='',shopprice=0,shopid=1) -> None:
        super().__init__()
        self.shopdesc = shopdesc
        self.shopname = shopname
        self.shoppic = shoppic
        self.shopprice = shopprice
        self.shopid = shopid


class UserAccount:
    def __init__(self, username, password) -> None:
        super().__init__()
        self.username = username
        self.password = password
class Messages:
    def __init__(self, contents,username) -> None:
        super().__init__()
        self.username = username
        self.contents = contents
