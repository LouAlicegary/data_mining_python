from chapter_02_recommender import recommender
from math import sqrt 

users = {
    "Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
    "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
    "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
    "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
    "Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
    "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
    "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
}



# Computes the Manhattan distance. Both rating1 and rating2 are dictionaries of the form
# {'The Strokes': 3.0, 'Slightly Stoopid': 2.5 ...}

def manhattan(rating1, rating2):

  distance = 0
 
  for key in rating1:
    if key in rating2:
      distance += abs(rating1[key] - rating2[key])
 
  return distance



# Computes the Minkowski distance. Both rating1 and rating2 are dictionaries of the form
# {'The Strokes': 3.0, 'Slightly Stoopid': 2.5 ...}
# r = 1 is Manhattan distance; r = 2 is Euclidian distance; r = oo is Supremum distance

def minkowski(rating1, rating2, r):

  distance = 0
 
  for key in rating1:
    if key in rating2:
      distance += pow(abs(rating1[key] - rating2[key]), r)
 
  return pow(distance, 1/r)


def pearson(rating1, rating2):
  
  sum_xi_yi = 0
  sum_xi    = 0
  sum_yi    = 0
  sum_x_2   = 0
  sum_y_2   = 0
  n         = 0
  
  for key in rating1:
    if key in rating2:
      n         += 1
      sum_xi    += rating1[key]
      sum_yi    += rating2[key]
      sum_x_2   += (rating1[key] ** 2)
      sum_y_2   += (rating2[key] ** 2)
      sum_xi_yi += (rating1[key] * rating2[key])

  if n == 0:
    return 0
  else:
    covar     = sum_xi_yi - (sum_xi * sum_yi / n)
    std_dev_x = sqrt(sum_x_2 - ((sum_xi ** 2) / n))
    std_dev_y = sqrt(sum_y_2 - ((sum_yi ** 2) / n))
    return covar / (std_dev_x * std_dev_y)



def cosine_similarity(rating1, rating2):
  
  dot_product = 0
  sum_x_2   = 0
  sum_y_2   = 0

  for key in rating1:
    sum_x_2   += (rating1[key] ** 2)
    if key in rating2:
      dot_product += (rating1[key] * rating2[key]) 

  for key in rating2:
    sum_y_2   += (rating2[key] ** 2)
 
  x_vector_length = sqrt(sum_x_2)
  y_vector_length = sqrt(sum_y_2)

  return dot_product / (x_vector_length * y_vector_length)


# Creates a sorted list of users based on their distance to username

def computeNearestNeighbor(username, users):

  distances = []

  for user in users:
    if user != username:
      distance = minkowski(users[user], users[username], 2)
      distances.append((distance, user))
      
      # sort based on distance -- closest first
      distances.sort()
 
  return distances


# Give list of recommendations
def recommend(username, users):
 
  recommendations = []

  # grab username's ratings
  userRatings = users[username]

  # find nearest neighbor and grab all their ratings
  nearest = computeNearestNeighbor(username, users)[0][1]
  neighborRatings = users[nearest]

  # now find bands neighbor rated that user didn't and append to rec list
  for artist in neighborRatings:
    if not artist in userRatings:
      recommendations.append((artist, neighborRatings[artist]))
 
  # (author note: using the fn sorted for variety - sort is more efficient)
  # key is an anonymous (lambda) function whose name (artistTuple) 
  # represents each object in the collection being sorted
  return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse = True)



""" ========================== ACTUALLY RUNNING CODE HERE =============================== """

print "\n\n"

# %.3f formats the float to 3 decimal places
print "The manhattan distance between Hailey and Veronica should be 2.0 => %.3f" % manhattan(users['Hailey'], users['Veronica'])
print "The manhattan distance between Hailey and Jordyn should be 7.5 => %.3f" % manhattan(users['Hailey'], users['Jordyn']) 

print "The computed Manhattan distances for Hailey are: %s" % computeNearestNeighbor("Hailey", users)

print "\n\n"

print "Recommended artists for Hailey are: %s" % recommend('Hailey', users) 
print "Recommended artists for Chan are: %s" % recommend('Chan', users)
print "Recommended artists for Sam are: %s" % recommend('Sam', users)
print "Recommended artists for Angelica are: %s" % recommend('Angelica', users)

print "\n\n"

print "Pearson coefficient between Angelica and Bill is %.3f" % pearson(users['Angelica'], users['Bill']) 
print "Pearson coefficient between Angelica and Hailey is %.3f" % pearson(users['Angelica'], users['Hailey']) 
print "Pearson coefficient between Angelica and Jordyn is %.3f" % pearson(users['Angelica'], users['Jordyn']) 

print "\n\n"

print "Cosine similarity between Angelica and Veronica is %.3f" % cosine_similarity(users['Angelica'], users['Veronica'])

print "\n\n"

r = recommender(users)
print "Jordyn's recommendations: %s" % r.recommend('Jordyn')
print "Hailey's recommendations: %s" % r.recommend('Hailey')

print "\n\n"

print "Loading CSV book data."
print "Result count: %s" % r.loadBookDB()

print "\n\n"

r.recommend('171118')

print "\n\n"

r.userRatings('171118', 5)

print "\n\n"