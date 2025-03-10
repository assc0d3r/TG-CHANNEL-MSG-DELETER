import asyncio
import os
from telethon import TelegramClient, events, types
import logging
import re
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

# Define environment variables if not provided in config file
API_ID = os.getenv("API_ID")
KEYWORD_PATTERN = os.getenv("KEYWORD_PATTERN")
SESSION = os.getenv("SESSION")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
API_HASH = os.getenv("API_HASH")
# Regex pattern for matching keywords (modify as needed)
#keyword_pattern = r'(?ims).*\b(R❤A|bik|akoam|sanjou|ironclad|zza|6113815320|7559738665|Salinan|dis|1939505067|Asham|cosmicduck|RoverX|Edgerunners|KMX|Frieren|newbsubs|S4G4R|Kartunisasi|Melon|kurdsubtitle|Urusei|GuodongSubs|Koby|Tenma|nAV1gator|AceAres|ReDone|pori|RISQUEMEGA|ASW|denisplay|AkihitoSubs|Globoplay|FplayFR|Hyouka|SedLyf|tooncore|400p|webm|DAT|GLaDOS|jfs24|NTSC|paheli|BollyFlix|MOCIESVERSE|DiRT|Sa3eed|Shahid|abdo|yom|VIU|Megas|BraveStarr|bionic|dsf|FraMeSToR|UJHS|HQCleanAUD|mamaa|yawnix|writers|THEKID|cfd|Ienai|Protozoan|Academia|SaizenYaba|btn|FraMeSToR|WatchiT|WM|moviesflicker|1XBET|Cman21|Paranoia|Recess|tribute|FckDubs|DCR|vedio|800MB|850MB|neutron|haveli|verdes|shorts|DVDremux|cbfm|edith|caffeine|skyfire|250mb|350mb|300mb|144mb|BRENTFORD|m2v|MIRCrew|tw4a|D&O|kaatera|Tottenham|LQ140170701|Fontaine|wmv|StevenUniverse|RH|SheRa|SubsPlus|ifo|bup|Occultcademy|250mb|400mb|700mb|kimo|mpeg|dadagiri|WeTVCorrected|MIRCrew|dhamakedaar|tw4a|D&O|Grandmaster|CHELSEA|TVSPOT|PARASYTE|HnY|Kakegurui|Returners|GJY|Jujutsu|Shinka|Superpoderosa|edv5|opv|subnow|NTb|LiveeviL|MyDaemon|Arcadia|EDGE2020|NOOBDL|ZIM|WASHiPATO|kappa|novice|pink|BlWorldNet|mpg|erza|Zom100|pantheon|UWU|Cleo|Berserk|ts|STORYBOARD|WOWmdsorcery|Jitsuryokusha|Ikenaikyo|Ikenaikyo|Filme|Amazingtranger|SamuraiJack|Kimizero|Katsudouki|S1|VINLAND|TAG|Nunes|SHINCHAN|jpg|Dance|Moozzi2|AniTV|HR|CV|serij|Boruto|NAME|OnePiece|gazoon|kobayashi|GMTeam|CleoManK|P9|fansub|Proxy|castlevania|Announcement|SanKyuu|Nado|DarkWispersIffylk|RedDevil|OnePiece|wma|Rx7|T3KASHi|Omniverse|russo|casting|intro|AQAD7QIAAo9eyUdy|rar|gif|tar|jpeg|bmp|tiff|mov|zip|mp4|7z|exe|apk|bin|3gp|vid|m4a|mp3|opus|flac|info|avi|txt|vhs|m2ts|m3u|m4b|m4v|top|cfd|mv|ts|8051|RyRo|Toonworld4all|vanshaj|extra|videoplayback|part|ANToNi|None|ucparadiso|Animesenpai4u|Anixlife|ASW|Datte13|DB|EMBER|judas|Kurina|Mo7tas|neosatsu|SAM|Setsugen|ShadoWalkeR|SubsPlus|trix|124p|1xbet|240p|2k|TamilMV|360p|480p|4k|540p|576P|AAJtAK|ACKZ|adaalat|AkatsukiXanimehub|Alibaba|ALLOUT|America|analysis|Anichintop|anime|Anime|Alliance|AnimePahe|Animerg|Animesenpai4u|AnimeX|Horizon|Anixverse|Anonymoose|application|aptitude|arab|Arabseed|Ass|attack|Australias|backend|Bank|Bhabhi|Bhagya|Bigg|Biology|Blog|Boolean|Breeze|cam|CameEsp|camprint|Camrip|camrip|canges|case|certificate|Chahatein|Challenge|CHANGE|chapter|chat|chef|Chinese|cima2cima9|cinema3d|cinevood|CIRCLES|clerk|client|coa|comedy|concept|CONICS|copy|course|cricket|csk|cum|data|database|dataset|day|dcan|debugging|deigo|Devilsfilm|diagram|dick|diploma|Diriliş|DKB|dodi|Doraemon|DVDrip|DVDscr|Education|EMBER|entrance|enum|episode|Ep|eporner|Erairaws|erotic|ertugrul|Ertuğrul|exam|facebook|facial|faltu|farsi|fifa|Flac|football|fps|French|friday|from|FumiRaws|fuzz|Game§|gangbang|gayab|genetry|gentry|genymotion|ghum|google|graphics|GUIDELINES|Gundam|Hall of C|Hatsuyuki|hdcam|hdcam|HDCAMRip|hdnewtamilmovies4k|HDScr|HDT|HDTC|Hdts|hdts|hekayat|moviesz|highlights|homeopathy|HorribleSubs|HQCAM|HQPreDVD|HQSPrint|HQSPrint|HQSprint|Html|HUSTLE|Hustler|IMDB|idol|imlie|Index|Indonesian|inserting|installation|interview|introduction|ipl|italian|iwannaplaychannel|japanese|java|javascript|judas|JySzE|Kaguyasam|Katha|Kathaa|Kehlata|keys|KHALIFA|kkr|koffee|Korean|Kusonime|laughter|launch|lec|lect|linkz|listcycle|logcat|lyric|main|Manchester|Mangastate|market|Masterbate|masterchef|maths|Mechanics|MiaM|Mobile|MODI|module|MTBB|muscle|naagin|Nacional|naruto|naughty|nazar|omi|opus|ORIENTATION|Orphanedone|ozclive|padding|paper|pdvd|pdvdrip|pee|periodic|permission|persian|phonics|Photoshop|php|physics|playlist|Png|Podcast|POKEMON|pooping|PornoD|ppt|pptx|practice|PREDVD|predvd|predvdrip|preview|probability|problems|programming|Project|projects|prompt|Properties|pushpa|Pussy|Puzzle|python|quant|rajjo|Rar|raw|reasoning|Receipe|reels|remastered|repack|report|Retr0|REVISION|Rododendron|ruby|rust|saregamapa|SaReGaMaPa|SAMEHADAKU|sample|Samsung|SASHA|savefbapp|sbi|school|scripting|ScrubsMofu|Security|SekhemSeichimReiki|senpai|sensei|setup|sgcinemas|ShadoWalkeR|signing|sir|smack|snooker|Sokudo|solution|song|sprint|sqlite|Srt|statistics|storage|strategy|structural|study|studyfever|subsplease|swallow|tagalog|TardSubs|task|Teaser|teminal|temptation|testing|Thermodynamics|titktok|tmkoc|tmv|Torrent|ToshY|track|trailer|trix|tutorial|types|UDF|understanding|upscale|url|Vagina|VHS|VID|VIXEN|vlog|Vob|VootKids|vulnerability|wagle|WhatsApp|WildBunch|wildcard|wob|wrestling|wwf|xvideos|Yameii|youtube|WWE|SH3LBY|Abystoma|Gugugaga|iaf|FitGirl|Freecoursesite|Koala|Kongming|BDMV|gigacoursecom|AIOVideos|TN|OrphanReDone|Zenryoku|Семьяшпиона|hchcsen|ullu|Bhojpuri|DBKUltimate|telegram|app|com|iso|DRAMADAYme|Smackdown|∆nkaj|crorepati|Radhakrishn|darq|kubo|VARYG|Toontastic|barbaad|Xspitfire911|renegades|kyunki|AkihitoSubs|RISQUEMEGA|Dancepro|dis|BOFURI|MaouGakuin|YuragiSou|Villainous|DokyuuHentaiHxEros|CyberpunkEdgerunners|ushio|sagas|MahouSensou|Tomodachi|MrKimiko|Shoukanshi|Azumanga|Tenchi|SharkTank|Sousou|Crocante|sujaidr|isekai|Kosaka|BTTH|Sakamoto|InitialD|Emmid|HoriMiya|Borax|Mocha|Keiei|Hi10|OASD|NCOP|Kaleidosubs|FateApocrypha|FateZero|Onmyoji|Hudie|Renascent|Koten|Gars|IPSO|YuGi|Dalton|Garshasp|Llamas|Katsugeki|Zestiria|Tesagure|ULTOR|Sav1or|Techmod|ufc|Hyakkano|Fashion|OTMCS|Gakuin|Jayce|chibiverse|MeM|ITA|Flugel|2TAMILMV|Raten|pelisenhd|streamershub|HODL|MULVAcoded|yawnix|FckDubs|MkvDrama|redone)\b'

