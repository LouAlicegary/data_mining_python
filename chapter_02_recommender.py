import codecs 
from math import sqrt


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






class Recommender:


    """ 
    Initialize recommender
    Currently, if data is dictionary the recommender is initialized to it.
    For all other data types of data, no initialization occurs.
    * k is the k value for k nearest neighbor
    * metric is which distance formula to use
    * n is the maximum number of recommendations to make 
    """
    def __init__(self, data, k=1, metric='pearson', n=5):

        self.k = k
        self.metric = metric
        self.n = n
        
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        
        if self.metric == 'pearson':
            self.fn = self.pearson

        # if data is dictionary set recommender data to it
        if type(data).__name__ == 'dict':
            self.data = data




    """ 
    Return n top ratings for user with id 
    """
    def userRatings(self, id, n):

        ratings = self.data[id]
        print(len(ratings))
        ratings = list(ratings.items())
        
        # finally sort and return
        ratings.sort(key = lambda artistTuple: artistTuple[1], reverse = True)
        
        return ratings[:n]
        

        


    """
    Calculates Pearson coefficient
    """
    def pearson(self, rating1, rating2):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        
        if n == 0:
            return 0
        
        # now compute denominator
        denominator = ( sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n) )
        
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator


    """ 
    Creates a sorted list of users based on their distance to username 
    """
    def computeNearestNeighbor(self, username):

        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username], self.data[instance])
                distances.append((instance, distance))
        
        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        
        return distances

    
    """ 
    Give list of recommendations 
    """
    def recommend(self, user):

       recommendations = {}
       
       # first get list of users  ordered by nearness
       nearest = self.computeNearestNeighbor(user)

       # now get the ratings for the user
       userRatings = self.data[user]

       # determine the total distance
       totalDistance = 0.0
       for i in range(self.k):
          totalDistance += nearest[i][1]
       
       # now iterate through the k nearest neighbors
       # accumulating their ratings
       for i in range(self.k):
          
          # compute slice of pie 
          weight = nearest[i][1] / totalDistance
          
          # get the name of the person
          name = nearest[i][0]
          
          # get the ratings for this person
          neighborRatings = self.data[name]
          
          # get the name of the person
          # now find bands neighbor rated that user didn't
          for artist in neighborRatings:
             if not artist in userRatings:
                if artist not in recommendations:
                   recommendations[artist] = (neighborRatings[artist] * weight)
                else:
                   recommendations[artist] = (recommendations[artist] + neighborRatings[artist] * weight)
       
       # now make list from dictionary (converts book ids to actual titles)
       recommendations = list(recommendations.items())

       # finally sort (index 1 is rating) and return
       recommendations.sort(key = lambda artistTuple: artistTuple[1], reverse = True)

       # Return the first n items
       return recommendations[:self.n]

