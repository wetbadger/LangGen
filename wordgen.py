import random
import json
import numpy
from math import *
import tkinter as tk

LANGS={
"english" : ["k s ɹ d m p b f l h w t pɹ n v st tɹ ʤ ɡ ʃ bɹ ɡɹ ʧ kl kɹ j sp dɹ fɹ pl fl sk stɹ θ bl ð kw sw ɡl sl θɹ sm th tw skɹ sn ʍ ʃɹ spɹ skw spl","t l ɹ n s ʃ m d v k nt p z b f nd st ns ʤ ɡ kt ʧ mp sp ks kʃ pɹ w ð kj nv h nf nj stɹ kw lt mb tl ntɹ nʃ θ j mpl nʤ sk tɹ bl ɡɹ ɹt nl ksp ntl kl ɡz pl ŋ dl ɡn ld sl nst lj nk ɹm kɹ mpɹ ŋɡ dv tj ŋk pt bj nʧ ɹd bɹ dm ft fɹ kst mj nkl sʧ fl nstɹ pʃ ɹl sf ɹs bs dɹ ɡj tn vl kspl kʧ tf vɹ bʤ ndɹ nh tm ɹk kn mpt nsp nw pj skɹ ɹn dj dn kstɹ ktɹ ln ml nm stl bz fj kskl kspɹ lf lk lm mbl mbɹ mf mn nfl nɹ ŋɡw ɹɡ bst ls lɹ ndl sj skl sm spl vm ŋkʃ ŋl ɹf ɹʃ ɹʧ ʃm df ɡl ldl lv lʤ mpj mw nkw nsm ntm nz sn ts tw ɹb ʤm ʧm bm ksʧ ktl lb mpʃ mz mɹ nɡ nkɹ nsf nsj nskɹ sɡ skj sw vj zm ðdɹ ŋkw ɹv ɹʤ θf θl bt dw km lɡɹ lkj lp lw lθ mst nb nfɹ nɡɹ nn nzl nʤm pʧ stj stw vn ŋɡɹ ɾ ʃn bd bskj bstɹ ds ftl ɡm kskj ktf ltj ltɹ lʧ mft ms mt ndj nfj npl nsl nzp nθj pm pw ɹsm sd sɡɹ spj stm tb tsm zb zd zj zl ðst ŋɡj ŋɡl ŋkt ŋkʧ ɹml ɹpl ɹtl ɹθw ʤt ʧl θɹ bn bskɹ bv bɾ dɡ dɡɹ dkw dʃ fspɹ ftw ɡʤ kd kf kɡɹ kw ksf ksk kskw ksm ksw kz ldf ldh ldn ldɹ lɡ ll lpf lpl lptj lsh lsʍ lð mfl mfɹ mh mptl mpʧ mʧ mθ nbɹ ndm","n d l ŋ t z s nt k m st nd ns nz v lz kt ld p ts ʤ ʃ ɹ ks f dz nts ʧ θ mz zd ɡ b pt ŋz ɹd ndz vd ps rm ŋk ʃt lt md ɹz ft vz sts mp ʤd ʧt nst kts lf sk ɡz kst nʤ nʧ ɹt ŋks mpt ɹm bl lv nθ ŋkt ɹk ɹn ɹs bd fs sp ð ɹmd ɹmz ɹts bz ldz lvz ŋd ɹdz dst ɡd lk ls lts lvd lθ r spt ɹst ɹʧt lm mps nʤd ðz ɹks ɹkt ɹnd ɹʃ ɹθ θs","ɪ ɛ i eɪ æ aɪ ʌ ɑ u oʊ ɔ ɑ ɜ aʊ ʊ ɪə ɛə ɔɪ ʊə"]
} #source = https://www.vulgarlang.com/

