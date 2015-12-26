import codecs 
from math import sqrt


class recommender:


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
    Given product id number return product name 
    """
    def convertProductID2name(self, id):
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id


    """ 
    Return n top ratings for user with id 
    """
    def userRatings(self, id, n):

        print ("Ratings for " + self.userid2name[id])
        ratings = self.data[id]
        print(len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v) for (k, v) in ratings]
        
        # finally sort and return
        ratings.sort(key = lambda artistTuple: artistTuple[1], reverse = True)
        ratings = ratings[:n]
        
        for rating in ratings:
            print("%s\t%.1f" % (rating[0], rating[1]))
        

    """ 
    Loads the BX book dataset. Path is where the BX files are located 
    """
    def loadBookDB(self, path='BX-Dump/'):
        
        self.data = {}
        i = 0

        # First load book ratings into self.data
        f = codecs.open(path + "BX-Book-Ratings.csv", 'r', 'utf8')
        for line in f:
            i += 1
            #separate line into fields
            fields = line.split(';')
            user = fields[0].strip('"')
            book = fields[1].strip('"')
            rating = int(fields[2].strip().strip('"'))
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}
            currentRatings[book] = rating
            self.data[user] = currentRatings
        f.close()

        # Now load books into self.productid2name
        # Books contains isbn, title, and author among other fields
        f = codecs.open(path + "BX-Books.csv", 'r', 'utf8')
        for line in f:
            i += 1
            #separate line into fields
            fields = line.split(';')
            isbn = fields[0].strip('"')
            title = fields[1].strip('"')
            author = fields[2].strip().strip('"')
            title = title + ' by ' + author
            self.productid2name[isbn] = title
        f.close()

        #  Now load user info into both self.userid2name and
        #  self.username2id
        f = codecs.open(path + "BX-Users.csv", 'r', 'utf8')
        for line in f:
            i += 1
            #print(line)
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
            self.userid2name[userid] = value
            self.username2id[location] = userid
        f.close()
        
        return i   

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
       recommendations = [(self.convertProductID2name(k), v) for (k, v) in recommendations]

       # finally sort (index 1 is rating) and return
       recommendations.sort(key = lambda artistTuple: artistTuple[1], reverse = True)

       print "Recommendations:"
       for recommendation in recommendations[:self.n]:
          print("%s\t%.1f" % (recommendation[0], recommendation[1]))

       # Return the first n items
       return recommendations[:self.n]
