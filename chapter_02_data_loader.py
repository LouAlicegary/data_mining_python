import codecs 

class DataLoader:


    """ 
    Initialize loader
    """
    def __init__(self, dataType='book'):

        return None


    """ 
    Loads the BX book dataset. Path is where the BX files are located 
    """
    def loadBookDB(self, path='BX-Dump/'):
        
        bookDb = {}

        bookDb['data'] = self.getBookRatings(path, "BX-Book-Ratings.csv")

        bookDb['productid2name'] = self.getBookRecords(path, "BX-Books.csv")

        userdata = self.getUserRecords(path, "BX-Users.csv")
        bookDb['userid2name'] = userdata['userid2name']
        bookDb['username2id'] = userdata['username2id']

        return bookDb  


    """
    Description
    """
    def getBookRatings(self, path, filename):

        # First load book ratings into self.data
        data = {}
        i = 0
        
        f = codecs.open(path + filename, 'r', 'utf8')
        for line in f:
            i += 1
            #separate line into fields
            fields = line.split(';')
            user = fields[0].strip('"')
            book = fields[1].strip('"')
            rating = int(fields[2].strip().strip('"'))
            
            if user in data:
                currentRatings = data[user]
            else:
                currentRatings = {}
            currentRatings[book] = rating
            data[user] = currentRatings
        
        f.close()

        return data



    # Now load books into self.productid2name
    # Books contains isbn, title, and author among other fields
    def getBookRecords(self, path, filename):

        productid2name = {}
        i = 0

        f = codecs.open(path + filename, 'r', 'utf8')
        
        for line in f:
            i += 1
            #separate line into fields
            fields = line.split(';')
            isbn = fields[0].strip('"')
            title = fields[1].strip('"')
            author = fields[2].strip().strip('"')
            title = title + ' by ' + author
            productid2name[isbn] = title
        
        f.close()

        return productid2name



    #  Now load user info into both self.userid2name and self.username2id
    def getUserRecords(self, path, filename):
        
        userdata = {
            'userid2name': {},
            'username2id': {}
        }
        
        i = 0

        f = codecs.open(path + filename, 'r', 'utf8')
        
        for line in f:
            i += 1

            #separate line into fields
            fields = line.split(';')
            userid = fields[0].strip('"')
            location = fields[1].strip('"')
            
            if len(fields) > 3:
                age = fields[2].strip().strip('"')
            else:
                age = 'NULL'
            
            if age != 'NULL':
                value = location + '  (age: ' + age + ')'
            else:
                value = location
            
            userdata['userid2name'][userid] = value
            userdata['username2id'][location] = userid
        
        f.close()

        return userdata
