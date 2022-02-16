import logging

from logging_context import LoggingContext


def test_context_adds_params(caplog):
    logger = logging.getLogger()

    with caplog.at_level(logging.INFO):
        logger.info("before context")
        assert "region" not in caplog.records[-1].__dict__

        with LoggingContext(region="br"):
            logger.info("inside context")
            assert "region" in caplog.records[-1].__dict__
            assert caplog.records[-1].region == "br"


def test_nested_contexts(caplog):
    logger = logging.getLogger()

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


def test_nested_context_override(caplog):
    logger = logging.getLogger()

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
