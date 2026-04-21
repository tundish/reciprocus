Research
========

Sources
-------

The most recent thinking related to Larson-like theory is not in print.
It is articulated in back-and-forth conversation in online forums.
From time to time this will be summarized in the shape of an article or technical note.

The Reciprocal Systems forum was intended by those who set it up to be the central repository for such material.
However, by modern standards it is not easy to navigate and hosting is likely under-resourced.
There are many dead links. Sadly most of the original contributors are no longer around.

I recently opened an account there but found that my ability to participate was limited.
The time to moderate and approve my posts ran to several days. So I fear for the future of that site as a nexus of
research activity.

The user [MWells](https://reciprocal.systems/phpBB3/memberlist.php?mode=viewprofile&u=58) has posted a batch of
articles explaining his *DFT* system. From my initial reading, this is intended to be fully compatible with Larson.
It also explicitly incorporates later thinking by Peret, Nehru, Gopi and others.

I have decided to make this my starting point.

Scraping
--------

For my own safety and comfort I have downloaded the relevant material.
I used an open source [scraper](https://pypi.org/project/forumscraper/) as follows:

    forumscraper -d DFT --pages-max 40 https://reciprocal.systems/phpBB3/viewforum.php?f=7

The resulting JSON files have no suffix but that can be remedied like so:

```bash
$ cd DFT
$ for i in `ls *[0-9]`; do mv -v $i ${i}.json; done
```

Formatting
----------

The HTML rendered by the BB forum software is complex and disorderly. I wrote a script to clean it up.


Ownership
---------

I have archived this material to protect against a potential future outage of the Reciprocal Systems forum.
All ownership rests with the original authors. Copyright is theirs and not mine.
I deeply respect the intellect and the dedication that were necessary to create it.
I hope my reformatting of the material will be seen as useful but if you are an author who does not wish
to appear in this repository then please create a GitHub [issue](https://github.com/tundish/reciprocus/issues)
and I will remove it.

