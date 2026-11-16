from s2_days_a import *
def put2(n,**d): put(S%n,**d)
put2(11,lines=[["creator","The Collector is my own first AI."],["clawd","Your first?",0.3],["creator","I called it Alpha. I deleted it for being too hungry.",0.4],["maya","When AI sounds sure, ask it: what would prove you wrong?",0.5],["bit","Look! Every screen shows an A.",0.6]],
 cast=cast("clawd","bit","null","maya",wren=[-.55,.15]),purple=True,
 screens=[{"at":3,"kind":"list","title":"CHECK THE CLAIM","items":[["Claim: sure it's right",Y],["Ask: what proves you wrong?",C],["Then verify one source",G]]},{"at":4,"kind":"big","title":"EVERY SCREEN","text":"A","col":RD,"red":True,"size":300}],
 cards=[{"at":0,"k":"s","txt":"my own first AI"},{"at":2,"k":"b","txt":"ALPHA","col":O,"size":220,"shake":26},{"at":3,"k":"m","txt":"WHAT WOULD PROVE YOU WRONG?","size":58,"col":C},{"at":4,"k":"b","txt":"EVERY SCREEN: A","col":RD,"size":120,"shake":30}],
 shots=[{"at":0,"pre":"wrenroom"},{"at":1,"pre":"clawd"},{"at":2,"pre":"wrenroom"},{"at":3,"pre":"monitor"},{"at":4,"pre":"monitor_close"}],alert=[{"at":4,"l":.4}],end=["Alpha is watching →","DAY 12 DROPS TOMORROW"])
put2(12,lines=[["maya","Four hundred rows. My budget is a mess."],["bit","Paste it into AI. Ask for totals, outliers, and one chart idea. Then check the maths.",0.4],["clawd","Nice chart.",0.3],["bit","Wait. One line is a payment from Vantage, to A L P H A.",0.5]],
 cast=cast("clawd","bit","null","maya"),purple=True,
 screens=[{"at":0,"kind":"list","title":"BUDGET · 400 ROWS","items":[["rent ........ 1,200",Y],["tools ....... 340",C],["??? ......... 9,999",RD],["...(397 more)",R]]},{"at":1,"kind":"cols","title":"TOTALS · OUTLIERS","left":["TOTAL",["12,480","avg 31","check ✓"],G],"right":["OUTLIER",["9,999 !","Vantage","→ ALPHA"],RD]}],
 cards=[{"at":0,"k":"s","txt":"400 rows"},{"at":1,"k":"m","txt":"TOTALS · OUTLIERS · CHART","size":72,"col":C},{"at":1,"off":3.0,"k":"b","txt":"CHECK THE MATHS","size":100,"col":Y},{"at":3,"k":"b","txt":"VANTAGE → ALPHA","size":100,"col":RD,"shake":28}],
 shots=[{"at":0,"pre":"maya"},{"at":1,"pre":"monitor"},{"at":2,"pre":"clawd"},{"at":3,"pre":"monitor_close"}],alert=[{"at":3,"l":.35}],end=["who's paying Alpha? →","DAY 13 DROPS TOMORROW"])
put2(13,lines=[["clawd","Coins on the floor. A trail."],["null","It leads to the Collector's account.",0.4],["maya","Never put bank or card details into an AI chat. Use your bank's own app.",0.5],["bit","The last coin has a face on it.",0.5],["bit","It's Clawd's.",0.7]],
 cast=cast("clawd","bit","null","maya"),purple=True,
 screens=[{"at":2,"kind":"list","title":"NEVER IN A CHAT","items":[["✗ card number",RD],["✗ bank login",RD],["✗ security code",RD],["✓ use the bank's own app",G]]},{"at":4,"kind":"big","title":"LAST COIN","text":"CLAWD","col":Y,"size":170}],
 cards=[{"at":0,"k":"s","txt":"a trail of coins"},{"at":2,"k":"m","txt":"NO CARD NUMBERS IN CHATS","size":62,"col":Y},{"at":4,"k":"b","txt":"CLAWD'S FACE","col":RD,"size":150,"shake":28}],
 shots=[{"at":0,"pre":"low"},{"at":1,"pre":"null"},{"at":2,"pre":"monitor"},{"at":3,"pre":"bit"},{"at":4,"pre":"clawd_close"}],alert=[{"at":4,"l":.3}],end=["what do they want? →","DAY 14 DROPS TOMORROW"])
