import gensim
import gensim.downloader
import nltk

someArray = []
# We skip the first line in the file since it's explanatory information and not data
# Set this to 0 if your file is all data
skipLine = 1
#Task 1

def getTerms():
    global skipLine
    file = open("C:\\Users\\Pub\\Desktop\\Data\\synonyms.csv","r")
    content = file.read()
    array = [line for line in content.split('\n') if line]

    for line in array:
        if skipLine == 0:
            r = line.replace(',', ' ')
            someArray.append(r)
        else:
            skipLine -= 1

def evaluation(m_name):
    c_count = 0
    w_count = 0
    g_count = 0

    output_line = ""
    correct_word = ""
    guess_word = ""
    NOT_FOUND_FLAG = False
    model = gensim.downloader.load(m_name)
    path = 'C:\\Users\\Pub\\Desktop\\Data\\'
    myfile = path + m_name + ".csv"
    f = open(myfile, "x")

    for line in someArray:
        word_array = line.split(" ")
        output_line += word_array[0]
        output_line += ","

        correct_word = word_array[1]
        output_line += correct_word
        output_line += ","

        guess_word = ""

        try:
            list = model.similar_by_vector(word_array[0])
            #print(list)
            for guess in list:
                for i in range(2,len(word_array)):
                    if guess[0].lower() == word_array[i].lower():
                        guess_word = guess[0]
                        break
                if guess_word != "":
                    break

            if guess_word != '':
                output_line += guess_word
                output_line += ","
            else:
                output_line += list[0][0]
                output_line += ","

        except KeyError:
            output_line += "NOT FOUND"
            output_line += ","

        if guess_word == '':
            output_line += 'guess'
            g_count += 1
        elif correct_word.lower() == guess_word.lower():
            output_line += 'correct'
            c_count += 1
        else:
            output_line += 'wrong'
            w_count += 1

        f.write(output_line+'\n')
        output_line = ""

    # After all 80 terms have been analyzed, write to file
    an_line = m_name +","+str(len(model))+","+str(c_count)+","+str(80-g_count)+","+str(c_count/80)
    analysis_file = path + "analysis.csv"
    f2 = open(analysis_file, "a")
    f2.write(an_line)


getTerms()
evaluation("word2vec-google-news-300")
# C1 != C2 E1 = E2
evaluation("glove-twitter-200")
evaluation("glove-wiki-gigaword-200")
# C3 = C4 E3 != E4
evaluation("glove-wiki-gigaword-100")
evaluation("glove-wiki-gigaword-300")



