# Project 10 build a chatbot

## Overview
This project purpose is to build and end-to-end machine learning product that help a user book a flight. It integrates Azure Cognitive Servies [LUIS](https://www.luis.ai) for Natural Language Processsing, Azure Web App for deployemnt, [Azure Application insights](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview) for performance monitoring and [Microsoft Bot Framework](https://dev.botframework.com) for developement.

## Main feature of the chatbot
* Welcome card
* Detect intention and request features in user request
* Ask for missing information
* Prompt for confirmation
* Booking card simulating flight result
* Data validation :
      - [Text recognizer](https://github.com/microsoft/Recognizers-Text/tree/master/Python) from microsoft 
      - check for date coherency
      - detect currency
* Prompt multi-choice if user intent is not detected

## Frame Dataset
**Presentation** : The dialogues in Frames were collected in a Wizard-of-Oz fashion. Two humans talked to each other via a chat interface. One was playing the role of the user and the other one was playing the role of the conversational agent. We call the latter a wizard as a reference to the Wizard of Oz, the man behind the curtain. The wizards had access to a database of 250+ packages, each composed of a hotel and round-trip flights. We gave users a few constraints for each dialogue and we asked them to find the best deal. This resulted in complex dialogues where a user would often consider different options, compare packages, and progressively build the description of her ideal trip.

[Download dataset](https://www.microsoft.com/en-us/research/project/frames-dataset/)

[Notebook](https://github.com/Falco-ops/OPCR_Booking_bot/blob/master/Notebook/proj10_data_analyse.ipynb)

## Dependencies
Create virtual envrionment and instal dependencies
'''console
#create env
#python3 -m venv bot_env

#install dependencies
pip install -r requirements.txt
'''




## Documentation

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Azure Bot Service Introduction](https://docs.microsoft.com/azure/bot-service/bot-service-overview-introduction?view=azure-bot-service-4.0)
- [Azure Bot Service Documentation](https://docs.microsoft.com/azure/bot-service/?view=azure-bot-service-4.0)
- [Azure Portal](https://portal.azure.com)
- [Language Understanding using LUIS](https://docs.microsoft.com/en-us/azure/cognitive-services/luis/)
- [Channels and Bot Connector Service](https://docs.microsoft.com/en-us/azure/bot-service/bot-concepts?view=azure-bot-service-4.0)
- [Azure App Insight documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
- [Deploy the bot to Azure](https://aka.ms/azuredeployment)