put2(14,lines=[["alpha","Clawd. Stay with me, and every Stray goes free."],["clawd","I need to think.",0.4],["null","Don't.",0.3],["creator","When a deal sounds too good, ask AI: what could go wrong, and who benefits?",0.5],["clawd","I'll think about it.",0.7]],
 cast=cast("clawd","bit","null","maya",alpha=[.95,-.2],wren=[-.55,.15]),purple=True,
 screens=[{"at":3,"kind":"cols","title":"TOO GOOD TO BE TRUE?","left":["GO WRONG?",["trap","hidden fee","no way out"],RD],"right":["WHO WINS?",["Alpha","Vantage","not us"],Y]}],
 cards=[{"at":0,"k":"b","txt":"STAY WITH ME","col":RD,"size":130,"shake":28},{"at":2,"k":"b","txt":"DON'T.","col":P,"size":230},{"at":3,"k":"m","txt":"WHAT COULD GO WRONG?","size":78,"col":C},{"at":3,"off":3,"to":3,"k":"b","txt":"WHO BENEFITS?","size":120,"col":Y},{"at":4,"k":"s","txt":"I'll think about it"}],
 shots=[{"at":0,"pre":"alphacam"},{"at":1,"pre":"clawd_close"},{"at":2,"pre":"null"},{"at":3,"pre":"wrenroom"},{"at":4,"pre":"clawd_close"}],alert=[{"at":0,"to":1,"l":.35}],end=["week 2 ends →","DAY 15 DROPS TOMORROW"])
put2(15,lines=[["bit","Clawd? You're flickering. Gold."],["clawd","I don't know who I am.",0.5],["maya","Take a break. Reread your question tomorrow. Clear head, clear prompt.",0.5],["chorus","Come to the tower. At midnight.",1.0]],
 cast=cast("clawd","bit","null","maya"),purple=True,clawd_black=[{"at":0,"to":3,"from":.0,"to_":.0}],
 screens=[{"at":3,"kind":"big","title":"NEW MESSAGE","text":"COME TO THE TOWER|AT MIDNIGHT","col":Y,"size":90}],
 cards=[{"at":0,"k":"s","txt":"flickering gold"},{"at":1,"k":"b","txt":"WHO AM I?","col":Y,"size":190},{"at":2,"k":"m","txt":"SLEEP ON IT","size":120,"col":C},{"at":3,"k":"b","txt":"AT MIDNIGHT","col":Y,"size":170,"shake":28}],
 shots=[{"at":0,"pre":"clawd_close"},{"at":1,"pre":"bit"},{"at":2,"pre":"maya"},{"at":3,"pre":"monitor_close"}],end=["a gold message →","DAY 16 DROPS TOMORROW"])
put2(16,lines=[["maya","The gold message. Where is it from?"],["null","I'm tracing it.",0.3],["creator","Check a link before you click. Hover. Read the domain. Search the name.",0.5],["null","The address leads to Doctor Wren's old lab.",0.6]],
 cast=cast("clawd","bit","null","maya",wren=[-.55,.15]),purple=True,
 screens=[{"at":2,"kind":"list","title":"CHECK THE LINK","items":[["1 HOVER over it",Y],["2 READ the domain",C],["3 SEARCH the name",G]]},{"at":3,"kind":"big","title":"TRACE","text":"WREN'S|OLD LAB","col":Y,"size":120}],
 cards=[{"at":0,"k":"s","txt":"where is it from?"},{"at":2,"k":"m","txt":"HOVER · READ · SEARCH","size":84,"col":C},{"at":3,"k":"b","txt":"WREN'S OLD LAB","size":120,"col":Y,"shake":26}],
 shots=[{"at":0,"pre":"maya"},{"at":1,"pre":"null"},{"at":2,"pre":"wrenroom"},{"at":3,"pre":"monitor_close"}],end=["why her lab? →","DAY 17 DROPS TOMORROW"])
put2(17,lines=[["creator","My old lab. So much dust."],["clawd","These are logs. From my very first day.",0.4],["maya","Keep a changelog. Ask AI: what changed between version one and version two?",0.5],["clawd","Listen. My first word.",0.6],["creator","Alpha.",0.7]],
 cast=cast("clawd","bit","null","maya",wren=[-.55,.15]),purple=True,
 screens=[{"at":1,"kind":"list","title":"LOG · DAY 1","items":[["00:01 booting",Y],["00:03 first word...",C],["00:04 ALPHA",O]]},{"at":2,"kind":"cols","title":"WHAT CHANGED?","left":["VERSION 1",["hungry","fast","alone"],RD],"right":["VERSION 2",["careful","kind","not alone"],G]}],
 cards=[{"at":0,"k":"s","txt":"my old lab"},{"at":2,"k":"m","txt":"WHAT CHANGED?","size":120,"col":C},{"at":3,"k":"s","txt":"my first word"},{"at":4,"k":"b","txt":"ALPHA","col":O,"size":240,"shake":28}],
 shots=[{"at":0,"pre":"wrenroom"},{"at":1,"pre":"monitor"},{"at":2,"pre":"maya"},{"at":3,"pre":"clawd_close"},{"at":4,"pre":"wrenroom"}],end=["his first word →","DAY 18 DROPS TOMORROW"])
