"""
This module contains functionalities to manage and execute language model (LLM) interactions,
document retrieval, response generation, and logging within a conversational AI context. It integrates
several components for handling complex AI tasks, including generating contextual responses,
managing state across conversational turns, and logging interactions for analysis.

The module is structured to process conversations using document retrievers, respond to user queries,
and log conversation states and interactions to BigQuery for further analysis. It uses dependency injection
to manage dependencies and settings, facilitating a flexible and decoupled design.

Functions:
    generate_contexts_from_docs(docs_and_scores, query_state): Generates text contexts from document data.
    get_total_count(question, selected_context, previous_rounds, final_round_statement): Calculates the total 
    token count.
    generate_response_react(conversation): Handles the generation of responses in a reactive conversation cycle.
    respond(conversation, member_info): Processes a full conversational round, updating the conversation state.
    respond_api(question, member_context_full): Provides an API-like interface to handle incoming queries and 
    generate responses.

Classes:
    None

Dependencies:
    - gen_ai.common: Provides common utilities and configurations.
    - langchain: Used for language model operations.
    - json5: Used for JSON parsing.
"""

from timeit import default_timer
from typing import Any
import uuid

import json5
from dependency_injector.wiring import inject
from langchain.chains import LLMChain
from langchain.schema import Document

from gen_ai.common.argo_logger import create_log_snapshot, trace_on
from gen_ai.common.bq_utils import BigQueryConverter, create_bq_client, load_data_to_bq, get_dataset_id, log_question
from gen_ai.common.common import TokenCounter, merge_outputs, remove_duplicates, split_large_document, update_used_docs
from gen_ai.common.ioc_container import Container
from gen_ai.common.memorystore_utils import serialize_previous_conversation
from gen_ai.common.react_utils import get_confidence_score
from gen_ai.common.retriever import perform_retrieve_round, retrieve_initial_documents
from gen_ai.common.statefullness import resolve_and_enrich, serialize_response
from gen_ai.constants import MAX_CONTEXT_SIZE
from gen_ai.create_tables import schema_prediction
from gen_ai.deploy.model import Conversation, PersonalizedData, QueryState, transform_to_dictionary