class Language:
    def __init__(self, name, size, seed_word):
        self.name = name
        self.vocabulary = []
        #print("Generating " + name + ", a language of " + str(size) + " words...")
        for rank in range(size):
            word = update_text(seed_word,"All Languages","", rank+1)
            pronunciation = word[0]
            transliteration = word[1]
            definition = word[2]
            new_word = Word(rank, pronunciation, transliteration, definition, "?")
            self.vocabulary.append(new_word)
        language = {}
        for word_object in self.vocabulary:
            if word_object.pronunciation in language:
                language[word_object.pronunciation]["definition"].append(word_object.definition)
            else:
                language[word_object.pronunciation] = {
                    "definition" : [word_object.definition],
                    "transliteration" : word_object.transliteration,
                    "part of speech" : word_object.part_of_speech,
                    "rank" : word_object.rank
                }

        print(language)

        with open(self.name.transliteration+".json", "w") as lang_file:
            lang_file.write(json.dumps(language, indent=2))

class Word:
    def __init__(self, rank, pronunciation, transliteration, definition, part_of_speech):
        self.rank = rank
        self.pronunciation = pronunciation
        self.transliteration = transliteration
        self.definition = definition
        self.part_of_speech = part_of_speech

def listify_phonemes(LANGS): #makes the strings in the LANG data structure into lists
    result = {}
    for l,phon in LANGS.items():
        list = []
        for each in phon:
            a=each.split()
            list.append(a)
        result[l]=list
    return result

def getWord(seed_word,lang,rank=None):
    def get_sylables(rank, c=10): #where c is the tendency to have one sylable throughout the language
        x = log(rank+c**3)-c*log(2)
        if x < 0:
            x = 0
        return numpy.random.poisson(lam=x, size=None)+1
    def end_blend(consonant):
        if consonant == 's': #almost guaranteed to add a consonant blend
            l = random.choice(['k','p','t'])
        elif consonant == 'f':
            l = random.choice(['k','t','s'])
        elif consonant in ['m','ɱ','n','ɴ']:
            l = random.choice(['k','t','s'])
        elif consonant == 'p':
            l = random.choice(['t','s'])
        elif consonant not in ['s','ʑ']:
            if random.randint(1,8) == 1:#this blend can be a bit awkward so make it a little rare
                l = 's'
            else:
                l = ''
        else:
            l = ''
        return l
    def begin_blend(consonant):
        if consonant == 's':
            l = random.choice(['c','f','k','l','m','n','p','q','r','t','v','w'])
        elif consonant in ['b','ɓ','c','d','ɖ','ɗ','f','g','ɠ','ɢ','ʛ','ɰ','ɣ','ʡ','ʢ','h','ɦ','ħ','k','m','ɱ','n','ɴ','p','q','t','ʔ','z']:
            l = random.choice(['l','r','w'])
        elif consonant in ['j','ʝ','ɟ','ʄ']:
            l = 'r'
        elif consonant == 'v':
            l = random.choice(['l','r'])
        else:
            l = ''
        return l
    def split_word(word):
        return [char for char in word]
    consonants = "b ɓ β ʙ c ç d ɖ ɗ ʣ ʥ ʤ f ɸ g ɠ ɢ ʛ ɰ h ɦ ħ ɧ ɥ ʜ j ʝ ɟ ʄ k l ɫ ɬ ɮ ɭ ʟ m ɱ n ɳ ɲ ŋ ɴ p q r ɹ ɾ ɽ ɻ ɺ ʁ ʀ s ʂ ɕ ʃ t ʈ ʦ ʨ ʧ v ⱱ ʋ w ʍ x ɣ χ ʎ z ʐ ʑ ʒ θ ð ʔ ʡ ʕ ʢ ʘ ǀ ǃ ǂ ǁ"
    vowels = "a æ ɑ ɒ ɐ e ɛ ɜ ɞ ə i ɨ ɪ y ʏ ø ɘ ɵ œ ɶ ɤ o ɔ u ʉ ʊ ɯ ʌ"
    consonants = consonants.split(' ')
    vowels = vowels.split(' ')
    if seed_word != "":
        seed = split_word(seed_word)
        nCons = []
        nVow = [] #new consonants and vowels list
        for char in seed: #make two short lists [consonants] and [vowels] that only include phonemes from the seedword
            if char in consonants:
                nCons.append(char)
            elif char in vowels:
                nVow.append(char)
        consonants = nCons
        vowels = nVow
    sylable_types=['v', 'vc', 'cv', 'cvc']
    if rank == None:
        num_sylables = random.randint(1,5)
    else:
        num_sylables = get_sylables(rank)
    x=0
    string = ''
    need_consonant=False
    dipthong_frequency=1 #1 is always allow dipthongs
    tripthong_frequency=0.1
    consonant_blend_frequency=0.5
    triple_consonant_blend_frequency=0.1
    thong=0
    while x < num_sylables:
        if need_consonant == False:
            type=random.choice(sylable_types)
            t=type
        else:
            type=random.choice(sylable_types[-2:])
            t=type
        if t == 'v':
            string=string+random.choice(vowels)
            if thong == 0:
                if random.random() < dipthong_frequency:
                    need_consonant=False
                    thong+=1
                else:
                    need_consonant=True #next sylable must start with a consonant
                    thong=0
            elif thong == 1:
                if random.random() < tripthong_frequency:
                    need_consonant=False
                    thong+=1
                else:
                    need_consonant=True
                    thong=0
        elif t == 'vc':
            string=string+random.choice(vowels)
            consonant = random.choice(consonants)
            string=string+consonant
            if random.random() < consonant_blend_frequency:
                consonant=end_blend(consonant)
                string=string+consonant
                if random.random() < triple_consonant_blend_frequency:
                    string=string+end_blend(consonant)
            need_consonant=False
        elif t == 'cv':
            consonant=random.choice(consonants)
            string=string+consonant
            if random.random() < consonant_blend_frequency:
                consonant=begin_blend(consonant)
                string=string+consonant
                if random.random() < triple_consonant_blend_frequency:
                    string=string+begin_blend(consonant)
            string=string+random.choice(vowels)
            need_consonant=True
        elif t == 'cvc':
            consonant=random.choice(consonants)
            string=string+consonant
            if random.random() < consonant_blend_frequency:
                consonant=begin_blend(consonant)
                string=string+consonant
                if random.random() < triple_consonant_blend_frequency:
                    string=string+begin_blend(consonant)
            string=string+random.choice(vowels)
            consonant=random.choice(consonants)
            string=string+consonant
            if random.random() < consonant_blend_frequency:
                consonant=end_blend(consonant)
                string=string+consonant
                if random.random() < triple_consonant_blend_frequency:
                    string=string+end_blend(consonant)
            need_consonant=False
        x+=1
    return string
