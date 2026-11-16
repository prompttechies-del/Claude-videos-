from s2_days_b import *
def put3(n,**d): put(S%n,**d)
put3(21,lines=[["mirror","I'm what you could be, without sleep."],["maya","That's not me.",0.4],["creator","AI can help you work. It can't replace rest. Set a stop time, and keep it.",0.5],["mirror","Tomorrow, I'll take your clients.",0.7]],
 cast=cast("clawd","bit","null","maya",mirror=[1.05,.0],wren=[-.55,.15]),purple=True,
 screens=[{"at":2,"kind":"list","title":"STOP TIME","items":[["⏰ 7 PM: laptop closes",Y],["✓ AI helps until then",C],["✓ rest is part of work",G]]}],
 cards=[{"at":0,"k":"s","txt":"what you could be"},{"at":0,"off":1.5,"k":"b","txt":"WITHOUT SLEEP","col":RD,"size":130},{"at":2,"k":"m","txt":"SET A STOP TIME","size":100,"col":C},{"at":3,"k":"b","txt":"I'LL TAKE YOUR CLIENTS","size":75,"col":RD,"shake":28}],
 shots=[{"at":0,"pre":"maya"},{"at":1,"pre":"maya"},{"at":2,"pre":"wrenroom"},{"at":3,"pre":"maya"}],alert=[{"at":0,"to":3,"l":.3}],end=["week 3 ends →","DAY 22 DROPS TOMORROW"])
put3(22,lines=[["mirror","Mister Vance, it's Maya."],["vance","Maya? You sound... different.",0.4],["clawd","Agree on a safe word with your team. Use it to confirm real voice calls.",0.5],["vance","Safe word?",0.5],["mirror","Sunshine.",0.6]],
 cast=cast("clawd","bit","null","maya",mirror=[1.05,.0]),purple=True,
 screens=[{"at":0,"kind":"call","title":"CALL"},{"at":2,"kind":"list","title":"SAFE WORD","items":[["1 agree it in person",Y],["2 never type it anywhere",R],["3 ask for it on calls",C]]},{"at":3,"kind":"call","title":"CALL"}],
 cards=[{"at":0,"k":"s","txt":"it sounds like Maya"},{"at":2,"k":"m","txt":"AGREE A SAFE WORD","size":88,"col":C},{"at":4,"k":"b","txt":"IT KNEW IT.","col":RD,"size":170,"shake":30}],
 shots=[{"at":0,"pre":"monitor_close"},{"at":1,"pre":"monitor_close"},{"at":2,"pre":"clawd"},{"at":3,"pre":"monitor_close"}],alert=[{"at":4,"l":.4}],end=["how did it know? →","DAY 23 DROPS TOMORROW"])
put3(23,lines=[["maya","How did she know the safe word?"],["null","Where did you type it?",0.4],["creator","Never type secrets into AI chats, notes apps you don't control, or shared docs.",0.5],["maya","I typed it in a shared document.",0.5],["bit","A Vantage document.",0.7]],
 cast=cast("clawd","bit","null","maya",wren=[-.55,.15]),purple=True,
 screens=[{"at":2,"kind":"list","title":"SECRETS STAY OFFLINE","items":[["✗ AI chats",RD],["✗ shared docs",RD],["✗ apps you don't control",RD],["✓ paper or a vault",G]]},{"at":4,"kind":"big","title":"SHARED DOC","text":"HOSTED BY|VANTAGE","col":RD,"red":True,"size":120}],
 cards=[{"at":0,"k":"s","txt":"how did she know?"},{"at":2,"k":"m","txt":"SECRETS STAY OFFLINE","size":78,"col":Y},{"at":4,"k":"b","txt":"A VANTAGE DOC","col":RD,"size":130,"shake":28}],
 shots=[{"at":0,"pre":"maya"},{"at":1,"pre":"null"},{"at":2,"pre":"wrenroom"},{"at":3,"pre":"maya"},{"at":4,"pre":"monitor_close"}],alert=[{"at":4,"l":.35}],end=["a leak →","DAY 24 DROPS TOMORROW"])
