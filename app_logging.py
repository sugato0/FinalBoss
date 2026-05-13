import logging


def setup_logging() -> None:
    # Настраиваем, как будут выглядеть служебные сообщения в консоли.
    # Например: когда бот запустился или когда база данных готова.
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
