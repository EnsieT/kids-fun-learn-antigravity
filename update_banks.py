import os
import re

cur_dir = os.path.dirname(__file__)
act_dir = os.path.join(cur_dir, 'activities')

# 1. Update Match Columns
match_val = """const ROUND_TYPES = [
  // 1
  {
    titleHi: '🐄 जानवर और आवाज़', titleEn: '🐄 Animals & Sounds', titleGu: '🐄 પ્રાણી અને અવાજ',
    pairs: [
      {left:{emoji:'🐄',hi:'गाय',en:'Cow',gu:'ગાય'}, right:{emoji:'🐮',hi:'मू',en:'Moo',gu:'મૂ'}},
      {left:{emoji:'🐕',hi:'कुत्ता',en:'Dog',gu:'કૂતરો'}, right:{emoji:'🔔',hi:'भौं',en:'Woof',gu:'ભૌ '}},
      {left:{emoji:'🐈',hi:'बिल्ली',en:'Cat',gu:'બિલાડી'}, right:{emoji:'🎵',hi:'म्याऊं',en:'Meow',gu:'મ્યાઉ'}},
      {left:{emoji:'🦁',hi:'शेर',en:'Lion',gu:'સિંહ'}, right:{emoji:'💥',hi:'दहाड़',en:'Roar',gu:'ગર્જના'}},
      {left:{emoji:'🐘',hi:'हाथी',en:'Elephant',gu:'હાથી'}, right:{emoji:'📢',hi:'चिंघाड़',en:'Trumpet',gu:'ત્રાંસો'}},
    ]
  },
  // 2
  {
    titleHi: '🥭 फल और रंग', titleEn: '🥭 Fruits & Colors', titleGu: '🥭 ફળ અને રંગ',
    pairs: [
      {left:{emoji:'🥭',hi:'आम',en:'Mango',gu:'કેરી'}, right:{emoji:'🟡',hi:'पीला',en:'Yellow',gu:'પીળો'}},
      {left:{emoji:'🍎',hi:'सेब',en:'Apple',gu:'સફરજન'}, right:{emoji:'🔴',hi:'लाल',en:'Red',gu:'લાલ'}},
      {left:{emoji:'🍌',hi:'केला',en:'Banana',gu:'કેળું'}, right:{emoji:'🟡',hi:'पीला',en:'Yellow',gu:'પીળો'}},
      {left:{emoji:'🍊',hi:'संतरा',en:'Orange',gu:'નારંગી'}, right:{emoji:'🟠',hi:'नारंगी',en:'Orange',gu:'નારંગી'}},
      {left:{emoji:'🍇',hi:'अंगूर',en:'Grapes',gu:'દ્રાક્ષ'}, right:{emoji:'🟣',hi:'बैंगनी',en:'Purple',gu:'જાંબલી'}},
    ]
  },
  // 3
  {
    titleHi: '🔢 संख्या और बिंदु', titleEn: '🔢 Numbers & Dots', titleGu: '🔢 સંખ્યા અને ટપકાં',
    pairs: [
      {left:{emoji:'1️⃣',hi:'एक',en:'One',gu:'એક'}, right:{emoji:'⚫',hi:'एक',en:'1 dot',gu:'1 ટપકું'}},
      {left:{emoji:'2️⃣',hi:'दो',en:'Two',gu:'બે'}, right:{emoji:'⚫⚫',hi:'दो',en:'2 dots',gu:'2 ટપકાં'}},
      {left:{emoji:'3️⃣',hi:'तीन',en:'Three',gu:'ત્રણ'}, right:{emoji:'⚫⚫⚫',hi:'तीन',en:'3 dots',gu:'3 ટપકાં'}},
      {left:{emoji:'4️⃣',hi:'चार',en:'Four',gu:'ચાર'}, right:{emoji:'⚫⚫⚫⚫',hi:'चार',en:'4 dots',gu:'4 ટપકાં'}},
      {left:{emoji:'5️⃣',hi:'पाँच',en:'Five',gu:'પાંચ'}, right:{emoji:'⚫⚫⚫⚫⚫',hi:'पाँच',en:'5 dots',gu:'5 ટપકાં'}},
    ]
  },
  // 4
  {
    titleHi: '🌍 चीज़ें और श्रेणी', titleEn: '🌍 Things & Categories', titleGu: '🌍 વસ્તુ અને શ્રેણી',
    pairs: [
      {left:{emoji:'🥭',hi:'आम',en:'Mango',gu:'કેરી'}, right:{emoji:'🍽️',hi:'फल',en:'Fruit',gu:'ફળ'}},
      {left:{emoji:'🥔',hi:'आलू',en:'Potato',gu:'બટાટા'}, right:{emoji:'🥗',hi:'सब्ज़ी',en:'Veggie',gu:'શાક'}},
      {left:{emoji:'🐄',hi:'गाय',en:'Cow',gu:'ગાય'}, right:{emoji:'🐾',hi:'जानवर',en:'Animal',gu:'પ્રાણી'}},
      {left:{emoji:'🚗',hi:'कार',en:'Car',gu:'ગાડી'}, right:{emoji:'🛣️',hi:'वाहन',en:'Vehicle',gu:'વાહન'}},
      {left:{emoji:'📚',hi:'किताब',en:'Book',gu:'ચોપડી'}, right:{emoji:'✏️',hi:'पढ़ाई',en:'Study',gu:'ભણતર'}},
    ]
  },
  // 5
  {
    titleHi: '⚖️ उलटे शब्द', titleEn: '⚖️ Opposites', titleGu: '⚖️ વિરુદ્ધ શબ્દો',
    pairs: [
      {left:{emoji:'☀️',hi:'दिन',en:'Day',gu:'દિવસ'}, right:{emoji:'🌙',hi:'रात',en:'Night',gu:'રાત'}},
      {left:{emoji:'🔥',hi:'गर्म',en:'Hot',gu:'ગરમ'}, right:{emoji:'🧊',hi:'ठंडा',en:'Cold',gu:'ઠંડુ'}},
      {left:{emoji:'😊',hi:'खुश',en:'Happy',gu:'ખુશ'}, right:{emoji:'😢',hi:'उदास',en:'Sad',gu:'ઉદાસ'}},
      {left:{emoji:'🐢',hi:'धीमा',en:'Slow',gu:'ધીમું'}, right:{emoji:'🐇',hi:'तेज़',en:'Fast',gu:'ઝડપી'}},
      {left:{emoji:'🐘',hi:'बड़ा',en:'Big',gu:'મોટું'}, right:{emoji:'🐁',hi:'छोटा',en:'Small',gu:'નાનું'}},
    ]
  },
  // 6
  {
    titleHi: '🔷 आकार और चीज़ें', titleEn: '🔷 Shapes & Objects', titleGu: '🔷 આકાર અને વસ્તુઓ',
    pairs: [
      {left:{emoji:'🔴',hi:'गोल',en:'Circle',gu:'ગોળ'}, right:{emoji:'⚽',hi:'गेंद',en:'Ball',gu:'દડો'}},
      {left:{emoji:'🟩',hi:'चौकोर',en:'Square',gu:'ચોરસ'}, right:{emoji:'🎁',hi:'डिब्बा',en:'Box',gu:'ખોખું'}},
      {left:{emoji:'🔺',hi:'तिकोना',en:'Triangle',gu:'ત્રિકોણ'}, right:{emoji:'🍕',hi:'पिज्ज़ा',en:'Pizza',gu:'પિઝા'}},
      {left:{emoji:'⭐',hi:'तारा',en:'Star',gu:'તારો'}, right:{emoji:'✨',hi:'चमक',en:'Sparkle',gu:'ચમક'}},
      {left:{emoji:'♥️',hi:'दिल',en:'Heart',gu:'દિલ'}, right:{emoji:'💌',hi:'चिट्ठी',en:'Letter',gu:'પત્ર'}},
    ]
  },
  // 7
  {
    titleHi: '🚀 वाहन और जगह', titleEn: '🚀 Vehicles & Places', titleGu: '🚀 વાહન અને જગ્યા',
    pairs: [
      {left:{emoji:'✈️',hi:'हवाई जहाज़',en:'Plane',gu:'વિમાન'}, right:{emoji:'☁️',hi:'आसमान',en:'Sky',gu:'આકાશ'}},
      {left:{emoji:'🚢',hi:'जहाज़',en:'Ship',gu:'જહાજ'}, right:{emoji:'🌊',hi:'पानी',en:'Water',gu:'પાણી'}},
      {left:{emoji:'🚗',hi:'कार',en:'Car',gu:'ગાડી'}, right:{emoji:'🛣️',hi:'सड़क',en:'Road',gu:'રસ્તો'}},
      {left:{emoji:'🚂',hi:'ट्रेन',en:'Train',gu:'ટ્રેन'}, right:{emoji:'🛤️',hi:'पटरी',en:'Track',gu:'પાટા'}},
      {left:{emoji:'🚀',hi:'रॉकेट',en:'Rocket',gu:'રોકેટ'}, right:{emoji:'🌌',hi:'अंतरिक्ष',en:'Space',gu:'અંતરિક્ષ'}},
    ]
  },
  // 8
  {
    titleHi: '🔧 कामगार और औज़ार', titleEn: '🔧 Jobs & Tools', titleGu: '🔧 કામદાર અને ઓજારો',
    pairs: [
      {left:{emoji:'👨‍⚕️',hi:'डॉक्टर',en:'Doctor',gu:'ડૉક્ટર'}, right:{emoji:'🩺',hi:'स्टेथोस्कोप',en:'Stethoscope',gu:'સ્ટેથોસ્કોપ'}},
      {left:{emoji:'👨‍🍳',hi:'कुक',en:'Chef',gu:'રસોઈયો'}, right:{emoji:'🍳',hi:'बर्तन',en:'Pan',gu:'તપેલી'}},
      {left:{emoji:'👮‍♂️',hi:'पुलिस',en:'Police',gu:'પોલીસ'}, right:{emoji:'🚓',hi:'पुलिस कार',en:'Police Car',gu:'પોલીસ ગાડી'}},
      {left:{emoji:'🧑‍🏫',hi:'शिक्षक',en:'Teacher',gu:'શિક્ષક'}, right:{emoji:'📚',hi:'किताब',en:'Book',gu:'ચોપડી'}},
      {left:{emoji:'👨‍🌾',hi:'किसान',en:'Farmer',gu:'ખેડૂત'}, right:{emoji:'🚜',hi:'ट्रैक्टर',en:'Tractor',gu:'ટ્રેક્ટર'}},
    ]
  },
  // 9
  {
    titleHi: '👕 मौसम और कपड़े', titleEn: '👕 Weather & Clothes', titleGu: '👕 હવામાન અને કપડાં',
    pairs: [
      {left:{emoji:'🌧️',hi:'बारिश',en:'Rail',gu:'વરસાદ'}, right:{emoji:'☔',hi:'छाता',en:'Umbrella',gu:'છત્રી'}},
      {left:{emoji:'☀️',hi:'धूप',en:'Sun',gu:'તડકો'}, right:{emoji:'🧢',hi:'टोपी',en:'Cap',gu:'ટોપી'}},
      {left:{emoji:'❄️',hi:'ठंड',en:'Snow',gu:'બરફ'}, right:{emoji:'🧣',hi:'मफलर',en:'Scarf',gu:'મફલર'}},
      {left:{emoji:'💨',hi:'हवा',en:'Wind',gu:'પવન'}, right:{emoji:'🧥',hi:'जैकेट',en:'Jacket',gu:'જેકેટ'}},
      {left:{emoji:'🏖️',hi:'गर्मी',en:'Summer',gu:'ઉનાળો'}, right:{emoji:'🩳',hi:'निक्कर',en:'Shorts',gu:'ચડ્ડી'}},
    ]
  },
  // 10
  {
    titleHi: '🐾 जानवर और खाना', titleEn: '🐾 Animals & Food', titleGu: '🐾 પ્રાણી અને ખોરાક',
    pairs: [
      {left:{emoji:'🐒',hi:'बंदर',en:'Monkey',gu:'વાંદરો'}, right:{emoji:'🍌',hi:'केला',en:'Banana',gu:'કેળું'}},
      {left:{emoji:'🐇',hi:'खरगोश',en:'Rabbit',gu:'સસલું'}, right:{emoji:'🥕',hi:'गाजर',en:'Carrot',gu:'ગાજર'}},
      {left:{emoji:'🐄',hi:'गाय',en:'Cow',gu:'गાય'}, right:{emoji:'🌿',hi:'घास',en:'Grass',gu:'ઘાસ'}},
      {left:{emoji:'🐈',hi:'बिल्ली',en:'Cat',gu:'બિલાડી'}, right:{emoji:'🥛',hi:'दूध',en:'Milk',gu:'દૂધ'}},
      {left:{emoji:'🐕',hi:'कुत्ता',en:'Dog',gu:'કૂતરો'}, right:{emoji:'🦴',hi:'हड्डी',en:'Bone',gu:'હાડકું'}},
    ]
  },
  // 11
  {
    titleHi: '🔠 बड़ा और छोटा अक्षर', titleEn: '🔠 Big & Small Letter', titleGu: '🔠 મોટો અને નાનો અક્ષર',
    pairs: [
      {left:{emoji:'A',hi:'A',en:'A',gu:'A'}, right:{emoji:'a',hi:'a',en:'a',gu:'a'}},
      {left:{emoji:'B',hi:'B',en:'B',gu:'B'}, right:{emoji:'b',hi:'b',en:'b',gu:'b'}},
      {left:{emoji:'C',hi:'C',en:'C',gu:'C'}, right:{emoji:'c',hi:'c',en:'c',gu:'c'}},
      {left:{emoji:'D',hi:'D',en:'D',gu:'D'}, right:{emoji:'d',hi:'d',en:'d',gu:'d'}},
      {left:{emoji:'E',hi:'E',en:'E',gu:'E'}, right:{emoji:'e',hi:'e',en:'e',gu:'e'}},
    ]
  },
  // 12
  {
    titleHi: '✋ संख्या और उँगलियाँ', titleEn: '✋ Numbers & Fingers', titleGu: '✋ સંખ્યા અને આંગળીઓ',
    pairs: [
      {left:{emoji:'1️⃣',hi:'एक',en:'One',gu:'એક'}, right:{emoji:'☝️',hi:'एक',en:'1 Finger',gu:'1 આંગળી'}},
      {left:{emoji:'2️⃣',hi:'दो',en:'Two',gu:'બે'}, right:{emoji:'✌️',hi:'दो',en:'2 Fingers',gu:'2 આંગળીઓ'}},
      {left:{emoji:'3️⃣',hi:'तीन',en:'Three',gu:'ત્રણ'}, right:{emoji:'🤟',hi:'तीन',en:'3 Fingers',gu:'3 આંગળીઓ'}},
      {left:{emoji:'4️⃣',hi:'चार',en:'Four',gu:'ચાર'}, right:{emoji:'🖐️',hi:'चार',en:'4 (almost)',gu:'4 આંગળીઓ'}},
      {left:{emoji:'5️⃣',hi:'पाँच',en:'Five',gu:'પાંચ'}, right:{emoji:'✋',hi:'पाँच',en:'5 Fingers',gu:'5 આંગળીઓ'}},
    ]
  },
  // 13
  {
    titleHi: '🏠 जानवर और घर', titleEn: '🏠 Animals & Homes', titleGu: '🏠 પ્રાણી અને ઘર',
    pairs: [
      {left:{emoji:'🐦',hi:'चिड़िया',en:'Bird',gu:'પક્ષી'}, right:{emoji:'🪹',hi:'घोंसला',en:'Nest',gu:'માળો'}},
      {left:{emoji:'🐝',hi:'मधुमक्खी',en:'Bee',gu:'મધમાખી'}, right:{emoji:'🍯',hi:'छत्ता',en:'Hive',gu:'મધપૂડો'}},
      {left:{emoji:'🕷️',hi:'मकड़ी',en:'Spider',gu:'કરોળિયો'}, right:{emoji:'🕸️',hi:'जाला',en:'Web',gu:'જાળું'}},
      {left:{emoji:'🐕',hi:'कुत्ता',en:'Dog',gu:'કૂતરો'}, right:{emoji:'🛖',hi:'कुत्ता घर',en:'Doghouse',gu:'કૂતરાનું ઘર'}},
      {left:{emoji:'🐟',hi:'मछली',en:'Fish',gu:'માછલી'}, right:{emoji:'🌊',hi:'नदी',en:'Water',gu:'નદી'}},
    ]
  },
  // 14
  {
    titleHi: '🌳 पेड़ और पत्ते', titleEn: '🌳 Trees & Parts', titleGu: '🌳 વૃક્ષ અને ભાગો',
    pairs: [
      {left:{emoji:'🌳',hi:'पेड़',en:'Tree',gu:'ઝાડ'}, right:{emoji:'🍃',hi:'पत्ता',en:'Leaf',gu:'પાંદડું'}},
      {left:{emoji:'🍎',hi:'सेब',en:'Apple',gu:'સફરજન'}, right:{emoji:'🌱',hi:'बीज',en:'Seed',gu:'બીજ'}},
      {left:{emoji:'🌻',hi:'सूरजमुखी',en:'Sunflower',gu:'સૂરજમુખી'}, right:{emoji:'☀️',hi:'धूप',en:'Sun',gu:'તડકો'}},
      {left:{emoji:'🌹',hi:'गुलाब',en:'Rose',gu:'ગુલાબ'}, right:{emoji:'💧',hi:'पानी',en:'Water',gu:'પાણી'}},
      {left:{emoji:'🌵',hi:'कैक्टस',en:'Cactus',gu:'થોર'}, right:{emoji:'🏜️',hi:'रेत',en:'Sand',gu:'રેતી'}},
    ]
  },
  // 15
  {
    titleHi: '🛏️ कमरे और सामान', titleEn: '🛏️ Rooms & Items', titleGu: '🛏️ ઓરડાઓ અને વસ્તુઓ',
    pairs: [
      {left:{emoji:'🍳',hi:'रसोई',en:'Kitchen',gu:'રસોડું'}, right:{emoji:'🥣',hi:'प्याला',en:'Bowl',gu:'વાટકો'}},
      {left:{emoji:'🛏️',hi:'बेडरूम',en:'Bedroom',gu:'બેડરૂમ'}, right:{emoji:'🧸',hi:'खिलौना',en:'Teddy',gu:'રમકડું'}},
      {left:{emoji:'🚿',hi:'बाथरूम',en:'Bathroom',gu:'બાથરૂમ'}, right:{emoji:'🧼',hi:'साबुन',en:'Soap',gu:'સાબુ'}},
      {left:{emoji:'🛋️',hi:'हॉल',en:'Living Room',gu:'હોલ'}, right:{emoji:'📺',hi:'टीवी',en:'TV',gu:'ટીવી'}},
      {left:{emoji:'📚',hi:'पढ़ाई कमरा',en:'Study Room',gu:'અભ્યાસ રૂમ'}, right:{emoji:'✏️',hi:'पेंसिल',en:'Pencil',gu:'પેન્સિલ'}},
    ]
  },
  // 16
  {
    titleHi: '🎵 संगीत और साज़', titleEn: '🎵 Music & Instruments', titleGu: '🎵 સંગીત અને સાધનો',
    pairs: [
      {left:{emoji:'🎹',hi:'पियानो',en:'Piano',gu:'પિયાનો'}, right:{emoji:'🎼',hi:'धुन',en:'Notes',gu:'ધૂન'}},
      {left:{emoji:'🎸',hi:'गिटार',en:'Guitar',gu:'ગિટાર'}, right:{emoji:'🤘',hi:'रॉक',en:'Rock',gu:'રોક'}},
      {left:{emoji:'🥁',hi:'ड्रम',en:'Drum',gu:'ડ્રમ'}, right:{emoji:'🥁',hi:'ताल',en:'Beat',gu:'તાલ'}},
      {left:{emoji:'🎺',hi:'बाजा',en:'Trumpet',gu:'વાજું'}, right:{emoji:'🎷',hi:'हवा',en:'Blow',gu:'હવા'}},
      {left:{emoji:'🎤',hi:'माइक',en:'Mic',gu:'માઈક'}, right:{emoji:'🎶',hi:'गाना',en:'Sing',gu:'ગાવું'}},
    ]
  },
  // 17
  {
    titleHi: '🍔 खाना और स्वाद', titleEn: '🍔 Food & Taste', titleGu: '🍔 ખોરાક અને સ્વાદ',
    pairs: [
      {left:{emoji:'🍋',hi:'नींबू',en:'Lemon',gu:'લીંબુ'}, right:{emoji:'😖',hi:'खट्टा',en:'Sour',gu:'ખાટું'}},
      {left:{emoji:'🍫',hi:'चॉकलेट',en:'Chocolate',gu:'ચોકલેટ'}, right:{emoji:'😋',hi:'मीठा',en:'Sweet',gu:'મીઠું'}},
      {left:{emoji:'🌶️',hi:'मिर्च',en:'Chili',gu:'મરચું'}, right:{emoji:'🥵',hi:'तीखा',en:'Spicy',gu:'તીખું'}},
      {left:{emoji:'🥨',hi:'नमकीन',en:'Pretzel',gu:'નમકીન'}, right:{emoji:'🧂',hi:'नमक',en:'Salty',gu:'ખારું'}},
      {left:{emoji:'🧊',hi:'बर्फ',en:'Ice',gu:'બરફ'}, right:{emoji:'🥶',hi:'ठंडा',en:'Cold',gu:'ઠંડુ'}},
    ]
  },
  // 18
  {
    titleHi: '🎈 पार्टी और मज़ा', titleEn: '🎈 Party & Fun', titleGu: '🎈 પાર્ટી અને મજા',
    pairs: [
      {left:{emoji:'🎂',hi:'केक',en:'Cake',gu:'કેક'}, right:{emoji:'🕯️',hi:'मोमबत्ती',en:'Candle',gu:'મીણબત્તી'}},
      {left:{emoji:'🎁',hi:'गिफ्ट',en:'Gift',gu:'ભેટ'}, right:{emoji:'🎀',hi:'रिबन',en:'Ribbon',gu:'રબિન'}},
      {left:{emoji:'🎈',hi:'गुब्बारा',en:'Balloon',gu:'ફુગ્ગો'}, right:{emoji:'🌬️',hi:'हवा',en:'Air',gu:'હવા'}},
      {left:{emoji:'🎉',hi:'पार्टी',en:'Party',gu:'પાર્ટી'}, right:{emoji:'💃',hi:'नाच',en:'Dance',gu:'નાચવું'}},
      {left:{emoji:'📸',hi:'कैमरा',en:'Camera',gu:'કેમેરા'}, right:{emoji:'🖼️',hi:'फोटो',en:'Photo',gu:'ફોટો'}},
    ]
  },
  // 19
  {
    titleHi: '🛠️ काम और मशीन', titleEn: '🛠️ Jobs & Machines', titleGu: '🛠️ નોકરી અને મશીનો',
    pairs: [
      {left:{emoji:'📸',hi:'फोटोग्राफर',en:'Photog',gu:'ફોટોગ્રાફર'}, right:{emoji:'🖼️',hi:'फोटो',en:'Photo',gu:'ફોટો'}},
      {left:{emoji:'👨‍🚒',hi:'फायरमैन',en:'Fireman',gu:'ફાયરમેન'}, right:{emoji:'🚒',hi:'फायर ट्रक',en:'Fire Truck',gu:'ફાયરટ્રક'}},
      {left:{emoji:'🧑‍🚀',hi:'अंतरिक्षयात्री',en:'Astronaut',gu:'અંતરિક્ષયાત્રી'}, right:{emoji:'🚀',hi:'रॉकेट',en:'Rocket',gu:'રોકેટ'}},
      {left:{emoji:'👨‍🔧',hi:'मैकेनिक',en:'Mechanic',gu:'મિકેનિક'}, right:{emoji:'🔧',hi:'पाना',en:'Wrench',gu:'પાનું'}},
      {left:{emoji:'👨‍🎨',hi:'कलाकार',en:'Artist',gu:'કલાકાર'}, right:{emoji:'🎨',hi:'रंग',en:'Paint',gu:'રંગ'}},
    ]
  },
  // 20
  {
    titleHi: '🌈 इंद्रधनुष के रंग', titleEn: '🌈 Rainbow Colors', titleGu: '🌈 મેઘધનુષ્ય રંગો',
    pairs: [
      {left:{emoji:'🔴',hi:'लाल',en:'Red',gu:'લાલ'}, right:{emoji:'🍎',hi:'सेब',en:'Apple',gu:'સફરજન'}},
      {left:{emoji:'🟠',hi:'नारंगी',en:'Orange',gu:'નારંગી'}, right:{emoji:'🍊',hi:'संतरा',en:'Orange',gu:'નારંગી'}},
      {left:{emoji:'🟡',hi:'पीला',en:'Yellow',gu:'પીળો'}, right:{emoji:'🌻',hi:'सूरजमुखी',en:'Sun',gu:'સૂર્યમુખી'}},
      {left:{emoji:'🟢',hi:'हरा',en:'Green',gu:'લીલો'}, right:{emoji:'🍃',hi:'पत्ता',en:'Leaf',gu:'પાંદડું'}},
      {left:{emoji:'🟦',hi:'नीला',en:'Blue',gu:'વાદળી'}, right:{emoji:'💧',hi:'पानी',en:'Water',gu:'પાણી'}},
    ]
  }
];"""

