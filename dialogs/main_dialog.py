# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, ChoicePrompt
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, TurnContext
from botbuilder.schema import InputHints, Attachment
import json
from booking_details import BookingDetails
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from .booking_dialog import BookingDialog


class MainDialog(ComponentDialog):
    def __init__(
        self, luis_recognizer: FlightBookingRecognizer, booking_dialog: BookingDialog
    ):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self._luis_recognizer = luis_recognizer
        self._booking_dialog_id = booking_dialog.id

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(booking_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        #if luis is not configured we let the user choose from option prompt
        if not self._luis_recognizer.is_configured:
            #await step_context.context.send_activity(
             #   MessageFactory.text(
             #       "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
             #       "'LuisAPIHostName' to the appsettings.json file.",
              #      input_hint=InputHints.ignoring_input,
             #   )
            #)
            return await step_context.prompt(
                ChoicePrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Hello there ! I would be glad to help you today. What do you have in mind ?"),
                    choices=[Choice("Book a flight"), Choice("Change a flight"), Choice("Get weather")],
                ),
            )

            #return await step_context.next(None)

        message_text = (
            str(step_context.options)
            if step_context.options
            else "Hello there. Let me help you with your next travel plan! Where do you want to go?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        if step_context.result.value == 'Book a flight':
        #if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the BookingDialog path with an empty BookingDetailsInstance.
            return await step_context.begin_dialog(
                self._booking_dialog_id, BookingDetails()
            )
        
        elif step_context.result.value == 'Change a flight':
            get_weather_text = "TODO: change flight flow here"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_weather_message)
            return await step_context.next(None)

        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        if intent == Intent.BOOK_FLIGHT.value and luis_result:
            # Show a warning for Origin and Destination if we can't resolve them.
            await MainDialog._show_warning_for_unsupported_cities(
                step_context.context, luis_result
            )

            # Run the BookingDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._booking_dialog_id, luis_result)

        if intent == Intent.GET_WEATHER.value or step_context.result.value == 'Get weather':
            get_weather_text = "TODO: get weather flow here"
            get_weather_message = MessageFactory.text(
                get_weather_text, get_weather_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(get_weather_message)
        
        

        else:
            didnt_understand_text = (
                "Sorry, I didn't get that. Please try asking in a different way"
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the child dialog ("BookingDialog") was cancelled or the user failed to confirm,
        # the Result here will be null.
        if step_context.result is not None:
            result = step_context.result

            # Now we have all the booking details call the booking service.

            # If the call to the booking service was successful tell the user.
            # time_property = Timex(result.travel_date)
            # travel_date_msg = time_property.to_natural_language(datetime.now())
            msg_txt = "Glad I could help. Enjoy your trip."
            message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            await step_context.context.send_activity(message)

            card = self.create_adaptive_card_attachment(result)
            response = MessageFactory.attachment(card)
            await step_context.context.send_activity(response)

        prompt_message = "What else can I do for you?"
        return await step_context.replace_dialog(self.id, prompt_message)
    
    #booking card builder
    def create_adaptive_card_attachment(self, result):
        """Create an adaptive card."""
        
        path =  "cards/booking_Card.json"
        with open(path) as card_file:
            card = json.load(card_file)
        
        origin = result.origin
        destination = result.destination
        departure_date = result.departure_date
        return_date = result.return_date
        budget = result.budget
        curr = result.currency

        card['body'][2]['text'] = departure_date
        card['body'][3]["columns"][0]['items'][0]['text'] = origin
        card['body'][3]["columns"][2]['items'][0]['text'] = destination
        card['body'][5]['text'] = return_date
        card['body'][6]["columns"][0]['items'][0]['text'] = destination
        card['body'][6]["columns"][2]['items'][0]['text'] = origin
        card['body'][7]["columns"][1]['items'][0]['text'] = f"{budget} {curr}"

        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card)

    @staticmethod
    async def _show_warning_for_unsupported_cities(
        context: TurnContext, luis_result: BookingDetails
    ) -> None:
        if luis_result.unsupported_airports:
            message_text = (
                f"Sorry but the following airports are not supported:"
                f" {', '.join(luis_result.unsupported_airports)}"
            )
            message = MessageFactory.text(
                message_text, message_text, InputHints.ignoring_input
            )
            await context.send_activity(message)
