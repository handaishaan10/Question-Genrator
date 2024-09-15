import tkinter as tk
from tkinter import ttk
import spacy



nlp = spacy.load(r"C:\Users\handa\AppData\Local\Programs\Python\Python312\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.7.1")#Enter the file path where your en_core_web_sm is installed.

def generate_questions(paragraph):


  questions = []
  doc = nlp(paragraph)

  for sentence in doc.sents:
      root = sentence.root
      # Yes/No questions
      if root.dep_ == "ROOT":  # Check if it's a declarative sentence
          question = f"Does {sentence.text.strip('.')}"
          questions.append(question)

      # Open ended questions
      else:
          question = f"Can you elaborate on {root.text}?"
          questions.append(question)

      # Comparison Questions
      for token in sentence:
          if token.pos_ == "ADJ" and token.head == doc[2]:
              comparison_question = f"How does the Nile River compare to other {token.text} rivers?"
              questions.append(comparison_question)

      # Cause and Effect Questions
      for token in sentence:
          if token.dep_ == "nsubj" and root.dep_ == "auxpass":  # Passive voice sentences
              cause_question = f"What factors led to {root.text} {token.text}?"
              questions.append(cause_question)

      # Prediction Questions
      prediction_verbs = ["become", "evolve", "change", "develop", "grow", "increase", "decrease", "lead to",
                          "result in", "end up"]
      for token in sentence:
          if token.pos_ == "VERB" and token.text in prediction_verbs:
              subject = ""
              object_ = ""
              prediction_question = f"How might {sentence.text.strip('.')} in the future?"
              if subject:
                  prediction_question = f"How might {subject} {token.text} in the future?"
              if object_:
                  prediction_question = f"How might {sentence.text.strip('.')} {token.text} {object_}?"
              questions.append(prediction_question)

      # Example Questions
      for ent in doc.ents:
          if ent.label_ == "GPE" or ent.label_ == "ORG":
              example_question = f"Can you give some examples of {ent.text}?"
              questions.append(example_question)


  return questions

def generate_nouns():

    paragraph = text_entry.get("1.0", tk.END)
    doc = nlp(paragraph)

    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    noun_list.delete(0, tk.END)
    for noun in nouns:
        noun_list.insert(tk.END, noun)
    # return nouns

def extract_sentences():


    paragraph = text_entry.get("1.0", tk.END)
    tokens = noun_entry.get("1.0", tk.END).lower().split()
    doc = nlp(paragraph)
    extracted_sentences = []

    for sent in doc.sents:
        sent_tokens = [token.text.lower() for token in sent]
        if all(token in sent_tokens for token in tokens):
            extracted_sentences.append(sent.text)

    sen_list.delete(0, tk.END)
    sen_list.insert(tk.END, extracted_sentences)

def ask_questions():

  paragraph = text_entry.get("1.0", tk.END)
  questions = generate_questions(paragraph)
  question_list.delete(0, tk.END)
  for question in questions:
    question_list.insert(tk.END, question)


root = tk.Tk()
root.title("EduGenie - Your Education Assistant")

root.configure(bg='#6EACDA')

style = ttk.Style()


label = ttk.Label(root, text="Enter a paragraph:", style="TLabel")
label.pack(pady=10)



text_entry = tk.Text(root, width=50, height=3)
text_entry.pack(pady=10)


ask_button = ttk.Button(root, text="Ask Questions", command=ask_questions, style="TButton")
ask_button.pack(pady=10)

style.configure("TButton", foreground="red", font=('Papyrus',12,'bold'), background="black", borderwidth=5, relief="solid")
style.configure("TLabel", foreground="white", font=('Papyrus',12,'bold'), background="black")

question_list = tk.Listbox(root, width=80, height=3)
question_list.pack(pady=10)


gen_button = ttk.Button(root, text="Generate Keywords", command=generate_nouns, style="TButton")
gen_button.pack(pady=10)


noun_list = tk.Listbox(root, width=80, height=3)
noun_list.pack(pady=10)

label = ttk.Label(root, text="Enter the keywords from the above list:",  style="TLabel")
label.pack(pady=10)

noun_entry = tk.Text(root, width=50, height=2)
noun_entry.pack(pady=10)


ex_button = ttk.Button(root, text="Extract Sentences", command=extract_sentences, style="TButton")
ex_button.pack(pady=10)


sen_list = tk.Listbox(root, width=80)
sen_list.pack(pady=10)

root.mainloop()
