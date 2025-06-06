"""Option parser for extracting choices from user messages."""

import re

import structlog

logger = structlog.get_logger()


class OptionParser:
    """Parser for extracting options from user text messages."""

    def __init__(self, max_options: int = 5):
        """Initialize the parser with maximum number of options."""
        self.max_options = max_options

    def parse_options(self, text: str) -> list[str] | None:
        """
        Parse options from text message.

        Supports formats:
        - "Pizza or sushi?"
        - "Pizza, sushi, or burgers"
        - "Pizza\nSushi\nBurgers"
        - "1. Pizza\n2. Sushi"

        Args:
            text: User message text

        Returns:
            List of options if found, None if less than 2 options
        """
        if not text or not text.strip():
            return None

        text = text.strip()
        options = []

        # Try different parsing strategies
        strategies = [
            self._parse_or_separated,
            self._parse_comma_separated,
            self._parse_line_separated,
            self._parse_numbered_list,
        ]

        for strategy in strategies:
            options = strategy(text)
            if options and len(options) >= 2:
                break

        if not options or len(options) < 2:
            logger.warning("Could not parse options from text", text=text)
            return None

        # Limit to max_options
        if len(options) > self.max_options:
            options = options[: self.max_options]
            logger.info(
                "Truncated options to maximum",
                max_options=self.max_options,
                original_count=len(options),
            )

        # Clean up options
        options = [self._clean_option(opt) for opt in options if opt.strip()]

        logger.info("Parsed options successfully", options=options, count=len(options))
        return options

    def _parse_or_separated(self, text: str) -> list[str]:
        """Parse options separated by 'or' (or 'или' in Russian)."""
        # Remove question marks and exclamation marks
        text = re.sub(r"[?!]+$", "", text).strip()

        # Split by 'or' or 'или'
        options = re.split(r"\s+(?:or|или)\s+", text, flags=re.IGNORECASE)

        return [opt.strip() for opt in options if opt.strip()]

    def _parse_comma_separated(self, text: str) -> list[str]:
        """Parse options separated by commas."""
        # Handle "A, B, or C" format
        text = re.sub(r",?\s+or\s+", ", ", text, flags=re.IGNORECASE)
        text = re.sub(r",?\s+или\s+", ", ", text, flags=re.IGNORECASE)
        text = re.sub(r"[?!]+$", "", text).strip()

        options = [opt.strip() for opt in text.split(",")]
        return [opt for opt in options if opt.strip()]

    def _parse_line_separated(self, text: str) -> list[str]:
        """Parse options separated by line breaks."""
        lines = text.split("\n")
        options = []

        for line in lines:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
            # Remove leading numbers, bullets, dashes
            line = re.sub(r"^[\d\-\*\+•]+\.?\s*", "", line)
            if line:
                options.append(line)

        return options

    def _parse_numbered_list(self, text: str) -> list[str]:
        """Parse numbered list format."""
        lines = text.split("\n")
        options = []

        for line in lines:
            line = line.strip()
            # Match patterns like "1. Option", "1) Option", "1 Option"
            match = re.match(r"^(\d+)[.\)]\s*(.+)$", line)
            if match:
                options.append(match.group(2).strip())

        return options

    def _clean_option(self, option: str) -> str:
        """Clean up individual option text."""
        # Remove leading/trailing whitespace
        option = option.strip()

        # Remove quotes if they wrap the entire option
        if (option.startswith('"') and option.endswith('"')) or (
            option.startswith("'") and option.endswith("'")
        ):
            option = option[1:-1].strip()

        # Remove trailing punctuation except for necessary ones
        option = re.sub(r"[,;]+$", "", option)

        return option
