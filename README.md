## Pokemon

The objective of this project is to create a website that helps new players getting into VGC (competitive Pokemon).

With the release of Pokemon Champions, one of the tallest barriers to entry is the teambuilding. When one's trying to build a team, the things that they have to take into account are:
- Pokemon competitive viability (stats, typing, movesets, items, abilities, nature)
- Pokemons that work well in the same team 
- Pokemons that work well against possible Pokemons that get brought by the opponent

There are endless possibilities.

I'll fetch data from Tournaments, Videos, Webpages, Games and use that to train an Machine Learning model that helps the user building a team.
I'll build another model that helps the Machine Learning model to make decisions by using damaging calculations for certain pokemon interactions.

Some example of prompts:
Q: "I love Charizard, build me a team that works well with Charizard"
A: "Charizard has great synergy with Sun-based teams, it works well with other pokemons that normally want the Sun to be set up like Venasaur. Since Charizard is rather slow, we should also add a Pokemon that can set up tailwind..."

Q: "Great team, can you help me with the stats of each Pokemon?"
A: "Sure, statistically Charizard stats tend to be rather offensive, like 32 SpA, 32Speed and 2 Hp with a Modest Nature, Venasaur when paired with Charizard also likes to be more on the offensive side..."

Q: "With the team that you helped me build, I'm having a lot of trouble to deal with Sneasler, is there a way to account for Sneasler without changing the team much"
A: "Sneasler has a lot of trouble to deal with Aerodactyl, maybe you can change your Whimsicott that was setting up tailwind and you can use Aerodactyl instead. Also you can change that stats of your Charizard for 14 Def so it doesn't get 2 hit KO by Sneasler..."
