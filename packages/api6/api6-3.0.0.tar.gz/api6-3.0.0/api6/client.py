from api6 import Encryption
from json import dumps,loads
from requests import post
from random import seed
from random import randint
from pathlib import Path
from random import choices, randint
from time import time
from re import finditer, sub
from base64 import b64encode
from io import BytesIO
from tempfile import NamedTemporaryFile
from mutagen import mp3, File
from filetype import guess
from os import system, chmod, remove
from pathlib import Path
import time
from tqdm import tqdm
import os
from urllib3 import PoolManager, ProxyManager
import asyncio
from termcolor import colored
import pyfiglet
font = pyfiglet.Figlet(font='slant')
ascii_text = font.renderText('Luis api6')
print(ascii_text)
class Client:
	def __init__(self, auth:str,key:str=None,palqform:str='Android',pak:str='app.rbmain.a',v:str="3.4.3",type:str="rubika"):
		self.palqform = palqform
		self.v = v
		self.requ = PoolManager()
		self.pak = pak
		self.auth = auth
		self.auth_send = Encryption.authSet(auth)
		self.t = "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"
		if key == None:
			self.key = None
		else:
			privateKey = key.replace('=','')
			privateKey = privateKey.replace("\n","")
			privateKey = privateKey.replace("-----BEGIN RSA PRIVATE KEY-----","")
			privateKey = privateKey.replace("-----END RSA PRIVATE KEY-----","")
			self.key = privateKey
		if type == "rubika":
			self.url = "https://messengerg2c98.iranlms.ir/"
		else:
			 if type == "shad":
			 	self.url = "https://shadmessenger32.iranlms.ir/"
	def requests(self, input, method):
	   client = {"app_name": "Main", "package": self.pak, "app_version": self.v, "lang_code": "fa", "platform": self.palqform}
	   method_payload = {"input": input, "method": method, "client": client}
	   method_payload = dumps(method_payload)
	   data_enc = Encryption.encrypt(method_payload, self.auth)
	   sign = Encryption.sign_rsa(self.key, data_enc)
	   data = {"api_version": "6", "data_enc": data_enc, "sign": sign, "auth": self.auth_send}
	   Luis =  loads(self.requ.request("POST", url=self.url, body=dumps(data)).data.decode('utf-8'))
	   data_enc = Luis['data_enc']
	   data = Encryption.decode(data_enc, self.auth)
	   data = loads(data)
	   return data
	def getUser(self):
		return self.requests({},"getUserInfo")
	def joinGroup(self,link:str):
		return self.requests({"hash_link":link},'joinGroup')
	def sendMessage(self,goid:str,text:str,id:str=None):
		return self.requests({"object_guid":goid,"text":text,"rnd":str(randint(9282873, 102662617171)),"reply_to_message_id":id},"sendMessage")
	def leaveGroup(self,goid):
		return self.requests({"group_guid":goid},"leaveGroup")
	def joinChannelAction(self,goid):
		return self.requests({"channel_guid":goid,"action":"join"},"joinChannelAction")
	def leaveChannelAction(self,goid):
		return self.requests({"channel_guid":goid,"action":"Leave"},"joinChannelAction")
	def getServiceInfo(self):
		return self.requests({"service_guid":"s0B0e8da28a4fde394257f518e64e800"},"getServiceInfo")
	def deleteMessages(self,goid,id):
		return self.requests({"object_guid":goid,"message_ids":[id],"type":"Local"},"deleteMessages")
	def deleteMessagesAcon(self,goid,id):
		return self.requests({"object_guid":goid,"message_ids":[id],"type":"Global"},"deleteMessages")
	def getGroupInfo(self, goid:str):
		return self.requests({"group_guid":goid},"getGroupInfo")
	def groupPreviewByJoinLink(self, link:str):
		return self.requests({"hash_link":link},"groupPreviewByJoinLink")
	def channelPreviewByJoinLink(self, link:str):
		return self.requests({"hash_link":link},"channelPreviewByJoinLink")
	def updateUsername(self, id:str):
		return self.requests({"username":id},"updateUsername")
	def getGroupAllMembers(self, goid:str,start_id=None,text=None):
		return self.requests({"group_guid":goid,"search_text":text,"start_id":start_id},"getGroupAllMembers")
	def searchGlobalObjects(self, text):
		return self.requests({"search_text":text},"searchGlobalObjects")
	def updateProfile(self,name,bio):
		return self.requests({"first_name":name,"bio":bio,"updated_parameters":["first_name","bio"]},"updateProfile")
	def getObjectByUsername(self,user):
		return self.requests({"username":user},"getObjectByUsername")
	def getUserInfo(self,user):
		return self.requests({"user_guid":user},"getUserInfo")
	def getChats(self,start_id=None):
		return self.requests({"start_id":start_id},"getChats")
	def getChannelInfo(self,goid):
		return self.requests({"channel_guid":goid},"getChannelInfo")
	def joinChannelByLink(self,link):
		return self.requests({"hash_link":link},"joinChannelByLink")
	def setChatAdmin(self,goid,goidm):
		type = self.getType(goid)
		return self.requests({f"{type.lower()}_guid":goid,"member_guid":goidm,"action":"SetAdmin","access_list":["ChangeInfo","ViewMembers","ViewAdmins","PinMessages","SendMessages","EditAllMessages","DeleteGlobalAllMessages","AddMember","SetJoinLink","SetAdmin"]},f"set{type}Admin")
	def requestChangeObjectOwner(self,goid,goidm):
		return self.requests({"object_guid":goid,"new_owner_user_guid":goidm},"requestChangeObjectOwner")
	def getMySessions(self):
		return self.requests({},"getMySessions")
	def terminateOtherSessions(self):
		return self.requests({},"terminateOtherSessions")
	def getLinkFromAppUrl(self,link):
		return self.requests({"app_url":link},"getLinkFromAppUrl")
	def forwardMessages(self,goid,togoid,id:list):
		return self.requests({"from_object_guid":goid,"to_object_guid":togoid,"message_ids":id,"rnd":str(randint(9282873, 102662617171))},"forwardMessages")
	def getMessages(self,goid,id:int=None,type="Min",filterType:str=None):
		return self.requests({"object_guid":goid,f"{type.lower()}_id":id,"sort":f"From{type}","filter_type":filterType},"getMessages")
	def votePoll(self,id,num:int):
		num = num - 1
		return self.requests({"poll_id":id,"selection_index":num},"votePoll")
	def editMessage(self,goid,id,text):
		return self.requests({"object_guid":goid,"message_id":id,"text":text},"editMessage")
	def getContacts(self,start_id=None):
		return self.requests({"start_id":start_id},"getContacts")
	def getAvailableReactions(self):
		return self.requests({},"getAvailableReactions")
	def getMyGifSet(self):
		return self.requests({},"getMyGifSet")
	def getBlockedUsers(self,start_id=None):
		return self.requests({"start_id":start_id},"getBlockedUsers")
	def getPrivacySetting(self):
		return self.requests({},"getPrivacySetting")
	def getMessagesInterval(self,goid,id,type=None):
		return self.requests({"object_guid":goid,"middle_message_id":id,"filter_type":type},"getMessagesInterval")
	def getTime(self):
		return self.requests({},'getTime')
	def getChatsUpdates(self):
		data = self.getTime()["data"]['time']
		p = {"state":data}
		return self.requests(p,"getChatsUpdates")
	def getMessagesUpdates(self, goid):
		time = self.getTime()['data']['time']
		return self.requests({"object_guid":goid,"state":time},'getMessagesUpdates')
	def getTopChatUsers(self):
		return self.requests({},"getTopChatUsers")
	def removeFromTopChatUsers(self,guid:str):
		return self.requests({"user_guid":guid},"removeFromTopChatUsers")
	def leaveChat(self,guid):
		type = getType(guid)
		if type == "Group":
			return self.leaveGroup(guid)
		if type == "Channel":
			return self.leaveChannelAction(guid)
	def getChatLink(self,guid:str):
		type = self.getType(guid)
		input = {f"{type.lower()}_guid":guid}
		name = f"get{type}Link"
		return self.requests(input,name)
	def setChatAdmin(self,guid,toguid,action:str):
		chatType = self.getType(guid)
		name = f"set{chatType}Admin"
		input = {
            f"{chatType.lower()}_guid": guid,
            "member_guid": toguid,
            "action": action,
            "access_list": []
        }
		return self.requests(input,name)
	def addChatMember(self,guid,mamber:list):
		chatType = self.getType(guid)
		name = f"add{chatType}Members"
		input = {
                f"{chatType.lower()}_guid": guid,
                "member_guids": mamber
            }
		return self.requests(input,name)
	def banChatMember(self,guid,mamber:str,actoin:str):
		chatType = self.getType(guid)
		name = f"ban{chatType}Member"
		input = {
                f"{chatType.lower()}_guid": guid,
                "member_guid": mamber,
                "action": actoin
		}
		return self.requests(input,name)
	def getBannedChatMembers(self,guid,startId:str):
		chatType = self.getType(guid)
		name = f"getBanned{chatType}Members"
		input = {
                f"{chatType.lower()}_guid": guid,
                "start_id": startId
		}
		return self.requests(input,name)
	def getChatInfo(self,guid):
		type = self.getType(guid)
		if type == "User":
			return self.getUserInfo(guid)
		if type == "Group":
			return self.getGroupInfo(guid)
		if type == "Channel":
			return self.getChannelInfo(guid)
	def joinChat(self,guidorlink):
		if "https://rubika.ir/" in guidorlink :
			if "https://rubika.ir/joing/" in guidorlink:
				guidorlink = guidorlink.replace("https://rubika.ir/joing/","")
				return self.joinGroup(guidorlink)
			if "https://rubika.ir/joinc/" in guidorlink:
				guidorlink = guidorlink.replace("https://rubika.ir/joinc/","")
				return self.joinChannelByLink(guidorlink)
		else:
			if "@" in guidorlink:
				guid = self.getObjectByUsername(guidorlink.replace("@",""))['data']['channel']['channel_guid']
				return self.joinChannelAction(guid)
			else:
				return self.joinChannelAction(guidorlink)
	def getChatAllMembers(self,guid,startId:str=None,text:str=None):
		chatType = self.getType(guid)
		name = f"get{chatType}AllMembers"
		input = {
                f"{chatType.lower()}_guid": objectGuid,
                "search_text": text,
                "start_id": startId
            }
		return self.requests(input,name)
	def getChatAdminMembers(self,guid,startId=None):
		chatType = self.getType(guid)
		name = f"get{chatType}AdminMembers"
		input = {
                f"{chatType.lower()}_guid": guid,
                "start_id": startId
            }
		return self.requests(input,name)
	def createChatVoiceChat(self,guid):
		chatType = self.getType(guid)
		name = f"create{chatType}VoiceChat"
		input = {f"{chatType.lower()}_guid":guid}
		return self.requests(input,name)
	def joinVoiceChat(self,guid,id:str):
		myGuid = self.getUser()['data']['user']['user_guid']
		chatType = self.getType(guid)
		name = f"join{chatType}VoiceChat"
		input = {
                "chat_guid": guid,
                "sdp_offer_data": "v=0\no=- -6112403547879777339 2 IN IP4 127.0.0.1\ns=-\nt=0 0\na=group:BUNDLE 0\na=msid-semantic: WMS audio0\nm=audio 9 UDP\\/TLS\\/RTP\\/SAVPF 111\nc=IN IP4 0.0.0.0\na=rtcp:9 IN IP4 0.0.0.0\na=ice-ufrag:IqUf\na=ice-pwd:mwo47t9uImp1xuV9T1HBKcPD\na=ice-options:trickle\na=fingerprint:sha-256 44:84:68:B4:AE:68:1A:2A:D6:35:CB:CF:3F:EA:F6:59:BD:25:1F:E0:B2:35:49:FF:7A:72:80:6F:F4:4D:FC:0D\na=setup:passive\na=mid:0\na=sendrecv\na=msid:audio0 audio0\na=rtcp-mux\na=rtpmap:111 opus\\/48000\\/2\na=rtcp-fb:111 transport-cc\na=fmtp:111 minptime=10;useinbandfec=1\na=rtpmap:110 telephone-event\\/48000\na=ssrc:1343160491\na=ssrc:1343160491 msid:audio0 audio0\na=ssrc:1343160491 mslabel:audio0\na=ssrc:1343160491 label:audio0",
                "self_object_guid": myGuid,
                "voice_chat_id": id
            }
		return self.requests(input,name)
	def leaveChatVoiceChat(self,guid,id:str):
		chatType = self.getType(guid)
		name = f"leave{chatType}VoiceChat"
		input = {
                f"{chatType.lower()}_guid": guid,
                "voice_chat_id": id
            }
		return self.requests(input,name)
	def setActionChat(self,guid,action:str):
		name = "setActionChat"
		input = {
                "object_guid": guid,
                "action": action
            }
		return self.requests(input,name)
	def seenChats(self,listsenn:dict):
		name = "seenChats"
		input = {"seen_list": seenList}
		return self.requests(input,name)
	def seenChatMessages(self,guid,min:str,max:str):
		chatType = self.getType(guid)
		name = f"seen{chatType}Messages"
		input = {
                f"{chatType.lower()}_guid": guid,
                "min_id": min,
                "max_id": max
            }
		return self.requests(input,name)
	def sendChatActivity(self,guid,activity:str):
		name = "sendChatActivity"
		input = {
                "object_guid": guid,
                "activity": activity
            }
		return self.requests(input,name)
	def searchChatMessages(self,guid,text:str):
		name = "searchChatMessages"
		input = {
                "object_guid": guid,
                "search_text": text,
                "type": "Text"
		}
		return self.requests(input,name)
	def getAvatars(self,guid):
		name = "getAvatars"
		input = {"object_guid": guid}
		return self.requests(input,name)
	def deleteAvatar(self,guid,id:str):
		name = "deleteAvatar"
		input = {
                "object_guid": guid,
                "avatar_id": id
            }
		return self.requests(input,name)
	def deleteChatHistory(self,guid,lastId:str):
		name = "deleteChatHistory"
		input = {
                "object_guid": guid,
                "last_message_id": lastId
            }
		return self.requests(input,name)
	def deleteUserChat(self,guid,lastId):
		name = "deleteUserChat"
		input = {
                "user_guid": guid,
                "last_deleted_message_id": lastId
            }
		return self.requests(input,name)
	def getChatReaction(self,guid,min:str,max:str):
		name = "getChatReaction"
		input = {
                f"object_guid": guid,
                "min_id": min,
                "max_id": max
            }
		return self.requests(input,name)
	def setChatUseTime(self,guid,time:int):
		name = "setChatUseTime"
		input = {
                "object_guid": guid,
                "time": time
            }
		return self.requests(input,name)
	def setBlockUser(self,guid,action):
		name = "setBlockUser"
		input = {
                "user_guid": guid,
                "action": action
            }
		return self.requests(input,name)
	def checkUserUsername(self,usermame):
		name = "checkUserUsername"
		input = {"username":usermame}
		return self.requests(input,name)
	def addGroup(self,namee:str,mamberList:list):
		name = "addGroup"
		input = {
                "title": namee,
                "member_guids": mamberList
            }
		return self.requests(input,name)
	def getGroupMentionList(self,guid:str,searchMention:str=None):
		name = "getGroupMentionList"
		input = {
                "group_guid": guid,
                "search_mention": searchMention
            }
		return self.requests(input,name)
	def addChannel(self,namee,description:str=None,type:str="Public"):
		name = "addChannel"
		input = {
            "title": namee,
            "description": description,
            "member_guids": [],
            "channel_type": type
        }
		return self.requests(input,name)
	def updateChannelUsername(self,guid,user):
		name = "updateChannelUsername"
		input = {
                "channel_guid": guid,
                "username": user
            }
		return self.requests(input,name)
	def checkChannelUsername(self,user):
		name = "checkChannelUsername"
		input = {
                "username": user
            }
		return self.requests(input,name)
	def getChannelSeenCount(self,guid,min:str,max:str):
		name = "getChannelSeenCount"
		input = {
                "channel_guid": guid,
                "min_id": min,
                "max_id": max
            }
		return self.requests(input,name)
	def sendLocation(self,guid,latitude:int, longitude:int):
		rnd = str(randint(9282873, 102662617171))
		name = "sendMessage"
		input = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "object_guid":guid,
                "rnd": rnd
            }
		return self.requests(input,name)
	def commonGroup(self,guid):
		input = {
		"user_guid": guid
		}
		return self.requests(input,"commonGroup")
	def clickMessageUrl(self,guid,id,link):
		name = "clickMessageUrl"
		input = {
		"object_guid": guid,
		"link_url": link,
		"message_id": id
		}
		return self.requests(input,name)
	def resendCodeRecoveryEmail(self,rmz):
		name = "resendCodeRecoveryEmail"
		input = {
		"password": rmz
		}
		return self.requests(input,name)
	def setupTwoStepVerification(self,ramz,heds):
		name = "setupTwoStepVerification"
		input = {
		"hint": heds,
		"password": rmaz
		}
		return self.requests(input,name)
	def actionOnMessageReaction(self,guid,massId:str,id:int,action:str="Add"):
		name = "actionOnMessageReaction"
		input = {
                "action": action,
                "object_guid": objectGuid,
                "message_id": massId,
                "reaction_id": id
            }
		return self.requests(input,name)
	def abortTwoStepSetup(self):
		return self.requests({},"abortTwoStepSetup")
	def getProfileLinkItems(self,guid):
		input = {
		"object_guid": guid
		}
		return self.requests(input,"getProfileLinkItems")
	def getWalletTransactionMessage(self,a,b):
		input = {
		"access_transfer": a,
		"transfer_id": b
		}
		return self.requests(input,"getWalletTransactionMessage")
	def setPinMessage(self,guid,id:str,action:str):
		name = "setPinMessage"
		input = {
                "object_guid": guid,
                "message_id": id,
                "action": action
            }
		return self.requests(input,name)
	def getMessagesById(self,guid,id:list):
		name = "getMessagesById"
		input = {
                "object_guid": guid,
                "message_ids": id
            }
		return self.requests(input,name)
	def getMessageShareUrl(self,guid,id:str):
		name = "getMessageShareUrl"
		input = {
                "object_guid": guid,
                "message_id": id
            }
		return self.requests(input,name)
	def votePoll(self,pollId:str,im:int):
		im = im - 1
		name = "votePoll"
		input = {
                "poll_id": pollId,
                "selection_index": im
            }
		return self.requests(input,name)
	def logout(self):
		input = {}
		name = "logout"
		return self.requests(input,name)
		return self.requests(input,name)
	def discardCall(self,id:str):
		name = "discardCall"
		input = {
                "call_id": id,
                "duration": None,
                "reason": "Disconnect"
            }
		return self.requests(input,name)
	def sendBogToGroup(self,guid):
		rnd = str(randint(9282873, 102662617171))
		input = {"object_guid":guid,
		"rnd":"818779",
		"file_inline":None,
		"text":"Luis Luis'\n","metadata":{"meta_data_parts":[{"from_index":0,"length":4,
		"type":"MentionText","mention_text_object_guid":"u0GmeSL014a1aef06b715748a7d23d08","mention_text_object_type":"User"},{"from_index":5,
		"length":4,
		"type":"MentionText","mention_text_object_guid":"u0GmeSL014a1aef06b715748a7d23d08)'\n","mention_text_object_type":"User"}]}}
		return self.requests(input,"sendMessage")
	def sendMessageHyperLink(self,guid,text,link,id:str=None):
		input = {"object_guid":guid,"rnd":str(randint(9282873, 102662617171)),"text":text,"reply_to_message_id":id,"metadata":{"meta_data_parts":[{"from_index":0,"length":len(text),"link":{"hyperlink_data":{"url":link},"type":"hyperlink"},"type":"Link"}]}}
		return self.requests(input,"sendMessage")
	def sendMessageMentionText(self,guid,text,id=None):
		input = {"object_guid":guid,"text":text,"rnd":str(randint(9282873, 102662617171)),"reply_to_message_id":id,"metadata":{"meta_data_parts":[{"type":"MentionText","mention_text_object_guid":guid,"from_index":0,"length":len(text),"mention_text_object_type":"User"}]}}
		return self.requests(input,"sendMessage")
	def getMessageAllGroup(self,guid,number:int=10):
		last = self.getGroupInfo(guid)['data']['chat']['last_message']['message_id']
		list = []
		for x in range(int(number)):
				p = self.getMessages(guid,last,"Max")
				if "new_max_id" in p['data']:
					last = p['data']['new_max_id']
				list += p['data']['messages']
		return list
	def getMessageAllChannel(self,guid,number:int=10):
			last = self.getChannelInfo(guid)['data']['chat']['last_message_id']
			list =[]
			for x in range(int(number)):
				p = self.getMessages(guid,last,"Max")
				if "new_max_id" in p['data']:
					last = p['data']['new_max_id']
				list += p['data']['messages']
			return list
	def getChatsAll(self):
		input = {"start_id":None}
		list = []
		re = self.requests(input,"getChats")
		num=0
		for x in range(int(10)):
			start_id = int(len(re)) + int(num)
			if "data" in re:
				list += re['data']['chats']
			re = self.requests({"start_id":start_id},"getChats")
		return list
	def requestCall(self,guid,type=None):
		name = "requestCall"
		input = {
                "call_type": type,
                "library_versions": ["2.7.7","2.4.4"],
                "max_layer": 92,
                "min_layer": 65,
                "sip_version": 1,
                "support_call_out": True,
                "user_guid": guid
            }
		return self.requests(input,name)
	def sendSignalData(self,call_id,data=None):
		input = {
		"call_id": call_id,
		"data": data
		}
		return self.requests(input,"sendSignalData")
	def getSignalingData(self,call_id):
		input = {
		"call_id": call_id
		}
		return self.requests(input,'getSignalingData')
	def loginDisableTwoStep(self,emile,pas,phone):
		name = "loginDisableTwoStep"
		input = {
		"email_code": emile,
		"forget_password_code_hash": pas,
		"phone_number": phone
		}
		return self.requests(input,name)
	def deleteMyGifSet(self,file):
		name = "removeFromMyGifSet"
		input = {
		"file_id": file
		}
		return self.requests(input,name)
	def requestDeleteAccount(self):
		name = "requestDeleteAccount"
		input = {}
		return self.requests(input,name)
	def replyRequestObjectOwner(self,guid):
		name = "replyRequestObjectOwner"
		input = {
		"action": "Reject",
		"object_guid": guid
		}
		return self.requests(input,name)
	def getPendingObjectOwner(self,guid):
		name = "getPendingObjectOwner"
		input = {
		"object_guid": guid
		}
		return self.requests(input,name)
	def sendGroupVoiceChatActivity(self,guid,user,activity,id):
		name = "sendGroupVoiceChatActivity"
		input = {
		"voice_chat_id": id,
		"group_guid": guid,
		"participant_object_guid": user,
		"activity": activity
		}
		return self.requests(input,name)
	def getPollStatus(self,poll):
		name = "getPollStatus"
		input = {
		"poll_id": poll
		}
		return self.requests(input,name)
	def Authrandom(self):
	       auth = ""
	       meghdar = "qwertyuiopasdfghjklzxcvbnm"
	       for string in range(32):
	       	auth += choice(meghdar)
	       return auth
	def acceptCall(self,call_id,type=None):
		input = {
		"call_id": call_id,
		"library_versions":  ["2.7.7","2.4.4"],
		"max_layer": 92,
		"min_layer": 65
		}
		return self.requests(input,"acceptCall")
	def getTrendStickerSets(self,start_id=None):
		name = "getTrendStickerSets"
		input = {
		"start_id": start_id
		}
		return self.requests(input,name)
	def searchStickerSets(self,text):
		name = "searchStickerSets"
		input = {
		"start_id": None,
		"search_text": text
		}
		return self.requests(input,name)
	def removeGroup(self,guif):
		name = "removeGroup"
		input = {
		"group_guid": guid
		}
		return self.requests(input,name)
	def getGroupDefaultAccess(self,guid):
		name = "getGroupDefaultAccess"
		input = {
		"group_guid": guid
		}
		return self.requests(input,name)
	def stoptSupperBot(self,guid):
		return self.requests({
	"bot_guid": guid
	},"stopBot")
	def getBotInfo(self,guid):
		name = "getBotInfo"
		input = {
		"bot_guid": guid
		}
		return self.requests(input,name)
	def getGroupMentionList(self,guid,text=None):
		name = "getGroupMentionList"
		input = {
		"group_guid": guid,
		"search_mention": text
		}
		return self.requests(input,name)
	def sendContect(self,chat_guid,user_guid,phone,firstname,lastname=None):
		name = "sendMessage"
		input = {
		"object_guid": chat_guid,
		"type": "ContactMessage",
		"message_contact": {
		"first_name": firstname,
		"last_name": lastname,
		"phone_number": phone,
		"user_guid": user_guid
		},
		"rnd": str(randint(9282873, 102662617171))
		}
		return self.requests(input,name)
	def setChatUseTime(self,guid,time:int):
		name = "setChatUseTime"
		input = {
		"time": time,
		"object_guid": guid
		}
		return self.requests(input,name)
	def sendMessageAPICall(self,guid,text,id,baton_id):
		name = "sendMessageAPICall"
		input = {
		"message_id": id,
		"aux_data": {
		"button_id": baton_id
		},
		"object_guid": guid,
		"text": text
		}
		return self.requests(input,name)
	def getContactsLastOnline(self,guid:list):
		name = "getContactsLastOnline"
		input = {
		"user_guids": guid
		}
		return self.requests(input,name)
	def deleteContact(self,guid):
		name = "deleteContact"
		input = {
		"user_guid": guid
		}
		return self.requests(input,name)
	def getContactsUpdates(self):
		time = int(self.getTime()['data']["time"]) - 200
		name = "getContactsUpdates"
		input = {
		"state": time
		}
		return self.requests(input,name)
	def sendPoll(self,guid,question:str,options:list,messageId:str=None, multipleAnswers:bool = False,anonymous:bool = True,quiz:bool = False):
		name = "createPoll"
		input = {
		"allows_multiple_answers": multipleAnswers,
		"correct_option_index": None,
		"is_anonymous": anonymous,
		"object_guid": guid,
		"options": options if len(options) >= 2 else ["Luis","not eror api6"],
		"question": question,
		"type": "Quiz" if quiz else "Regular",
		"reply_to_message_id": messageId,
		"rnd": str(randint(9282873, 102662617171))
		}
		return self.requests(input,name)
		
	def report(self,guid,type:nt=102,text:str=None):
		if not type in [102, 101, 104, 103, 105, 106, 100]:
			return "not type"
		else:
			name = "reportObject"
			if not type == 100:
				input = {
				"object_guid": guid,
				"report_type": type,
				"report_type_object":"Object"
				}
				return self.requests(input,name)
			else:
				input = {
				"object_guid": guid,
				"report_type": type,
				"report_type_object": "Object",
				"report_description": text
				}
				return self.requests(input,name)
	def actionOnMessageReaction(self,guid,mass,id:int=1,type="Add"):
	 	input = {
	 	"action": type,
	 	"message_id": mass,
	 	"object_guid": guid,
	 	"reaction_id": id
	 	}
	 	return self.requests(input,"actionOnMessageReaction")
	def reportObject(self,guid,text):
		name = "reportObject"
		input = {
                "object_guid": guid,
                "report_description": text,
                "report_type": 100,
                "report_type_object": "Object"
            }
		return self.requests(input,name)
	
	def getType(self, guid:str):
		user = guid[0]
		if user == "u":
			return "User"
		if user == "c":
			return "Channel"
		if user == "g":
			return "Group"
	def convert_seconds(self, seconds):
	       minutes, seconds = divmod(seconds, 60)
	       return f"{int(minutes)} minutes and {int(seconds)} seconds"
	def requestSendFile(self, file:str):
		file_name = str(file.split("/")[-1])
		self.name = file_name
		size = Path(file).stat().st_size
		self.size = size
		self.mime = file.split(".")[-1]
		input = {"file_name":file_name,"size":size,"mime":self.mime}
		return self.requests(input,'requestSendFile')
	def uplodFile(self, file:str):
		chunkSize=131072
		p = self.requestSendFile(file=file)
		hash = p['data']['access_hash_send']
		url = p['data']['upload_url']
		id = p['data']['id']
		d = p['data']['dc_id']
		byte_data = open(file, "rb").read()
		total_part = (len(byte_data) - 1) // 131072 + 1
		parts = [byte_data[i:i + 131072] for i in range(0, len(byte_data), 131072)]
		for part_number, part_data in enumerate(parts, start=1):
		          headers = {
		                              'auth': self.auth,
		                              'file-id': id,
		                              'access-hash-send': hash,
		                              'accept-encoding': 'qzip',
		                              'chunk-size': str(len(part_data)),
		                              'content-length': str(len(part_data)),
		                              'part-number': str(part_number),
		                              'total-part': str(total_part)
		                              }
		                              
		          start_time = time.time()
		          print(headers)
		          response = post(url=url, data=part_data, headers=headers)
		          elapsed_time = time.time() - start_time
		          remaining_time = (total_part - part_number) * elapsed_time
		          upload_speed = len(part_data) / elapsed_time / 1024 / 1024
		          counter = 0
		          m = "0"
		          print(f"Part {part_number}/{total_part}")
		          m = f"Part {part_number}/{total_part}"
		                              
		          
		hash = loads(response.text)['data']['access_hash_rec']
		files = open(file, "rb").read()
		json =  {"id":id,"hash":hash,"size":self.size,"name":self.name,"mime":self.mime,"dc":d,"file":files}
		return json
            
	def uploadAvatar(self,file:str):
		goid = self.getUser()['data']['user']['user_guid']
		hash_rec = self.uplodFile(file)
		input = {"object_guid":goid,"thumbnail_file_id":hash_rec['id'],"main_file_id":hash_rec['id']}
		return self.requests(input,'uploadAvatar')
	def uploadAvatarBog(self,file:str,files:str):
		goid = self.getUser()['data']['user']['user_guid']
		hash_rec = self.uplodFile(file)
		to = self.uplodFile(files)
		input = {"object_guid":goid,"thumbnail_file_id":hash_rec['id'],"main_file_id":to['id']}
		return self.requests(input,'uploadAvatar')
	def uploadAvatarBogGroup(self,file:str,files:str,link):
		goid = self.joinGroup()['data']['group']['group_guid']
		hash_rec = self.uplodFile(file)
		to = self.uplodFile(files)
		input = {"object_guid":goid,"thumbnail_file_id":hash_rec['id'],"main_file_id":to['id']}
		return self.requests(input,'uploadAvatar')
	def postTmp(self, input,name):
		client = {"app_name":"Main","package":self.pak,"app_version":self.v,"lang_code":"fa","platform":self.palqform}
		method = {"client":client,"input":input,"method":name}
		dataEnc = Encryption.encrypt(method,selg.auth)
		api = {"api_version":"6","tmp_session":self.auth,"auth":None,"data_enc":dataEnc}
		p = post(url=self.url,json=api)
		return loads(Encryption.decode(loads(p.text)['data_enc'],self.auth))
	def registerDevice(self):
		rnd = str(randint(9282873, 10266261277277171))
		input = {"app_version":"MA_3.4.3","device_hash":rnd,"device_model":"api6","is_multi_account":False,"lang_code":"fa","system_version":"SDK 28","token":"","token_type":"Firebase"}
		return self.requests(input,'registerDevice')
	def sendCode(self, phone):
		phone = "##" + str(phone)
		phone = phone.replace('##0','')
		phone = phone.replace('##','')
		phone = '98'+ phone
		input = {"phone_number":str(phone),"send_type":"SMS"}
		return self.postTmp(input,'sendCode')['data']['phone_code_hash']
	def sendCodePass(self,phone,pas):
		phone = "##" + str(phone)
		phone = phone.replace('##0','')
		phone = phone.replace('##','')
		phone = '98'+ phone
		input = {"phone_number":str(phone),"send_type":"SMS","pass_key":pas}
		return self.postTmp(input,'sendCode')['data']['phone_code_hash']
	def signln(self,phone,hash,code):
		phone = "##" + str(phone)
		phone = phone.replace('##0','')
		phone = phone.replace('##','')
		phone = '98'+ phone
		key = Encryption.getKey()
		pubic_key = Encryption.authSet(key[0])
		private_key = Envryption.toPrivate(key[1])
		private_key = private_key.replace('-----BEGIN RSA PRIVATE KEY-----\n','')
		private_key = private_key.replace('\n-----END RSA PRIVATE KEY-----','')
		input = {
		"phone_number": str(phone),
		"phone_code_hash": str(hash),
		"phone_code": str(code),
		"public_key": pubic_key,
		}
		p = self.postTmp(input,'signIn')
		authOld = p['data']['auth']
		auth = Encryption.decrypt_rsa(authOld,private_key)
		self.auth = auth
		self.key = private_key
		m = self.registerDevice()
		return [auth,private_key]
	def sendViceBog(self,goid,file:str):
		rnd = str(randint(9282873, 102662617171))
		p = self.uplodFile(file=file)
		input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"Voice","is_spoil":False,"time":10000000009900000},"object_guid":goid,"rnd":rnd}
		p = self.requests(input,"sendMessage")
		return p
	def sendFile(self,goid,file:str):
		rnd = str(randint(9282873, 102662617171))
		p = self.uplodFile(file=file)
		input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"File","is_spoil":False},"object_guid":goid,"rnd":rnd}
		p = self.requests(input,"sendMessage")
		return p
	def sendViceBog(self,goid,file:str):
		rnd = str(randint(9282873, 102662617171))
		p = self.uplodFile(file=file)
		input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"Voice","is_spoil":False,"time":99000000009900000},"object_guid":goid,"rnd":rnd}
		pp = self.requests(input,"sendMessage")
		return pp
	def sendFileBog(self,goid,file:str):
		rnd = str(randint(9282873, 102662617171))
		p = self.uplodFile(file=file)
		input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":99999999999999999,"mime":p['mime'],"access_hash_rec":p['hash'],"type":"File","is_spoil":False},"object_guid":goid,"rnd":rnd}
		p = self.requests(input,"sendMessage")
		return p
	def sendGifBog(self,goid,file:str):
		width, height = [100,100]
		rnd = str(randint(9282873, 102662617171))
		p = self.uplodFile(file=file)
		input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"Gif","is_spoil":False,"time":999990990000,"height":height,"width":width,"auto_play":False,"thumb_inline":self.t},"object_guid":goid,"rnd":rnd}
		p = self.requests(input,"sendMessage")
		return p
	def getVoiceDuration(bytes:bytes) -> int:
	       file = BytesIO()
	       file.write(bytes)
	       file.seek(0)
	       return mp3.MP3(file).info.length
	def sendVice(self,goid,file:str):
	       rnd = str(randint(9282873, 102662617171))
	       p = self.uplodFile(file=file)
	       file = BytesIO()
	       file.write(p['file'])
	       file.seek(0)
	       time = mp3.MP3(file).info.length
	       input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"Voice","is_spoil":False,"time":int(time)},"object_guid":goid,"rnd":rnd}
	       p = self.requests(input,"sendMessage")
	       return p
	def sendMusic(self,goid,file:str):
	       rnd = str(randint(9282873, 102662617171))
	       p = self.uplodFile(file=file)
	       file = BytesIO()
	       file.write(p['file'])
	       file.seek(0)
	       time = mp3.MP3(file).info.length * 1
	       audio = File(BytesIO(p['file']), easy=True)
	       if audio and "artist" in audio:
	       	get = audio["artist"][0]
	       input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"Music","is_spoil":False,"time":int(time),"music_performer":get},"object_guid":goid,"rnd":rnd}
	       p = self.requests(input,"sendMessage")
	       return p
	def sendImage(self,goid,file:str):
	       from PIL import Image
	       rnd = str(randint(9282873, 102662617171))
	       p = self.uplodFile(file=file)
	       byte = p['file']
	       image = Image.open(BytesIO(byte))
	       width, height = image.size
	       if height > width:
	           new_height = 40
	           new_width  = round(new_height * width / height)
	       else:
	           new_width = 40
	           new_height = round(new_width * height / width)
	       image = image.resize((new_width, new_height), Image.LANCZOS)
	       changed_image = BytesIO()
	       image.save(changed_image, format="PNG")
	       thigo = b64encode(changed_image.getvalue()).decode("UTF-8")
	       width, height = Image.open(BytesIO(byte)).size
	       input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"Image","is_spoil":False,"width":width,"height":height,"thumb_inline":thigo},"object_guid":goid,"rnd":rnd}
	       p = self.requests(input,"sendMessage")
	       return p
	def sendVideo(self,goid,file:str):
	       from tinytag import TinyTag
	       rnd = str(randint(9282873, 102662617171))
	       p = self.uplodFile(file=file)
	       bytes = p['file']
	       from PIL import Image
	       getvideo = TinyTag.get(file)
	       width, height = [100,100]
	       input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"Video","is_spoil":False,"time":int(getvideo.duration * 1000),"height":height,"width":width,"thumb_inline":self.t},"object_guid":goid,"rnd":rnd}
	       p = self.requests(input,"sendMessage")
	       return p
	def sendGif(self,goid,file:str):
	       from tinytag import TinyTag
	       rnd = str(randint(9282873, 102662617171))
	       p = self.uplodFile(file=file)
	       bytes = p['file']
	       from PIL import Image
	       getvideo = TinyTag.get(file)
	       width, height = [100,100]
	       input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"Gif","is_spoil":False,"time":int(getvideo.duration * 1000),"height":height,"width":width,"thumb_inline":self.t},"object_guid":goid,"rnd":rnd}
	       p = self.requests(input,"sendMessage")
	       return p
	def sendVideoMessage(self,goid,file:str):
	       from tinytag import TinyTag
	       rnd = str(randint(9282873, 102662617171))
	       p = self.uplodFile(file=file)
	       bytes = p['file']
	       from PIL import Image
	       getvideo = TinyTag.get(file)
	       width, height = [100,100]
	       input = {"file_inline":{"dc_id":p['dc'],"file_id":p['id'],"file_name":p['name'],"size":p['size'],"mime":p['mime'],"access_hash_rec":p['hash'],"type":"Video","is_spoil":False,"time":int(getvideo.duration * 1000),"height":height,"width":width,"thumb_inline":self.t,"is_round":True},"object_guid":goid,"rnd":rnd}
	       p = self.requests(input,"sendMessage")
	       return p
	def download(self,link,path:str=None):
		linkFrom = self.getLinkFromAppUrl(link)
		luis = linkFrom['data']['link']['open_chat_data']
		p = self.getMessages(luis['object_guid'],luis['message_id'])
		hash = p['data']['messages'][0]['file_inline']
		fileId = hash['file_id']
		dcId = hash['dc_id']
		accessHashRec = hash['access_hash_rec']
		fileName = hash['file_name']
		size = int(hash['size'])
		chunkSize = 262143
		attempt = 0
		maxAttempts  = 2
		headers= {
            "auth": self.auth,
            "access-hash-rec": accessHashRec,
            "dc-id": str(dcId),
            "file-id": str(fileId),
            "Host": f"messenger{dcId}.iranlms.ir",
            "client-app-name": "Main",
            "client-app-version": self.v,
            "client-package": self.pak,
            "client-platform": self.palqform,
            "Connection": "Keep-Alive",
            "Content-Type": "application/json",
            "User-Agent": "okhttp/3.12.1"
        }
		url = f"https://messenger{dcId}.iranlms.ir/GetFile.ashx"
		response = self.requ.request("POST",preload_content=False,headers=headers,url=url)
		type=fileName.split(".")[-1]
		data:bytes = b""
		num = 0
		for x in response:
			data += x
			print(f"{ste(num)}/{len(response)}")
		if path == None:
			path = None
		else:
			with open(path, 'wb') as file:
				file.write(data)
		return data