file_name = None  # Initialize file_name variable as None

async def main():
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.start()

    entity = await client.get_entity(CHANNEL_USERNAME)

    async def process_media(message):
        # Check if the message contains a video
        if message.media and message.video:
            # Get the file name
            file_name = message.file.name

            # Proceed with current logic of checking for keywords and deleting files
            if file_name:
                text = message.message

                if re.search(KEYWORD_PATTERN, text, re.IGNORECASE):
                #if re.finditer(keyword_pattern, text, re.IGNORECASE):# | re.VERBOSE | re.MULTILINE):
                    try:
                        await message.delete()
                        print(f"Deleted video message with filename: {file_name}")
                    except Exception as e:
                        print(f"Error deleting video message: {e}")
                        await asyncio.sleep(45)  # Longer wait for potential flood wait errors
            else:
                # Handle files with None or empty string names
                try:
                    await message.delete()
                    print("Deleted video message with undefined filename.")
                except Exception as e:
                    print(f"Error deleting video message without filename: {e}")
                    await asyncio.sleep(45)
        else:
            # Ignore messages that are not video messages
            pass

    # @client.on(events.NewMessage(chats=entity, incoming=True))
    #async def handler(event):
        # await process_media(event.message)

    async def process_history():
        offset_id = 0
        limit = 100

        while True:
            messages = await client.get_messages(entity, limit=limit, offset_id=offset_id)
            if not messages:
                break

            for message in messages:
                # Process media messages only
                if message.media:
                    await process_media(message)

            offset_id = messages[-1].id
            await asyncio.sleep(9)  # Sleep for 9 seconds between batches

    await process_history()

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
