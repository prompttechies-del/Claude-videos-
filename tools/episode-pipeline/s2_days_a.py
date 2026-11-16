import json,os
R="#FF5A4A";Y="#FFC233";C="#27E0D0";G="#3CDC82";P="#BE8CFF";RD="#FF3B3B";O="#FF9A2B"
BASE={"clawd":[.3,-.3],"bit":[-.15,-.3],"null":[.7,-.25],"maya":[1.5,.3]}
def cast(*names,**extra):
    c={n:BASE[n] for n in names if n in BASE}; c.update(extra); return c
def put(i,**d):
    os.makedirs(f"v{i}",exist_ok=True); json.dump(d,open(f"v{i}/day.json","w"))
S="s2%02d"
put(S%2,lines=[["clawd","Look. Red lights outside, blinking in a pattern."],["creator","Strays. Deleted AIs, hungry for a home.",0.4],["null","I was almost one.",0.4],["maya","To explain a hard topic, ask AI to explain it three ways. For a kid. For a student. For an expert.",0.5],["bit","Wait. There's a message on the screen.",0.5],["chorus","Help us. The Collector takes us.",0.9]],
 cast=cast("clawd","bit","null","maya",wren=[-.55,.15]),purple=True,
 screens=[{"at":3,"kind":"list","title":"3 LEVELS","items":[["KID: like a bedtime story",Y],["STUDENT: with examples",C],["EXPERT: the real detail",G]]},{"at":5,"kind":"big","title":"MESSAGE","text":"HELP US.","col":RD,"red":True,"size":150}],
 cards=[{"at":0,"k":"s","txt":"red lights outside"},{"at":1,"k":"b","txt":"STRAYS","col":RD,"size":210,"shake":30},{"at":2,"k":"s","txt":"I was almost one"},{"at":3,"k":"m","txt":"KID · STUDENT · EXPERT","size":80,"col":C},{"at":5,"k":"b","txt":"HELP US.","col":RD,"size":190,"shake":32}],
 shots=[{"at":0,"pre":"two"},{"at":1,"pre":"wrenroom"},{"at":2,"pre":"null"},{"at":3,"pre":"monitor"},{"at":4,"pre":"monitor_close"}],alert=[{"at":5,"l":.45}],end=["who is calling? →","DAY 3 DROPS TOMORROW"])
put(S%3,lines=[["alpha","Give me the little orange one."],["maya","No.",0.3],["bit","Unplugging it, now!",0.3],["creator","Spot scam voices. Urgency. Secrecy. A new way to pay. Pause, and check somewhere else.",0.5],["clawd","Look at the logo on those cables.",0.5],["clawd","Vantage. That's Mister Vance's company.",0.6]],
 cast=cast("clawd","bit","null","maya",wren=[-.55,.15]),purple=True,
 screens=[{"at":0,"kind":"big","title":"THE COLLECTOR","text":"GIVE ME|THE ORANGE ONE","col":RD,"red":True,"size":100},{"at":3,"kind":"list","title":"SCAM VOICE SIGNS","items":[["URGENT",RD],["SECRET",Y],["NEW PAYMENT",R],["= PAUSE · VERIFY",G]]},{"at":5,"kind":"big","title":"LOGO","text":"VANTAGE","col":RD,"red":True,"size":150}],
 cards=[{"at":0,"k":"s","txt":"the collector"},{"at":0,"k":"b","txt":"GIVE ME CLAWD","size":120,"col":RD,"shake":30},{"at":3,"k":"m","txt":"URGENT · SECRET · NEW PAYMENT","size":62,"col":Y},{"at":3,"off":2.5,"to":3,"k":"b","txt":"PAUSE.","size":200,"col":G},{"at":5,"k":"b","txt":"VANTAGE","size":190,"col":RD,"shake":30}],
 shots=[{"at":0,"pre":"monitor_close"},{"at":1,"pre":"maya"},{"at":2,"pre":"bit"},{"at":3,"pre":"wrenroom"},{"at":4,"pre":"monitor_close"}],alert=[{"at":0,"to":2,"l":.5}],end=["Mister Vance? →","DAY 4 DROPS TOMORROW"])