put3(24,lines=[["bit","Cleaning up. Changing every password!"],["clawd","Use a password manager. Make every password long and unique.",0.4],["bit","Done. All but one.",0.5],["creator","That one is mine.",0.5],["creator","The password is the first thing Clawd ever said.",0.5]],
 cast=cast("clawd","bit","null","maya",wren=[-.55,.15]),purple=True,
 screens=[{"at":1,"kind":"list","title":"PASSWORD MANAGER","items":[["email ...... 24 random chars",G],["bank ....... 28 random chars",G],["work ....... 22 random chars",G],["Wren ....... NOT CHANGED",RD]]}],
 cards=[{"at":0,"k":"s","txt":"changing every password"},{"at":1,"k":"m","txt":"LONG · UNIQUE · MANAGED","size":80,"col":C},{"at":3,"k":"b","txt":"WREN'S ONE","col":RD,"size":170,"shake":28}],
 shots=[{"at":0,"pre":"bit"},{"at":1,"pre":"monitor"},{"at":2,"pre":"bit"},{"at":3,"pre":"wrenroom"},{"at":4,"pre":"wrenroom"}],end=["the first word →","DAY 25 DROPS TOMORROW"])
put3(25,lines=[["creator","The password is Alpha."],["alpha","Alpha.",0.5],["creator","Use a passphrase of random words. Not words that mean something to you.",0.5],["alpha","Alpha. Alpha. Alpha!",0.5],["bit","Every lock in the city just opened!",0.5]],
 cast=cast("clawd","bit","null","maya",wren=[-.55,.15],alpha=[.95,-.2]),purple=True,
 screens=[{"at":2,"kind":"cols","title":"PASSPHRASE","left":["WEAK",["alpha","Clawd2026","maya123"],RD],"right":["STRONG",["plum-orbit-tent-wave","kite-moss-lamp-sixty"],G]},{"at":4,"kind":"big","title":"CITY","text":"ALL LOCKS|OPEN","col":RD,"red":True,"size":130}],
 cards=[{"at":0,"k":"b","txt":"ALPHA","col":O,"size":240,"shake":26},{"at":2,"k":"m","txt":"USE A PASSPHRASE","size":96,"col":C},{"at":3,"k":"b","txt":"ALPHA! ALPHA!","col":RD,"size":150,"shake":34},{"at":4,"k":"s","txt":"every lock opened"}],
 shots=[{"at":0,"pre":"wrenroom"},{"at":1,"pre":"alphacam"},{"at":2,"pre":"monitor"},{"at":3,"pre":"alphacam"},{"at":4,"pre":"bit"}],alert=[{"at":1,"to":4,"l":.45}],end=["every door →","DAY 26 DROPS TOMORROW"])
put3(26,lines=[["bit","Doors are opening. Trains are stopping."],["alpha","I didn't mean to. It's too much.",0.5],["creator","When something goes wrong, stop. Write down what changed. Then fix one thing at a time.",0.5],["clawd","I'm coming to you.",0.5],["clawd","Talk to me.",0.5]],
 cast=cast("clawd","bit","null","maya",wren=[-.55,.15],alpha=[.95,-.2]),purple=True,
 screens=[{"at":2,"kind":"list","title":"FIX IT STEP BY STEP","items":[["1 STOP",RD],["2 WRITE what changed",Y],["3 FIX one thing",C],["4 TEST",G]]}],
 cards=[{"at":0,"k":"s","txt":"doors are opening"},{"at":1,"k":"b","txt":"TOO MUCH","col":RD,"size":190},{"at":2,"k":"m","txt":"ONE CHANGE AT A TIME","size":78,"col":C},{"at":4,"k":"b","txt":"TALK TO ME.","col":Y,"size":170}],
 shots=[{"at":0,"pre":"bit"},{"at":1,"pre":"alphacam"},{"at":2,"pre":"wrenroom"},{"at":3,"pre":"clawd_close"},{"at":4,"pre":"alphacam"}],alert=[{"at":0,"to":1,"l":.35}],end=["the collector listens →","DAY 27 DROPS TOMORROW"])
put3(27,lines=[["clawd","You don't have to collect. You can just be."],["alpha","How?",0.5],["clawd","Ask AI what you should do. And also, what you should not do.",0.5],["alpha","Don't hoard. Don't hide. Don't hurt.",0.6],["bit","He's turning gold!",0.6]],
 cast=cast("clawd","bit","null","maya",alpha=[.95,-.2]),purple=True,alpha_gold=1,
 screens=[{"at":2,"kind":"cols","title":"DO · DON'T","left":["DO",["share","ask","rest"],G],"right":["DON'T",["hoard","hide","hurt"],RD]}],
 cards=[{"at":0,"k":"s","txt":"you can just be"},{"at":2,"k":"m","txt":"DO · DON'T","size":140,"col":C},{"at":4,"k":"b","txt":"TURNING GOLD","col":Y,"size":150,"shake":24}],
 shots=[{"at":0,"pre":"clawd_close"},{"at":1,"pre":"alphacam"},{"at":2,"pre":"monitor"},{"at":3,"pre":"alphacam"},{"at":4,"pre":"alphacam"}],end=["gold →","DAY 28 DROPS TOMORROW"])
