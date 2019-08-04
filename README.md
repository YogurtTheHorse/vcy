English: this repository contains code for „Voice Game Jam“ which was taking place in Indicator, SPb on Augusth 4th. Code is very dirty and presented only for an "educational" purposes. All code was written in 45 hours.

Русский: этот репозиторий содержит код для «Голосового гейм джема», который проходил в Индиакторе, СПб четвертого августа. Код очень грязный и представлен исключительно для «образовательных» целей. Вест код был написан в течение 45-и часов. Посмотреть мое выступление можно [тут](https://vk.com/video-162707306_456239094), оно начинается с 1:14.

# Run steps

1. Create Yandex.Alice skill
2. Put credentials to `web_utils/config.json`
3. Setup a webhook
4. It could work...

# Deps

Install all requirements from `requirements.txt`. You should install the Graphviz and add it to the system path. And also, you have to run mongo on a default port.

# Contributors

Most of the code is written by me, YogurtTheHorse, but some parts were written by [ScaryTreeFF](https://github.com/ScaryTreeFF). 
Game concept is a combination of mine and ScaryTreeFF's ideas.

# Core concept

The game is played on voice assistant (repo contains Yandex.Alice implementation) with russian language by two players. The first player is Oracle who is guarding a dungeon and the second is thief who stole something from it and trying to escape. Game is turn based. Thief should explore the dungeon and look for keys to open doors between them and exit.

In the same time Oracle should cast spells to stop rogue. To cast a spell wizzard have to say a sentence with a code word connected to a spell. They also may say only the code word, but thieff will hear all they says, and will be able to counterattack. Thief's goal is to, actually, find out all code words of each spell and successfully resist them by using correct anti-spell items they has.

