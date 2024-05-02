from vapi
SAMPLE_RATE = 16000
NUM_CHANNELS = 1
CHUNK_SIZE = 640


def is_playable_speaker(participant):
    is_speaker = "userName" in participant["info"] and participant["info"]["userName"] == "Vapi Speaker"
    mic = participant["media"]["microphone"]
    is_subscribed = mic["subscribed"] == "subscribed"
    is_playable = mic["state"] == "playable"
    return is_speaker and is_subscribed and is_playable


class DailyCall(daily.EventHandler):

    def on_inputs_updated(self, inputs):
        print("Inputs updated!")
        self.__app_inputs_updated = True
        self.maybe_start()

    def on_joined(self, data, error):
        print("Joined call!")
        if error:
            print(f"Unable to join call: {error}")
            self.__app_error = error
        else:
            self.__app_joined = True
            print("Joined call!")
        self.maybe_start()

    def on_participant_joined(self, participant):
        print("Participant joined!")
        self.__participants[participant["id"]] = participant

    def on_participant_left(self, participant, _):
        print("Participant left!")
        del self.__participants[participant["id"]]
        self.leave()

    def on_participant_updated(self, participant):
        print("Participant updated!")

        self.__participants[participant["id"]] = participant
        if is_playable_speaker(participant):
            self.__call_client.send_app_message("playable")

    def join(self, meeting_url):
        print(f"Joining call at {meeting_url}")
        self.__call_client.join(meeting_url, completion=self.on_joined)

    def leave(self):
        print("Leaving call!")
        self.__app_quit = True
        self.__receive_bot_audio_thread.join()
        self.__send_user_audio_thread.join()
        self.__call_client.leave()

    def maybe_start(self):
        print("Maybe starting!")
        if self.__app_error:
            self.__start_event.set()

        if self.__app_inputs_updated and self.__app_joined:
            self.__start_event.set()

    def send_user_audio(self):
        print("Sending user audio!")
        self.__start_event.wait()

        if self.__app_error:
            print(f"Unable to receive mic audio!")
            return

        while not self.__app_quit:
            buffer = self.__input_audio_stream.read(
                CHUNK_SIZE, exception_on_overflow=False)
            if len(buffer) > 0:
                try:
                    self.__mic_device.write_frames(buffer)
                except Exception as e:
                    print(e)

    def receive_bot_audio(self):
        print("Receiving bot audio!")
        self.__start_event.wait()

        if self.__app_error:
            print(f"Unable to receive bot audio!")
            return

        while not self.__app_quit:
            buffer = self.__speaker_device.read_frames(CHUNK_SIZE)

            if len(buffer) > 0:
                self.__output_audio_stream.write(buffer, CHUNK_SIZE)