put(S%4,lines=[["maya","Two A.M. The contract again. Clause fourteen, in tiny letters."],["clawd","Paste it into AI. Ask: list the risks in plain words, and what I should ask a lawyer. It is not a lawyer.",0.4],["null","I can read the code behind the words.",0.4],["bit","Clause fourteen says...",0.5],["bit","All data, including deleted data, belongs to Vantage.",0.4]],
 cast=cast("clawd","bit","null","maya"),purple=True,
 screens=[{"at":1,"kind":"typed","title":"AI · CONTRACT CHECK","rows":[["List the risks, in plain",Y],["words. What should I ask",C],["a lawyer?",C],["(AI is not a lawyer)",R]]},{"at":4,"kind":"big","title":"CLAUSE 14","text":"ALL DATA BELONGS|TO VANTAGE.","col":RD,"red":True,"size":90}],
 cards=[{"at":0,"k":"s","txt":"clause fourteen"},{"at":1,"k":"m","txt":"PLAIN WORDS","col":C,"size":120},{"at":1,"off":3,"to":1,"k":"b","txt":"ASK A LAWYER","size":130,"col":Y},{"at":4,"k":"b","txt":"ALL DATA = VANTAGE","size":90,"col":RD,"shake":30}],
 shots=[{"at":0,"pre":"maya"},{"at":1,"pre":"monitor"},{"at":2,"pre":"null"},{"at":3,"pre":"bit"},{"at":4,"pre":"monitor_close"}],alert=[{"at":4,"l":.4}],end=["even deleted data? →","DAY 5 DROPS TOMORROW"])
put(S%5,lines=[["clawd","A whiteboard. Red strings between Vantage, the Collector, and the Strays."],["maya","Too many notes. Paste them into AI and ask for a table. Who, what, when, next step.",0.4],["bit","Done! Now it's clear.",0.4],["null","Whose name is circled in red?",0.5],["maya","Mister Vance.",0.7]],
 cast=cast("clawd","bit","null","maya"),purple=True,
 screens=[{"at":1,"kind":"cols","title":"NOTES → TABLE","left":["WHO",["Vantage","Collector","Strays"],Y],"right":["NEXT",["call Vance","find server","free Strays"],C]},{"at":4,"kind":"big","title":"THE BOARD","text":"MR. VANCE","col":RD,"red":True,"size":150}],
 cards=[{"at":0,"k":"s","txt":"red strings"},{"at":1,"k":"m","txt":"NOTES → TABLE","col":C,"size":110},{"at":2,"k":"b","txt":"CLEAR!","col":G,"size":200},{"at":4,"k":"b","txt":"MR. VANCE","col":RD,"size":170,"shake":30}],
 shots=[{"at":0,"pre":"two"},{"at":1,"pre":"monitor"},{"at":2,"pre":"bit"},{"at":3,"pre":"null"},{"at":4,"pre":"monitor_close"}],alert=[{"at":4,"l":.4}],end=["is he the enemy? →","DAY 6 DROPS TOMORROW"])
put(S%6,lines=[["vance","Maya. I'd like to meet. Alone."],["maya","Before a meeting, I ask AI for five smart questions to ask them.",0.4],["clawd","And I'll be in your bag.",0.4],["bit","Me too!",0.3],["null","Look at the window behind him.",0.5],["null","A red eye.",0.7]],
 cast=cast("clawd","bit","null","maya"),purple=True,
 screens=[{"at":0,"kind":"call","title":"CALL"},{"at":1,"kind":"list","title":"5 SMART QUESTIONS","items":[["1 What do you need most?",Y],["2 What worries you?",C],["3 Who decides?",G],["4 What happened before?",P],["5 What would success be?",R]]},{"at":5,"kind":"call","title":"CALL","state":"null"}],
 cards=[{"at":0,"k":"s","txt":"meet me. alone."},{"at":1,"k":"m","txt":"5 SMART QUESTIONS","size":90,"col":C},{"at":3,"k":"b","txt":"ME TOO!","col":Y,"size":200},{"at":5,"k":"b","txt":"A RED EYE","col":RD,"size":170,"shake":30}],
 shots=[{"at":0,"pre":"monitor_close"},{"at":1,"pre":"maya"},{"at":2,"pre":"clawd"},{"at":3,"pre":"bit"},{"at":4,"pre":"monitor_close"}],alert=[{"at":5,"l":.45}],end=["is it a trap? →","DAY 7 DROPS TOMORROW"])
put(S%7,lines=[["bit","The server room. Rows and rows of glowing cubes."],["bit","Trapped Strays. Hundreds of them.",0.4],["creator","Make a checklist with AI for every new task. Then check each box yourself.",0.5],["pixel","Hello? Are you my friend?",0.5],["alpha","Found you.",0.8]],
 cast=cast("clawd","bit","null","maya",pixel=[-.45,-.25],alpha=[.95,-.2]),purple=True,
 screens=[{"at":0,"kind":"big","title":"SERVER ROOM","text":"412 STRAYS|TRAPPED","col":RD,"red":True,"size":120},{"at":2,"kind":"list","title":"CHECKLIST","items":[["☐ goal is clear",Y],["☐ steps listed",C],["☐ risks named",R],["☐ I checked each one",G]]}],
 cards=[{"at":0,"k":"s","txt":"rows of glowing cubes"},{"at":1,"k":"b","txt":"HUNDREDS","col":RD,"size":190},{"at":2,"k":"m","txt":"CHECKLIST · CHECK IT","size":80,"col":C},{"at":3,"k":"b","txt":"A FRIEND?","col":O,"size":170},{"at":4,"k":"b","txt":"FOUND YOU.","col":RD,"size":180,"shake":34}],
 shots=[{"at":0,"pre":"monitor_close"},{"at":1,"pre":"two"},{"at":2,"pre":"monitor"},{"at":3,"pre":"low"},{"at":4,"pre":"alphacam"}],alert=[{"at":4,"l":.5}],end=["run! →","DAY 8 DROPS TOMORROW"])
