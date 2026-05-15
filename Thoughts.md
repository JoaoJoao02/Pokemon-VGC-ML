## Parser

I need a way to take the teams posted in pokepast.es to the program and separate them by pokemon, ability, moves, etc etc.
In the first iteration I did a function that built a dictionairy out of the pokemons, but it was hard-coded, that means that from pokemon[0] it means the name of the pokemon, but the problem is that trough different generations/games there are different mechanics and some have IV's and EV's and other teams dont, that means that sometime pokemon[2] can be his mechanic while other can be his moves. So I fixed that aswell.
The scrapper is pratically done, concerns that raise to my mind are:
- Pokemons with no items - the @ identifier wouldn't work, so the identifier funtion would return an unknown.
- Duplicate URLs - I have to find someway to deduplicate them, because different folders may contain the same team, and since im looking for a point system to rank the teams, if I go to my excel with the teams and there is one world champion team that gives x amount of points, but then I go to another url net, that has the same team, it would get x amount of points again, inflating the result.
- Rate limit if I need to fetch a lot of URLs.
- Also right now, I haven't come against any moves with hifen, but I'll see if it is a problem, becuase it can be
- Right now EVs and IVs are hard-coded for ints, but if for some reason someone pastes it bad, it may crash the whole program, I dont think pokepaste even let's paste floats EVS but might be worth solving.
How I can fix it:
- Pokemons are always in the first line, so I can run the @ identifier with an if-else cicle to check if there is the @ outside the loop (worked fine)
- To be honest I don't really know how to handle that, I can just place the unique urls in a set, let's see how it holds (hard to handle complex data, so I'll take care of that in the Scrapper).
- Done
- Still didn't fix that, I'll think about later, I think this way still handles it properly
- try/except, but this may constitute a problem later in the ML model, because the model can have a lot of wrong data this way (I still have no idea if there are a lot of files that may contain this erros, perhaps none, but if there are, i should hardcode to turn the float into ints, because ivs/evs are ints, and it's wrong if there is an ev of 200.5).
For now I'm done with this, if I have anything else/any problem with the parser I'll post after this comment.

## Scraper
I saw a google docs from the community with plenty of data regarding pokemon teams, they were documenting several teams from several tournament for formats, even the new one (which I had a lot of trouble finding this early).

So this scraper, at first, was going to be conceived to search trough different sites and look for teams, now it will just take the parameters that I want from the google sheets and feed the links that I want to the parser.

I started with the "Pokemon Champions" format, decided which was the data that was worth keeping:
- Team ID - For Tracking
- Full Name, Tournament / Event and Rank - These ones are for my point system, who ranks different teams, I'll go in detail abut this system further down.
- PokePaste - The usefull link that I need to feed the Parser to retrieve the Pokemon team.

Then I defined the Point System columns
-- Point System --
This is a system that is defined to classify teams, to feed the Machine Learning model, so the model gives more importance to certain teams than others. For instance, if I want to build a team around a pokemon, normally a team that got taken to world championship is presumably better composed that a team from a content creator video or a pokemon showdown ladder game. That's why I decided to make it so tournament teams contribute 100 points to the model, showdown matches contribute 50, video/content creator contributes 25 and unknown contribute 10. 
At first I was also planning on giving each category of points a multiplier, for exemple the champion of a world champions would x3 the 100 points, but I decided against it because most of the times, the skill of the player also counts, so basically what I decided to do was to make the gap bigger between categories, and the prominence of a team gives it a boost in terms of points (Sneasler + Incineroar is good when appears 20 times in worlds, on the other hand Garchomp + Rotom can win some games and even place higher than some Sneasler + Incineroar because the player could be better or abusing a niche strategy, that doesn't mean that the combo is better.)

I also implemented some deduplication by URL's, there can't be 2 URL's that are equal, otherwise the team gets added twice if they are on multiple URL's in the dataset, tho I can sense it as a problem in the future since I want to build a web scraper to get teams from the web, which means that some teams might overlap, but have different URL's, probably in the future what I'll do is change the deduplication by URL to player name/tournament/format.

## Web Scraper
This is the program that let's me fetch the teams from web pages, first considerations before building it, is that I have to find a way trough the duplicate teams, also I'll need to build a new Parser to deal with getting teams from different sites, which is a thing that I'll look if I can build one for every site, maybe if they have the teams in html format from the web page I can look into it.

Scraping isn't hard from the web, I had to learn everyting from the beginning, so it's a new thing, but I feel like it's hard. I also feel like I'm getting much better at programming. 

The startegy that I got for now is: I'll fetch teams from team page and I manually check where the S/V format starts, and I scrape from there. From the team page, it tells me which tournaments, the tean got used and the player that used it, that helps with deduplication further down the line. I think I'll hard code everything that I fetch from Limitless to 100 points because there are only tournaments there. 

Going this route a thing that is bothering me is when I'm scraping trough the lists of tournaments/players name I am spliting by "-" but that can be a problem is the name of the player/tournament has an hifen in the middle, and also there is no way to handle the fact that it may have the palyer name but not the tournament so I'll take that into account.

How I solved: Each "li" element has 2 href, one of them for tournament and one for name, I fetched both "a" elements and associate with a dictionairy. That way I solve both problems up there.

Also there was a problem with the "Tournament Info" key in the parser -> I was associating two lists, one for tournaments and one for players, that may cause dificulties for deduplication because I have no way to associate the tournament to the player that way, so I changed it to a dictionairy inside a list inside the dictionairy.

For now I think the problem is almost solved, the only thing that I want to change for now is to implement a function that retrieves the format from the tournament page, that way I don't have to hard code it. I'll fetch format first in the tournament page and then inside that page I'll assign the teams that are there. 

ONE THING THAT IS GIVING ME A HUGE HEADACHE FOR DEDUPLICATION IS "WHAT IF IN THE LIMITLESS HAS ONE NAME FOR THE TOURNAMENT AND IN THE EXCEL HAS ANOTHER..." I can normalize tournament names, but how do I distuinguish between regional prague 2024 and 2025, even worse if they are in the same format, and I can't think of a way to solve this for now.

The last thing was the format/tournament scraper: In the team page we have a link with the tournament, so what I do is I get that link, "open" the link and get the tournament, there I scrape the format, and attach to the dictionairy.

## Thoughts after scraping
I have around 7000 teams, that is ok enough to at least get a partner/item recommendation.
I forgot about one thing that is actually important which is win rate, because stronger win rate between partners means stronger relationship, also if I want my model to predict counters I obviously need to know win rate, aswell as teams that played against each other and that is tough. I need to work on a formula for that. What I'll do is, I'll make a model for now that predicts the best partner, and I'll see if it works well enough, then I think about the problems that come after.