mc_path = os.path.join(act_dir, 'match-columns.html')
with open(mc_path, 'r', encoding='utf-8') as f:
    mc_content = f.read()

mc_content = re.sub(r'const ROUND_TYPES = \[.*?\];', match_val, mc_content, flags=re.DOTALL)
with open(mc_path, 'w', encoding='utf-8') as f:
    f.write(mc_content)
print("Updated match-columns.html banks")

# 2. Update Odd One Out Puzzles
odd_val = """const PUZZLES = [
  { items:['🥭','🍌','🥥','🐄'], odd:'🐄',  hint:'Fruits vs Animal' },
  { items:['🐘','🦚','🥭','🐯'], odd:'🥭',  hint:'Animals vs Fruit' },
  { items:['🔴','🟦','🟢','🥔'], odd:'🥔',  hint:'Colors vs Veggie' },
  { items:['🚗','🚌','🐘','🚲'], odd:'🐘',  hint:'Vehicles vs Animal' },
  { items:['🍆','🥒','🧅','🍌'], odd:'🍌',  hint:'Vegetables vs Fruit' },
  { items:['🐄','🐕','🐈','🌻'], odd:'🌻',  hint:'Animals vs Flower' },
  { items:['✏️','📚','🖊️','🐒'], odd:'🐒',  hint:'School items vs Animal' },
  { items:['🪔','🎆','🎇','🥥'], odd:'🥥',  hint:'Festival vs Fruit' },
  { items:['🏠','🏫','🏥','🍎'], odd:'🍎',  hint:'Buildings vs Fruit' },
  { items:['🌧️','☀️','❄️','🐯'], odd:'🐯',  hint:'Weather vs Animal' },
  { items:['🥭','🥔','🍆','🧅'], odd:'🥭',  hint:'Vegetables vs Fruit' },
  { items:['🚌','✈️','🚂','🦜'], odd:'🦜',  hint:'Transport vs Bird' },
  { items:['🐒','🦁','🐯','🚗'], odd:'🚗',  hint:'Animals vs Vehicle' },
  { items:['📱','💻','📺','🥦'], odd:'🥦',  hint:'Electronics vs Veggie' },
  { items:['🌸','🌺','🌻','🐘'], odd:'🐘',  hint:'Flowers vs Animal' },
  { items:['🔴','🔴','🔴','🟦'], odd:'🟦',  hint:'3 Red vs 1 Blue' },
  { items:['🍫','🎂','🍩','🥨'], odd:'🥨',  hint:'Sweet vs Salty' },
  { items:['👕','👖','🧦','🧸'], odd:'🧸',  hint:'Clothes vs Toy' },
  { items:['🐕','🐈','🐎','🦜'], odd:'🦜',  hint:'4 legs vs Bird' },
  { items:['⚽','🏀','🎾','📱'], odd:'📱',  hint:'Balls vs Phone' },
  { items:['🍓','🍒','🍉','🍋'], odd:'🍋',  hint:'Red Fruits vs Yellow' },
  { items:['🌲','🌳','🌴','🌹'], odd:'🌹',  hint:'Trees vs Flower' },
  { items:['🚢','🚤','🛶','✈️'], odd:'✈️',  hint:'Water vs Air' },
  { items:['🐝','🦋','🐞','🐀'], odd:'🐀',  hint:'Insects vs Mammal' },
  { items:['👨‍🍳','👨‍⚕️','👮‍♂️','🐕'], odd:'🐕',  hint:'Jobs vs Animal' },
  { items:['🎹','🎸','🎺','🍔'], odd:'🍔',  hint:'Instruments vs Food' },
  { items:['🥶','🧊','❄️','🔥'], odd:'🔥',  hint:'Cold vs Hot' },
  { items:['🛏️','🛋️','🪑','🚗'], odd:'🚗',  hint:'Furniture vs Vehicle' },
  { items:['👓','🧤','🧣','📸'], odd:'📸',  hint:'Wearable vs Camera' },
  { items:['🌙','⭐','🌌','☀️'], odd:'☀️',  hint:'Night vs Day' },
];"""

