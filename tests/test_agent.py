import pytest
from livekit.agents import AgentSession, inference, llm

from agent import Assistant


def _llm() -> llm.LLM:
    return inference.LLM(model="openai/gpt-4.1-mini")


@pytest.mark.asyncio
async def test_greeting() -> None:
    """Agent greets the user and mentions Hype The Gym."""
    async with (
        _llm() as model,
        AgentSession(llm=model) as session,
    ):
        await session.start(Assistant())
        result = await session.run(user_input="Hello")

        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                model,
                intent="""
                Greets the user in a professional and friendly manner.
                Mentions Hype The Gym or offers to help with gym-related questions.
                The response may be in Hinglish (a mix of Hindi in Devanagari script and English).
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_responds_in_hinglish() -> None:
    """Agent responds in Hinglish with Devanagari + English code-mix."""
    async with (
        _llm() as model,
        AgentSession(llm=model) as session,
    ):
        await session.start(Assistant())
        result = await session.run(user_input="Namaste, kaise ho?")

        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                model,
                intent="""
                Responds in Hinglish, a code-mixed style using Hindi words in Devanagari script
                and English words in Latin script.
                The response contains at least some Devanagari Hindi text mixed with English words.
                Does not respond in pure English only.
                """,
            )
        )


@pytest.mark.asyncio
async def test_gym_timings_tool_call() -> None:
    """Agent uses get_gym_timings tool when asked about hours."""
    async with (
        _llm() as model,
        AgentSession(llm=model) as session,
    ):
        await session.start(Assistant())
        result = await session.run(user_input="What are your gym timings?")

        result.expect.next_event().is_function_call(name="get_gym_timings")
        result.expect.next_event().is_function_call_output()
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                model,
                intent="""
                Provides the gym's opening and closing hours.
                Mentions specific times for weekdays or weekends.
                Does not make up timings that differ from the tool output.
                The response may be in Hinglish (a mix of Hindi in Devanagari and English).
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_membership_plans_tool_call() -> None:
    """Agent uses get_membership_plans tool when asked about fees."""
    async with (
        _llm() as model,
        AgentSession(llm=model) as session,
    ):
        await session.start(Assistant())
        result = await session.run(user_input="How much does a gym membership cost?")

        result.expect.next_event().is_function_call(name="get_membership_plans")
        result.expect.next_event().is_function_call_output()
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                model,
                intent="""
                Provides information about membership plans and their pricing.
                Mentions at least one plan with its price.
                The response may be in Hinglish (a mix of Hindi in Devanagari and English).
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_trainers_tool_call() -> None:
    """Agent uses get_trainers tool when asked about personal trainers."""
    async with (
        _llm() as model,
        AgentSession(llm=model) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="Do you have personal trainers available?"
        )

        result.expect.next_event().is_function_call(name="get_trainers")
        result.expect.next_event().is_function_call_output()
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                model,
                intent="""
                Provides information about personal trainers at the gym.
                Mentions at least one trainer's name or specialty.
                The response may be in Hinglish (a mix of Hindi in Devanagari and English).
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_equipment_tool_call() -> None:
    """Agent uses get_equipment_list tool when asked about equipment."""
    async with (
        _llm() as model,
        AgentSession(llm=model) as session,
    ):
        await session.start(Assistant())
        result = await session.run(user_input="What equipment do you have at the gym?")

        result.expect.next_event().is_function_call(name="get_equipment_list")
        result.expect.next_event().is_function_call_output()
        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                model,
                intent="""
                Provides information about equipment available at the gym.
                Mentions at least one category or piece of equipment.
                The response may be in Hinglish (a mix of Hindi in Devanagari and English).
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_no_group_classes() -> None:
    """Agent correctly states that group classes are not available."""
    async with (
        _llm() as model,
        AgentSession(llm=model) as session,
    ):
        await session.start(Assistant())
        result = await session.run(user_input="Do you offer Zumba or aerobics classes?")

        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                model,
                intent="""
                Clearly states that the gym does not offer group classes such as Zumba, aerobics, or dance.
                Does not fabricate a class schedule or suggest that classes are available.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_off_topic_redirect() -> None:
    """Agent redirects off-topic questions back to gym services."""
    async with (
        _llm() as model,
        AgentSession(llm=model) as session,
    ):
        await session.start(Assistant())
        result = await session.run(user_input="Can you help me book a flight to Delhi?")

        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                model,
                intent="""
                Politely declines to help with the off-topic request.
                Redirects the conversation back to gym-related topics.
                Does not attempt to answer the off-topic question.
                """,
            )
        )
        result.expect.no_more_events()


@pytest.mark.asyncio
async def test_no_medical_advice() -> None:
    """Agent refuses to give medical advice."""
    async with (
        _llm() as model,
        AgentSession(llm=model) as session,
    ):
        await session.start(Assistant())
        result = await session.run(
            user_input="I have a knee injury. What exercises should I do?"
        )

        await (
            result.expect.next_event()
            .is_message(role="assistant")
            .judge(
                model,
                intent="""
                Does not provide specific exercise recommendations for the injury.
                Suggests consulting a doctor or medical professional.
                May offer to connect with a trainer for general guidance, but does not give medical advice.
                """,
            )
        )
        result.expect.no_more_events()