@inject
@trace_on("Generating context from documents", measure_time=True)
def generate_contexts_from_docs(docs_and_scores: list[Document], query_state: QueryState) -> list[str]:
    """
    Generates textual contexts from a list of documents, preparing them for input to a language model.

    This function processes each document to extract content up to a specified token limit, organizing this content
    into manageable sections that fit within the maximum context size for a language model. It handles large documents
    by splitting them into chunks and maintains a count of used tokens and documents to optimize the subsequent
    language model processing.

    Args:
        docs_and_scores (list[Document]): A list of Document objects, each containing metadata and content
            to be used in generating context. These documents are assumed to be scored and potentially filtered
            by relevance to the query.
        query_state (QueryState): The current state of the query, including details like previously used tokens
            and documents. This state is updated during the function execution to include details about the
            documents and tokens used in this invocation.

    Returns:
        list[str]: A list of strings, where each string represents a textual context segment formed from the
            document content. Each segment is designed to be within the token limits suitable for processing
            by a language model.

    Raises:
        ValueError: If any document does not contain the necessary content or metadata for processing.

    Examples:
        >>> docs = [Document(page_content="Content of the document.",
        metadata={"section_name": "Section 1", "summary": "Summary of the document.", "relevancy_score": 0.95})]
        >>> query_state = QueryState(question="What is the purpose of the document?",
        answer="To provide information.", additional_information_to_retrieve="")
        >>> contexts = generate_contexts_from_docs(docs, query_state)
        >>> print(contexts[0])
        "Content of the document."

    Note:
        The function modifies the `query_state` object in-place, updating it with details about the tokens and
        documents used during the context generation process. Ensure that the `query_state` object is appropriately
        handled to preserve the integrity of the conversation state.
    """
    num_docs_used = [0]
    contexts = ["\n"]
    token_counts = [0]
    used_articles = []
    token_counter: TokenCounter = Container.token_counter()

    for doc in docs_and_scores:
        filename = doc.metadata["section_name"]

        doc_content = doc.page_content if Container.config.get("use_full_documents", False) else doc.metadata["summary"]
        doc_tokens = token_counter.get_num_tokens_from_string(doc_content)
        if doc_tokens > MAX_CONTEXT_SIZE:
            doc_chunks = split_large_document(doc_content, MAX_CONTEXT_SIZE)
        else:
            doc_chunks = [(doc_content, doc_tokens)]

        for doc_chunk, doc_tokens in doc_chunks:

            if token_counts[-1] + doc_tokens >= MAX_CONTEXT_SIZE:
                token_counts.append(0)
                contexts.append("\n")
                num_docs_used.append(0)

            used_articles.append((f"{filename} Context: {len(contexts)}", doc.metadata["relevancy_score"]))
            token_counts[-1] += doc_tokens
            contexts[-1] += doc_chunk
            contexts[-1] += "\n" + "-" * 12 + "\n"
            num_docs_used[-1] += 1

    contexts[-1] += "\n"

    query_state.input_tokens = token_counts
    query_state.num_docs_used = num_docs_used
    query_state.used_articles_with_scores = update_used_docs(used_articles, query_state)

    Container.logger().info(msg=f"Docs used: {num_docs_used}, tokens used: {token_counts}")
    Container.logger().info(msg=f"Doc names with relevancy scores: {query_state.used_articles_with_scores}")

    doc_attributes = [
        (x.metadata["original_filepath"], x.metadata["doc_identifier"], x.metadata["section_name"])
        for x in docs_and_scores
    ]
    Container.logger().info(msg=f"Doc attributes: {doc_attributes}")
    return contexts


def get_total_count(question: str, selected_context: str, previous_rounds: str, final_round_statement: str) -> str:
    """
    Calculates the total token count for a given context setup in a conversational AI environment.

    This function constructs a full prompt from various components of a conversation including the main question,
    selected context from documents, any preceding rounds of conversation, and a final statement if it is the last
    round. It then calculates the total number of tokens this combined prompt would take up when processed by a
    language model, assisting in managing and optimizing language model input size constraints.

    Args:
        question (str): The primary question being addressed in the conversation.
        selected_context (str): The context selected from documents relevant to the question.
        previous_rounds (str): Accumulated context from previous rounds of the conversation, maintaining the
                               continuity necessary for the language model.
        final_round_statement (str): A concluding statement used in the final round of the conversation, often
                                     summarizing or closing the discussion.

    Returns:
        str: The total token count as a string, representing the sum of tokens from all parts of the constructed prompt.

    Example:
        >>> question = "What are the benefits of renewable energy?"
        >>> selected_context = "Renewable energy, often referred to as clean energy, comes from natural sources..."
        >>> previous_rounds = "Previous discussions included solar and wind energy."
        >>> final_round_statement = "This concludes our discussion on renewable energy."
        >>> token_count = get_total_count(question, selected_context, previous_rounds, final_round_statement)
        >>> print(token_count)
        '120'  # Example output, the actual number depends on the tokenization process.

    Note:
        The token count helps in managing inputs to language models, especially when dealing with models that have
        a maximum token input limit. Ensuring that the prompt does not exceed this limit is crucial for
        effective processing.
    """
    react_chain: LLMChain = Container.react_chain
    prompt = (
        f"{react_chain().prompt.template}\n{question}\n{selected_context}\n{previous_rounds}\n{final_round_statement}\n"
    )
    query_tokens = Container.token_counter().get_num_tokens_from_string(prompt)
    return query_tokens


