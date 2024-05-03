"""
Copyright (c) Microsoft Corporation. All rights reserved.
Licensed under the MIT License.
"""

from typing import cast
from unittest import IsolatedAsyncioTestCase

from botbuilder.core import TurnContext

from teams_ai_azml.ai.models import PromptResponse
from teams_ai_azml.ai.tokenizers import GPTTokenizer
from teams_ai_azml.ai.validators import DefaultResponseValidator
from teams_ai_azml.state import TurnState


class TestDefaultResponseValidator(IsolatedAsyncioTestCase):
    async def test_should_be_valid(self):
        validator = DefaultResponseValidator()
        res = await validator.validate_response(
            context=cast(TurnContext, {}),
            memory=TurnState(),
            tokenizer=GPTTokenizer(),
            response=PromptResponse(),
            remaining_attempts=3,
        )

        self.assertTrue(res.valid)
