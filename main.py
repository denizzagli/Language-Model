# In this section, I called the libraries required for the code. I used the Math library to do logarithm operations, and
# I used the random library to do random operations.

import math
import random


# Opens the file in the path it takes as a parameter.  New line markings at theend of lines.  Strips the line numbers at
# the beginning of the line.

def dataset(folderPath):
    input_file = open(folderPath, "r")
    sentences = []
    for line in input_file.readlines():
        line = line.strip("\n")
        if len(line) != 0:
            temp = line.split(' ', 1)
            sentences.append(temp[1])
    input_file.close()
    return sentences


# This function removes all punctuation marks in English indataset.  This function has been created separately in order
# to be able to examine transactions bothwith and without punctuations.
# Source: "https://www.ef.com/ca/english-resources/english-grammar/punctuation/".

def removing_punctuation(sentences):
    for index in range(len(sentences)):
        sentences[index] = sentences[index].replace(".", "")
        sentences[index] = sentences[index].replace(",", "")
        sentences[index] = sentences[index].replace("!", "")
        sentences[index] = sentences[index].replace("?", "")
        sentences[index] = sentences[index].replace(";", "")
        sentences[index] = sentences[index].replace(":", "")
        sentences[index] = sentences[index].replace("\"", "")
        sentences[index] = sentences[index].replace("`", "")
        sentences[index] = sentences[index].replace("_", "")
        sentences[index] = sentences[index].replace("-", "")
        sentences[index] = sentences[index].replace("[", "")
        sentences[index] = sentences[index].replace("]", "")
        sentences[index] = sentences[index].replace("(", "")
        sentences[index] = sentences[index].replace("/", "")
        sentences[index] = sentences[index].replace("<", "")
        sentences[index] = sentences[index].replace(">", "")
        sentences[index] = sentences[index].replace("{", "")
        sentences[index] = sentences[index].replace("}", "")


# Removes marks other than punctuation marks from the dataset.

def removing_marking(sentences):
    for index in range(len(sentences)):
        sentences[index] = sentences[index].replace("\t", " ")
        sentences[index] = sentences[index].replace("|", " ")
        sentences[index] = sentences[index].replace("£", "")
        sentences[index] = sentences[index].replace("#", "")
        sentences[index] = sentences[index].replace("+", "")
        sentences[index] = sentences[index].replace("$", "")
        sentences[index] = sentences[index].replace("%", "")
        sentences[index] = sentences[index].replace("&", "")
        sentences[index] = sentences[index].replace("*", "")
        sentences[index] = sentences[index].replace("@", "")


# Converts all the letters of the words in the dataset to low-ercase.

def lowercasing_the_tokens(sentences):
    for index in range(len(sentences)):
        sentences[index] = sentences[index].lower()


# This function was created to perform all preprocessing operations un-der a single function.  Empty strings are also
# cleaned.  To indicate the beginning of sentences, a ¡s¿token is placed at the beginning of each sentence.  To indicate
# the end of the sentences, the token </s> is put.

def preprocessing(sentences):
    removing_punctuation(sentences)
    removing_marking(sentences)
    lowercasing_the_tokens(sentences)
    for index in range(len(sentences)):
        temp = sentences[index].split(" ")
        temp = list(filter((" ").__ne__, temp))
        temp = list(filter(("").__ne__, temp))
        str_temp = "<s> "
        for item in temp:
            str_temp = str_temp + item + " "
        str_temp = str_temp + "</s>"
        sentences[index] = str_temp


# It is almost the same as the preprocessing function. The only difference is that it does not remove punctuation.

def preprocessing_without_punctuation(sentences):
    removing_marking(sentences)
    lowercasing_the_tokens(sentences)
    for index in range(len(sentences)):
        temp = sentences[index].split(" ")
        temp = list(filter((" ").__ne__, temp))
        temp = list(filter(("").__ne__, temp))
        str_temp = "<s> "
        for item in temp:
            str_temp = str_temp + item + " "
        str_temp = str_temp + "</s>"
        sentences[index] = str_temp