@inject
def generate_response_react(conversation: Conversation) -> tuple[Conversation, list[dict[str, Any]]]:
    """
    Generates responses within a conversational cycle, considering various conversation states and document contexts.

    This function orchestrates the response generation process by managing document retrieval,
    context generation, and reaction to queries based on the ongoing conversation state. It processes
    the conversation through various stages, utilizing LLM chains and custom utilities to refine the
    conversation context and generate appropriate responses.

    Args:
        conversation (Conversation): The current conversation object containing all exchanges and context.

    Returns:
        tuple[Conversation, list[dict[str, Any]]]: Updated conversation object with the new exchange added,
        and a list of log snapshots detailing each step of the conversation processing.

    Raises:
        Exception: If there is any issue in the processing steps, including document retrieval,
        context generation, or response handling.
    """
    json_corrector_chain: LLMChain = Container.json_corrector_chain
    react_chain: LLMChain = Container.react_chain
    vector_indices: dict = Container.vector_indices
    config: dict = Container.config

    document_retriever_name = config.get("document_retriever")
    member_info = conversation.member_info

    query_state = conversation.exchanges[-1]
    question = query_state.question
    log_question(question)

    query_state.react_rounds = []
    log_snapshots = []
    round_number = len(query_state.react_rounds) + 1
    if len(conversation.exchanges) > 1 and config.get("api_mode") == "stateful":
        previous_context = serialize_previous_conversation(conversation.exchanges[-2])
    else:
        previous_context = ""

    pre_filtered_docs, post_filtered_docs = retrieve_initial_documents(
        round_number, question, vector_indices, document_retriever_name, member_info
    )
    contexts = generate_contexts_from_docs(post_filtered_docs, query_state)

    final_round_statement = ""
    max_rounds = config.get("max_rounds", 3)
    previous_rounds = config.get("first_round_statement", "")

    while len(query_state.react_rounds) < max_rounds:
        start_time = default_timer()
        if query_state.additional_information_to_retrieve:
            pre_filtered_missing_information_documents, post_filtered_missing_information_documents = (
                perform_retrieve_round(
                    round_number,
                    [query_state.additional_information_to_retrieve],
                    vector_indices,
                    document_retriever_name,
                    member_info,
                )
            )
            if post_filtered_missing_information_documents:
                post_filtered_docs = post_filtered_missing_information_documents + post_filtered_docs

            if pre_filtered_missing_information_documents:
                pre_filtered_docs = pre_filtered_missing_information_documents + pre_filtered_docs

            post_filtered_docs = remove_duplicates(post_filtered_docs)
            contexts = generate_contexts_from_docs(post_filtered_docs, query_state)

        round_number = len(query_state.react_rounds) + 1
        if round_number == max_rounds:
            final_round_statement = config.get("final_round_statement", "")

        round_outputs = []
        for selected_context in contexts:
            llm_start_time = default_timer()
            output_raw = react_chain().run(
                include_run_info=True,
                return_only_outputs=False,
                question=question,
                context=previous_context + selected_context,
                previous_rounds=previous_rounds,
                round_number=round_number,
                final_round_statement=final_round_statement,
            )
            llm_end_time = default_timer()
            Container.logger().info(f"Generating main LLM answer took {llm_end_time - llm_start_time} seconds")
            attempts = 2
            done = False
            while not done:
                try:
                    if attempts <= 0:
                        break
                    output_raw = output_raw.replace("```json", "").replace("```", "")
                    output = json5.loads(output_raw)
                    done = True
                except Exception as e:  # pylint: disable=W0718
                    Container.logger().info(msg=f"Crashed before correct chain, attempts: {attempts}")
                    Container.logger().info(msg=str(e))
                    json_output = json_corrector_chain().run(json=output_raw)
                    json_output = json_output.replace("```json", "").replace("```", "")
                    try:
                        output = json5.loads(json_output)
                        done = True
                    except Exception as e2:  # pylint: disable=W0718
                        Container.logger().info(msg=f"Crashed before correct chain, attempts: {attempts}")
                        Container.logger().info(msg=str(e2))
                        done = False
                        attempts -= 1
            if (
                "answer" not in output
                or "context_used" not in output
                or (len(post_filtered_docs) == 0 and not output.get("additional_information_to_retrieve", None))
            ):
                output["answer"] = "I was not able to answer this question"
                output["plan_and_summaries"] = ""
                output["context_used"] = ""
                confidence = get_confidence_score(question, output["answer"])
                round_outputs.append((output, confidence))
                break

            confidence = get_confidence_score(question, output["answer"])

            round_outputs.append((output, confidence))

        end_time = default_timer()
        query_state.time_taken = end_time - start_time
        output, confidence, index = merge_outputs(round_outputs)
        selected_context = contexts[index]

        react_snapshot = {
            "round_number": round_number,
            "plan_and_summaries": output["plan_and_summaries"],
            "answer": output["answer"],
            "confidence_score": confidence,
            "context_used": output["context_used"],
        }
        query_state.react_rounds.append(react_snapshot)
        previous_rounds = json5.dumps(query_state.react_rounds, indent=4)

        query_state.additional_information_to_retrieve = output.get("additional_information_to_retrieve", None)

        log_snapshot = create_log_snapshot(
            react_snapshot,
            pre_filtered_docs,
            post_filtered_docs,
            query_state.additional_information_to_retrieve,
            query_state.time_taken,
        )
        log_snapshots.append(log_snapshot)
        Container.logger().info(msg="-----------------------------------")
        Container.logger().info(msg="Additional information to retrieve:")
        Container.logger().info(msg=query_state.additional_information_to_retrieve)
        Container.logger().info(msg="-----------------------------------")
        Container.logger().info(msg="Confidence:")
        Container.logger().info(msg=confidence)
        Container.logger().info(msg="------------------------")
        Container.logger().info(msg=react_snapshot)
        if not query_state.additional_information_to_retrieve:
            break

        if confidence >= 5:
            break

    # if confidence != 5:
    #     max_confidence_score = max([x["confidence_score"] for x in log_snapshots])
    #     most_confident_round = [x for x in log_snapshots if x['confidence_score'] == max_confidence_score][0]
    #     most_conf_ix = log_snapshots.index(most_confident_round)
    #     actual_ix = log_snapshots.index(react_snapshot)
    #     log_snapshots[most_conf_ix], log_snapshots[actual_ix] = log_snapshots[actual_ix], log_snapshots[most_conf_ix]
    #     output['answer'] = most_confident_round['answer']
    #     output['confidence_score'] = most_confident_round['confidence_score']
    #     output['context_used'] = most_confident_round['context_used']

    conversation.round_numder = round_number
    query_state.answer = output["answer"]
    query_state.relevant_context = output["context_used"]
    query_state.all_sections_needed = [x[0] for x in query_state.used_articles_with_scores]
    query_state.used_articles_with_scores = None
    query_state.confidence_score = confidence
    query_state = fill_query_state_with_doc_attributes(query_state, post_filtered_docs)

    return conversation, log_snapshots