odd_path = os.path.join(act_dir, 'odd-one-out.html')
with open(odd_path, 'r', encoding='utf-8') as f:
    odd_content = f.read()

odd_content = re.sub(r'const PUZZLES = \[.*?\];', odd_val, odd_content, flags=re.DOTALL)
with open(odd_path, 'w', encoding='utf-8') as f:
    f.write(odd_content)
print("Updated odd-one-out.html banks")

# 3. Update Sorting Game Arrays
sort_val = """const ROUND_TYPES = [
  { titleHi: '🍎 फल vs 🥕 सब्ज़ी', catA: {label:{en:'Fruits', hi:'फल', gu:'ફળ'}, emoji:'🍎'}, catB: {label:{en:'Veggies', hi:'सब्ज़ी', gu:'શાક'}, emoji:'🥕'}, items: [ {emoji:'🥭',hi:'आम', cat:'a'}, {emoji:'🍌',hi:'केला', cat:'a'}, {emoji:'🍎',hi:'सेब', cat:'a'}, {emoji:'🍊',hi:'संतरा', cat:'a'}, {emoji:'🥥',hi:'नारियल', cat:'a'}, {emoji:'🥕',hi:'गाजर', cat:'b'}, {emoji:'🥔',hi:'आलू', cat:'b'}, {emoji:'🍆',hi:'बैंगन', cat:'b'}, {emoji:'🌽',hi:'मकई', cat:'b'}, {emoji:'🧅',hi:'प्याज', cat:'b'} ] },
  { titleHi: '🐾 जानवर vs 🚗 वाहन', catA: {label:{en:'Animals', hi:'जानवर', gu:'પ્રાણી'}, emoji:'🐾'}, catB: {label:{en:'Vehicles', hi:'वाहन', gu:'વાહન'}, emoji:'🚗'}, items: [ {emoji:'🐄',hi:'गाय', cat:'a'}, {emoji:'🐘',hi:'हाथी', cat:'a'}, {emoji:'🦚',hi:'मोर', cat:'a'}, {emoji:'🐯',hi:'बाघ', cat:'a'}, {emoji:'🐕',hi:'कुत्ता', cat:'a'}, {emoji:'🚗',hi:'कार', cat:'b'}, {emoji:'🚌',hi:'बस', cat:'b'}, {emoji:'✈️',hi:'हवाई जहाज', cat:'b'}, {emoji:'🚂',hi:'ट्रेन', cat:'b'}, {emoji:'🚲',hi:'साइकिल', cat:'b'} ] },
  { titleHi: 'उड़ने वाले vs पानी वाले', catA: {label:{en:'Flies', hi:'उड़ता है', gu:'ઉડે છે'}, emoji:'✈️'}, catB: {label:{en:'Swims', hi:'पानी में', gu:'પાણીમાં'}, emoji:'🐟'}, items: [ {emoji:'✈️',hi:'हवाई जहाज', cat:'a'}, {emoji:'🦅',hi:'चील', cat:'a'}, {emoji:'🦋',hi:'तितली', cat:'a'}, {emoji:'🦜',hi:'तोता', cat:'a'}, {emoji:'🚁',hi:'हेलीकॉप्टर', cat:'a'}, {emoji:'🐟',hi:'मछली', cat:'b'}, {emoji:'🐬',hi:'डॉल्फिन', cat:'b'}, {emoji:'🦈',hi:'शार्क', cat:'b'}, {emoji:'🐊',hi:'मगरमच्छ', cat:'b'}, {emoji:'🐸',hi:'मेंढक', cat:'b'} ] },
  { titleHi: 'गर्म vs ठंडा', catA: {label:{en:'Hot', hi:'गर्म', gu:'ગરમ'}, emoji:'🔥'}, catB: {label:{en:'Cold', hi:'ठंडा', gu:'ઠંડુ'}, emoji:'🧊'}, items: [ {emoji:'☀️',hi:'सूरज', cat:'a'}, {emoji:'☕',hi:'चाय', cat:'a'}, {emoji:'🔥',hi:'आग', cat:'a'}, {emoji:'🌋',hi:'ज्वालामुखी', cat:'a'}, {emoji:'🍳',hi:'गर्म तवा', cat:'a'}, {emoji:'🧊',hi:'बर्फ', cat:'b'}, {emoji:'🍦',hi:'आइसक्रीम', cat:'b'}, {emoji:'❄️',hi:'स्नो', cat:'b'}, {emoji:'🥶',hi:'ठंड', cat:'b'}, {emoji:'⛄',hi:'स्नोमैन', cat:'b'} ] },
  { titleHi: 'लाल vs नीला', catA: {label:{en:'Red', hi:'लाल', gu:'લાલ'}, emoji:'🔴'}, catB: {label:{en:'Blue', hi:'नीला', gu:'વાદળી'}, emoji:'🔵'}, items: [ {emoji:'🍎',hi:'लाल', cat:'a'}, {emoji:'🌹',hi:'लाल', cat:'a'}, {emoji:'🍅',hi:'लाल', cat:'a'}, {emoji:'🌶️',hi:'लाल', cat:'a'}, {emoji:'🎈',hi:'लाल', cat:'a'}, {emoji:'🫐',hi:'नीला', cat:'b'}, {emoji:'💧',hi:'नीला', cat:'b'}, {emoji:'🌊',hi:'नीला', cat:'b'}, {emoji:'🔷',hi:'नीला', cat:'b'}, {emoji:'🫙',hi:'नीला', cat:'b'} ] },
  { titleHi: 'खिलौना vs फर्नीचर', catA: {label:{en:'Toys', hi:'खिलौने', gu:'રમકડાં'}, emoji:'🧸'}, catB: {label:{en:'Furniture', hi:'फर्नीचर', gu:'ફર્નિચર'}, emoji:'🪑'}, items: [ {emoji:'🧸',hi:'खिलौना', cat:'a'}, {emoji:'🪀',hi:'यो-यो', cat:'a'}, {emoji:'🪁',hi:'पतंग', cat:'a'}, {emoji:'🎮',hi:'गेम', cat:'a'}, {emoji:'🧩',hi:'पहेली', cat:'a'}, {emoji:'🪑',hi:'कुर्सी', cat:'b'}, {emoji:'🛏️',hi:'बिस्तर', cat:'b'}, {emoji:'🛋️',hi:'सोफा', cat:'b'}, {emoji:'🚪',hi:'दरवाजा', cat:'b'}, {emoji:'🛁',hi:'टब', cat:'b'} ] },
  { titleHi: 'मीठा vs नमकीन', catA: {label:{en:'Sweet', hi:'मीठा', gu:'મીઠું'}, emoji:'🍩'}, catB: {label:{en:'Salty', hi:'नमकीन', gu:'નમકીન'}, emoji:'🥨'}, items: [ {emoji:'🍩',hi:'डोनट', cat:'a'}, {emoji:'🎂',hi:'केक', cat:'a'}, {emoji:'🍫',hi:'चॉकलेट', cat:'a'}, {emoji:'🍭',hi:'लॉलीपॉप', cat:'a'}, {emoji:'🍬',hi:'टॉफी', cat:'a'}, {emoji:'🥨',hi:'नमकीन', cat:'b'}, {emoji:'🍟',hi:'फ्रेंच फ्राइज़', cat:'b'}, {emoji:'🍕',hi:'पिज्ज़ा', cat:'b'}, {emoji:'🍿',hi:'पॉपकॉर्न', cat:'b'}, {emoji:'🧀',hi:'पनीर', cat:'b'} ] },
  { titleHi: 'दिन vs रात', catA: {label:{en:'Day', hi:'दिन', gu:'દિવસ'}, emoji:'☀️'}, catB: {label:{en:'Night', hi:'रात', gu:'રાત'}, emoji:'🌙'}, items: [ {emoji:'☀️',hi:'सूरज', cat:'a'}, {emoji:'🌻',hi:'धूप', cat:'a'}, {emoji:'🌈',hi:'इंद्रधनुष', cat:'a'}, {emoji:'🕶️',hi:'धूप का चश्मा', cat:'a'}, {emoji:'🏖️',hi:'गर्मी', cat:'a'}, {emoji:'🌙',hi:'चांद', cat:'b'}, {emoji:'⭐',hi:'तारा', cat:'b'}, {emoji:'🌌',hi:'रात', cat:'b'}, {emoji:'🦉',hi:'उल्लू', cat:'b'}, {emoji:'🦇',hi:'चमगादड़', cat:'b'} ] }
];"""

