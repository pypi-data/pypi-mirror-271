from vapi_python.daily_call import DailyCall

class QaiCall(DailyCall):
    def on_inputs_updated(self, inputs):
        print("Inputs updated!")
        return super().on_inputs_updated(inputs)

    def on_joined(self, data, error):
        print("Joined call!")
        return super().on_joined(data, error)

    def on_participant_joined(self, participant):
        print(f"Participant joined!, {participant}")
        return super().on_participant_joined(participant)

    def on_participant_left(self, participant, _):
        print(f"Participant left!, {participant}")
        return super().on_participant_left(participant, _)
    
    def on_participant_updated(self, participant):
        print(f"Participant updated!, {participant}")
        return super().on_participant_updated(participant)
    
    def join(self, meeting_url):
        print(f"Joining call at {meeting_url}")
        return super().join(meeting_url)
    
    def leave(self):
        print("Leaving call!")
        return super().leave()
    
    def maybe_start(self):
        print("Maybe starting!")
        return super().maybe_start()
    
    def send_user_audio(self):
        print("Sending user audio!")
        return super().send_user_audio()
    
    def receive_bot_audio(self):
        print("Receiving bot audio!")
        return super().receive_bot_audio()
    

