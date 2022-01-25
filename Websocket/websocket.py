import requests
import json
import discord
from discord.ext import commands
import datetime
from sseclient import SSEClient
import aiohttp
import asyncio

class Websocket:
	
	def __init__(self):
		self.prize = 50
		self.web_url = "https://discord.com/api/webhooks/935505589642080277/oZ1aV-YFH5eWxWNjT47ptf023KgtuPIH11PpICMFUFsPEIzciOHwQsTLJRgxy_ajlwNk"
		self.token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFXeURtS0VhR0NweTFqb0twckRCYSJ9.eyJuaWNrbmFtZSI6InNha2htYW4yMDAxIiwibmFtZSI6InNha2htYW4yMDAxQGdtYWlsLmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci85NGUyZTFkZDdkYjE2YmQ0OGE2NzY2NDE5OWQ1NWIxMz9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnNhLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDIyLTAxLTIzVDE1OjEwOjUxLjgwMVoiLCJlbWFpbCI6InNha2htYW4yMDAxQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL2F1dGgubWltaXItcHJvZC5jb20vIiwic3ViIjoiYXV0aDB8NjFjYzMwODIzMjgxNmEwMDcxM2E2NmI4IiwiYXVkIjoiSm9vc0FWNU9qblVNYWpIdVR5RHB1WGM1OVRxQk5aYmMiLCJpYXQiOjE2NDMxMTI4MzYsImV4cCI6MTY0MzE0ODgzNiwibm9uY2UiOiJiVUp3Y3pGV2IwSlpNeTFhTkVaMmRtUkdUVTB4V25wVlZtWkJWRVZ0ZEZVek1Gb3dTMFZOVWxOb2R3PT0ifQ.hPk-3XasC552wdZHNlrh7SfBRO6xFdQIMirj3ylPWFXErGkSfwxUKmuiHmWSofsRPpBUWi9fsbnUrEy8s7Pi5JtfZc_yL0jtLuIgKHIQZhhnHRdiEJm-6TuHz4wGvDKmT5ziFTSLRgPFE76R_oGw7y4AQRptkLjQbYslNgMeUhdLRuyb0yOSbUPfAuNpymFUB6dJsI-6hWFMiPi0P6zMGNbch6WxzjTCQmjVQzTQmgQ6Z5KSosUA1kbz4g4uqQpYSGmW1CFerEitHd9h2FtRJowSGSFxH-a6TlcofUUMtr8Yv7yJBhmH6D7iecg9f3egvwqQMN10Sj0GmnxZNd2mOw:0x4357d1eE11E7db4455527Fe3dfd0B882Cb334357"
		self.ws_is_opened = False
		self.icon_url = "https://cdn.discordapp.com/emojis/924632014617972736.png"
		self.game_is_active = False
		self.game_id = None
		self.partner_id = None
		self.user_id = None
		self.bearer_token = None

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
					await self.send_hook("The token has expired!")
					raise commands.CommandError("Token has expired!")
				r = await response.json()
				data = r["data"]["data"][0]
				self.game_is_active = data["active"]
				image = data["backgroundImageLandscapeUrl"]
				topic = data["label"]
				description = data["description"]
				self.prize = data["reward"]
				time = data["scheduled"]
				time = datetime.datetime.fromtimestamp(int(time)/1000)
				time = time.strftime("%d-%m-%Y | %I:%M %p")
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
			"accept": "application/json, text/plain, */*",    "content-type":"application/json",
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
					await self.send_hook("Get access token error...")
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
					await self.send_hook("Host Error...(Game is not live)")
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
		except:
			return await self.send_hook("Failed to connect websocket!")
		self.ws_is_opened = True
		for msg in messages:
			event = msg.event
			data = json.loads(msg.data)
			await self.send_hook(event)
			if event == "GameStatus":
				pass

			elif event == "ViewCountUpdate":
				pass

			elif event == "QuestionStart":
				question = data["question"]
				question_number = data["number"]
				total_question = data["total"]
				option_1 = choices[0]["choice"]
				option_2 = choices[1]["choice"]
				option_3 = choices[2]["choice"]
				embed = discord.Embed(
					title = f"Question {question_number} out of {total_question}",
					description = question,
					color = discord.Colour.random(),
					timestamp = datetime.datetime.utcnow()
					)
				embed.add_field(name = "Option - 1", value = option_1, inline = False)
				embed.add_field(name = "Option - 2", value = option_2, inline = False)
				embed.add_field(name = "Option - 3", value = option_3, inline = False)
				embed.set_thumbnail(url = self.icon_url)
				embed.set_footer(text = "Mimir Quiz")
				await self.send_hook(embed = embed)

			elif event == "QuestionEnd":
				embed = discord.Embed(title = "Question End!", color = discord.Colour.random())
				await self.send_hook(embed = embed)

			elif event == "QuestionResult":
				question = data["question"]
				s = 0
				for index, choice in enumerate(data["choices"]):
					if correct == "true":
						ans_num = index + 1
						answer = choice["answer"]
						advance_players = choice["responses"]
					s += choice["responses"]
				eliminate_players = s - advance_players
				embed = discord.Embed(
					title = "Question Result!",
					description = question,
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