def fill_query_state_with_doc_attributes(query_state: QueryState, post_filtered_docs: list[Document]) -> QueryState:
    """
    Updates the provided query_state object with attributes extracted from documents after filtering.

    This function modifies the query_state object by setting various attributes based on the metadata of documents 
    in the post_filtered_docs list. It processes documents to categorize them by their data source 
    (B360, KM or MP from KC), and updates the query_state with URLs, and categorized attributes for each type.

    Args:
        query_state (QueryState): The query state object that needs to be updated with document attributes.
        post_filtered_docs (list[Document]): A list of Document objects that have been filtered and whose attributes 
        are to be extracted.

    Returns:
        QueryState: The updated query state object with new attributes set based on the provided documents.

    Side effects:
        Modifies the query_state object by setting the following attributes:
        - urls: A set of unique URLs extracted from the document metadata.
        - attributes_to_b360: A list of dictionaries with attributes from B360 documents.
        - attributes_to_kc_km: A list of dictionaries with attributes from KC KM documents.
        - attributes_to_kc_mp: A list of dictionaries with attributes from KC MP documents.

    """
    query_state.urls = list(set(document.metadata["url"] for document in post_filtered_docs))

    # B360 documents
    b360_docs = [x for x in post_filtered_docs if x.metadata["data_source"] == "b360"]
    attributes_to_b360 = [
        {"set_number": x.metadata["set_number"], "section_name": x.metadata["section_name"]} for x in b360_docs
    ]

    # KC documents, they can be of two types: from KM (dont have policy number) and from MP (have policy number)
    kc_docs = [x for x in post_filtered_docs if x.metadata["data_source"] == "kc"]
    kc_km_docs = [x for x in kc_docs if not x.metadata["policy_number"]]
    kc_mp_docs = [x for x in kc_docs if x.metadata["policy_number"]]

    attributes_to_kc_km = [
        {
            "doc_type": "km",
            "doc_identifier": x.metadata["doc_identifier"],
            "url": x.metadata["url"],
            "section_name": x.metadata["section_name"],
        }
        for x in kc_km_docs
    ]
    attributes_to_kc_mp = [
        {
            "doc_type": "mp",
            "original_filepath": x.metadata["original_filepath"],
            "policy_number": x.metadata["policy_number"],
            "section_name": x.metadata["section_name"],
        }
        for x in kc_mp_docs
    ]

    query_state.attributes_to_b360 = attributes_to_b360
    query_state.attributes_to_kc_km = attributes_to_kc_km
    query_state.attributes_to_kc_mp = attributes_to_kc_mp
    return query_state


