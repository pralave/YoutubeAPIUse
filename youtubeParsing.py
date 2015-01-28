from xml.dom import minidom as md
import urllib


class Query():
    def __init__(self,feed_id=1,max_results=1,time='today'):
        self.feed_id = feed_id
        self.max_results = max_results
        self.time = time
        
        
    def queries(self):
        if self.feed_id == 1:
            information = urllib.urlopen("http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?max-results=%d&time=%s" %(self.max_results,self.time))
        elif self.feed_id == 2:
            information = urllib.urlopen("http://gdata.youtube.com/feeds/api/standardfeeds/top_favorites?max-results=%d&time=%s" %(self.max_results,self.time))
        elif self.feed_id == 3:
            information = urllib.urlopen("http://gdata.youtube.com/feeds/api/standardfeeds/most_viewed?max-results=%d&time=%s" %(self.max_results,self.time))
        else :
            print 'input feed id is wrong'
            
        root = md.parse(information)
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
            #userData = User(a)
            print a
            print videoData #,userData
            

    
class User(Query):
    def __init__(self,author_name):
        self.author_name = author_name.replace(' ','').upper()
        author_info = urllib.urlopen('http://gdata.youtube.com/feeds/api/users/%s' %(self.author_name))
        author_root = md.parse(author_info)
        entries = author_root.getElementsByTagName('entry')
        stats = entries[0].getElementsByTagName('yt:statistics')
        self.subscribersCount = stats[0].getAttribute('subscriberCount')
        self.totalUploadViews = stats[0].getAttribute('totalUploadViews')

    
    

    def __str__(self):
        return 'number of subscribers = {}\nTotal upload Views {}\n'.format(self.subscribersCount,self.totalUploadViews)


class Video(User):
    def __init__(self,title,viewCount,favCount):
        self.title = title
        self.viewCount = viewCount
        self.favCount = favCount

    def __str__(self):
        return 'Title={}\nView Count={}\nFavorite Count={}\n'.format(self.title,self.viewCount,self.favCount)
        

if __name__== '__main__':
    feed_id = int(raw_input('''1) Top Rated
                               2) Top Favorite
                               3) Most Viewed

                    choose your type(1 or 2 or 3)  '''))

    time = raw_input('''1) today
                        2) this_week
                        3) this_month

                    choose your time  ''')

    max_results = int(raw_input('input your maximum results  '))
    


    results = Query(feed_id,max_results,time)
    results.queries()







        
        

     