# Takes integer and dictionary as parameters. The integer value it takes as aparameter is actually the N value in
# N-Gram. It also synchronizes this model to the dictionary ittakes as a parameter. Since the function will create a
# new model before starting all operations, it completely clears the model it takes as a parameter.

unigram_model = {}
bigram_model = {}
trigram_model = {}

def Ngram(n, model):
    model.clear()
    for index in range(len(sentences)):
        temp = sentences[index].split(" ")
        for index2 in range(len(temp) - (n - 1)):
            str_temp = ""
            index3 = 0
            while index3 != n:
                str_temp = str_temp + temp[index2 + index3] + " "
                index3 = index3 + 1
            str_temp = str_temp[:-1]
            if str_temp in model.keys():
                model[str_temp] = model[str_temp] + 1
            else:
                model[str_temp] = 1


# There were 3 dictionaries that we created empty before. These are uni-grammodel, bigrammodel,
# trigrammodel. This function creates these models using the Ngram function.

def language_models():
    Ngram(1, unigram_model)
    Ngram(2, bigram_model)
    Ngram(3, trigram_model)


# If a sentence is to be entered as a parameter, it prepro-cessing it to make it suitable.

def preprocessing_the_sentence(sentence):
    preprocessing_sentence = [sentence]
    preprocessing(preprocessing_sentence)
    return preprocessing_sentence[0]


# It takes sentence and dictionary as parameters.  Dictionary is actually amodel.  Calculates the probability of MLE
# according to the desired model of the sentence given as aparameter.

def prob(sentence, model):
    list_temp = list(model.keys())[0].split(" ")
    n = len(list_temp)
    str_temp = preprocessing_the_sentence(sentence)
    list_temp2 = str_temp.split(" ")
    if len(list_temp2) > 0:
        result = 1
        for index in range(len(list_temp2) - (n - 1)):
            str_temp2 = ""
            index2 = 0
            while index2 != n:
                str_temp2 = str_temp2 + list_temp2[index + index2] + " "
                index2 = index2 + 1
            str_temp2 = str_temp2[:-1]
            if str_temp2 in list(model.keys()):
                count_of_words = 0
                values = list(model.values())
                for value in values:
                    count_of_words = count_of_words + value
                result = result * (model[str_temp2] / count_of_words)
            else:
                result = result * 0
        return result
    else:
        return -1


# The only difference from the prob function is using laplace smoothing when calculating probability.

def sprob(sentence, model):
    list_temp = list(model.keys())[0].split(" ")
    n = len(list_temp)
    str_temp = preprocessing_the_sentence(sentence)
    list_temp2 = str_temp.split(" ")
    if len(list_temp2) > 0:
        result = 1
        for index in range(len(list_temp2) - (n - 1)):
            str_temp2 = ""
            index2 = 0
            while index2 != n:
                str_temp2 = str_temp2 + list_temp2[index + index2] + " "
                index2 = index2 + 1
            str_temp2 = str_temp2[:-1]
            if str_temp2 in list(model.keys()):
                count_of_words = 0
                values = list(model.values())
                for value in values:
                    count_of_words = count_of_words + value
                result = result * ((model[str_temp2] + 1) / (count_of_words + len(list(model.keys()))))
            else:
                count_of_words = 0
                values = list(model.values())
                for value in values:
                    count_of_words = count_of_words + value
                result = result * (1 / (count_of_words + len(list(model.keys()))))
        return result
    else:
        return -1


# By applying preprocessing to the given sentence, perplexity is calculatedaccording to the desired model.

def ppl(sentence, model):
    list_temp = list(model.keys())[0].split(" ")
    n = len(list_temp)
    str_temp = preprocessing_the_sentence(sentence)
    list_temp2 = str_temp.split(" ")
    if len(list_temp2) > 0:
        count_of_words = 0
        values = list(model.values())
        for value in values:
            count_of_words = count_of_words + value
        sums = 0
        for index in range(len(list_temp2) - (n - 1)):
            str_temp2 = ""
            index2 = 0
            while index2 != n:
                str_temp2 = str_temp2 + list_temp2[index + index2] + " "
                index2 = index2 + 1
            str_temp2 = str_temp2[:-1]
            if str_temp2 in list(model.keys()):
                sums = sums + math.log2(((model[str_temp2] + 1) / (count_of_words + len(list(model.keys())))))
            else:
                sums = sums + math.log2(((1) / (count_of_words + len(list(model.keys())))))
        base = (-1 / count_of_words) * sums
        result = 2 ** base
        return result
    else:
        return -1


