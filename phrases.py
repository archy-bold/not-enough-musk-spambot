#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

submission_replies = {
    "tesla": [
        "We don’t control the federal reserve. The higher the rates, the harder they fall",
        "The fun police made us do it (sigh)"],
    "files": ["!!", "Interesting"],
    "twitter": [
        "Looking into this.",
        "This is bizarre. Looking into it.",
        "Interesting",
        "Concerning",
        "Extremely concerning",
        "Negative feedback is a good thing",
        "\U0001F3AF", # bullseye
        "\U0001F4AF", # 100
        "\U0001F4AF\U0001F3AF\U0001F923", # 100/bullseye/laugh
        "Twitter is now trending to breakeven if we keep at it.",
        "Something fundamental is wrong",
        "Something is wrong",
        "Turns out we just needed to blow on the cartridge",
        "I get all my opinions from Twitter"],
    " bot": [
        "Looking into this.",
        "This is bizarre. Looking into it.",
        "Interesting",
        "Concerning",
        "Extremely concerning",
        "Negative feedback is a good thing",
        "Something fundamental is wrong",
        "Something is wrong",
        "Turns out we just needed to blow on the cartridge",
        "Just ~$100/month for API access with ID verification will clean things up greatly.",
        "We will defeat the spam bots or die trying!"],
    "bug ": [
        "Something fundamental is wrong",
        "Something is wrong",
        "Turns out we just needed to blow on the cartridge"],
    " error": [
        "Something fundamental is wrong",
        "Something is wrong",
        "Turns out we just needed to blow on the cartridge"],
    "culture": ["End of days vibes"],
    "no plan": ["Amazing. You're a jackass!"],
    "wealth": ["I’m rich, bitch!"],
    "fascist": [
        "Comedy is now legal on Twitter.",
        "Interesting",
        "We should stop canceling comedy!"],
    "racism": [
        "Comedy is now legal on Twitter.",
        "Interesting",
        "We should stop canceling comedy!",
        "Simultaneously, an interesting question and a tongue twister!"],
    "racist": [
        "Comedy is now legal on Twitter.",
        "Interesting",
        "We should stop canceling comedy!",
        "Simultaneously, an interesting question and a tongue twister!"],
    "severance": ["You’re fired."],
    "engineer": [
        "Print out 50 pages of code you’ve done in the last 30 days",
        "Bring me 10 screenshots of the most salient lines of code you’ve written in the last 6 months.",
        "Bring me 10 screenshots of the most salient lines of code you’ve written in the last 6 months.",
    ],
    "takeover": ["Let that sink in"],
    "vote ": ["Vox Populi Vox Dei"],
    " poll": ["Vox Populi Vox Dei"],
    " ad ": ["Press the heart"],
    "advert": ["Press the heart"],
    "competitor": ["Press the heart"],
    "opinion": [
        "\U0001F3AF", # bullseye
        "\U0001F4AF", # 100
        "\U0001F4AF\U0001F3AF\U0001F923", # 100/bullseye/laugh
        "Interesting",
        "Concerning",
        "Extremely concerning",
        "Negative feedback is a good thing",
        "I get all my opinions from Twitter"],
    "reddit": [
        "\U0001F3AF", # bullseye
        "\U0001F4AF", # 100
        "\U0001F4AF\U0001F3AF\U0001F923", # 100/bullseye/laugh
        "Interesting",
        "Concerning",
        "Extremely concerning",
        "Negative feedback is a good thing",
        "I get all my opinions from Twitter"],
    "block": ["Negative feedback is a good thing"],
    "?$": ["Simultaneously, an interesting question and a tongue twister!"],
}

