import logging

import pytest

from logging_context import LoggingContext, LoggingContextFilter

@pytest.fixture
def logger():
    logger = logging.getLogger()
    logger.addFilter(LoggingContextFilter())
    yield logger


def test_context_adds_params(caplog, logger):
    with caplog.at_level(logging.INFO):
        logger.info("before context")
        assert "region" not in caplog.records[-1].__dict__

        with LoggingContext(region="br"):
            logger.info("inside context")
            assert "region" in caplog.records[-1].__dict__
            assert caplog.records[-1].region == "br"


def test_nested_contexts(caplog, logger):
    with caplog.at_level(logging.INFO):
        with LoggingContext(region="br"):
            logger.info("outer context")
            assert "region" in caplog.records[-1].__dict__
            assert caplog.records[-1].region == "br"
            assert "request_id" not in caplog.records[-1].__dict__

            with LoggingContext(request_id=1):
                logger.info("inner context")
                assert "region" in caplog.records[-1].__dict__
                assert caplog.records[-1].region == "br"
                assert "request_id" in caplog.records[-1].__dict__
                assert caplog.records[-1].request_id == 1

            logger.info("outer context")
            assert "region" in caplog.records[-1].__dict__
            assert caplog.records[-1].region == "br"
            assert "request_id" not in caplog.records[-1].__dict__


def test_nested_context_override(caplog, logger):
    with caplog.at_level(logging.INFO):
        with LoggingContext(region="br"):
            logger.info("outer context")
            assert "region" in caplog.records[-1].__dict__
            assert caplog.records[-1].region == "br"
            assert "request_id" not in caplog.records[-1].__dict__

            with LoggingContext(region="us"):
                logger.info("inner context")
                assert "region" in caplog.records[-1].__dict__
                assert caplog.records[-1].region == "us"

            logger.info("outer context")
            assert "region" in caplog.records[-1].__dict__
            assert caplog.records[-1].region == "br"


def test_explicit_logging_overrides_context(caplog, logger):
    with caplog.at_level(logging.INFO):
        with LoggingContext(region="br"):
            logger.info("should use context")
            assert "region" in caplog.records[-1].__dict__
            assert caplog.records[-1].region == "br"

            logger.info("should use context", extra={"region": "us"})
            assert "region" in caplog.records[-1].__dict__
            assert caplog.records[-1].region == "us"