# This function actually takes string parameters in 3 different ways. An empty string,a one-word string, or a 2-word
# string. If it takes an empty string as a parameter, it makes a randomprediction using unigram according to the
# frequency of the words. If it takes a single string as aparameter, it makes a weighted random prediction between
# words whose previous word is this string.Meanwhile, he uses a diagram. If it takes a two-word string as a parameter,
# it makes a predominant random prediction between words whose previous words are this string. It uses trigram when
# making the prediction.

def next(word):
    if len(word) == 0:
        weighted_list = []
        keys = list(unigram_model.keys())
        for index in range(len(keys)):
            for count in range(unigram_model[keys[index]]):
                weighted_list.append(keys[index])
        random.shuffle(weighted_list)
        random.shuffle(weighted_list)
        random.shuffle(weighted_list)
        word = random.choice(weighted_list)
        return word
    else:
        list_temp = word.split(" ")
        if len(list_temp) == 1:
            keys = list(bigram_model.keys())
            weighted_list = []
            for index in range(len(keys)):
                temp = keys[index].split(" ")
                if temp[0] == word:
                    for count in range(bigram_model[keys[index]]):
                        weighted_list.append(temp[1])
            random.shuffle(weighted_list)
            random.shuffle(weighted_list)
            random.shuffle(weighted_list)
            word = random.choice(weighted_list)
            return word
        if len(list_temp) == 2:
            keys = list(trigram_model.keys())
            weighted_list = []
            for index in range(len(keys)):
                temp = keys[index].split(" ")
                if temp[0] == list_temp[0] and temp[1] == list_temp[1]:
                    for count in range(trigram_model[keys[index]]):
                        weighted_list.append(temp[2])
            random.shuffle(weighted_list)
            random.shuffle(weighted_list)
            random.shuffle(weighted_list)
            word = random.choice(weighted_list)
            return word
        else:
            return -1


# The sentence generation phase has been created separately for unigram, bigram and trigram. It takes length as the
# parameter, that is, two integer values for the length ofthe sentence and how many sentences we want. It uses the next
# function when creating sentences.It takes <s> as the initial value.

def generate_unigram(length, count):
    generated_sentences = []
    for index in range(count):
        word = ""
        sentence = ""
        for index2 in range(length):
            word_temp = next(word)
            if word_temp == "</s>":
                break
            else:
                sentence = sentence + word_temp + " "
        sentence = sentence[:-1]
        generated_sentences.append(sentence)
    return generated_sentences


def generate_bigram(length, count):
    generated_sentences = []
    for index in range(count):
        word = "<s>"
        sentence = ""
        for index2 in range(length):
            word = next(word)
            if word == "</s>":
                break
            else:
                sentence = sentence + word + " "
        sentence = sentence[:-1]
        generated_sentences.append(sentence)
    return generated_sentences

def generate_trigram(length, count):
    generated_sentences = []
    for index in range(count):
        word = "<s>"
        sentence = ""
        counter = 0
        control = 0
        for index2 in range(length):
            if counter == 0:
                str_temp = next(word)
                sentence = sentence + str_temp + " "
                word = "<s> " + str_temp
                counter = counter + 1
            else:
                list_temp = word.split(" ")
                str_temp = next(word)
                if str_temp == "</s>":
                    control = control + 1
                else:
                    sentence = sentence + str_temp + " "
                    word = list_temp[-1] + " " + str_temp
            if control == 1:
                break
        sentence = sentence[:-1]
        generated_sentences.append(sentence)
    return generated_sentences

sentences = dataset("D:\PyCharm Projects\Assignment1\Assignment1-dataset.txt")
preprocessing(sentences)
language_models()
