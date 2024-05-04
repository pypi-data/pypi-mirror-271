from negate.negate import Negator

# negator = Negator(use_transformers=True)
negator = Negator()

while True:
    sentence = input("Sentence: ")
    print(negator.negate_sentence(sentence, True))