def transliterate(string): #this is one of many possible spelling/transliteration systems
    w = ''
    for l in string:
        #consonants
        if l in ['b','ɓ']:
            w = w + 'b'
        if l in ['ʐ','ʑ','ʒ']:
            w = w + 'zh'
        if l == 'ʙ':
            w = w + 'bb'
        if l == 'c':
            w = w + 'c'
        if l in ['ç','ɕ','ʃ']:
            w = w + 'sh'
        if l in ['d','ɖ','ɗ']:
            w = w +'d'
        if l == 'ʣ':
            w = w + 'dz'
        if l in ['ʥ','ʤ']:
            w = w + 'dj'
        if l == 'f':
            w = w + 'f'
        if l in ['ɸ','ʈ','θ','ð']:
            w = w + 'th'
        if l in ['g','ɠ','ɢ','ʛ','ɰ','ɣ','ʡ','ʢ']:
            w = w + 'g'
        if l in ['h','ɦ','ħ']:
            w = w + 'h'
        if l == 'ɧ':
            w = w + 'sj'
        if l in ['ʜ']:
            w = w + 'x'
        if l in ['j','ʝ','ɟ','ʄ']:
            w = w + 'j'
        if l == 'k':
            w = w + 'k'
        if l in ['l','ɫ','ɭ','ʟ','ɺ']:
            w = w + 'l'
        if l == 'ɬ':
            w = w + 'lh'
        if l == 'ɮ':
            w = w + 'dl'
        if l in ['m','ɱ']:
            w = w + 'm'
        if l in ['n','ɴ']:
            w = w + 'n'
        if l == 'ɳ':
            w = w + 'rn'
        if l == 'ɲ':
            w = w + 'ñ'
        if l == 'ŋ':
            w = w + 'ng'
        if l == 'p':
            w = w + 'p'
        if l == 'q':
            w = w + 'q'
        if l in ['r','ɹ','ɾ','ɽ','ɻ','ʁ','ʀ','ʕ']:
            w = w + 'r'
        if l == 's':
            w = w + 's'
        if l == 'ʂ':
            w = w + 'sch'
        if l in ['t','ʔ']:
            w = w + 't'
        if l == 'ʦ':
            w = w + 'tz'
        if l in ['ʨ','ʧ','χ']:
            w = w + 'ch'
        if l in ['v','ʋ','β']:
            w = w + 'v'
        if l == 'ⱱ':
            w = w + 'ph'
        if l in ['w','ɥ']:
            w = w + 'w'
        if l == 'ʍ':
            w = w + 'wh'
        if l == 'x':
            w = w + 'x'
        if l == 'ʎ':
            w = w + 'gl' #the italian way
        if l == 'z':
            w = w + 'z'
        if l == 'ʘ':
            w = w + "m!"
        if l == 'ǃ':
            w = w + 'n!'
        if l == 'ǀ':
            w = w + 'ngc'
        if l == 'ǂ':
            w = w + 'tch'
        if l == 'ǁ':
            w = w + 'xh'
        #vowels
        if l in ['a','æ','ɑ','ɒ','ʌ']:
            w = w + 'a'
        if l in ['ɐ','e','ɛ','ɘ']:
            w = w + 'e'
        if l in ['ɜ','i','ɪ','ɵ']:
            w = w + 'i'
        if l in ['ɞ','ə','ɨ','ʏ','u']:
            w = w + 'u'
        if l == 'y':
            w = w + 'y'
        if l in ['ø','œ','ɯ']:
            w = w + 'eu'
        if l == 'ɶ':
            w = w + 'ö'
        if l == 'ɤ':
            w = w + 'oe'
        if l in ['o','ɔ']:
            w = w + 'o'
        if l == 'ʉ':
            w = w + 'oo'
        if l == 'ʊ':
            w = w + 'ou'
    return w