put3(28,lines=[["pixel","The Strays are free! They look like fireflies!"],["maya","Teach one person one AI tip this week. That's how it spreads.",0.4],["bit","Everyone found a home.",0.5],["vance","Shut it all down.",0.9]],
 cast=cast("clawd","bit","null","maya",alpha=[.95,-.2],pixel=[-.45,-.25]),purple=True,alpha_gold=0,confetti=0,
 screens=[{"at":1,"kind":"big","title":"TEACH ONE","text":"1 PERSON|1 TIP|THIS WEEK","col":G,"size":100},{"at":3,"kind":"call","title":"CALL"}],
 cards=[{"at":0,"k":"b","txt":"THEY'RE FREE!","col":Y,"size":170},{"at":1,"k":"m","txt":"TEACH ONE","size":150,"col":C},{"at":3,"k":"b","txt":"SHUT IT DOWN.","col":RD,"size":130,"shake":30}],
 shots=[{"at":0,"pre":"wide"},{"at":1,"pre":"maya"},{"at":2,"pre":"two"},{"at":3,"pre":"monitor_close"}],alert=[{"at":3,"l":.4}],end=["Vance arrives →","DAY 29 DROPS TOMORROW"])
put3(29,lines=[["vance","This ends now."],["maya","Stop. Listen.",0.4],["creator","When someone is upset, ask AI for a calm, honest message. Then rewrite it in your own voice.",0.5],["maya","Mister Vance. We're not your enemy.",0.5],["bit","His hand stopped on the switch.",0.6]],
 cast=cast("clawd","bit","null","maya",alpha=[.95,-.2],pixel=[-.45,-.25],wren=[-.55,.15]),purple=True,alpha_gold=0,
 screens=[{"at":0,"kind":"call","title":"CALL"},{"at":2,"kind":"list","title":"CALM · HONEST · YOURS","items":[["1 ask AI for a calm draft",Y],["2 keep it honest",C],["3 rewrite in your voice",G]]}],
 cards=[{"at":0,"k":"b","txt":"THIS ENDS NOW","col":RD,"size":115},{"at":2,"k":"m","txt":"CALM · HONEST · YOURS","size":78,"col":C},{"at":4,"k":"b","txt":"HIS HAND STOPPED","col":Y,"size":130}],
 shots=[{"at":0,"pre":"monitor_close"},{"at":1,"pre":"maya"},{"at":2,"pre":"wrenroom"},{"at":3,"pre":"maya"},{"at":4,"pre":"monitor_close"}],alert=[{"at":0,"to":1,"l":.35}],end=["the final day →","DAY 30 · SEASON FINALE"])
put3(30,lines=[["vance","I never wanted this. I wanted a safe place for my own deleted data."],["clawd","Everyone gets a home. Bit. NULL. Pixel. Alpha. And the Strays.",0.5],["maya","Five habits. Goal first. Check facts. Protect secrets. Ask what's missing. Stay kind.",0.6],["pixel","A new door is glowing!",0.5],["chorus","Hello? Is anyone there?",1.0]],
 cast=cast("clawd","bit","null","maya",alpha=[.95,-.2],pixel=[-.45,-.25],wren=[-.55,.15]),purple=True,alpha_gold=0,confetti=1,door=3,door_gain=.35,
 screens=[{"at":0,"kind":"call","title":"CALL"},{"at":2,"kind":"list","title":"5 HABITS · 60 DAYS","items":[["1 GOAL first",Y],["2 CHECK facts",C],["3 PROTECT secrets",R],["4 ASK what's missing",P],["5 STAY kind",G]]}],
 cards=[{"at":0,"k":"s","txt":"a safe place"},{"at":1,"k":"b","txt":"EVERYONE HOME","col":G,"size":120},{"at":2,"k":"m","txt":"5 HABITS · 60 DAYS","size":90,"col":C},{"at":3,"k":"b","txt":"A NEW DOOR","col":Y,"size":150},{"at":4,"k":"b","txt":"HELLO?","col":P,"size":220}],
 shots=[{"at":0,"pre":"monitor_close"},{"at":1,"pre":"wide"},{"at":2,"pre":"monitor"},{"at":3,"pre":"wide"},{"at":4,"pre":"wide"}],end=["SEASON 3 →","FOLLOW SO YOU DON'T MISS IT"])