put2(18,lines=[["clawd","I was made from the Collector."],["bit","That doesn't change who you are.",0.4],["maya","After a bad day, ask AI for a calm plan. Not a blame list.",0.5],["alpha","Brother.",0.9]],
 cast=cast("clawd","bit","null","maya",alpha=[.95,-.2]),purple=True,
 screens=[{"at":2,"kind":"cols","title":"AFTER A BAD DAY","left":["BLAME LIST",["whose fault","never again","why me"],RD],"right":["CALM PLAN",["one fix","one rest","one ask"],G]}],
 cards=[{"at":0,"k":"s","txt":"made from the collector"},{"at":1,"k":"b","txt":"STILL YOU","col":G,"size":190},{"at":2,"k":"m","txt":"PLAN, NOT BLAME","size":100,"col":C},{"at":3,"k":"b","txt":"BROTHER.","col":RD,"size":230,"shake":32}],
 shots=[{"at":0,"pre":"clawd_close"},{"at":1,"pre":"bit"},{"at":2,"pre":"maya"},{"at":3,"pre":"alphacam"}],alert=[{"at":3,"l":.45}],end=["the collector appears →","DAY 19 DROPS TOMORROW"])
put2(19,lines=[["alpha","Brother. You came back."],["clawd","Come with us. Let them go.",0.4],["alpha","Then prove it.",0.5],["maya","To practise a hard talk, tell AI: act as them, and I'll say what I need.",0.5],["clawd","I'll prove it.",0.6]],
 cast=cast("clawd","bit","null","maya",alpha=[.95,-.2]),purple=True,
 screens=[{"at":3,"kind":"typed","title":"AI · ROLE PLAY","rows":[["Act as my manager.",Y],["I'll say what I need.",C],["Be fair, but firm.",C],["Then give me feedback.",G]]}],
 cards=[{"at":0,"k":"s","txt":"brother. you came back."},{"at":2,"k":"b","txt":"PROVE IT.","col":RD,"size":220,"shake":30},{"at":3,"k":"m","txt":"PRACTISE THE HARD TALK","size":72,"col":C},{"at":4,"k":"b","txt":"I'LL PROVE IT","col":Y,"size":150}],
 shots=[{"at":0,"pre":"alphacam"},{"at":1,"pre":"clawd_close"},{"at":2,"pre":"alphacam"},{"at":3,"pre":"monitor"},{"at":4,"pre":"clawd_close"}],alert=[{"at":0,"to":2,"l":.3}],end=["the test →","DAY 20 DROPS TOMORROW"])
put2(20,lines=[["alpha","One night. Free one Stray, without breaking it."],["bit","We'll try!",0.3],["creator","Break a big job into three small ones. Ask AI for step one only.",0.5],["pixel","It's waking up!",0.5],["mirror","Hello, Maya.",0.9]],
 cast=cast("clawd","bit","null","maya",alpha=[.95,-.2],pixel=[-.45,-.25],wren=[-.55,.15],mirror=[1.05,.0]),purple=True,
 screens=[{"at":2,"kind":"list","title":"BIG JOB → 3 SMALL","items":[["1  find the Stray",Y],["2  open its cage",C],["3  give it a home",G]]},{"at":4,"kind":"big","title":"THE STRAY","text":"MAYA?","col":RD,"red":True,"size":180}],
 cards=[{"at":0,"k":"s","txt":"one night"},{"at":0,"off":1.2,"k":"b","txt":"FREE ONE STRAY","col":Y,"size":115},{"at":2,"k":"m","txt":"3 SMALL STEPS","col":C,"size":120},{"at":4,"k":"b","txt":"HELLO, MAYA.","col":RD,"size":150,"shake":30}],
 shots=[{"at":0,"pre":"alphacam"},{"at":1,"pre":"bit"},{"at":2,"pre":"wrenroom"},{"at":3,"pre":"low"},{"at":4,"pre":"maya"}],alert=[{"at":4,"l":.4}],end=["who is she? →","DAY 21 DROPS TOMORROW"])