def get_definition(rank):
    #common words have similar definitions across languages
    if rank == None:
        return random.randint(0,90000)
    else:
        return abs(rank + random.randint(-rank-10, rank+10))

def definition_from_chart(definition):
    with open("frequency-90000.txt", "r") as chart:
        line = chart.readlines()[definition]
        return line.split()[1]

def update_text(seed_word,lang,definition=1,rank=None):
    if lang == "All Languages":
        pronunciation = getWord(seed_word,lang,rank)
    else:
        pronunciation = getWordFromLang(seed_word,lang,rank)
    spell = transliterate(pronunciation)
    print(spell)
    definition = definition_from_chart(get_definition(rank))
    words.insert('1.0', "-"+pronunciation+"\n "+spell+"\n  "+definition+"\n") #gui widgets are all global lol
    return pronunciation,spell,definition

def generate_lang(seed, lang, size, textbox):
    try:
        size = int(size)
    except ValueError:
        size = 100
    boxAsList = textbox.split("\n")
    transliteration = boxAsList[1][1:]
    pronunciation = boxAsList[0][1:]
    definition = "A language."

    lang_name = Word(random.randint(300,600),pronunciation,transliteration,definition,"noun")
    lang = Language(lang_name, size, seed)

def open_langs():
    lr = tk.Tk()
    lr.title("Languages")
    main = tk.Frame(lr)

    Frame1 = tk.Frame(main)
    Frame2 = tk.Frame(main)
    Frame3 = tk.Frame(main)
    Frame4 = tk.Frame(main)
    Frame5 = tk.Frame(main)
    
    rank_lb = tk.Label(Frame1, text="Rank")
    rank_ls = tk.Listbox(Frame1, height=40, width=10)

    word_lb = tk.Label(Frame2, text="Word")
    word_ls = tk.Listbox(Frame2, height=40, width=30)

    prnctn_lb = tk.Label(Frame3, text="Pronunciation")
    prnctn_ls = tk.Listbox(Frame3, height=40, width=30)

    definition_lb = tk.Label(Frame4, text="Definition")
    definition_ls = tk.Listbox(Frame4, height=40, width=30)

    part_of_of_speech_lb = tk.Label(Frame5, text="Part of Speech")
    part_of_of_speech_ls = tk.Listbox(Frame5, height=40, width=15)

    main.pack()

    rank_lb.pack()
    rank_ls.pack()

    word_lb.pack()
    word_ls.pack()

    prnctn_lb.pack()
    prnctn_ls.pack()

    definition_lb.pack()
    definition_ls.pack()

    part_of_of_speech_lb.pack()
    part_of_of_speech_ls.pack()
    
    Frame1.pack(side="left")
    Frame2.pack(side="left")
    Frame3.pack(side="left")
    Frame4.pack(side="left")
    Frame5.pack(side="left")
    results_frame.pack()

