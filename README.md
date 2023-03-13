# rasa_toolkit
Python script to update your rasa model without retraining.

##  Issue solved by this project
When you have trained a model and you made changes to a response text in of your domain file, the model needs to be retrained. 
For a model that takes too much time in the training process, this can be time-consuming.
- https://forum.rasa.com/t/do-you-always-have-to-run-rasa-train-when-making-changes-to-domain-yml-for-response-text/36225

## Usage
Ssimply download the main.py file and place it inside your Rasa project directory.
Then, run the script using the command:
```bash
python main.py
```
