from qai.agent.agents.email import EmailAgent

class QRevEmailAgent(OpenAIAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def on_email_complete(sequence_id, email: EmailModel) -> None:
        print(f"Email completed: {email}")
        mongo = cfg.db.mongo
        client = MongoClient(mongo.uri)
        db = client[mongo.db]

        collection = db[mongo.collection]
        js = {
            "sequence_id": sequence_id,
            "prospect_email": email.email,
            "prospect_name": email.name,
            "prospect_phone": email.phone,
            "message_subject": email.subject,
            "message_body": email.body,
            "is_message_generation_complete": True,
        }
        print(f"Inserting into collection: {collection.name} ")
        collection.insert_one(js)

    @staticmethod
    def on_all_emails_complete(sequence_id: str, url: str, successes: int, errors: int) -> None:
        print(f"All Email completed: {successes} success, {errors} errors.")
        print(f"Sending call to {url}  sequence_id={sequence_id}")
        requests.post(
            url, json={"sequence_id": sequence_id, "nsuccesses": successes, "nerrors": errors}
        )