sort_path = os.path.join(act_dir, 'sorting-game.html')
with open(sort_path, 'r', encoding='utf-8') as f:
    sort_content = f.read()

sort_content = re.sub(r'const ROUND_TYPES = \[.*?\];', sort_val, sort_content, flags=re.DOTALL)
# Make sure sorting-game only selects 5 categories tops!
sort_content = sort_content.replace('const TOTAL_ROUNDS = ROUND_TYPES.length;', 'const TOTAL_ROUNDS = Math.min(5, ROUND_TYPES.length);')
# sorting-game uses `shuffle([...ROUND_TYPES])` in initGame:
#   const rt = ROUND_TYPES[idx];
# We need to change that so it shuffles only once and takes 5.
import re
def inject_sort_shuffle(m):
    return "ROUND_TYPES = shuffle(ROUND_TYPES).slice(0, TOTAL_ROUNDS);\n  roundIdx = 0;"
sort_content = re.sub(r'roundIdx = 0;.*?\n(.*?)hideFeedback\(\);', "hideFeedback();\n  // Shuffle ROUND_TYPES once\n  " + r"var currentRounds = shuffle(ROUND_TYPES).slice(0, TOTAL_ROUNDS);\n  window.currentRounds = currentRounds;\n  roundIdx = 0;\n  mistakes = 0; totalAnswered = 0;\n", sort_content, flags=re.DOTALL)

# Fixing the reference
sort_content = sort_content.replace('const rt = ROUND_TYPES[idx];', 'const rt = window.currentRounds[idx];')

with open(sort_path, 'w', encoding='utf-8') as f:
    f.write(sort_content)
    
print("Updated sorting-game.html banks")