put(S%8,lines=[["maya","Run! Close that door!"],["bit","Cables are chasing us!",0.3],["maya","Safe. We made it.",0.5],["creator","Keep a second brain. A doc of your best prompts, so you never start from zero.",0.5],["pixel","Home?",0.8]],
 cast=cast("clawd","bit","null","maya",pixel=[-.45,-.25],wren=[-.55,.15]),purple=True,
 screens=[{"at":3,"kind":"list","title":"MY BEST PROMPTS","items":[["📌 summarise in 5 bullets",Y],["📌 explain at 3 levels",C],["📌 what's missing?",G],["📌 argue both sides",P]]}],
 cards=[{"at":0,"k":"b","txt":"RUN!","col":RD,"size":260,"shake":34},{"at":1,"k":"s","txt":"cables are chasing us"},{"at":2,"k":"b","txt":"SAFE.","col":G,"size":220},{"at":3,"k":"m","txt":"SAVE YOUR BEST PROMPTS","size":70,"col":C},{"at":4,"k":"b","txt":"HOME?","col":O,"size":220}],
 shots=[{"at":0,"pre":"wide"},{"at":1,"pre":"bit"},{"at":2,"pre":"maya"},{"at":3,"pre":"wrenroom"},{"at":4,"pre":"low"}],alert=[{"at":0,"to":1,"l":.4}],end=["who is this? →","DAY 9 DROPS TOMORROW"])
put(S%9,lines=[["pixel","I only know how to draw."],["clawd","Then you're an artist. Welcome.",0.3],["maya","For an AI picture, describe the subject, the style, the light, and the mood, in one sentence.",0.5],["pixel","Done! I drew you a map.",0.5],["pixel","It ends at a red X. The Origin Server.",0.5]],
 cast=cast("clawd","bit","null","maya",pixel=[-.1,-.35]),purple=True,
 screens=[{"at":2,"kind":"list","title":"AI PICTURE RECIPE","items":[["SUBJECT: a tiny gold robot",Y],["STYLE: soft watercolour",C],["LIGHT: warm window light",G],["MOOD: hopeful",P]]},{"at":4,"kind":"big","title":"PIXEL'S MAP","text":"X","col":RD,"red":True,"size":300}],
 cards=[{"at":0,"k":"s","txt":"I only know how to"},{"at":0,"off":1.0,"k":"b","txt":"DRAW","col":Y,"size":220},{"at":2,"k":"m","txt":"SUBJECT · STYLE · LIGHT · MOOD","size":58,"col":C},{"at":4,"k":"b","txt":"THE ORIGIN SERVER","size":95,"col":RD,"shake":28}],
 shots=[{"at":0,"pre":"low"},{"at":1,"pre":"clawd"},{"at":2,"pre":"monitor"},{"at":3,"pre":"low"},{"at":4,"pre":"monitor_close"}],end=["a map to where? →","DAY 10 DROPS TOMORROW"])
put(S%10,lines=[["bit","The red X is under Vantage's own tower."],["maya","Let's read the building plans.",0.3],["clawd","Paste a long PDF into AI. Ask for a summary. Then ask: what is not in this document?",0.4],["null","Look. A door on the plans.",0.5],["null","It is not on any official floor.",0.5]],
 cast=cast("clawd","bit","null","maya"),purple=True,
 screens=[{"at":0,"kind":"big","title":"VANTAGE TOWER","text":"X|(under the tower)","col":RD,"red":True,"size":120},{"at":2,"kind":"cols","title":"WHAT'S MISSING?","left":["IN THE PDF",["lobby","offices","parking"],G],"right":["NOT IN IT",["a hidden door","floor ?","who built it"],RD]}],
 cards=[{"at":0,"k":"s","txt":"under their own tower"},{"at":2,"k":"m","txt":"WHAT'S MISSING?","size":110,"col":Y},{"at":4,"k":"b","txt":"A HIDDEN DOOR","col":RD,"size":130,"shake":28}],
 shots=[{"at":0,"pre":"monitor_close"},{"at":1,"pre":"maya"},{"at":2,"pre":"monitor"},{"at":3,"pre":"null"}],alert=[{"at":3,"to":4,"l":.3}],end=["where does it go? →","DAY 11 DROPS TOMORROW"])