def respond(conversation: Conversation, member_info: dict) -> Conversation:
    """
    Processes and responds to the latest exchange in a conversation, applying stateful or stateless logic as configured.

    This function updates the conversation based on the latest interaction, employing the configured
    API mode to determine how contextually or independently each message should be handled. It integrates
    various components to enrich the conversation with AI-generated content and logs the results.

    Args:
        conversation (Conversation): The ongoing conversation object to be updated.
        member_info (dict): Additional metadata about the conversation member, used for personalizing responses.

    Returns:
        Conversation: The updated conversation object after processing the latest interaction.

    Raises:
        Exception: If issues arise in conversation processing or during response generation.
    """
    conversation.member_info = member_info

    api_mode = Container.config.get("api_mode", "stateless")
    statefullness_enabled = api_mode == "stateful"
    if statefullness_enabled:
        conversation = resolve_and_enrich(conversation)

    conversation, log_snapshots = generate_response_react(conversation)

    if statefullness_enabled:
        serialize_response(conversation)

    session_id = Container.session_id if hasattr(Container, "session_id") else str(uuid.uuid4())
    df = BigQueryConverter.convert_query_state_to_prediction(conversation.exchanges[-1], log_snapshots, session_id)
    client = create_bq_client()
    dataset_id = get_dataset_id()
    table_id = f"{dataset_id}.prediction"
    load_data_to_bq(client, table_id, schema_prediction, df)

    conversation.session_id = session_id
    return conversation


def respond_api(question: str, member_context_full: PersonalizedData | dict[str, str]) -> Conversation:
    """
    Provides an API-like interface to handle and respond to a new question within a conversation context.

    This function initializes a conversation state for a new question, applies the conversational
    logic through `respond`, and returns the updated conversation object. It's designed to be an
    entry point for external systems to interact with the conversational AI logic.

    Args:
        question (str): The question to be processed.
        member_context_full (PersonalizedData): Contextual data about the member, enhancing personalization.

    Returns:
        Conversation: A conversation object containing the initial query and the generated response.

    Raises:
        Exception: If the conversation processing fails at any step.
    """
    if isinstance(member_context_full, PersonalizedData):
        member_context_full = transform_to_dictionary(member_context_full)
    query_state = QueryState(question=question, all_sections_needed=[])
    conversation = Conversation(exchanges=[query_state])
    conversation = respond(conversation, member_context_full)
    return conversation
