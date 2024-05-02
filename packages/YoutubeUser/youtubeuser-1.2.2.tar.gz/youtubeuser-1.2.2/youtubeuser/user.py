import requests


def getUser(channel_name : str) :
  youtube = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={channel_name}&key=AIzaSyDBfcnjBerpgTFI5VCk_f3Rh-T_bc9LbEQ")
  if youtube.status_code == 200 :
     #get channel
      getchannel = youtube.json()["items"][0]
      #channel_name = getchannel["snippet"]["title"]
  
      #channel_id = getchannel["snippet"]["channelId"]
  
      #channel_description = getchannel["snippet"]["description"]
        
      #channel_profile = getchannel["snippet"]["thumbnails"]["default"]["url"]
      #channel_subscriber = getchannel.get("statistics", {}).get("subscriberCount")
  #JSON
      #data = {
    #"name" : channel_name,
    #"description" : channel_description,
    #"id" : channel_id,
    #"profile_url" : channel_profile,
    #"subscriber" : channel_subscriber
  #}
  
      return getchannel