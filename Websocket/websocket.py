import requests
import json
import discord
from discord.ext import commands
import datetime
from sseclient import SSEClient
import aiohttp
import asyncio
from bs4 import BeautifulSoup
google_question = "https://google.com/search?q="
question_number = total_question = 0

class Websocket:
	
	def __init__(self):
		self.prize = 50
		self.web_url = "https://discord.com/api/webhooks/935505589642080277/oZ1aV-YFH5eWxWNjT47ptf023KgtuPIH11PpICMFUFsPEIzciOHwQsTLJRgxy_ajlwNk"
		self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFXeURtS0VhR0NweTFqb0twckRCYSJ9.eyJuaWNrbmFtZSI6InNha2htYW4yMDAxIiwibmFtZSI6InNha2htYW4yMDAxQGdtYWlsLmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci85NGUyZTFkZDdkYjE2YmQ0OGE2NzY2NDE5OWQ1NWIxMz9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnNhLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDIyLTAxLTI1VDE3OjA4OjI2LjYxMVoiLCJlbWFpbCI6InNha2htYW4yMDAxQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL2F1dGgubWltaXItcHJvZC5jb20vIiwic3ViIjoiYXV0aDB8NjFjYzMwODIzMjgxNmEwMDcxM2E2NmI4IiwiYXVkIjoiSm9vc0FWNU9qblVNYWpIdVR5RHB1WGM1OVRxQk5aYmMiLCJpYXQiOjE2NDMxNjQ5ODAsImV4cCI6MTY0MzIwMDk4MCwibm9uY2UiOiJaSDVYTmpSWWZtOXdWVTVOZEhSeWNFSXhaMGhwUm05eWFqQkVSVFpHUkV4WFFVOUtjRWQ0Y0hOSE1nPT0ifQ.H_zit94kgEVMX5S_4DJZZChga-OflsmoU6fzy-BeHCbppjZiR1Qj84QIIlx4COS9J_ru1hXOTo1ioG4Higiev4KdZCsBljw3XZJhhZNM-T_bZuQxiRxvOMMxm4otKrOgh11LXrWJIZDQy4Q2PisDi_kVZJ5Jzzy8nfe-nUDRa29ZpCSpqgdmH2u9nFePvjU9kcptebjfYVWgLK66exw5iBNN6sFHihiaiy3hX0WeaLDJEPcCZhlB8q9lC6A3fjHFY7GgAAXTxuoIlvywrDaGKCD9tFXvWnx8ce4Lqm6kpdZb-BzbpSrEjYgTqKdxsswoZ3JBGQgusDhfC1rqafX6jw:0x4357d1eE11E7db4455527Fe3dfd0B882Cb334357"
		self.ws_is_opened = False
		self.icon_url = "https://cdn.discordapp.com/emojis/924632014617972736.png"
		self.game_is_active = False
		self.game_id = None
		self.partner_id = None
		self.user_id = None
		self.bearer_token = None

	def embeded(self,x):
		embed = discord.Embed(title = f"{x}", color = discord.Colour.random())
		return embed

	async def send_hook(self, content = "", embed = None):
		async with aiohttp.ClientSession() as session:
			webhook = discord.Webhook.from_url(self.web_url, adapter=discord.AsyncWebhookAdapter(session))
			await webhook.send(
				content = content,
				embed = embed,
				username = "Mimir Quiz",
				avatar_url = self.icon_url
				)
				
	async def get_quiz_details(self, get_type = None):
		url = "https://api.mimir-prod.com//games/list?type=play_free"
		headers = {
			"host": "api.mimir-prod.com",
			"authorization": f"Bearer {self.token}",
			"user-agent": "Mozilla/5.0 (Linux; Android 10; RMX1827) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36",
			"content-type": "application/json",
			"accept": "*/*",
			"origin": "https://app.mimirquiz.com",
			"referer": "https://app.mimirquiz.com/",
			"accept-encoding": "gzip, deflate",
			"accept-language": "en-US,en;q=0.9"
		}
		async with aiohttp.ClientSession() as session:
			async with session.get(url = url, headers = headers) as response:
				if response.status != 200:
					embed = self.embeded("The Auth token has expired!")
					await self.send_hook(embed = embed)
					raise commands.CommandError("Token has expired!")
				r = await response.json()
				data = r["data"]["data"][0]
				self.game_is_active = data["active"]
				image = data["backgroundImageLandscapeUrl"]
				topic = data["label"]
				description = data["description"]
				self.prize = data["reward"]
				time = f'<t:{int(data["scheduled"]/1000)}>'
				gameType = data["winCondition"]
				self.game_id = data["id"]
				self.partner_id = data["partnerId"]
				embed = discord.Embed(
					title = "Mimir Upcoming Quiz Details!",
					description = description,
					color = discord.Colour.random()
					)
				embed.add_field(name = "Quiz Topic :", value = topic, inline = False)
				embed.add_field(name = "Prize Money :", value = self.prize, inline = False)
				embed.add_field(name = "Date & Time :", value = time, inline = False)
				embed.set_thumbnail(url = image)
				if get_type == "send":
					await self.send_hook(embed = embed)

	async def get_access_token(self):
		await self.get_quiz_details()
		url = f"https://apic.us.theq.live/v2/oauth/token?partnerCode={self.partner_id}"
		headers = {
			"host": "apic.us.theq.live",
			"user-Agent": "Mozilla/5.0 (Linux; Android 10; RMX1827) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36",
			"accept": "application/json, text/plain, */*",
			"content-type":"application/json",
			"origin": "https://play.us.theq.live",
			"referer": "https://play.us.theq.live/",
			"accept-encoding": "gzip, deflate",
			"accept-language": "en-US,en;q=0.9"
		}
		post_data='{"mimir":{"accessToken":"token"}}'
		newdata = json.loads(post_data)
		newdata["mimir"]["accessToken"] = self.token
		post_data = json.dumps(newdata)
		async with aiohttp.ClientSession() as session:
			async with session.post(url = url, headers = headers, data = post_data) as response:
				if response.status != 200:
					embed = self.embeded("Get access token error!")
					await self.send_hook(embed = embed)
					raise commands.CommandError("Get access token error...")
				r = await response.json()
				new_token = r["oauth"]["accessToken"]
				token_type = r["oauth"]["tokenType"]
				self.user_id = r["user"]["id"]
				self.bearer_token = token_type + " " + new_token
				
	async def get_host(self):
		await self.get_access_token()
		url = f"https://apic.us.theq.live/v2/games/active/{self.game_id}?userId={self.user_id}"
		headers = {
			"Host": "apic.us.theq.live",
			"accept": "application/json, text/plain, */*",
			"authorization": f"{self.bearer_token}",
			"sec-ch-ua-mobile": "?1",
			"user-agent": "Mozilla/5.0 (Linux; Android 10; RMX1911) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36",
			"origin": "https://play.us.theq.live",
			"referer": "https://play.us.theq.live/",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "en-US,en;q=0.9,bn;q=0.8,hi;q=0.7"
		}
		async with aiohttp.ClientSession() as session:
			async with session.get(url = url, headers = headers) as response:
				if response.status != 200:
					embed = self.embeded("Host Error...(Game is not live)")
					await self.send_hook(embed = embed)
					raise commands.CommandError("Host Error")
				r = await response.json()
				data = r["game"]
				self.game_is_active = data["active"]
				host = data["host"]
				return host

	async def start_hook(self):
		host = await self.get_host()
		url = f"https://{host}/v2/event-feed/games/{self.game_id}"
		headers = {
			"Host": host,
			"Connection": "keep-alive",
			"Authorization": self.bearer_token,
			"Accept": "text/event-stream",
			"Cache-Control": "no-cache",
			"User-Agent": "Mozilla/5.0 (Linux; Android 10; RMX1827) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36",
			"Origin": "https://play.us.theq.live",
			"Sec-Fetch-Site": "same-site",
			"Sec-Fetch-Mode": "cors",
			"Referer": "https://play.us.theq.live/",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "en-US,en;q=0.9"
		}
		try:
			messages = SSEClient(url, headers = headers)
			embed = self.embeded("Websocket is Connected Successfully!")
			await self.send_hook(embed = embed)
		except:
			embed = self.embeded("Failed to connect websocket!")
			return await self.send_hook(embed = embed)
		self.ws_is_opened = True
		for msg in messages:
			event = msg.event
			if event == "QuestionStart":
				global google_question, question_number, total_question
				data = json.loads(msg.data)
				question = data["question"]
				question_number = data["number"]
				total_question = data["total"]
				choices = data["choices"]
				option_1 = choices[0]["choice"]
				option_2 = choices[1]["choice"]
				if len(choices) == 3: option_3 = choices[2]["choice"]
				if len(choices) == 4: option_4 = choices[3]["choice"]
				raw_question = str(question).replace(" ", "+")
				raw_options = str(option_1 + option_2 + option_3).replace(" ", "+")
				google_question = "https://google.com/search?q=" + raw_question
				search_with_all = "https://google.com/search?q=" + raw_question + raw_options
				
				embed = discord.Embed(
					title = f"Question {question_number} out of {total_question}",
					description = f"[{question}]({google_question})\n\n[Search with all options]({search_with_all})",
					color = discord.Colour.random(),
					timestamp = datetime.datetime.utcnow()
					)
				embed.add_field(name = "Option - 1", value = f"[{option_1}]({search_with_all})", inline = False)
				embed.add_field(name = "Option - 2", value = f"[{option_2}]({search_with_all})", inline = False)
				embed.add_field(name = "Option - 3", value = f"[{option_3}]({search_with_all})", inline = False)
				if len(choices) == 4: embed.add_field(name = "Option - 4", value = f"[{option_4}]({search_with_all})", inline = False)
				embed.set_thumbnail(url = self.icon_url)
				embed.set_footer(text = "Mimir Quiz")
				await self.send_hook(embed = embed)
				
				r = requests.get(google_question)
				soup = BeautifulSoup(r.text, 'html.parser')
				response = soup.find_all("span", class_="st")
				res = str(r.text)
				cnop1 = res.count(option_1)
				cnop2 = res.count(option_2)
				cnop3 = res.count(option_3)
				maxcount = max(cnop1, cnop2, cnop3)
				mincount = min(cnop1, cnop2, cnop3)
				embed = discord.Embed(title="**__Google Results !__**", color=0x000000)
				if cnop1 == maxcount:
					embed.description=f"**１. {option_1} : {cnop1}**  ✅\n**２. {option_2} : {cnop2}**\n**３. {option_3} : {cnop3}**"
				elif cnop2 == maxcount:
					embed.description=f"**１. {option_1} : {cnop1}**\n**２. {option_2} : {cnop2}**  ✅\n**３. {option_3} : {cnop3}**"
				else:
					embed.description=f"**１. {option_2} : {cnop1}**\n**２. {option_2} : {cnop2}**\n**３. {option_3} : {cnop3}**  ✅"
				await self.send_hook(embed = embed)

				r = requests.get(google_question)
				soup = BeautifulSoup(r.text , "html.parser")
				response = soup.find("div" , class_='BNeawe')
				result = str(response.text)
				embed = discord.Embed(
					description=result,
					color = discord.Colour.random(),
					timestamp = datetime.datetime.utcnow()
					)
				embed.set_footer(text="Search with Google")
				if option_1.lower() in result.lower():
					embed.title=f"**__Option １. {option_1}__**"
				elif option_2.lower() in result.lower():
					embed.title=f"**__Option ２. {option_2}__**"
				elif option_3.lower() in result.lower():
					embed.title=f"**__Option ３. {option_3}__**"
				else:
					embed.title=f"**__Direct Search Result !__**"
				await self.send_hook(embed = embed)

			elif event == "QuestionEnd":
				embed = discord.Embed(title = "Question has Ended!", color = discord.Colour.random())
				await self.send_hook(embed = embed)

			elif event == "QuestionResult":
				data = json.loads(msg.data)
				question = data["question"]
				total_players = 0
				for index, choice in enumerate(data["choices"]):
					if choice["correct"] == True:
						ans_num = index + 1
						answer = choice["choice"]
						advance_players = choice["responses"]
					total_players += choice["responses"]
				eliminate_players = total_players - advance_players
				embed = discord.Embed(
					title = f"Question {question_number} out of {total_question}",
					description = f"[{question}]({google_question})",
					color = discord.Colour.random(),
					timestamp = datetime.datetime.utcnow()
					)
				embed.add_field(name = "Correct Answer :", value = f"Option {ans_num}. {answer}", inline = False)
				embed.add_field(name = "Status :",
					value = f"Advancing Players : {advance_players}\nEliminated Players : {eliminate_players}",
					inline = False
				)
				embed.set_footer(text = "Mimir Quiz")
				embed.set_thumbnail(url = self.icon_url)
				await self.send_hook(embed = embed)

			elif event == "GameWinners":
				data = json.loads(msg.data)
				winners = int(data["winnerCount"])
				ans = (self.prize)/(winners)
				payout = float("{:.2f}".format(ans))
				embed = discord.Embed(title = "Game Summary !",
					description = f"● Payout : {payout}\n● Total Winners : {winners}\n● Prize Money : {self.prize}",
					color = discord.Colour.random(),
					timestamp = datetime.datetime.utcnow()
					)
				embed.set_thumbnail(url = self.icon_url)
				embed.set_footer(text = "Mimir Quiz")
				await self.send_hook(embed = embed)
				
			elif event == "GameEnded":
				embed = discord.Embed(title = "Game has Ended !",
					description = "Thanks for playing!", color = discord.Colour.random()
					)
				await self.send_hook(embed = embed)
				self.ws_is_opened = False
				return
