# rasa_toolkit
Python script to update your rasa model without retranning.

##  Issue solved by this project
When you have trained a model and you made changes to a response text in of your domain file, the model needs to be retrained. 
For a model that takes too much time in the training process, this can be time-consuming.
- https://forum.rasa.com/t/do-you-always-have-to-run-rasa-train-when-making-changes-to-domain-yml-for-response-text/36225

## Usage
Put the `main.py` file inside your rasa project.
```bash
python main.py
```
