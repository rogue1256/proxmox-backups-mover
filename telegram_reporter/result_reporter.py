import datetime

import telegram
import config_provider
from file_handler.models import VmFilesCopyResult, FailReason


def get_telegram_bot() -> telegram.Bot:
    config = config_provider.get_config()
    return telegram.Bot(config.telegram_AT)


def convert_failed_reason_to_friendly(reason: FailReason) -> str:
    if reason == FailReason.DifferentSha256:
        return "hashes mismatch between origin and target"
    elif reason == FailReason.CopyFailed:
        return "error in copying files"
    else:
        return "unknown reason"


def prepare_message(results: [VmFilesCopyResult]) -> str:
    messages: [str] = []
    for res in results:
        if len(res.copied_files) == 0 and len(res.failed_copies) == 0:
            continue
        copied_files_str = ""
        for (origin, target) in res.copied_files:
            copied_files_str += f"{origin} to {target}\n"

        failed_files_str = ""
        for (failed_file, reason) in res.failed_copies:
            failed_files_str += f"File {failed_file} failed to" \
                                f" copy due to {convert_failed_reason_to_friendly(reason)}.\n"

        success_message = f"""
_Succeeded files_``` 
{copied_files_str}```"""

        failed_files_message = f"""
_Failed files:_
```
{failed_files_str}```"""

        msg = f"""
*{res.vm.friendly_name}*
{success_message if copied_files_str.strip() != "" else ""}
{failed_files_message if failed_files_str.strip() != "" else ""}"""
        messages.append(msg)
    msg = "*Report on backup copying process*\n"
    for m in messages:
        msg += f"{m}"

    generated_on = str(datetime.datetime.now()).replace('-', '\\-').replace('.', '\\.')
    msg += f"\n\nGenerated on: {generated_on}"
    return msg


async def report(results: [VmFilesCopyResult]):
    bot = get_telegram_bot()
    config = config_provider.get_config()
    async with bot:
        await bot.send_message(config.chat_id, prepare_message(results), telegram.constants.ParseMode.MARKDOWN_V2)


async def report_error():
    pass