comment_replies = {
    "crypto": ["I will keep supporting Dogecoin"],
    "dogecoin": ["I will keep supporting Dogecoin"],
    "spacex": [
        "My car is currently orbiting mars",
        "Humanity will reach Mars in 2026",
        "Unless it is stopped, the woke mind virus will destroy civilization and humanity will never reached Mars"],
    "stephen king": ["I’m still a fan tbh"],
    "mastadon": ["What do you call someone who is a master at baiting?"],
    "mastodon": ["What do you call someone who is a master at baiting?"],
    "files": ["!!", "Interesting"],
    "twitter blue": ["We need to pay the bills somehow! How about $20?"],
    "twitter": [
        "Pay me $8!",
        "Looking into this.",
        "This is bizarre. Looking into it.",
        "Interesting",
        "Concerning",
        "Extremely concerning ...",
        "\U0001F3AF", # bullseye
        "\U0001F4AF", # 100
        "\U0001F4AF\U0001F3AF\U0001F923", # 100/bullseye/laugh
        "Twitter is now trending to breakeven if we keep at it.",
        "Something fundamental is wrong",
        "Something is wrong",
        "Turns out we just needed to blow on the cartridge",
        "I get all my opinions from Twitter"],
    "culture": ["End of days vibes"],
    "king of twitter": ["Let that sink in"],
    "dad joke": ["Let that sink in"],
    "takeover": ["Let that sink in"],
    "engineer": [
        "Print out 50 pages of code you’ve done in the last 30 days",
        "Bring me 10 screenshots of the most salient lines of code you’ve written in the last 6 months.",
        "Bring me 10 screenshots of the most salient lines of code you’ve written in the last 6 months.",
    ],
    "developer": [
        "Print out 50 pages of code you’ve done in the last 30 days",
        "Bring me 10 screenshots of the most salient lines of code you’ve written in the last 6 months.",
        "Just ~$100/month for API access with ID verification will clean things up greatly."],
    "server": [
        "Print out 50 pages of code you’ve done in the last 30 days",
        "Bring me 10 screenshots of the most salient lines of code you’ve written in the last 6 months.",
    ],
    "severance": ["You’re fired."],
    "employee": ["You’re fired.", "We’re going to need you to stay in overnight, we’re going ultra hardcore."],
    "fired": ["You’re fired!"],
    " fire ": ["You’re fired, you’re fired!"],
    "working hours": ["Are you super hardcore?", "Are you extremely hardcore?"],
    "hardcore": ["Are you super hardcore?", "Are you extremely hardcore?"],
    "covid": ["My pronouns are Prosecute/Fauci", "The coronavirus pandemic is dumb"],
    "daughter": ["Can’t win ‘em all"],
    "thai": ["Sorry pedo guy, you really did ask for it."],
    "wealth": ["I’m rich, bitch!"],
    "stock": ["Funding secured."],
    "loan": ["Funding secured."],
    "interest rate": ["Funding secured.", "Interesting"],
    "republican": ["I’m not right wing.", "Interesting"],
    " ban ": ["Comedy is now legal on Twitter."],
    " bans": ["Comedy is now legal on Twitter."],
    " bot": [
        "Looking into this.",
        "This is bizarre. Looking into it.",
        "Interesting",
        "Concerning",
        "Extremely concerning",
        "Negative feedback is a good thing",
        "Something fundamental is wrong",
        "Something is wrong",
        "Turns out we just needed to blow on the cartridge",
        "Just ~$100/month for API access with ID verification will clean things up greatly.",
        "We will defeat the spam bots or die trying!"],
    "bug ": [
        "Something fundamental is wrong",
        "Something is wrong",
        "Turns out we just needed to blow on the cartridge"],
    " error": [
        "Something fundamental is wrong",
        "Something is wrong",
        "Turns out we just needed to blow on the cartridge"],
    "suspend": ["Comedy is now legal on Twitter."],
    "fascist": [
        "Comedy is now legal on Twitter.",
        "Interesting",
        "We should stop canceling comedy!"],
    "racism": [
        "Comedy is now legal on Twitter.",
        "Interesting",
        "We should stop canceling comedy!",
        "Simultaneously, an interesting question and a tongue twister!"],
    "racist": [
        "Comedy is now legal on Twitter.",
        "Interesting",
        "We should stop canceling comedy!",
        "Simultaneously, an interesting question and a tongue twister!"],
    "resign": ["I will resign as CEO as soon as I find someone foolish enough to take the job! After that, I will just run the software & servers teams."],
    "woke": [
        "The woke mind virus is either defeated or nothing else matters",
        "Unless it is stopped, the woke mind virus will destroy civilization and humanity will never reached Mars"],
    "pronouns": [
        "My pronouns are Prosecute/Fauci",
        "Pronouns suck",
        "The woke mind virus is either defeated or nothing else matters"],
    "chappelle": ["Dave, what should I say?"],
    "neuralink": ["We are now confident that the Neuralink device is ready for humans"],
    "batchnorm": ["Gaming rocks"],
    "game": ["Gaming rocks"],
    "vote ": ["Vox Populi Vox Dei"],
    " poll": ["Vox Populi Vox Dei"],
    " ad ": ["Press the heart"],
    "advert": ["Press the heart"],
    "competitor": ["Press the heart"],
    "opinion": [
        "\U0001F3AF", # bullseye
        "\U0001F4AF", # 100
        "\U0001F4AF\U0001F3AF\U0001F923", # 100/bullseye/laugh
        "Interesting",
        "Concerning",
        "Extremely concerning",
        "Negative feedback is a good thing",
        "I get all my opinions from Twitter"],
    "reddit": [
        "\U0001F3AF", # bullseye
        "\U0001F4AF", # 100
        "\U0001F4AF\U0001F3AF\U0001F923", # 100/bullseye/laugh
        "Interesting",
        "Concerning",
        "Extremely concerning",
        "Negative feedback is a good thing",
        "I get all my opinions from Twitter"],
    "block": ["Negative feedback is a good thing"],
    "?$": ["Simultaneously, an interesting question and a tongue twister!"],
    # "trans": ["My pronouns are Prosecute/Fauci", "Pronouns suck"],
    # boring company
    # microservices just add bloat
}
