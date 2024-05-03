import os

import click.testing
import paperqa
import pytest
import requests

from pqapi import (
    AnswerResponse,
    QueryRequest,
    UploadMetadata,
    agent_query,
    async_agent_query,
    async_query,
    async_send_feedback,
    check_dois,
    delete_bibliography,
    get_bibliography,
    get_prompts,
    upload_file,
    upload_paper,
)


def test_get_prompts() -> None:
    prompts, agent_prompts = get_prompts()
    some_prompt = prompts["default"]
    assert isinstance(some_prompt, paperqa.PromptCollection)
    assert agent_prompts.timeout > 0
    assert len(agent_prompts.agent_search_tool) > 25


def test_bad_bibliography():
    with pytest.raises(requests.exceptions.HTTPError):
        get_bibliography("bad-bibliography")


def test_query_str():
    response = agent_query("How are bispecific antibodies engineered?", "default")
    assert isinstance(response, AnswerResponse)


def test_query_model():
    response = agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"),
        "default",
    )
    assert isinstance(response, AnswerResponse)


def test_query_obj():
    prompt_collection = paperqa.PromptCollection()
    prompt_collection.post = (
        "This answer below was generated for {cost}. "
        "Provide a critique of this answer that could be used to improve it.\n\n"
        "{question}\n\n{answer}"
    )
    request = QueryRequest(
        query="How are bispecific antibodies engineered?",
        prompts=prompt_collection,
        max_sources=2,
        consider_sources=5,
    )
    agent_query(request)


def test_upload_file() -> None:
    script_dir = os.path.dirname(__file__)
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    response = upload_file(
        "default",
        file,
        UploadMetadata(filename="paper.pdf", citation="Test Citation"),
    )
    assert response["success"], f"Expected success in response {response}."


def test_upload_public() -> None:
    # create a public bibliography
    script_dir = os.path.dirname(__file__)
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    response = upload_file(
        "api-test-public",
        file,
        UploadMetadata(filename="paper.pdf", citation="Test Citation"),
        public=True,
    )
    assert response["success"], f"Expected success in response {response}."

    # get status of public bibliography
    status = get_bibliography("api-test-public", public=True)

    assert status.writeable
    assert status.doc_count == 1

    # delete public bibliography
    delete_bibliography("api-test-public", public=True)


# now test async
@pytest.mark.asyncio()
async def test_async_query_str():
    response = await async_agent_query(
        "How are bispecific antibodies engineered?", "default"
    )
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio()
async def test_async_query_model():
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"), "default"
    )
    assert isinstance(response, AnswerResponse)


@pytest.mark.asyncio()
async def test_feedback_model() -> None:
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"), "default"
    )
    assert isinstance(response, AnswerResponse)
    feedback = {"test_feedback": "great!"}
    assert await async_send_feedback([response.answer.id], [feedback], "default")


@pytest.mark.asyncio()
async def test_async_tmp():
    response = await async_agent_query(
        QueryRequest(query="How are bispecific antibodies engineered?"),
    )
    assert isinstance(response, AnswerResponse)


def test_upload_paper() -> None:
    script_dir = os.path.dirname(__file__)
    file = open(os.path.join(script_dir, "paper.pdf"), "rb")  # noqa: SIM115
    upload_paper("10.1021/acs.jctc.2c01235", file)


@pytest.mark.asyncio()
async def test_async_query_noagent():
    response = await async_query("Why is KRAS studied?", "public:pqa-bench")
    assert isinstance(response, AnswerResponse)


def test_check_dois() -> None:
    response = check_dois(
        dois=[
            "10.1126/science.1240517",
            "10.1126/science.1240517",  # NOTE: duplicate input DOI
            "10.1016/j.febslet.2014.11.036",
        ]
    )
    assert response == {
        "10.1016/j.febslet.2014.11.036": [
            "4f81e5a9ba561b9431b5919252ca677e34d1315a",
            "cached",
        ],
        "10.1126/science.1240517": ["", "DOI not found"],
    }


@pytest.mark.skip(reason="This test is broken since it imports nonexistent module.")
def test_main() -> None:
    from pqapi.main import main  # type: ignore[import-not-found,unused-ignore]

    runner = click.testing.CliRunner()
    with runner.isolated_filesystem():
        with open("test.jinja2", "w") as f:
            f.write(
                """
{% with bib = "covid" %}
## Info
{{ "Are COVID-19 vaccines effective?" | pqa(bib)}}

## More
{{ "Are COVID-19 vaccines available?" | pqa_fast(bib)}}
{% endwith %}
"""
            )

        result = runner.invoke(main, ["test.jinja2"])
    assert result.exit_code == 0