class rubino:
	def  __init__(self, auth:str=None):
		self.auth = auth
	def method(auth,input,name,url= 'https://rubino5.iranlms.ir/'):
		method = {"api_version":"0","auth":auth,"client":{"app_name":"Main","app_version":"3.6.4","lang_code":"fa","package":"app.rbmain.a","platform":"Android"},"data":input,"method":name}
		p = post(url=url,json=method)
		return loads(p.text)
	def Uploder(self, file:str,id:str):
		with open(file) as f:
			size = f.seek(0, 2)
		input = {"file_name":"m.jpg","file_size":size,"file_type":"Picture","profile_id":id}
		p = self.method(self.auth,input,'requestUploadFile')
		up = p['data']['server_url']
		fileId = p['data']['file_id']
		hs = p['data']['hash_file_request']
		byte_file = open(file, 'rb').read()
		heders = {"auth":self.auth,"file-id":fileId,"chunk-size":str(len(byte_file)),"total-part":"1","part-number":"1","hash-file-request":hs}
		pos = post(url=up,headers=heders)
		p = pos.text
		p= loads(p)
		try:
			m = p['data']['hash_file_receive']
		except Exception:
				print('')
		dataEnc = {"auth":self.auth,"id":fileId,"hs":hs,"hash_file_receive":m}
		return dataEnc
	def addStory(self,file,id):
			p = self.Uploder(self.auth,file,id)
			idd = p['id']
			hs = p['hs']
			hash = p['hash_file_receive']
			rnd = random.randint(71772818,128827710)
			input = {"duration":0,"file_id":idd,"hash_file_receive":hash,"height":1280,"profile_id":id,"rnd":rnd,"story_type":"Picture","thumbnail_file_id":idd,"thumbnail_hash_file_receive":hash,"width":720}
			name = "addStory"
			return self.method(self.auth,input,name,self.url)
	def addPost(self, file , id):
		p = self.Uploder(self.auth,file,id)
		idd = p['id']
		hs = p['hs']
		hash = p['hash_file_receive']
		rnd = random.randint(71772818,128827710)
		input = {"caption":"Luis","file_id":idd,"hash_file_receive":hash,"height":800,"profile_id":id,"post_type":"Picture","rnd":rnd,"tagged_profiles":[],"thumbnail_file_id":idd,"thumbnail_hash_file_receive":hash,"width":800}
		name = "addPost"
		p = self.method(self.auth,input,name,self.url)
		return p
	def getProFileList(self):
	   data = {
	   "equal": False,
	   "limit": 10,
	   "sort": "FromMax"
	   }
	   name = 'getProfileList'
	   return self.method(self.auth,data,name,self.url)
	def folo(auth,id,myId):
		data = {"followee_id":id,"f_type":"Follow","profile_id":myId}
		name = 'requestFollow'
		return self.method(self.auth,data,name,self.url)
	def addCode(self):
		data = {"auth":self.auth,"api_version":"0","client":{"app_name":"Main","app_version":"2.1.4","package":"m.rubika.ir","platform":"PWA","lang_code":"fa"},"data":{"type":"wincodeprize","barcode":"chalesh1402prize*norouz1403rubino"},"method":"getBarcodeAction"}
		p = post(url='https://barcode2.iranlms.ir',json=data)
		return p
	def postText(auth,id,post,idto):
		data = {"content":"Luis","post_id":post,"post_profile_id":idto,"profile_id":id}
		name = "addComment"
		return self.method(self.auth,data,name,self.url)
class rubika(Client):...
class bot(Client):...
class RobotRubika(Client):...
class Luis(Client):...
class BotX(Luis):...
class client(Luis):...
class auth(Luis):...
class private(Luis):...
class privateKey(Luis):...
class key(Luis):...
class methods(Luis):...
class shad(Luis):...	