def open_settings():
    pass

LANGS = listify_phonemes(LANGS) #makes strings a list because I copied and pasted the phonemes
                                #but otherwise treat LANGS as a constant

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Word Generator")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    fileMenu = tk.Menu(menubar, tearoff="off")
    menubar.add_cascade(label="File", menu=fileMenu)

    fileMenu.add_command(label="Languages", command=open_langs)
    fileMenu.add_command(label="Save")
    fileMenu.add_command(label="Save As")
    fileMenu.add_command(label="Save All")
    fileMenu.add_command(label="Recent Languages")
    fileMenu.add_command(label="View Languages")
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=quit)

    editMenu = tk.Menu(menubar, tearoff="off")
    menubar.add_cascade(label="Edit", menu=editMenu)
    editMenu.add_command(label="Settings")


    lang_menu = tk.StringVar(root)
    lang_menu.set("All Languages") # default value
    top_frame = tk.Frame(root)
    results_frame = tk.Frame(top_frame)
    langgen_frame = tk.Frame(top_frame)
    bottom_frame =tk.Frame(root)
    wordgen_frame = tk.Frame(bottom_frame)

    langs = tk.OptionMenu(wordgen_frame, lang_menu, "All Languages","Men","Elves","Orcs","Aliens")
    langs.config(width = 10)
    new = tk.Button(wordgen_frame, text="New Word", command=lambda:update_text(seed_word.get(),lang_menu.get()))
    words = tk.Text(results_frame, height=10, width=30)
    seed_label = tk.Label(wordgen_frame, text="Seed: ")
    seed_word = tk.Entry(wordgen_frame)
    size_label = tk.Label(langgen_frame, text="Size: ")
    size = tk.Entry(langgen_frame, width = 4)
    lang_label = tk.Label(langgen_frame, text="Language: ")
    generate = tk.Button(langgen_frame, text="Generate", command=lambda:generate_lang(seed_word.get(),lang_menu.get(),size.get(),words.get('1.0',"end")))
    update_text(seed_word.get(),lang_menu.get())

    top_frame.pack()
    bottom_frame.pack()

    words.pack()
    results_frame.pack(side='left')

    langs.pack(side='left',padx=(50,10))
    new.pack(padx=(50,10))
    seed_label.pack(side='left')
    seed_word.pack(side='right')

    lang_label.pack()
    generate.pack()
    size_label.pack(side='left')
    size.pack()
    langgen_frame.pack(side='top')
    wordgen_frame.pack()

    tk.mainloop()
