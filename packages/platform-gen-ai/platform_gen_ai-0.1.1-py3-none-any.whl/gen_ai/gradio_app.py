#!/usr/bin/env python3

import argparse
import copy
import json
import os
from dataclasses import asdict
from datetime import datetime

import customer
import gradio as gr
import llm
from dotenv import load_dotenv

from gen_ai.constants import FAVICON_PATH, LOGS_DIRECTORY, SSL_CERTFILE, SSL_KEYFILE, USERS_FILE
from gen_ai.deploy.model import Conversation, QueryState
from gen_ai.common.ioc_container import Container

# TODO: temp fix with sqlite3. Need to look into in on Monday.
# For now the goal is to make sure it can work fine
__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(os.getcwd(), "db.sqlite3"),
    }
}


# Predict function
def predict(conversation: Conversation, input_query, input_metadata, request: gr.Request):
    if not input_query:
        gr.Warning("Please enter a question.")
        return {session_conversation: conversation, prompt_box: gr.update(value="")}
    conversation.user = conversation.user or request.username
    conversation.exchanges = conversation.exchanges or []

    start_time = datetime.now()
    conversation.date_time = conversation.date_time or datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    query_state = QueryState(question=input_query, all_sections_needed=[])
    print("--" * 80)
    print(f"Query by user {request.username}: {input_query}")

    conversation.exchanges.append(query_state)

    if input_metadata:
        input_metadata = {"set_number": input_metadata.lower()}
    else:
        input_metadata = None
    llm.respond(conversation, input_metadata)

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    seconds = elapsed_time.seconds + round(elapsed_time.microseconds / 1_000_000, 1)

    query_state.time_taken = seconds
    chatbot_list = [(item.question, item.answer) for item in conversation.exchanges]

    # interim state @ each predict
    log_interim_state(conversation)
    return {
        session_conversation: conversation,
        chatbot: chatbot_list,
        response_feedback_box: gr.update(visible=True),
        good_answer_dropdown: gr.update(value=None, visible=True),
        articles_not_relevant: gr.update(visible=True, value=False),
        expected_article_id_box: gr.update(visible=True, value=""),
        submit_feedback_btn: gr.update(visible=True),
        time_taken_box: gr.update(value=f"{seconds} seconds", visible=True),
        prompt_box: gr.update(value=""),
        context_box: gr.update(
            value="\n".join(query_state.urls),
            visible=True,
        ),
    }


def log_interim_state(
    conversation,
):
    conversation_num = conversation.conversation_num
    date_time = conversation.date_time
    username = conversation.user
    exchange_num = len(conversation.exchanges)
    with open(
        f"{LOGS_DIRECTORY}/{username}__{conversation_num}__{date_time}__interim__{exchange_num}.json",
        "a",
        encoding="utf-8",
    ) as feedback_file:
        record = copy.deepcopy(conversation.exchanges[-1])
        record.date_time = date_time
        record.user = username
        record.conversation_num = conversation_num
        record.exchange_num = exchange_num
        record_json = asdict(record)

        print(f"----> > > >---- Interim state: {json.dumps(record_json, indent=4)}")
        print("\n\n\n")
        print(".." * 80)
        feedback_file.write(json.dumps(record_json, indent=4))


# Feedback function
def feedback(
    conversation,
    response_feedback_text,
    correct,
    not_relevant,
    expected_article_id,
    request: gr.Request,
):
    if not correct:
        gr.Warning("Was the answer fully accurate or not - please select radio button.")
        return {session_conversation: conversation}

    # Disable correctness check - might need in future
    # if correct != "Accurate and Complete" and response_feedback_text == "":
    #     gr.Warning("Please enter the expected answer in the Response Feedback textbox.")
    #     return {session_conversation: conversation}

    if not_relevant is True and not expected_article_id:
        gr.Warning("Please enter the document that should have been used.")
        return {session_conversation: conversation}

    conversation_num = conversation.conversation_num
    date_time = conversation.date_time
    with open(
        f"{LOGS_DIRECTORY}/{request.username}__{conversation_num}__{date_time}.json",
        "a",
        encoding="utf-8",
    ) as feedback_file:
        conversation.correct = correct
        conversation.articles_not_relevant = not_relevant
        # disabling these, need to talk with Anna and Dauren
        # if expected_article_id:
        #     conversation["expected_article_id"] = expected_article_id
        # if response_feedback_text:
        #     conversation["feedback"] = response_feedback_text
        # conversation["ip_address"] = request.client.host

        total_time_taken = 0
        for item in conversation.exchanges:
            total_time_taken += item["time_taken"]
        conversation["total_time_taken"] = total_time_taken
        print(f"----> > > >---- Completion feedback: {json.dumps(conversation, indent=4)}")

        print("\n\n\n")
        print(".." * 80)
        feedback_file.write(json.dumps(conversation, indent=4))
        gr.Info("Feedback Sent!")
    conversation.clear()
    conversation.conversation_num = conversation_num + 1
    return {
        chatbot: [("", "")],
        session_conversation: conversation,
        response_feedback_box: gr.update(visible=False, value=""),
        good_answer_dropdown: gr.update(visible=False),
        articles_not_relevant: gr.update(visible=False),
        expected_article_id_box: gr.update(visible=False),
        submit_feedback_btn: gr.update(visible=False),
        process_btn: gr.update(visible=True, variant="primary"),
        prompt_box: gr.update(visible=True, value=""),
        time_taken_box: gr.update(visible=False),
        articles_box: gr.update(visible=False),
        tags_used_box: gr.update(visible=False),
        context_box: gr.update(visible=False),
    }


