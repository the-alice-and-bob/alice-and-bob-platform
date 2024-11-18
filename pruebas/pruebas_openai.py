import uuid
from pathlib import Path

from openai import OpenAI
from openai.types.beta.threads.message import Attachment, AttachmentTool

OPENAI_API_KEY = "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"


def main():
    # El contenido de la página web en fragmentos. La variable "plain_text" es el contenido completo en texto plano.
    # Generamos los fragmentos dividiendo el contenido en oraciones. con el tamaño máximo posible de los máximos tokens.
    fragments = []
    model = "gpt-4o-2024-08-06"
    raw_site_content = open("./content.txt").read()

    # Genero un fichero temporal con el contenido de la página web
    upload_filename = Path(f"{uuid.uuid4().hex}.txt")

    with open(upload_filename, "w") as f:
        f.write(raw_site_content)

    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        # Subo el fichero a OpenAI
        my_file = client.files.create(
            file=upload_filename,
            purpose="assistants"
        )

        # assistant_id = "asst_Voir8tIzJIQWSHbsNShHSCB8"
        assistant_id_file_search = "asst_h4x7EASeXfWtjycgPVr98TuE"

        # completion = client.chat.completions.create(
        #     model=model,
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": "Genera un resumen de este fichero para publicarlo en LinkedIn y Twitter. Sino puedes acceder al fichero, solo dime: NO PUEDO",
        #             # Attach the new file to the message.
        #             "attachments": [
        #                 {"file_id": my_file.id, "tools": [{"type": "assistants"}]}
        #             ]
        #         }
        #     ]
        # )
        #
        # print("completion: ", completion.choices[0].message.content)
        # return

        # my_thread = client.beta.threads.create()
        my_thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "Genera un resumen de este fichero para publicarlo en LinkedIn y Twitter. De 200 - 300 palabras. Yo solo resumeno, así que habla en tercera persona.",
                    # Attach the new file to the message.
                    "attachments": [
                        {"file_id": my_file.id, "tools": [{"type": "file_search"}]}
                    ],
                }
            ]
        )

        # my_thread_message = client.beta.threads.messages.create(
        #     thread_id=my_thread.id,
        #     role="user",
        #     content="Genera un resumen de este fichero para publicarlo en LinkedIn y Twitter.",
        #     attachments=[
        #         Attachment(
        #             file_id=my_file.id,
        #             tools=[AttachmentTool(type="assistants")]
        #         )
        #     ]
        # )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=my_thread.id,
            assistant_id=assistant_id_file_search,
            instructions="Por favor genera un resumen de este fichero para publicarlo en LinkedIn y Twitter.",
        )

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=my_thread.id)

            print("messages: ")
            for message in messages:
                assert message.content[0].type == "text"
                print({"role": message.role, "message": message.content[0].text.value})

    finally:
        # client.files.delete(file_id=my_file.id)
        upload_filename.unlink()

if __name__ == '__main__':
    main()
