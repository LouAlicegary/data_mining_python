from math import sqrt

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