def authenticate(username, password):
    # Default user and password, stored in .env file (not commited to github)
    gradio_user = os.getenv("gradio_user")
    gradio_password = os.getenv("gradio_password")
    if gradio_user is None or gradio_password is None:
        raise ValueError("You forgot to populate user and password in .env file")

    default_auth_users = {
        gradio_user: gradio_password,
    }

    auth_users = {}
    if os.path.isfile(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as users_file:
            auth_users = json.load(users_file)
    auth_users.update(default_auth_users)
    if username in auth_users:
        if auth_users[username] == password:
            print(f"----> > > >---- User {username} authenticated successfully: {datetime.now()}.")
            return True
    print(f"----X X X X---- User {username} unsuccessful authentication: {datetime.now()}.")
    return False


if __name__ == "__main__":
    load_dotenv()
    # disable for now, we will need to dive deeper why it stopped working with gradio
    # container = Container()
    # container.init_resources()
    # container.wire(packages=[ioc_container])

    parser = argparse.ArgumentParser(description="Gradio app for LLM Chatbot.")
    parser.add_argument("--use_ft", action="store_true", help="Use fine-tuned model")
    args = parser.parse_args()

    if not os.path.exists(LOGS_DIRECTORY):
        os.makedirs(LOGS_DIRECTORY)

    # Gradio interface code starts here
    with gr.Blocks(
        css="""
            footer { display: none !important; } 
            .gradio-container { min-height: 0px !important; } 
            h1 {color: #204031; }
        """,
        theme=gr.themes.Default(primary_hue=customer.THEME_HUE, secondary_hue="orange"),
    ) as gradio_app:
        gradio_app.queue()
        session_conversation = gr.State(Conversation(exchanges=[]))

        # Title of the app (goes in <head> tag of the page source)
        gradio_app.title = f"Customer Advocate Assistant"

        # App's <body> starts here
        with gr.Row(elem_id="title_row", equal_height=True):
            with gr.Column():
                gr.HTML(
                    "<div style='display: flex; align-items: center; justify-content: flex-start; width: 100%;'>"
                    + "<img src='https://www.gstatic.com/pantheon/images/welcome/supercloud.svg'"
                    + " alt='Google Cloud Logo' style='max-height:80px;'>"
                    + "</div>"
                )
            with gr.Column():
                gr.HTML(
                    f"""
                    <div style='display: flex; align-items: center; justify-content: center; width: 100%;'>
                        <h1>Customer Advocate Assistant</h1>
                    </div>
                    """
                )
            with gr.Column():
                gr.HTML(
                    f"""
                    <div style='display: flex; align-items: center; justify-content: flex-end; width: 100%;'>
                        <img src='{customer.LOGO}' 
                            alt='Logo' style='max-height:50px; transform: scale(0.7);'>
                    </div>
                    """
                )

        gr.HTML("<div><hr></div>")

        # Chatbot interface display
        gr.HTML("<div><h3>Chat History</h3></div>")
        chatbot = gr.Chatbot(elem_id="chatbot", label="Chat History", container=False, show_label=True)
        # Row of input for text box and the primary process button
        with gr.Row(variant="panel", equal_height=True):
            with gr.Column(scale=2):
                with gr.Row():
                    prompt_box = gr.Textbox(
                        label="Enter the question",
                        lines=2,
                        placeholder="Input question text here and click Send.",
                    )

                with gr.Row():
                    metadata_box = gr.Textbox(
                        label="Optional. Enter the set number. Example: ACIS001",
                        lines=1,
                        placeholder="Input set number",
                    )

            with gr.Column(scale=1):
                clear_btn = gr.Button("Clear", variant="secondary", scale=1)
                process_btn = gr.Button("Send", variant="primary", scale=1)

        with gr.Row(variant="panel", equal_height=True):
            # gradio relevant context text box
            context_box = gr.Textbox(
                label="Citations",
                lines=4,
                max_lines=30,
                placeholder="Citations for the current question",
                interactive=False,
                visible=False,
            )

        with gr.Group():
            with gr.Row(variant="default", equal_height=True):
                time_taken_box = gr.Textbox(
                    interactive=False,
                    label="Elapsed Time",
                    lines=1,
                    placeholder="",
                    visible=False,
                )
                tags_used_box = gr.Textbox(
                    interactive=False,
                    label="Country Tags Used",
                    lines=1,
                    max_lines=3,
                    placeholder="",
                    visible=False,
                )
            articles_box = gr.Textbox(
                interactive=False,
                label="Article(s) Used",
                lines=3,
                max_lines=15,
                placeholder="Article ID and Content",
                visible=False,
            )

        with gr.Group():
            good_answer_dropdown = gr.Dropdown(
                container=True,
                label="Was the answer accurate and complete? (Required)",
                choices=[
                    "5 = Completely accurate and complete (The information was correct and included all necessary details.)",
                    "4 = Very accurate and complete (The information was correct and included most, if not all, relevant details.)",
                    "3 = Mostly accurate and complete (The information was mostly correct but might have missed some minor details.)",
                    "2 = Somewhat inaccurate or incomplete (The information had some errors or lacked some important details.)",
                    "1 = Not at all accurate or complete (The information was mostly wrong or missing important details.)",
                ],
                visible=False,
            )
            with gr.Row():
                articles_not_relevant = gr.Checkbox(
                    label="Document(s) are Not Relevant",
                    value=False,
                    info="Check the box if the Document(s) are not relevant to the conversation",
                    visible=False,
                )
                expected_article_id_box = gr.Textbox(
                    label="Expected Document",
                    lines=1,
                    placeholder="Add relevant document here",
                    visible=False,
                )
            response_feedback_box = gr.Textbox(
                label="Response Feedback",
                lines=5,
                placeholder="If the response was not fully accurate, add the correct response here",
                visible=False,
            )
            submit_feedback_btn = gr.Button("Send Response Feedback", variant="primary", visible=False)

        # Event handlers.
        clear_btn.click(lambda: "", inputs=[], outputs=[prompt_box])
        process_btn.click(
            fn=predict,
            inputs=[session_conversation, prompt_box, metadata_box],
            outputs=[
                session_conversation,
                chatbot,
                response_feedback_box,
                good_answer_dropdown,
                articles_not_relevant,
                expected_article_id_box,
                submit_feedback_btn,
                time_taken_box,
                prompt_box,
                context_box,
            ],
        )
        submit_feedback_btn.click(
            fn=feedback,
            inputs=[
                session_conversation,
                response_feedback_box,
                good_answer_dropdown,
                articles_not_relevant,
                expected_article_id_box,
            ],
            outputs=[
                session_conversation,
                chatbot,
                response_feedback_box,
                good_answer_dropdown,
                articles_not_relevant,
                expected_article_id_box,
                submit_feedback_btn,
                process_btn,
                prompt_box,
                time_taken_box,
                articles_box,
                tags_used_box,
                context_box,
            ],
        )

        # Examples for the chatbot
        gr.Examples(
            [
                ["I injured my back. Is massage therapy covered?"],
                ["I am traveling to Europe on vacation. Do I have coverage if I need to seek medical treatment?"],
                ["Is acupuncture a covered service?"],
                ["Do I have a copay for a routine colonoscopy?"],
                ["Can my partner be covered under my plan?"],
                ["Now that I've lost my employment, will my dependents be covered under COBRA?"],
                ["What is the effective date of my current coverage?"],
            ],
            inputs=prompt_box,
            outputs=chatbot,
        )

        use_ssl = os.environ.get("PORT") and (int(os.environ.get("PORT")) == 443 or int(os.environ.get("PORT")) == 7861)
        ssl_keyfile = SSL_KEYFILE if use_ssl else None
        ssl_certfile = SSL_CERTFILE if use_ssl else None
        FAVICON_PATH_USED = FAVICON_PATH if os.path.isfile(FAVICON_PATH) else None
        server_name = "0.0.0.0"  # if use_ssl else "127.0.0.1"

        print("Starting UI server...")
        gr.close_all()
        gradio_app.launch(
            debug=Container.config.get("is_debug", False),
            show_error=True,
            max_threads=2,
            favicon_path=FAVICON_PATH_USED,
            show_api=False,
            root_path=Container.config.get("gradio_root_path", None),
            server_name=server_name,
            server_port=int(os.environ.get("PORT", 7860)),
            auth=authenticate,
            ssl_verify=False,
            ssl_keyfile=ssl_keyfile,
            ssl_certfile=ssl_certfile,
            share=False,
        )
