from xml.dom import minidom as md
from sys import exit
import urllib



class Query():
    def __init__(self,feed_id=1,max_results=1,time='today'):
        self.feed_id = feed_id
        self.max_results = max_results
        self.time = time
        
        
    def queries(self):
        try:
            if self.feed_id == 1:
                information = urllib.urlopen("http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?max-results=%d&time=%s" %(self.max_results,self.time))
            elif self.feed_id == 2:
                information = urllib.urlopen("http://gdata.youtube.com/feeds/api/standardfeeds/top_favorites?max-results=%d&time=%s" %(self.max_results,self.time))
            elif self.feed_id == 3:
                information = urllib.urlopen("http://gdata.youtube.com/feeds/api/standardfeeds/most_viewed?max-results=%d&time=%s" %(self.max_results,self.time))
            root = md.parse(information)

        except Exception :
            print 'input feed id is wrong.Try again'
            exit(0)
            
        entries = root.getElementsByTagName('entry')
        favCount,viewCount,authorNames,title =[],[],[],[]
        
        for entry in entries:
            author = entry.getElementsByTagName('author')
            authorNames.append(author[0].getElementsByTagName('name')[0].firstChild.data)
            stats = entry.getElementsByTagName('yt:statistics')
            favCount.append(stats[0].getAttribute('favoriteCount'))
            viewCount.append(stats[0].getAttribute('viewCount'))
            title.append(entry.getElementsByTagName('media:title')[0].firstChild.data)

        for a,t,f,v in zip(authorNames,title,favCount,viewCount):
            videoData = Video(t,v,f)
            print 'Uploader name = %s'%(a)
            userData = User(a)
            
            print videoData,userData
            

    
class User(Query):
    def __init__(self,author_name):
        self.author_name = author_name.replace(' ','').upper()
        try:
            author_info = urllib.urlopen('http://gdata.youtube.com/feeds/api/users/%s' %(self.author_name))
            author_root = md.parse(author_info)
            entries = author_root.getElementsByTagName('entry')
            stats = entries[0].getElementsByTagName('yt:statistics')
            self.subscribersCount = stats[0].getAttribute('subscriberCount')
            self.totalUploadViews = stats[0].getAttribute('totalUploadViews')
        except Exception:
            pass
        


    def __str__(self):
        try:
            return 'number of subscribers = {}\nTotal upload Views {}\n'.format(self.subscribersCount,self.totalUploadViews)
        except AttributeError:
            return 'no user data available'

class Video(User):
    def __init__(self,title,viewCount,favCount):
        self.title = title
        self.viewCount = viewCount
        self.favCount = favCount

    def __str__(self):
        return 'Title={}\nView Count={}\nFavorite Count={}\n'.format(self.title,self.viewCount,self.favCount)
        

if __name__== '__main__':
    while True:
        try:
            feed_id = int(raw_input('''1) Top Rated
2) Top Favorite
3) Most Viewed

choose your type(1 or 2 or 3)  '''))
            break
        except Exception:
            print 'Incorrect Input. Please enter 1 or 2 or 3'
    while True:        
        try:
            time = str(raw_input('''1) today
2) this_week
3) this_month

choose your time  '''))
            break
        except Exception:
            print 'Try again and please insert correct Input from above options'

    max_results = int(raw_input('input your maximum results  '))
    


    results = Query(feed_id,max_results,time)
    results.queries()







        
        

     
