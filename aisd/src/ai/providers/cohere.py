import logging

import cohere

from aisd.src.ai.providers.base import Provider

logger = logging.getLogger(__name__)


class CohereProvider(Provider):
    def get_songs_from_prompt(self, prompt: str) -> list[str]:
        co = cohere.Client(
            api_key=self.api_key,
        )
        response = co.chat(
            model="command-r-08-2024",
            message=self.prompt_template.format(prompt),
            temperature=0.2,
            chat_history=[
                {
                    "role": "User",
                    "message": "give me a list of christmast songs that i can mix for christmast party on CDJ. i want list of 50 titles. no numeration just a next line",
                },
                {
                    "role": "Chatbot",
                    "message": "Christmas (Baby Please Come Home) Darlene Love\nWhite Christmas The Drifters\nBack Door Santa Clarence Carter\nRun Rudolph Run Chuck Berry\nSanta Claus Is Back In Town Elvis Presley\nRudolph The Red Nosed Reindeer Temptations\nHappy Xmas (War Is Over) John Lennon & Yoko Ono\nMerry Christmas Baby Charles Brown\nSanta Claus Is Coming To Town Jackson 5\nRockin' Around The Christmas Tree Brenda Lee\nJingle Bell Rock Bobby Helms\nRudolph The Red-Nosed Reindeer The Ventures\n(It's Gonna Be A) Lonely Christmas The Orioles\nSanta Baby Eartha Kitt\nChristmas Time's A-Coming Mac Wiseman\nChristmas Celebration B.B. King\nFather Christmas The Kinks\nIf We Make It Through December Merle Haggard\nChristmas Celebration Weezer\nStep Into Christmas Elton John\nSanta's Rap Treacherous Three\nFeliz Navi-Nada El Vez\nSomeday At Christmas Stevie Wonder\nMerry Christmas Baby Otis Redding\nNothing For Christmas The Reducers\nThat Punchbowl Full Of Joy Sonny Columbus & His Del Fuegos\nPlease Come Home For Christmas Charles Brown\nEvery Day Will Be Like A Holiday William Bell\nDon't Believe In Christmas The Sonics\nWho Say There Ain't No Santa Claus Ron Holden\nBoogie Woogie Santa Claus Mabel Scott\nFairytale Of New York The Pogues & Kirsty MacColl\nHere Comes Santa Claus Gene Autry\nHow I Hate To See Christmas Come Around Jimmy Witherspoon\n(Everybody's Waitin' For) The Man With The Bag Baby It's Cold Outside Dean Martin\nWe Three Kings The Cherry-Tree Carol\nChildren, Go Where I Send Thee Christians, awake, salute the happy morn\nChristmas Song (Chestnuts Roasting on an Open Fire) (Merry Christmas to You) Robert Wells and Mel Tormé\nCome and I will sing you Come, Thou Long Expected Jesus\nCoventry Carol (Lullay, Thou Tiny Little Child) Ding Dong Merrily on High\nGood King Wenceslas",
                },
            ],
            prompt_truncation="AUTO",
            preamble="You are a song recommender for DJ/Mix/Producers also include classics. You are given a prompt and you need to generate a list of songs that match the prompt.",
            connectors=[{"id": "web-search"}],
        )
        logger.debug(f"Response from cohere model: {response.text}")
        return response.text.split("\n")
