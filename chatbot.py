# importing the chatterbot and flask libraries
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from flask import Flask, render_template, request

app = Flask(__name__)
try:

    my_chatbot = ChatBot('Tom',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///db_file.sqlite3',
        logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'sorry, Iam donot understand what you are saying',
            'maximum_similarity_threshold': 0.90
        }
    ]
)
except:
    print("compiled sucessfully")

    training_data_for_mybot = open('training_data_for_mychatbot/Ques and Anes.txt').read().splitlines()

    trainer = ListTrainer(my_chatbot)
    trainer.train(training_data_for_mybot)

    trainer = ChatterBotCorpusTrainer(my_chatbot)
    trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_request = request.args.get('msg')
    return str(my_chatbot.get_response(user_request))

if __name__ == "__main__":
    app.run(debug = True)
